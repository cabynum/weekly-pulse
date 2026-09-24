# Data Processing - Weekly Highlights Draft
Generated: 2026-09-24 17:01

## Suggested Section for AAET Weekly Pulse Check

**Data Processing** (Chris Bynum) - 31 issues completed

Highlights:

- Completed the team's [3.6 EA2 release gate requirements](https://redhat.atlassian.net/browse/RHOAIENG-92098), including test plan sign-off and Week 2 test matrix execution, clearing the final milestone checkpoint.
- Closed out the remaining [critical CVEs in the 3.5.1 GA Spark operator image](https://redhat.atlassian.net/browse/RHOAIENG-81575), adding vim-minimal, vim-filesystem, and additional Python 3.12 packages to the set resolved last week. All open CVE tickets on that image are now closed.
- Fixed a test infrastructure bug where [E2E jobs on release branches](https://redhat.atlassian.net/browse/RHOAIENG-88219) were pulling the `:main` test image instead of the release-matched tag, ensuring release validation runs against the correct artifacts.
- Synced the latest upstream kubeflow/spark-operator changes [into the ODH midstream](https://redhat.atlassian.net/browse/RHOAIENG-94191), continuing to keep the midstream current ahead of the 3.6 release.
- Reviewed and approved a midstream PR to [scope the Spark operator webhook to configurable job namespaces](https://github.com/opendatahub-io/spark-operator/pull/190), a multi-tenancy improvement enabling operators to restrict which namespaces they watch.

## Suggested Addition to Risks/Issues Section

- No new risks to report this week.

---

## Raw Bullets (for editing)

### DATA_PROCESSING

- Completed the team's [3.6 EA2 release gate requirements](https://redhat.atlassian.net/browse/RHOAIENG-92098), including test plan sign-off and Week 2 test matrix execution, clearing the final milestone checkpoint.
- Closed out the remaining [critical CVEs in the 3.5.1 GA Spark operator image](https://redhat.atlassian.net/browse/RHOAIENG-81575), adding vim-minimal, vim-filesystem, and additional Python 3.12 packages to the set resolved last week. All open CVE tickets on that image are now closed.
- Fixed a test infrastructure bug where [E2E jobs on release branches](https://redhat.atlassian.net/browse/RHOAIENG-88219) were pulling the `:main` test image instead of the release-matched tag, ensuring release validation runs against the correct artifacts.
- Synced the latest upstream kubeflow/spark-operator changes [into the ODH midstream](https://redhat.atlassian.net/browse/RHOAIENG-94191), continuing to keep the midstream current ahead of the 3.6 release.
- Reviewed and approved a midstream PR to [scope the Spark operator webhook to configurable job namespaces](https://github.com/opendatahub-io/spark-operator/pull/190), a multi-tenancy improvement enabling operators to restrict which namespaces they watch.

### RISKS

- No new risks to report this week.

---

## Source Data Summary

- Jira: 31 completed by team, 78 in progress
- GitHub: 0 PRs merged, 0 by team
- Sections: DATA_PROCESSING, RISKS
