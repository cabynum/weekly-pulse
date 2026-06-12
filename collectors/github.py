"""
Collect GitHub activity for Data Processing team members across tracked repos.
PRs authored, PRs reviewed, issues, and commits.
"""

import requests
from datetime import datetime, timedelta
from typing import List


class GitHubCollector:

    def __init__(self, token: str, repos: List[str], members: List[dict]):
        self.token = token
        self.repos = repos
        self.members = members
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {token}",
        }
        self._github_usernames = {
            m["github"].lower() for m in members if m.get("github")
        }

    def _get(self, url: str, params: dict = None) -> list | dict:
        resp = requests.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        return resp.json()

    def _is_team_member(self, username: str) -> bool:
        return username.lower() in self._github_usernames

    def get_merged_prs(self, repo: str, since: datetime) -> List[dict]:
        """Get PRs merged by team members."""
        prs = self._get(
            f"https://api.github.com/repos/{repo}/pulls",
            {"state": "closed", "sort": "updated", "direction": "desc", "per_page": 100},
        )
        results = []
        for pr in prs:
            if not pr.get("merged_at"):
                continue
            merged = datetime.strptime(pr["merged_at"], "%Y-%m-%dT%H:%M:%SZ")
            if merged < since:
                continue
            author = pr["user"]["login"]
            results.append({
                "number": pr["number"],
                "title": pr["title"],
                "url": pr["html_url"],
                "author": author,
                "is_team_member": self._is_team_member(author),
                "merged_at": pr["merged_at"],
            })
        return results

    def get_pr_reviews(self, repo: str, since: datetime) -> List[dict]:
        """Get PR reviews submitted by team members."""
        prs = self._get(
            f"https://api.github.com/repos/{repo}/pulls",
            {"state": "all", "sort": "updated", "direction": "desc", "per_page": 50},
        )
        results = []
        for pr in prs:
            updated = datetime.strptime(pr["updated_at"], "%Y-%m-%dT%H:%M:%SZ")
            if updated < since:
                break
            reviews = self._get(
                f"https://api.github.com/repos/{repo}/pulls/{pr['number']}/reviews"
            )
            for review in reviews:
                submitted = review.get("submitted_at")
                if not submitted:
                    continue
                review_date = datetime.strptime(submitted, "%Y-%m-%dT%H:%M:%SZ")
                if review_date < since:
                    continue
                reviewer = review["user"]["login"]
                if self._is_team_member(reviewer):
                    results.append({
                        "pr_number": pr["number"],
                        "pr_title": pr["title"],
                        "pr_url": pr["html_url"],
                        "reviewer": reviewer,
                        "state": review["state"],
                        "submitted_at": submitted,
                    })
        return results

    def get_closed_issues(self, repo: str, since: datetime) -> List[dict]:
        """Get issues closed in the period."""
        issues = self._get(
            f"https://api.github.com/repos/{repo}/issues",
            {"state": "closed", "since": since.isoformat() + "Z", "per_page": 100},
        )
        return [
            {
                "number": i["number"],
                "title": i["title"],
                "url": i["html_url"],
                "closed_by": i.get("user", {}).get("login", ""),
            }
            for i in issues
            if "pull_request" not in i
        ]

    def collect(self, days_back: int = 7) -> dict:
        """Main entry point."""
        since = datetime.utcnow() - timedelta(days=days_back)
        print(f"Collecting GitHub activity since {since.strftime('%Y-%m-%d')}...")

        all_prs = []
        all_reviews = []
        all_issues = []

        for repo in self.repos:
            print(f"  {repo}...")
            prs = self.get_merged_prs(repo, since)
            all_prs.extend(prs)
            print(f"    {len(prs)} merged PRs")

            reviews = self.get_pr_reviews(repo, since)
            all_reviews.extend(reviews)
            print(f"    {len(reviews)} reviews by team")

            issues = self.get_closed_issues(repo, since)
            all_issues.extend(issues)

        team_prs = [p for p in all_prs if p["is_team_member"]]
        external_prs = [p for p in all_prs if not p["is_team_member"]]

        return {
            "team_prs": team_prs,
            "external_prs": external_prs,
            "team_reviews": all_reviews,
            "closed_issues": all_issues,
            "total_merged": len(all_prs),
        }
