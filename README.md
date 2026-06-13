# Weekly Pulse

Generates Data Processing team highlights for the **AAET Weekly Pulse Check**.

A two-phase system: CI generates a draft autonomously every Thursday, then
an interactive review step handles Slack enrichment and Google Docs publishing
with a human in the loop.

The long-term goal is full autonomy - remove the human from Phase 2 entirely.
Two blockers remain: a pending Slack App approval (for CI-based message
collection) and a Google Docs publisher module (Python, not MCP).

## How it works

![Weekly Pulse flow](weekly-pulse-flow.png)

**Phase 1 - Automated (CI Pipeline, every Thursday 12:30pm ET):**

1. **Cron trigger** - GitHub Actions fires 30min after Cat's baseline AAET report
2. **Collect** - pulls from GitHub PRs/reviews, Jira tickets, and the baseline
   report. Slack message collection requires a Slack App with `search:read`
   scope, which is pending internal approval. Skipped gracefully without it.
3. **Synthesize** - Claude (Vertex AI) distills raw data into concise,
   style-matched bullet points
4. **Output** - draft committed to repo, Dashboard notification fires

**Phase 2 - Interim Manual Steps (goal: automate away):**

1. **Human trigger** - user initiates the review flow locally
2. **Slack sweep** - uses a local MCP tool to search team member messages.
   This is a workaround until the Slack App is approved, at which point
   collection moves into the CI pipeline (Phase 1, step 2).
3. **Enrich** - notable Slack findings are folded into the draft
4. **Review + Approve** - user reviews the final version
5. **Publish** - writes the DP section to the live Google Doc. Currently
   uses a local MCP tool; long-term, this becomes a Python module
   (`google-api-python-client`) running in CI.

## Architecture

![System architecture](system-architecture.png)

The CI layer is a Python pipeline orchestrated by `generate.py`. GitHub Actions
triggers it on a cron schedule (or manual dispatch). The orchestrator calls
collector modules in sequence, each hitting a different external API. Collected
data flows into `synthesize.py`, which formats it against `prompt.md` templates
and calls Vertex AI (Claude) for final bullet generation. Output is committed
back to the repo and a Dashboard notification fires.

The interim manual steps run locally via MCP tools. Slack sweep uses
`search_messages` (browser-authenticated token) to compensate for the
missing CI token. Publishing uses `find_and_replace_doc` or `modify_doc_text`
for Google Docs section replacement. Both of these will become Python modules
in the CI pipeline once the Slack App is approved and Google Docs auth is
configured as a CI secret.

## Quick start

```bash
cp .env.example .env
# Fill in credentials

pip install -r requirements.txt
python generate.py --days-back 7
```

## Automated schedule

GitHub Actions runs every Thursday at 12:30pm ET (after Cat's AAET baseline
report generates at noon). Draft is ready for review by ~12:35pm. You can
also trigger the CI manually from the Actions tab.

## Configuration

Edit `config.yaml` to update:

- Team members (names, emails, GitHub usernames)
- GitHub repos to track
- Jira component and projects
- LLM model settings

## Credentials

| Variable | Purpose |
|---|---|
| `GITHUB_TOKEN` | Access to Cat's report repo + team activity |
| `JIRA_USERNAME` | Jira API auth |
| `JIRA_API_TOKEN` | Jira API auth |
| `SLACK_USER_TOKEN` | Slack message search (xoxp token, `search:read` scope) - pending Slack App approval |
| `GCP_CREDENTIALS` | Vertex AI for Claude (JSON service account key) |

## Automation roadmap

| Blocker | Status | Once resolved |
|---|---|---|
| Slack App (`search:read` scope) | Pending approval | Slack collection moves to CI (Phase 1) |
| Google Docs publisher module | Designed, needs Python impl | Publishing moves to CI, no human needed |
| Full autonomy | Blocked on above | Phase 2 disappears entirely |
