"""
Read prompt.md, format collected data into the template, call the LLM,
and return bullet points for the weekly report.
"""

import os
import re
from pathlib import Path
from typing import Optional

try:
    from anthropic import AnthropicVertex
except ImportError:
    AnthropicVertex = None


PROMPT_FILE = Path(__file__).parent / "prompt.md"


def _load_prompt() -> tuple[str, str]:
    """Parse prompt.md into (system_prompt, user_template)."""
    text = PROMPT_FILE.read_text()

    system_match = re.search(
        r"## System Prompt\s*\n(.*?)(?=\n---\n)", text, re.DOTALL
    )
    system_prompt = system_match.group(1).strip() if system_match else ""

    template_match = re.search(r"```\n(.*?)```", text, re.DOTALL)
    user_template = template_match.group(1).strip() if template_match else ""

    return system_prompt, user_template


class Synthesizer:
    """Turns collected data into human-readable bullet points via LLM."""

    def __init__(self, vertex_project: str = None, vertex_region: str = None,
                 model: str = None):
        self.model = model or os.getenv(
            "LLM_MODEL", "claude-sonnet-4-5@20250929"
        )
        self.system_prompt, self.user_template = _load_prompt()

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

    # -- Data formatting helpers ------------------------------------------

    def _fmt_tickets(self, tickets: list) -> str:
        if not tickets:
            return "(none)"
        return "\n".join(
            f"- [{t['key']}]({t['url']}) {t['summary']} "
            f"[{t['status']}] assigned:{t['assignee']} priority:{t['priority']}"
            for t in tickets[:20]
        )

    def _fmt_prs(self, prs: list) -> str:
        if not prs:
            return "(none)"
        return "\n".join(
            f"- #{pr['number']} {pr['title']} by {pr['author']} ({pr['url']})"
            for pr in prs[:15]
        )

    def _fmt_reviews(self, reviews: list) -> str:
        if not reviews:
            return "(none)"
        return "\n".join(
            f"- {r['reviewer']} reviewed #{r['pr_number']} {r['pr_title']} "
            f"[{r['state']}] ({r['pr_url']})"
            for r in reviews[:15]
        )

    def _fmt_github_summary(self, github_data: dict) -> str:
        team = len(github_data.get("team_prs", []))
        external = len(github_data.get("external_prs", []))
        reviews = len(github_data.get("team_reviews", []))
        return (
            f"{github_data.get('total_merged', 0)} PRs merged total "
            f"({team} by team, {external} external). "
            f"{reviews} reviews by team members."
        )

    def _fmt_slack(self, slack_data: dict) -> str:
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

    # -- Core synthesis ---------------------------------------------------

    def synthesize(self, report_data: dict, github_data: dict,
                   jira_data: dict, slack_data: dict = None) -> str:
        """Generate bullet points from all collected data."""
        prompt = self.user_template.format(
            current_dp_section=report_data.get("dp_section", "(not available)"),
            jira_completed_count=jira_data.get("counts", {}).get("completed", 0),
            jira_in_progress_count=jira_data.get("counts", {}).get("in_progress", 0),
            jira_completed=self._fmt_tickets(jira_data.get("completed", [])),
            jira_features=self._fmt_tickets(jira_data.get("features", [])),
            github_summary=self._fmt_github_summary(github_data),
            team_prs=self._fmt_prs(github_data.get("team_prs", [])),
            team_reviews=self._fmt_reviews(github_data.get("team_reviews", [])),
            slack_summary=self._fmt_slack(slack_data),
        )

        if not self.client:
            return self._fallback(jira_data, github_data)

        try:
            resp = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                system=self.system_prompt,
                messages=[{"role": "user", "content": prompt}],
            )
            return resp.content[0].text.strip()
        except Exception as e:
            print(f"LLM error: {e}")
            return self._fallback(jira_data, github_data)

    def _fallback(self, jira_data: dict, github_data: dict) -> str:
        """Basic bullet generation when LLM is unavailable."""
        bullets = []
        for t in jira_data.get("completed", [])[:5]:
            bullets.append(f"- Completed [{t['key']}]({t['url']}): {t['summary']}")
        team_prs = github_data.get("team_prs", [])
        if team_prs:
            bullets.append(f"- Merged {len(team_prs)} PRs across tracked repositories")
        if not bullets:
            bullets.append("- (No significant activity captured this period)")
        return "\n".join(bullets)

    def format_full_section(self, bullets: str, jira_data: dict,
                            team_name: str = "Data Processing",
                            leader_name: str = "Chris Bynum") -> str:
        """Format the complete team section for the report."""
        completed = jira_data.get("counts", {}).get("completed", 0)
        in_progress = jira_data.get("counts", {}).get("in_progress", 0)
        features = jira_data.get("features", [])

        lines = [
            f"**{team_name}** ({leader_name}) - {completed} issues completed\n",
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
