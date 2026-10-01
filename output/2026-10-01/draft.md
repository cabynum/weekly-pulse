# Data Processing - Weekly Highlights Draft
Generated: 2026-10-01 17:01

## Suggested Section for AAET Weekly Pulse Check

**Data Processing** (Chris Bynum) - 23 issues completed

Highlights:

- Completed the team's [3.6 EA1 release gate requirements](https://redhat.atlassian.net/browse/RHOAIENG-82988), executing the RC1 test matrix and clearing the sign-off checkpoint for this milestone.
- Resolved a persistent pattern of [DAG Ordering and Spark operator component validation test failures](https://redhat.atlassian.net/browse/RHOAIENG-93080) that had been surfacing as blockers across multiple CI runs. Closing this cluster of tickets removes ongoing noise from the release pipeline.
- Completed [OLMv1 compliance sign-off](https://redhat.atlassian.net/browse/RHOAIENG-95585) for the Spark operator, a required gate for 3.6 GA distribution through the operator catalog.
- Cleaned up a [duplicate SparkConnect query test](https://redhat.atlassian.net/browse/RHOAIENG-77656) in the ODH midstream that became redundant after the corresponding upstream PR merged, keeping the test suite lean and avoiding false signal.
- Reviewed and approved a midstream PR to [configure Spark operator controller resource limits](https://github.com/opendatahub-io/spark-operator/pull/191), enabling operators to be tuned for production workload profiles.
- Active work underway on [TLS compliance for 3.6 GA](https://redhat.atlassian.net/browse/RHAISTRAT-2826) and [official Spark operator scaling guidelines for OpenShift AI](https://redhat.atlassian.net/browse/RHAISTRAT-2591), both targeting the GA milestone.

## Suggested Addition to Risks/Issues Section

- The [DAG Ordering E2E test](https://redhat.atlassian.net/browse/RHOAIENG-93080) has appeared as a blocker across more than ten CI runs over multiple weeks. While individual instances are being closed, the recurring pattern suggests an underlying instability that warrants a root-cause investigation rather than per-run triage.

---

## Raw Bullets (for editing)

### DATA_PROCESSING

- Completed the team's [3.6 EA1 release gate requirements](https://redhat.atlassian.net/browse/RHOAIENG-82988), executing the RC1 test matrix and clearing the sign-off checkpoint for this milestone.
- Resolved a persistent pattern of [DAG Ordering and Spark operator component validation test failures](https://redhat.atlassian.net/browse/RHOAIENG-93080) that had been surfacing as blockers across multiple CI runs. Closing this cluster of tickets removes ongoing noise from the release pipeline.
- Completed [OLMv1 compliance sign-off](https://redhat.atlassian.net/browse/RHOAIENG-95585) for the Spark operator, a required gate for 3.6 GA distribution through the operator catalog.
- Cleaned up a [duplicate SparkConnect query test](https://redhat.atlassian.net/browse/RHOAIENG-77656) in the ODH midstream that became redundant after the corresponding upstream PR merged, keeping the test suite lean and avoiding false signal.
- Reviewed and approved a midstream PR to [configure Spark operator controller resource limits](https://github.com/opendatahub-io/spark-operator/pull/191), enabling operators to be tuned for production workload profiles.
- Active work underway on [TLS compliance for 3.6 GA](https://redhat.atlassian.net/browse/RHAISTRAT-2826) and [official Spark operator scaling guidelines for OpenShift AI](https://redhat.atlassian.net/browse/RHAISTRAT-2591), both targeting the GA milestone.

### RISKS

- The [DAG Ordering E2E test](https://redhat.atlassian.net/browse/RHOAIENG-93080) has appeared as a blocker across more than ten CI runs over multiple weeks. While individual instances are being closed, the recurring pattern suggests an underlying instability that warrants a root-cause investigation rather than per-run triage.

---

## Source Data Summary

- Jira: 23 completed by team, 82 in progress
  (2 additional completed on the Data Processing component but assigned outside the team roster, excluded from this report)
- GitHub: 11 PRs merged, 1 by team
- Sections: DATA_PROCESSING, RISKS
