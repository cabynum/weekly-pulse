# Weekly Pulse

Generates Data Processing team highlights for the **AAET Weekly Pulse Check**.

Runs every Thursday morning, before the 12:30pm ET leadership notification.
Collects activity from GitHub, Jira, and Slack, then uses an LLM to
synthesize raw data into human-readable bullet points matching the report format.

## How it works

1. **Fetches** the latest auto-generated AAET report from `catrobson/AAET-Weekly-Status`
2. **Collects** additional context: GitHub PRs/reviews by team members, Jira ticket
   details, Slack messages
3. **Synthesizes** everything into concise bullet points via Claude (Vertex AI)
4. **Outputs** a draft to `output/` and optionally posts to Slack for team review

The draft gives you a head start on supplementing the report before the Friday noon deadline.

## Quick start

```bash
cp .env.example .env
# Fill in credentials

pip install -r requirements.txt
python generate.py --days-back 7
```

## Automated schedule

GitHub Actions runs every Thursday at 9:00am ET. You can also trigger manually
from the Actions tab.

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
