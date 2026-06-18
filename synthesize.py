"""
Read prompt.md, format collected data into the template, call the LLM,
and return structured bullet points routed to report sections.
"""

import os
import re
from datetime import datetime, timedelta
from pathlib import Path

try:
    from anthropic import AnthropicVertex
except ImportError:
    AnthropicVertex = None


PROMPT_FILE = Path(__file__).parent / "prompt.md"

SECTION_KEYS = ["DATA_PROCESSING", "RISKS", "CUSTOMERS", "ASSOCIATES"]


def _load_prompt() -> tuple[str, str]:
    """Parse prompt.md into (system_prompt, user_template)."""
    text = PROMPT_FILE.read_text()

    system_match = re.search(
        r"## System Prompt\s*\n(.*?)(?=\n---\n)", text, re.DOTALL
    )
    system_prompt = system_match.group(1).strip() if system_match else ""

    template_match = re.search(
        r"## User Prompt Template\s*\n.*?```\w*\n(.*?)```", text, re.DOTALL
    )
    user_template = template_match.group(1).strip() if template_match else ""

    return system_prompt, user_template


def parse_sections(raw: str) -> dict[str, str]:
    """Parse LLM output with [SECTION] markers into a dict.

    Returns a dict keyed by section name (DATA_PROCESSING, RISKS, etc.)
    with the bullet text as values. Sections not present in the output
    are omitted from the dict. Untagged content at the top defaults to
    DATA_PROCESSING.
    """
    sections: dict[str, list[str]] = {}
    current = None

    for line in raw.split("\n"):
        stripped = line.strip()
        marker = re.match(r"^\[([A-Z_]+)\]$", stripped)
        if marker:
            key = marker.group(1)
            if key in SECTION_KEYS:
                current = key
                if current not in sections:
                    sections[current] = []
            continue

        if stripped:
            if current is None:
                current = "DATA_PROCESSING"
                sections.setdefault(current, [])
            sections[current].append(line)

    return {k: "\n".join(v).strip() for k, v in sections.items() if v}


class Synthesizer:
    """Turns collected data into human-readable bullet points via LLM."""

    def __init__(self, vertex_project: str = None, vertex_region: str = None,
                 model: str = None):
        self.model = model or os.getenv(
            "LLM_MODEL", "claude-sonnet-4-6"
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
        self.client = AnthropicVertex(project_id=project, region=region)
        print(f"LLM: Vertex AI ({project}/{region}) model={self.model}")

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

    # -- Dedup helpers ----------------------------------------------------

    def _find_previous_draft(self) -> str | None:
        """Find the most recent prior draft with real content."""
        output_dir = Path(__file__).parent / "output"
        if not output_dir.exists():
            return None

        today = datetime.now().strftime("%Y-%m-%d")
        date_dirs = sorted(
            [d for d in output_dir.iterdir()
             if d.is_dir() and d.name != today and (d / "draft.md").exists()],
            key=lambda d: d.name,
            reverse=True,
        )

        for d in date_dirs:
            text = (d / "draft.md").read_text()
            refs = self._extract_references(text)
            if refs:
                print(f"  Dedup baseline: {d.name} ({len(refs)} references)")
                return text

        return None

    def _extract_references(self, draft_text: str) -> set[str]:
        """Extract Jira keys and PR URLs from a draft for dedup."""
        refs = set()
        refs.update(re.findall(r"(?:RHAIENG|RHOAIENG|RHAISTRAT)-\d+", draft_text))
        refs.update(re.findall(r"github\.com/[^\s)]+/pull/\d+", draft_text))
        return refs

    def _build_dedup_clause(self) -> str:
        """Build a prompt clause listing previously reported references."""
        prev_draft = self._find_previous_draft()
        if not prev_draft:
            return ""

        refs = self._extract_references(prev_draft)
        if not refs:
            return ""

        ref_list = "\n".join(f"- {r}" for r in sorted(refs))
        return (
            "\n\n## Previously Reported (DO NOT REPEAT)\n"
            "The following tickets and PRs appeared in last week's report. "
            "Do NOT include bullets about them unless there is genuinely new "
            "progress this week (e.g., a ticket that was 'in review' last week "
            "is now 'shipped'). If a ticket appears below and the only update "
            "is that it was completed, skip it - it was already reported.\n\n"
            f"{ref_list}\n"
        )

    # -- Core synthesis ---------------------------------------------------

    def synthesize(self, report_data: dict, github_data: dict,
                   jira_data: dict, slack_data: dict = None) -> dict[str, str]:
        """Generate bullet points from all collected data.

        Returns a dict keyed by section name (DATA_PROCESSING, RISKS,
        CUSTOMERS, ASSOCIATES) with bullet text as values.
        """
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

        dedup_clause = self._build_dedup_clause()
        if dedup_clause:
            prompt += dedup_clause
            dedup_refs = self._extract_references(
                self._find_previous_draft() or ""
            )
            print(f"  Dedup: {len(dedup_refs)} references from previous draft")

        if not self.client:
            raise RuntimeError(
                "LLM client not initialized. Cannot synthesize without it. "
                "Check anthropic[vertex] install and GCP credentials."
            )

        resp = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            system=self.system_prompt,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = resp.content[0].text.strip()
        sections = parse_sections(raw)
        if not sections.get("DATA_PROCESSING"):
            raise RuntimeError(
                f"LLM returned no DATA_PROCESSING section. Raw output:\n{raw[:500]}"
            )
        return sections

    def format_full_section(self, sections: dict[str, str], jira_data: dict,
                            team_name: str = "Data Processing",
                            leader_name: str = "Chris Bynum") -> str:
        """Format all sections for the draft markdown output."""
        completed = jira_data.get("counts", {}).get("completed", 0)
        in_progress = jira_data.get("counts", {}).get("in_progress", 0)
        features = jira_data.get("features", [])

        dp_bullets = sections.get("DATA_PROCESSING", "- (No updates)")

        lines = [
            f"**{team_name}** ({leader_name}) - {completed} issues completed\n",
            "Highlights:\n",
            dp_bullets,
        ]

        section_labels = {
            "RISKS": "Risks/Issues",
            "CUSTOMERS": "Customers",
            "ASSOCIATES": "Associates",
        }
        for key, label in section_labels.items():
            if key in sections and sections[key].strip():
                lines.append(f"\n## Suggested Addition to {label} Section\n")
                lines.append(sections[key])

        return "\n".join(lines)
