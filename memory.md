# Weekly Pulse - Project Memory

## Pipeline Architecture (READ FIRST)

Human-in-the-loop pipeline with two phases in different environments:

**Phase 1 - Generate (GitHub Actions, automated):**
GH Action (Thursday cron or manual) collects Jira + GitHub + baseline
report, synthesizes via LLM, saves draft to `output/YYYY-MM-DD/draft.md`,
commits and uploads artifact. CI NEVER collects Slack and NEVER publishes.
The `--skip-slack` flag is always passed.

**Phase 2 - Enrich + Publish (Cursor/Argus, interactive):**
User says "review the pulse" which triggers the `weekly-pulse-review`
skill. Skill sweeps Slack via MCP, enriches the draft, presents for
user approval, then publishes to Google Doc via GWS MCP.

**Critical rules:**

- Target Google Doc is ALWAYS discovered dynamically from the Drive
  reports folder (`1Nfir4VgHzPSUGZBJHFRM0GPYj8k5VeHu`). Never
  hardcode a doc ID.
- Slack data comes from Cursor's Slack MCP, not from CI.
- Nothing publishes without user approval.

---

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

CI pipeline runs green. Cron at 1:00pm ET (after Cat's noon report).
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

Publisher module (`publish.py`) works end-to-end in CI - credentials,
section detection, and Google Docs write all validated. But it has a
critical bug: the doc ID is hardcoded to a stale document
(`1jMyzuYlkKyl_...`) instead of the actual live doc
(`18FVFNqzjKuMUyCQXnpzWZnVKMKIlGvYLN8Tvjfd9Vvw`). The plan specified
dynamic discovery via Slack channel search but this was not implemented.
The stale doc got test data written to it (no harm done - it's not the
live one).

Additionally: output quality is formulaic (mechanical "Completed X" bullets).
The hand-edited v3 draft in `output/2026-06-12/draft.md` shows what good
output looks like. `prompt.md` tuning needed.

### Next Session

1. Fix `publish.py` doc discovery - remove hardcoded ID, implement lookup
   (Slack search for CI won't work without token; use a config file
   `doc_id.txt` that gets updated manually or via the review skill)
2. Create a TEST doc for CI validation (don't use the live doc)
3. Tune `prompt.md` for higher quality synthesis output
4. Update the README/architecture to reflect the live doc is
   `18FVFNqzjKuMUyCQXnpzWZnVKMKIlGvYLN8Tvjfd9Vvw` (DO NOT WRITE TO IT
   without explicit approval)

---

## 2026-06-14 - Multi-Section Routing + Native Formatting

### Resume

Publish pipeline rewritten. Multi-section routing, native Google Docs
formatting, Drive folder discovery, UTF-16 link math, LLM sentiment
emoji. All pushed to remote.

### Done

- Multi-section synthesis: DATA_PROCESSING, RISKS, CUSTOMERS, ASSOCIATES
- Drive folder discovery (folder ID: 1Nfir4VgHzPSUGZBJHFRM0GPYj8k5VeHu,
  shared drive support)
- Native bullets (createParagraphBullets), inline hyperlinks, bold removal
- UTF-16 offset math for emoji + link positioning
- LLM-based sentiment emoji for Associates
- CI cron skips publish; interactive-only via review skill
- prompt.md tuned with quality examples and anti-patterns
- Test doc: "Weekly Pulse - TEST" (1BLo26JCsoZSUta_KoP_BSkXZvGYyW0iO_EcJTFGkwgY)

### Left Off

Code pushed. Need to trigger the GitHub Action (workflow_dispatch) to
test the full generate + publish pipeline e2e. The local generate run
failed because the local environment doesn't have Cat's repo access
(CI secrets handle this). Next step: run the GH Action, then publish
its output to the test doc.

### Next Session

1. Trigger GH Action via workflow_dispatch
2. Pull the new draft and publish to test doc
3. Validate multi-section routing and formatting quality
4. If good, Thursday flow is ready

---

## 2026-06-14 (session 2) - Pipeline Validated E2E

### Resume

Pipeline fully validated. Every layer of silent failure found and fixed.

### Done

- LLM was 403ing every run (wrong SA key). Fixed with fresh
  `dp-ai-usage` key. Model updated to `claude-sonnet-4-6`.
- Template regex matched wrong code block. Prompt never reached LLM.
  Fixed regex to anchor on `## User Prompt Template`.
- Silent fallback removed. Pipeline fails red when LLM is unreachable.
- GH Action stripped to generate-only. No publish, no Slack.
- Stale doc ID (`1jMyzuYlkKyl...`) removed everywhere.
- Skill updated: uses `publish.py` locally (not MCP) for native links.
- Dashboard notification says "produce the report" not "review."
- Boilerplate "in progress" and "feature watch" removed from draft.

### Left Off

Pipeline working e2e against test doc. Three sections routed
(DATA_PROCESSING, RISKS, ASSOCIATES) with inline Jira hyperlinks.
Minor: publish.py can't match "Risks / Issues" heading (space issue).

### Next Session

Fix "Risks / Issues" heading match. Thursday: real run.
