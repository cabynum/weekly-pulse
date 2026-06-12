# Weekly Pulse

Generates Data Processing team highlights for the **AAET Weekly Pulse Check**.

Runs every Thursday morning, before the 12:30pm ET leadership notification.
Collects activity from GitHub, Jira, and Slack, then uses an LLM to
synthesize raw data into human-readable bullet points matching the report format.

## How it works

![Weekly Pulse autonomous flow](weekly-pulse-flow.png)

1. **Cron trigger** - GitHub Actions fires every Thursday at 12:30pm ET
2. **Collect** - pulls from four sources in parallel: GitHub PRs/reviews,
   Jira tickets, Slack messages, and the baseline AAET report
3. **Synthesize** - Claude (Vertex AI) distills raw data into concise,
   style-matched bullet points
4. **Publish** - a Google Docs publisher module finds and replaces the
   Data Processing section in the live Pulse doc
5. **Notify** - posts the draft to Slack for a quick human review before
   the Friday noon deadline

The goal is full autonomy: no human in the loop until the review step.
Today, steps 1-3 work; steps 4-5 (publish + notify) are the remaining gaps.

## Architecture

![System architecture](system-architecture.png)

The system is a Python pipeline orchestrated by `generate.py`. GitHub Actions
triggers it on a cron schedule (or manual dispatch). The orchestrator calls four
collector modules in sequence, each hitting a different external API. Collected
data flows into `synthesize.py`, which formats it against `prompt.md` templates
and calls Vertex AI (Claude) for final bullet generation. Output is committed
back to the repo. Google Docs publishing and Slack notification are the next
modules to build (dashed cards above).

## Quick start

```bash
cp .env.example .env
# Fill in credentials

pip install -r requirements.txt
python generate.py --days-back 7
```

## Automated schedule

GitHub Actions runs every Thursday at 12:30pm ET (after Cat's AAET baseline
report generates at noon). Draft is ready for review by ~12:35pm, targeting
team Slack post by 2pm. You can also trigger manually from the Actions tab.

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
| `SLACK_USER_TOKEN` | Slack message search (xoxp token, `search:read` scope) |
| `GCP_CREDENTIALS` | Vertex AI for Claude (JSON service account key) |
