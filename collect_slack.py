"""
Standalone Slack collector for the Weekly Pulse pipeline.

Runs locally (not in CI) after dispatch.sh pulls the CI-generated draft.
Collects team member messages via the Slack Web API and saves them to
output/YYYY-MM-DD/slack.json for the weekly-pulse-review skill to read.

Usage:
    python collect_slack.py [--days-back 7] [--date 2026-06-25]
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path

import yaml
from dotenv import load_dotenv

from collectors.slack import SlackCollector

CONFIG_FILE = Path(__file__).parent / "config.yaml"
OUTPUT_DIR = Path(__file__).parent / "output"


def main():
    parser = argparse.ArgumentParser(description="Collect Slack messages for Weekly Pulse")
    parser.add_argument("--days-back", type=int, default=7)
    parser.add_argument("--date", type=str, default=None,
                        help="Target date folder (YYYY-MM-DD). Defaults to today.")
    args = parser.parse_args()

    load_dotenv(Path(__file__).parent / ".env")
    token = os.getenv("SLACK_USER_TOKEN") or os.getenv("SLACK_XOXC_TOKEN", "")
    cookie = os.getenv("SLACK_XOXD_TOKEN", "")
    if not token:
        print("Error: set SLACK_USER_TOKEN (xoxp) or SLACK_XOXC_TOKEN + SLACK_XOXD_TOKEN in .env")
        return 1

    with open(CONFIG_FILE) as f:
        config = yaml.safe_load(f)

    members = config.get("team", {}).get("members", [])
    if not members:
        print("Error: no team members in config.yaml")
        return 1

    date_str = args.date or datetime.now().strftime("%Y-%m-%d")
    date_dir = OUTPUT_DIR / date_str
    if not date_dir.exists():
        print(f"Warning: output folder {date_dir} does not exist, creating it")
        date_dir.mkdir(parents=True, exist_ok=True)

    collector = SlackCollector(token=token, members=members, cookie=cookie or None)
    slack_data = collector.collect(days_back=args.days_back)

    total = sum(d["count"] for d in slack_data.values())
    print(f"\nCollected {total} messages across {len(members)} team members")

    out_path = date_dir / "slack.json"
    with open(out_path, "w") as f:
        json.dump(slack_data, f, indent=2, default=str)
    print(f"Saved: {out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
