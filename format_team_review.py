#!/usr/bin/env python3
"""
Format the Weekly Pulse draft as a Slack mrkdwn post for team review.

Writes output/YYYY-MM-DD/team-review.md (copy-paste ready for
#aaiet-data-processing). Does not post to Slack.

Usage:
    python format_team_review.py [--date YYYY-MM-DD] [--print]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output"
CONFIG_PATH = ROOT / "config.yaml"

HEADER = ":ptal: *Weekly Report - Please review*"

# Slack post section order (Associates first when present, matching
# the live channel precedent).
SECTION_ORDER = [
    ("associates", "Associates"),
    ("data_processing", "Data Processing"),
    ("risks", "Risks"),
    ("customers", "Customers"),
]


def load_config() -> dict:
    with CONFIG_PATH.open() as f:
        return yaml.safe_load(f)


def slack_id_map(config: dict) -> dict[str, str]:
    return {
        m["name"]: m["slack_id"]
        for m in config.get("team", {}).get("members", [])
        if m.get("name") and m.get("slack_id")
    }


def find_draft(date: str | None) -> Path:
    if date:
        path = OUTPUT / date / "draft.md"
        if not path.exists():
            print(f"Error: no draft at {path}", file=sys.stderr)
            sys.exit(1)
        return path

    dated = sorted(
        (p for p in OUTPUT.glob("*/draft.md") if p.parent.name[:4].isdigit()),
        key=lambda p: p.parent.name,
        reverse=True,
    )
    if not dated:
        print("Error: no draft.md under output/", file=sys.stderr)
        sys.exit(1)
    return dated[0]


def extract_sections(content: str) -> dict[str, str]:
    result: dict[str, str] = {}

    dp_match = re.search(
        r"## Suggested Section.*?\n\n(.*?)(?=\n---\n|\n## Suggested Addition)",
        content,
        re.DOTALL,
    )
    if not dp_match:
        dp_match = re.search(
            r"## Suggested Section.*?\n\n(.*?)(?=\n## |\Z)",
            content,
            re.DOTALL,
        )
    if not dp_match:
        print("Error: could not find Suggested Section in draft", file=sys.stderr)
        sys.exit(1)
    result["data_processing"] = dp_match.group(1).strip()

    secondary = {
        "Risks/Issues": "risks",
        "Customers": "customers",
        "Associates": "associates",
    }
    for label, key in secondary.items():
        pattern = (
            rf"## Suggested Addition to {re.escape(label)} Section\s*\n"
            r"(.*?)(?=\n## |\n---\n|\Z)"
        )
        match = re.search(pattern, content, re.DOTALL)
        if match and match.group(1).strip():
            result[key] = match.group(1).strip()

    return result


def md_links_to_slack(text: str) -> str:
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"<\2|\1>", text)


def mentionize_associates(text: str, ids: dict[str, str]) -> str:
    # Longest names first so "Ali Maredia" wins over partial matches.
    for name in sorted(ids.keys(), key=len, reverse=True):
        text = re.sub(
            rf"(?<![<@/\w]){re.escape(name)}\b",
            f"<@{ids[name]}>",
            text,
        )
    return text


def bullets_to_slack(section_md: str, *, associates: bool, ids: dict[str, str]) -> list[str]:
    lines: list[str] = []
    for raw in section_md.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("**") or stripped == "Highlights:":
            continue
        if stripped.startswith("- "):
            body = stripped[2:]
        else:
            continue
        body = md_links_to_slack(body)
        if associates:
            body = mentionize_associates(body, ids)
        lines.append(f"• {body}")
    return lines


def completed_count(dp_md: str) -> str | None:
    match = re.search(r"(\d+)\s+issues?\s+completed", dp_md, re.IGNORECASE)
    if match:
        return match.group(1)
    return None


def format_post(sections: dict[str, str], ids: dict[str, str]) -> str:
    parts = [HEADER, ""]

    for key, title in SECTION_ORDER:
        if key not in sections:
            continue
        bullets = bullets_to_slack(
            sections[key],
            associates=(key == "associates"),
            ids=ids,
        )
        if not bullets:
            continue

        if key == "data_processing":
            count = completed_count(sections[key])
            header = f"*{title}*"
            if count:
                header = f"*{title}* ({count} issues completed)"
            parts.append(header)
        else:
            parts.append(f"*{title}*")

        parts.append("")
        parts.extend(bullets)
        parts.append("")

    return "\n".join(parts).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Format draft.md as Slack team-review post")
    parser.add_argument("--date", help="Draft date folder YYYY-MM-DD (default: latest)")
    parser.add_argument("--print", action="store_true", help="Print post to stdout")
    args = parser.parse_args()

    draft_path = find_draft(args.date)
    date_dir = draft_path.parent
    config = load_config()
    ids = slack_id_map(config)

    sections = extract_sections(draft_path.read_text())
    post = format_post(sections, ids)

    out_path = date_dir / "team-review.md"
    out_path.write_text(post)
    print(f"Wrote: {out_path}")

    if args.print:
        print()
        print(post)


if __name__ == "__main__":
    main()
