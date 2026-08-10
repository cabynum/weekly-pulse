# Data Processing - Weekly Highlights Draft
Generated: 2026-08-06 17:06
Enriched: 2026-08-07 10:14 (Slack)
Revised: 2026-08-07 11:20 (team feedback)
Late add: 2026-08-07 12:20 (Alina Slack)

## Suggested Section for AAET Weekly Pulse Check

**Data Processing** (Chris Bynum) - 30 issues completed

Highlights:

- Addressed five Critical Spark Operator CVE blockers for 3.5 ([RHOAIENG-80812](https://redhat.atlassian.net/browse/RHOAIENG-80812) through [RHOAIENG-80816](https://redhat.atlassian.net/browse/RHOAIENG-80816)): triage confirmed the flagged Java packages are not on the spark-submit execution path the operator uses, and the tickets are closed as Not a Bug.
- Completed the [3.5 GA Week 4 test matrix execution](https://redhat.atlassian.net/browse/RHOAIENG-79113), finishing the final scheduled test run ahead of GA. This follows three prior weeks of execution and closes out the team's GA release gate testing commitment.
- Wrapped up [Spark upgrade test coverage](https://redhat.atlassian.net/browse/RHOAIENG-63123) and [published the upgrade testing overview](https://github.com/opendatahub-io/spark-operator/pull/152) to the midstream docs site, giving customers and field teams a clear reference for operator upgrade paths.
- Resolved a [disconnected environment E2E test failure](https://redhat.atlassian.net/browse/RHOAIENG-75980) caused by a missing mirrored image, improving reliability for air-gapped cluster validation.
- Fixed an intermittent [Konflux build failure](https://redhat.atlassian.net/browse/RHOAIENG-72988) caused by `go mod download` network errors, unblocking the downstream build pipeline.
- Validated the Spark Connect + Workbenches workflow end-to-end on a fresh 3.5 cluster, including a simulated FSI use case with 10,000 transactions. Doc fixes from that testing landed in [PR #160](https://github.com/opendatahub-io/spark-operator/pull/160); the Spark UI port-forwarding guide was also removed, now superseded by the HTTPS Route workflow documented last week.
- Wrapped up [hermetic model sourcing for Docling](https://redhat.atlassian.net/browse/RHAIENG-5860): ran an end-to-end OCR conversion test in a UBI9 container with docling from the RHAI index, confirming disconnected operation works.
- Scoped and began [refinement on a continuous indexing and enrichment pipeline reference architecture](https://redhat.atlassian.net/browse/RHAISTRAT-1786) for agent and RAG knowledge bases, targeting use cases across the AI platform.
- Followed up last week's Dynamic Resource Allocation (DRA) assessment with a practical path for 3.6 EA1: Spark may already support DRA through existing pod templates, so the team does not need to wait on new upstream API fields. Aligning with platform on [verification](https://redhat.atlassian.net/browse/RHOAIENG-78648) ([upstream discussion](https://github.com/kubeflow/spark-operator/issues/2858)).
- Started work to [automate upstream-to-midstream Spark Operator sync](https://redhat.atlassian.net/browse/RHOAIENG-80361), coordinating with DevTestOps on merge configs and exploring agent-assisted conflict resolution for future sprints.
- Advanced the [Spark platform modularization PR](https://github.com/opendatahub-io/opendatahub-operator/pull/3836): latest review comments addressed. After approval, RHOAI component onboarding is next so related-image CI validation can pass.

<!-- Publish scope 2026-08-07: DP only. Team feedback: dropped Sophrosyne; modularization reframed from risk to progress. Late add 2026-08-07: Alina Spark Connect E2E + RHAIENG-5860 Docling hermetic sourcing. -->

---

## Raw Bullets (for editing)

### DATA_PROCESSING

- Addressed five Critical Spark Operator CVE blockers for 3.5 ([RHOAIENG-80812](https://redhat.atlassian.net/browse/RHOAIENG-80812) through [RHOAIENG-80816](https://redhat.atlassian.net/browse/RHOAIENG-80816)): triage confirmed the flagged Java packages are not on the spark-submit execution path the operator uses, and the tickets are closed as Not a Bug.
- Completed the [3.5 GA Week 4 test matrix execution](https://redhat.atlassian.net/browse/RHOAIENG-79113), finishing the final scheduled test run ahead of GA. This follows three prior weeks of execution and closes out the team's GA release gate testing commitment.
- Wrapped up [Spark upgrade test coverage](https://redhat.atlassian.net/browse/RHOAIENG-63123) and [published the upgrade testing overview](https://github.com/opendatahub-io/spark-operator/pull/152) to the midstream docs site, giving customers and field teams a clear reference for operator upgrade paths.
- Resolved a [disconnected environment E2E test failure](https://redhat.atlassian.net/browse/RHOAIENG-75980) caused by a missing mirrored image, improving reliability for air-gapped cluster validation.
- Fixed an intermittent [Konflux build failure](https://redhat.atlassian.net/browse/RHOAIENG-72988) caused by `go mod download` network errors, unblocking the downstream build pipeline.
- Validated the Spark Connect + Workbenches workflow end-to-end on a fresh 3.5 cluster, including a simulated FSI use case with 10,000 transactions. Doc fixes from that testing landed in [PR #160](https://github.com/opendatahub-io/spark-operator/pull/160); the Spark UI port-forwarding guide was also removed, now superseded by the HTTPS Route workflow documented last week.
- Wrapped up [hermetic model sourcing for Docling](https://redhat.atlassian.net/browse/RHAIENG-5860): ran an end-to-end OCR conversion test in a UBI9 container with docling from the RHAI index, confirming disconnected operation works.
- Scoped and began [refinement on a continuous indexing and enrichment pipeline reference architecture](https://redhat.atlassian.net/browse/RHAISTRAT-1786) for agent and RAG knowledge bases, targeting use cases across the AI platform.
- Followed up last week's Dynamic Resource Allocation (DRA) assessment with a practical path for 3.6 EA1: Spark may already support DRA through existing pod templates, so the team does not need to wait on new upstream API fields. Aligning with platform on [verification](https://redhat.atlassian.net/browse/RHOAIENG-78648) ([upstream discussion](https://github.com/kubeflow/spark-operator/issues/2858)).
- Started work to [automate upstream-to-midstream Spark Operator sync](https://redhat.atlassian.net/browse/RHOAIENG-80361), coordinating with DevTestOps on merge configs and exploring agent-assisted conflict resolution for future sprints.
- Advanced the [Spark platform modularization PR](https://github.com/opendatahub-io/opendatahub-operator/pull/3836): latest review comments addressed. After approval, RHOAI component onboarding is next so related-image CI validation can pass.

### RISKS

- The [Spark Application UI and spark-history MCP server](https://redhat.atlassian.net/browse/RHAISTRAT-1408) feature is in Release Pending state. Awaiting final product release steps to clear.
- ~~Spark Operator modularization CI blocked~~ dropped; reframed as DP progress per team feedback (2026-08-07).

### ASSOCIATES

- ~~Rishabh Sophrosyne Phase 1~~ dropped per team feedback (2026-08-07): not continuing.

---

## Source Data Summary

- Jira: 30 completed, 100 in progress
- GitHub: 10 PRs merged, 3 by team
- Slack: 43 messages across 5 team members
- Sections: DATA_PROCESSING (published); RISKS/ASSOCIATES held or dropped after team feedback
