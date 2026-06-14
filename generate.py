#!/usr/bin/env python3
"""
Weekly Pulse - Data Processing Team Highlights Generator

Collects activity from multiple sources, synthesizes into bullet points,
and produces a draft for the AAET Weekly Pulse Check.

Usage:
    python generate.py [--days-back 7] [--skip-slack] [--output-only]
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import yaml
from dotenv import load_dotenv

from collectors.baseline import BaselineCollector
from collectors.github import GitHubCollector
from collectors.jira import JiraCollector
from collectors.slack import SlackCollector
from synthesize import Synthesizer


def load_config(config_path: str = None) -> dict:
    if config_path is None:
        config_path = Path(__file__).parent / "config.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description="Generate Data Processing weekly highlights")
    parser.add_argument("--days-back", type=int, default=7, help="Days to look back")
    parser.add_argument("--skip-slack", action="store_true", help="Skip Slack collection")
    parser.add_argument("--config", type=str, help="Path to config.yaml")
    args = parser.parse_args()

    load_dotenv()
    config = load_config(args.config)

    print("=" * 60)
    print("WEEKLY PULSE - Data Processing Highlights")
    print(f"Looking back {args.days_back} days")
    print("=" * 60)

    # 1. Fetch the generated AAET report as baseline
    github_token = os.getenv("GITHUB_TOKEN", "")
    aaet = config.get("github", {}).get("aaet_report", {})
    baseline = BaselineCollector(
        github_token=github_token,
        owner=aaet.get("owner", "catrobson"),
        repo=aaet.get("repo", "AAET-Weekly-Status"),
    )
    report_data = baseline.collect()

    # 2. Collect GitHub activity
    members = config.get("team", {}).get("members", [])
    repos = config.get("github", {}).get("repos", [])
    gh_collector = GitHubCollector(token=github_token, repos=repos, members=members)
    github_data = gh_collector.collect(days_back=args.days_back)

    # 3. Collect Jira activity
    jira_cfg = config.get("jira", {})
    jira_collector = JiraCollector(
        base_url=jira_cfg.get("base_url", "https://redhat.atlassian.net"),
        username=os.getenv("JIRA_USERNAME") or os.getenv("JIRA_EMAIL", ""),
        api_token=os.getenv("JIRA_API_TOKEN", ""),
        component=jira_cfg.get("component", "Data Processing"),
        projects=jira_cfg.get("projects"),
    )
    jira_data = jira_collector.collect(days_back=args.days_back)

    # 4. Collect Slack activity (optional)
    slack_data = None
    if not args.skip_slack:
        slack_token = os.getenv("SLACK_USER_TOKEN", "")
        if slack_token:
            slack_collector = SlackCollector(token=slack_token, members=members)
            slack_data = slack_collector.collect(days_back=args.days_back)
        else:
            print("\nSkipping Slack (no SLACK_USER_TOKEN set)")

    # 5. Synthesize into bullet points
    llm_cfg = config.get("llm", {})
    synth = Synthesizer(
        vertex_project=llm_cfg.get("vertex_project"),
        vertex_region=llm_cfg.get("vertex_region"),
        model=llm_cfg.get("model"),
    )

    print("\n" + "=" * 60)
    print("Synthesizing highlights...")
    print("=" * 60)

    team_cfg = config.get("team", {})
    bullets = synth.synthesize(report_data, github_data, jira_data, slack_data)
    full_section = synth.format_full_section(
        bullets, jira_data,
        team_name=team_cfg.get("name", "Data Processing"),
        leader_name=team_cfg.get("leader", "Chris Bynum"),
    )

    # 6. Save output
    output_dir = Path(__file__).parent / "output"
    date_str = datetime.now().strftime("%Y-%m-%d")
    date_dir = output_dir / date_str
    date_dir.mkdir(parents=True, exist_ok=True)

    draft_path = date_dir / "draft.md"
    with open(draft_path, "w") as f:
        f.write(f"# Data Processing - Weekly Highlights Draft\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("## Suggested Section for AAET Weekly Pulse Check\n\n")
        f.write(full_section)
        f.write("\n\n---\n\n")
        f.write("## Raw Bullets (for editing)\n\n")
        f.write(bullets)
        f.write("\n\n---\n\n")
        f.write("## Source Data Summary\n\n")
        f.write(f"- Jira: {jira_data['counts']['completed']} completed, "
                f"{jira_data['counts']['in_progress']} in progress\n")
        f.write(f"- GitHub: {github_data['total_merged']} PRs merged, "
                f"{len(github_data['team_prs'])} by team\n")
        if slack_data:
            total_msgs = sum(d["count"] for d in slack_data.values())
            f.write(f"- Slack: {total_msgs} messages scanned across team\n")

    print(f"\nDraft saved: {draft_path}")

    # Save plain-text version (no markdown links, ready for Google Docs)
    plain_path = date_dir / "plain.txt"
    plain_section = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", full_section)
    with open(plain_path, "w") as f:
        f.write(plain_section)
    print(f"Plain text saved: {plain_path}")

    # Save raw data for debugging
    raw_path = date_dir / "raw.json"
    with open(raw_path, "w") as f:
        json.dump({
            "report": {k: v for k, v in report_data.items() if k != "full_report"},
            "github": github_data,
            "jira": jira_data,
            "slack": {
                name: {"count": d["count"]}
                for name, d in (slack_data or {}).items()
            },
        }, f, indent=2, default=str)

    # 7. Print the draft
    print("\n" + "=" * 60)
    print("DRAFT OUTPUT")
    print("=" * 60 + "\n")
    print(full_section)

    print("\n" + "=" * 60)
    print("DONE")
    print(f"Edit the draft at: {draft_path}")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
