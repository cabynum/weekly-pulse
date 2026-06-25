# Weekly Pulse

Generates Data Processing team highlights for the **AAET Weekly Pulse Check**.

A two-phase system: CI generates a draft autonomously every Thursday, then
an interactive review step collects Slack data and publishes with a human
in the loop.

## How it works

![Weekly Pulse flow](weekly-pulse-flow.png)

**Phase 1 - Automated (CI + local post-processing, every Thursday 1:00pm ET):**

1. **Dispatch** - macOS LaunchAgent triggers GitHub Actions via `dispatch.sh`
2. **Generate** - CI collects GitHub PRs/reviews, Jira tickets, and the
   baseline AAET report. Claude (Vertex AI) synthesizes into style-matched
   bullets with multi-section routing (DATA_PROCESSING, RISKS, CUSTOMERS,
   ASSOCIATES). Draft committed to repo.
3. **Poll + pull** - `dispatch.sh` polls until CI completes, then pulls the
   draft locally
4. **Notify** - `build.py` updates Dashboard notifications, and a macOS
   desktop notification fires ("Weekly Pulse draft is ready for review")

**Phase 2 - Interactive (Argus session, human in the loop):**

Orchestrated by the `weekly-pulse-review` Argus skill, triggered by the
phrase "produce the report."

1. **Slack collection** - `collect_slack.py` sweeps team member messages
   via the Slack Web API (XOXC/XOXD browser tokens, no admin approval
   needed). Results inform draft enrichment.
2. **Enrich** - notable Slack findings are folded into the draft
3. **Review + approve** - user reviews the final version
4. **Publish** - `publish.py` writes all sections to the live Google Doc
   with native formatting (bullets, hyperlinks, bold removal)

## Architecture

![System architecture](system-architecture.png)

## File overview

| File | Purpose |
|---|---|
| `generate.py` | CI entry point: orchestrates collectors + LLM synthesis |
| `collect_slack.py` | Local Slack collector: sweeps team messages via Web API |
| `synthesize.py` | LLM synthesis: formats data, calls Vertex AI, routes to sections |
| `publish.py` | Google Docs publisher: native formatting with hyperlinks |
| `prompt.md` | LLM system + user prompt templates (edit to tune output) |
| `config.yaml` | Team members, repos, Jira config, LLM settings |
| `collectors/` | Data collectors: baseline, github, jira, slack |

## Quick start

```bash
cp .env.example .env
# Fill in credentials (see table below)

pip install -r requirements.txt
python generate.py --days-back 7
```

## Automated schedule

A macOS LaunchAgent (`com.argus.weekly-pulse-scheduler`) dispatches the
GitHub Actions workflow every Thursday at 1:00pm ET. `dispatch.sh` polls
for CI completion (~2 min), pulls the draft locally, updates Dashboard
notifications, and fires a desktop notification. Draft is ready for
review by ~1:05pm.

You can also trigger manually: `gh workflow run weekly-pulse.yml --repo cabynum/weekly-pulse`

## Configuration

Edit `config.yaml` to update:

- Team members (names, emails, GitHub usernames, Slack IDs)
- GitHub repos to track
- Jira component and projects
- LLM model settings

## Credentials

Stored in `.env` (gitignored). CI uses GitHub Secrets for the same values.

| Variable | Purpose |
|---|---|
| `GITHUB_TOKEN` | Access to Cat's report repo + team activity |
| `JIRA_USERNAME` | Jira API auth |
| `JIRA_API_TOKEN` | Jira API auth |
| `SLACK_XOXC_TOKEN` | Slack message search (browser session token) |
| `SLACK_XOXD_TOKEN` | Slack cookie (companion to XOXC token) |
| `GCP_CREDENTIALS` | Vertex AI for Claude (JSON service account key) |
| `GOOGLE_DOCS_CREDENTIALS` | Google Docs publish (service account JSON) |

**Slack tokens:** Extract XOXC + XOXD from your browser session using
[slack-token-extractor](https://github.com/maorfr/slack-token-extractor).
No Slack App or admin approval needed. Tokens last weeks to months; re-run
the extractor when they expire. Alternatively, use a `SLACK_USER_TOKEN`
(xoxp) if you have a Slack App with `search:read` scope.

## Setup: Google Docs publishing

1. Create a GCP service account (or reuse an existing one)
2. Enable the Google Docs API in the project
3. Share the Weekly Summary doc with the service account email (Editor access)
4. Download the service account JSON key
5. Set `GOOGLE_DOCS_CREDENTIALS` in `.env` or GitHub Secrets
6. Test with: `python publish.py --dry-run`
