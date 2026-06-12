"""
Synthesize collected data into human-readable bullet points
matching the AAET Weekly Pulse Check format.
"""

import os
import json
from typing import Optional

try:
    from anthropic import AnthropicVertex
except ImportError:
    AnthropicVertex = None


SYSTEM_PROMPT = """\
You are a technical writing assistant for an engineering manager. Your job is \
to transform raw engineering activity data into concise, impactful bullet \
points for a weekly status report.

The audience is executive technical leaders at Red Hat. The format is the \
AAET Weekly Pulse Check - a weekly email sent to engineering leadership.

Rules:
- Output ONLY bullet points (markdown "- " prefix), no headers or paragraphs
- Each bullet should be 1-2 sentences max
- Translate PR titles and Jira tickets into business/product language
- Name team members when they did something noteworthy
- Link to Jira tickets as [KEY](url) and PRs as [descriptive text](url)
- Prioritize: releases > customer impact > features shipped > bugs fixed > \
process improvements > reviews
- Group related items into a single bullet when possible (e.g., multiple \
CVE fixes become one bullet about security remediation)
- Skip trivial changes (dependency bumps, lock file updates) unless they \
fix a CVE or unblock something
- If Slack messages reveal decisions, cross-team collaboration, or customer \
interactions, surface those - they often matter more than code changes
- Never fabricate information. If the data is thin, produce fewer but \
accurate bullets rather than padding
- Do not use em dashes. Use commas, colons, or separate sentences instead.
- Target 4-8 bullets total. Quality over quantity.
"""

USER_PROMPT_TEMPLATE = """\
Generate the Data Processing team's "Weekly Updates" bullet points for the \
AAET Weekly Pulse Check.

## Current Generated Report Section
(This is what the automated report already produced. Improve on it.)
{current_dp_section}

## Jira Activity
Completed: {jira_completed_count} tickets
In progress: {jira_in_progress_count} tickets

Completed tickets:
{jira_completed}

Active features:
{jira_features}

## GitHub Activity
{github_summary}

Team PRs merged:
{team_prs}

PR reviews by team:
{team_reviews}

## Slack Activity (team member messages this week)
{slack_summary}

---

Produce the bullet points now. Output ONLY the bullets, nothing else."""


class ReportWriter:

    def __init__(self, vertex_project: str = None, vertex_region: str = None,
                 model: str = None):
        self.model = model or "claude-sonnet-4-5@20250929"

        if AnthropicVertex is None:
            print("Warning: anthropic[vertex] not installed. Using fallback.")
            self.client = None
            return

        project = vertex_project or os.getenv(
            "ANTHROPIC_VERTEX_PROJECT_ID", "itpc-gcp-ai-eng-claude"
        )
        region = vertex_region or os.getenv(
            "ANTHROPIC_VERTEX_REGION", "us-east5"
        )
        try:
            self.client = AnthropicVertex(project_id=project, region=region)
            print(f"LLM: Vertex AI ({project}/{region}) model={self.model}")
        except Exception as e:
            print(f"Warning: Could not init Vertex AI: {e}")
            self.client = None

    def _format_jira_tickets(self, tickets: list) -> str:
        if not tickets:
            return "(none)"
        lines = []
        for t in tickets[:20]:
            lines.append(
                f"- [{t['key']}]({t['url']}) {t['summary']} "
                f"[{t['status']}] assigned:{t['assignee']} priority:{t['priority']}"
            )
        return "\n".join(lines)

    def _format_prs(self, prs: list) -> str:
        if not prs:
            return "(none)"
        lines = []
        for pr in prs[:15]:
            lines.append(f"- #{pr['number']} {pr['title']} by {pr['author']} ({pr['url']})")
        return "\n".join(lines)

    def _format_reviews(self, reviews: list) -> str:
        if not reviews:
            return "(none)"
        lines = []
        for r in reviews[:15]:
            lines.append(
                f"- {r['reviewer']} reviewed #{r['pr_number']} {r['pr_title']} "
                f"[{r['state']}] ({r['pr_url']})"
            )
        return "\n".join(lines)

    def _format_github_summary(self, github_data: dict) -> str:
        team = len(github_data.get("team_prs", []))
        external = len(github_data.get("external_prs", []))
        reviews = len(github_data.get("team_reviews", []))
        return (
            f"{github_data.get('total_merged', 0)} PRs merged total "
            f"({team} by team, {external} external). "
            f"{reviews} reviews by team members."
        )

    def _format_slack_summary(self, slack_data: dict) -> str:
        if not slack_data:
            return "(Slack data not available)"
        lines = []
        for name, data in slack_data.items():
            msgs = data.get("messages", [])
            if not msgs:
                lines.append(f"- {name}: no notable messages")
                continue
            lines.append(f"- {name}: {data['count']} messages. Samples:")
            for msg in msgs[:5]:
                text = msg["text"][:200].replace("\n", " ")
                ch = msg.get("channel", "?")
                lines.append(f"  - [{ch}] {text}")
        return "\n".join(lines)

    def synthesize(self, report_data: dict, github_data: dict,
                   jira_data: dict, slack_data: dict = None) -> str:
        """Generate bullet points from all collected data."""
        prompt = USER_PROMPT_TEMPLATE.format(
            current_dp_section=report_data.get("dp_section", "(not available)"),
            jira_completed_count=jira_data.get("counts", {}).get("completed", 0),
            jira_in_progress_count=jira_data.get("counts", {}).get("in_progress", 0),
            jira_completed=self._format_jira_tickets(jira_data.get("completed", [])),
            jira_features=self._format_jira_tickets(jira_data.get("features", [])),
            github_summary=self._format_github_summary(github_data),
            team_prs=self._format_prs(github_data.get("team_prs", [])),
            team_reviews=self._format_reviews(github_data.get("team_reviews", [])),
            slack_summary=self._format_slack_summary(slack_data),
        )

        if not self.client:
            return self._fallback(jira_data, github_data)

        try:
            resp = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
            return resp.content[0].text.strip()
        except Exception as e:
            print(f"LLM error: {e}")
            return self._fallback(jira_data, github_data)

    def _fallback(self, jira_data: dict, github_data: dict) -> str:
        """Basic bullet generation without LLM."""
        bullets = []
        for t in jira_data.get("completed", [])[:5]:
            bullets.append(f"- Completed [{t['key']}]({t['url']}): {t['summary']}")
        team_prs = github_data.get("team_prs", [])
        if team_prs:
            bullets.append(f"- Merged {len(team_prs)} PRs across tracked repositories")
        if not bullets:
            bullets.append("- (No significant activity captured this period)")
        return "\n".join(bullets)

    def format_full_section(self, bullets: str, jira_data: dict) -> str:
        """Format the complete Data Processing section for the report."""
        completed = jira_data.get("counts", {}).get("completed", 0)
        in_progress = jira_data.get("counts", {}).get("in_progress", 0)
        features = jira_data.get("features", [])

        lines = [
            f"**Data Processing** (Chris Bynum) - {completed} issues completed\n",
            "Highlights:\n",
            bullets,
            "",
            f"In progress: {in_progress} active issues.",
        ]

        if features:
            feature_notes = []
            for feat in features:
                color_tag = f" ({feat['color']})" if feat["color"] else ""
                tv = ", ".join(feat.get("target_versions", []))
                tv_note = f" TV:{tv}" if tv else ""
                feature_notes.append(
                    f"[{feat['key']}]({feat['url']}) {feat['summary']}{color_tag}{tv_note}"
                )
            lines.append(f"\nFeature watch: {'; '.join(feature_notes[:4])}")

        return "\n".join(lines)
