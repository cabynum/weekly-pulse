"""
Collect Jira activity for the Data Processing component.
Completed tickets, status transitions, sprint progress.
"""

import requests
from datetime import datetime, timedelta
from typing import List


FIELDS = (
    "summary,status,assignee,created,updated,resolutiondate,"
    "priority,components,labels,issuetype,fixVersions,"
    "customfield_10855,customfield_10712,customfield_10814"
)


class JiraCollector:

    def __init__(self, base_url: str, username: str, api_token: str,
                 component: str = "Data Processing",
                 projects: List[str] = None):
        self.base_url = base_url
        self.auth = (username, api_token)
        self.component = component
        self.projects = projects or ["RHAIENG", "RHAISTRAT", "RHOAIENG"]

    def _search(self, jql: str, max_results: int = 100) -> List[dict]:
        url = f"{self.base_url}/rest/api/3/search/jql"
        all_issues = []
        start = 0
        while True:
            resp = requests.get(url, auth=self.auth, params={
                "jql": jql,
                "maxResults": min(max_results - len(all_issues), 100),
                "startAt": start,
                "fields": FIELDS,
            })
            resp.raise_for_status()
            data = resp.json()
            issues = data.get("issues", [])
            all_issues.extend(issues)
            if len(all_issues) >= data.get("total", 0) or len(all_issues) >= max_results:
                break
            start += len(issues)
        return all_issues

    def _format(self, issue: dict) -> dict:
        f = issue.get("fields", {})
        assignee = f.get("assignee")
        color_field = f.get("customfield_10712")
        color = color_field.get("value", "") if isinstance(color_field, dict) else ""

        status_summary = f.get("customfield_10814")
        if isinstance(status_summary, dict):
            try:
                ss_text = status_summary["content"][0]["content"][0]["text"]
            except (KeyError, IndexError):
                ss_text = ""
        else:
            ss_text = str(status_summary) if status_summary else ""

        tv = f.get("customfield_10855") or []
        target_versions = [
            v.get("name", "") if isinstance(v, dict) else str(v) for v in tv
        ]
        fv = f.get("fixVersions") or []
        fix_versions = [v.get("name", "") for v in fv]

        return {
            "key": issue["key"],
            "summary": f.get("summary", ""),
            "status": f.get("status", {}).get("name", ""),
            "assignee": assignee.get("displayName", "") if assignee else "Unassigned",
            "priority": f.get("priority", {}).get("name", ""),
            "type": f.get("issuetype", {}).get("name", ""),
            "color": color,
            "status_summary": ss_text[:200],
            "target_versions": target_versions,
            "fix_versions": fix_versions,
            "updated": f.get("updated", ""),
            "resolved": f.get("resolutiondate", ""),
            "url": f"{self.base_url}/browse/{issue['key']}",
        }

    def _base_jql(self) -> str:
        projects = ", ".join(self.projects)
        return f'project in ({projects}) AND component = "{self.component}"'

    def collect(self, days_back: int = 7) -> dict:
        since = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        base = self._base_jql()
        print(f"Collecting Jira activity for {self.component} since {since}...")

        completed = self._search(f'{base} AND resolutiondate >= "{since}"')
        completed_fmt = [self._format(i) for i in completed]
        print(f"  {len(completed_fmt)} completed")

        updated = self._search(f'{base} AND updated >= "{since}" AND status != Done')
        updated_fmt = [self._format(i) for i in updated]
        print(f"  {len(updated_fmt)} in progress/updated")

        created = self._search(f'{base} AND created >= "{since}"')
        created_fmt = [self._format(i) for i in created]
        print(f"  {len(created_fmt)} created")

        features = self._search(
            f'project = RHAISTRAT AND issuetype = Feature '
            f'AND component = "{self.component}" '
            f'AND status in (Refinement, "In Progress", Review)'
        )
        features_fmt = [self._format(i) for i in features]
        print(f"  {len(features_fmt)} active features")

        return {
            "completed": completed_fmt,
            "in_progress": updated_fmt,
            "created": created_fmt,
            "features": features_fmt,
            "counts": {
                "completed": len(completed_fmt),
                "in_progress": len(updated_fmt),
                "created": len(created_fmt),
            },
        }
