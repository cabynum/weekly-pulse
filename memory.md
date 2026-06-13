## 2026-06-12

### Resume

Weekly-pulse v1 built, tested, and pushed to `cabynum/weekly-pulse`. First
draft produced for Jun 11 report. Style rules established and captured in
`prompt.md`. Codebase refactored for clarity.

### Left Off

Three gaps for full automation:

1. Google Docs publisher (find DP section in weekly doc, replace with draft)
2. GitHub Actions secrets (GH_PAT_TOKEN, JIRA creds, GCP_CREDENTIALS)
3. Slack webhook or posting mechanism for team review

### Open Questions

- Best approach for Google Docs updates from CI: gws CLI (like Cat's system)
  or google-api-python-client?
- Should we contribute DP-specific repos to Cat's config.yaml upstream?
- Rishabh wants to help improve the tooling: loop him in?

---

## 2026-06-12 - CI + Notifications

### Resume

CI pipeline runs green. Cron at 12:30pm ET (after Cat's noon report).
4 of 5 secrets set. Dashboard notification system pulsing when draft ready.
Output organized into date folders.

### Left Off

Remaining for full autonomy: Slack user token, Google Docs publisher, Slack
notify step. All else is working end-to-end.

### Open Questions

- Is the Slack user token worth the complexity for weekly collection, or is
  manual MCP sweep during review sufficient?
- Google Docs publisher: use google-api-python-client directly, or explore
  Cat's gws CLI approach?

---

## 2026-06-13 - Review and Publish Skill

### Resume

Built the interactive "review and publish" flow as an Argus skill. Ran a
feasibility spike on the Google Docs publisher, validated MCP tools work
for section replacement. Created the `weekly-pulse-review` skill and
enhanced the Dashboard notification with an action button.

### Done

- Feasibility spike: confirmed Google Docs MCP tools can read/write the
  "Weekly Summary" doc (ID: `1jMyzuYlkKyl_CULDhyb2CaWGUrAkk4DI6rW0diI0J38`)
- Validated `find_and_replace_doc` works for unique text replacement (no-op test)
- Identified doc structure: teams are bullets under "Weekly Updates", not headings
- Created `.cursor/skills/weekly-pulse-review/SKILL.md` with full 7-step workflow
- Designed Slack MCP sweep: `search_messages` per team member (5 calls)
- Added "Review Pulse" button to Dashboard notification bar (copies trigger phrase)
- Updated `/argus.start` action item text to mention the skill trigger

### Decisions

- 2026-06-13: Google Docs publisher approach is interactive (Argus session),
  not CI. Use `find_and_replace_doc` for filled sections, `modify_doc_text`
  with index calculation for blank templates.
- 2026-06-13: Slack sweep uses MCP `search_messages` (browser token) during
  review session, not a CI-stable xoxp token. Human-in-loop is the design.
- 2026-06-13: Re-synthesis skips LLM call; manually integrate notable Slack
  findings as extra bullets to keep it fast and predictable.

### Left Off

Skill is scaffolded and ready for first live test. The next Thursday
(Jun 18) will be the first real run. Key things to validate live:
1. Does the Slack sweep return useful signal from MCP?
2. Does the section boundary detection work on the current week's template?
3. Does the full publish flow work end-to-end?

### Open Questions

- How does Sarah prepare the doc each week? Does she insert the date into
  the template beforehand, or fill it after collecting content?
- Should we auto-detect "current week" by date proximity, or always ask?
