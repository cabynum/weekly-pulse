"""
Fetch the latest generated AAET Weekly Status report from Cat's GitHub repo
and extract the Data Processing section as a baseline.
"""

import re
import requests
from datetime import datetime
from typing import Optional


class ReportCollector:

    def __init__(self, github_token: str, owner: str = "catrobson",
                 repo: str = "AAET-Weekly-Status"):
        self.token = github_token
        self.owner = owner
        self.repo = repo
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {github_token}",
        }

    def _api(self, path: str) -> dict:
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/{path}"
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def find_latest_report(self) -> Optional[str]:
        """Find the most recent AAET_Weekly_Status report file."""
        contents = self._api("contents/reports")
        report_files = [
            f for f in contents
            if f["name"].startswith("AAET_Weekly_Status")
        ]
        if not report_files:
            return None
        report_files.sort(key=lambda f: f["name"], reverse=True)
        return report_files[0]["path"]

    def fetch_report(self, path: str) -> str:
        """Download a report file's content."""
        import base64
        data = self._api(f"contents/{path}")
        return base64.b64decode(data["content"]).decode("utf-8")

    def extract_dp_section(self, report_text: str) -> str:
        """Extract the Data Processing section from the full report."""
        pattern = r"\*\*Data Processing\*\*.*?(?=\*\*[A-Z]|\Z)"
        match = re.search(pattern, report_text, re.DOTALL)
        return match.group(0).strip() if match else ""

    def extract_executive_summary(self, report_text: str) -> str:
        """Extract the executive summary for context."""
        pattern = r"\*\*Executive Summary\*\*\s*(.*?)\s*\*\*Risks"
        match = re.search(pattern, report_text, re.DOTALL)
        return match.group(1).strip() if match else ""

    def collect(self) -> dict:
        """Main entry point: fetch latest report and extract DP section."""
        print("Fetching latest AAET report from GitHub...")
        path = self.find_latest_report()
        if not path:
            print("  No report found")
            return {"report_path": None, "dp_section": "", "exec_summary": ""}

        print(f"  Found: {path}")
        text = self.fetch_report(path)
        dp_section = self.extract_dp_section(text)
        exec_summary = self.extract_executive_summary(text)

        print(f"  DP section: {len(dp_section)} chars")
        return {
            "report_path": path,
            "full_report": text,
            "dp_section": dp_section,
            "exec_summary": exec_summary,
        }
