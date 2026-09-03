# Data Processing - Weekly Highlights Draft
Generated: 2026-09-03 17:01

## Suggested Section for AAET Weekly Pulse Check

**Data Processing** (Chris Bynum) - 15 issues completed

Highlights:

- Cleared all 3.5 GA RC3 release gate requirements, completing [test matrix execution, ROSA HCP smoke tests, disconnected bare metal install, and disconnected upgrade from 3.4 to 3.5](https://redhat.atlassian.net/browse/RHOAIENG-88072) across OCP 4.21 and 4.22. Documentation sign-off for [3.5 GA](https://redhat.atlassian.net/browse/RHOAIENG-74581) was also closed this week.
- Following last week's 3.6 EA1 Week 1 test execution, completed the [Week 2 test matrix run](https://redhat.atlassian.net/browse/RHOAIENG-82901), advancing the team's EA1 release gate obligations through the second validation cycle.
- Added [weekly scheduled CI runs on the midstream main branch](https://github.com/opendatahub-io/spark-operator/pull/172) with failure notifications, giving the team continuous visibility into regressions between release cycles.
- Resolved a [noisy CI issue](https://redhat.atlassian.net/browse/RHOAIENG-85763) where unrelated tests were being triggered and attributed to Spark E2E runs, improving signal quality in test reporting.
- Updated [PySpark to version 4.0.4](https://redhat.atlassian.net/browse/RHAIENG-6956) in the downstream build, keeping the downstream aligned with the latest upstream PySpark release.
- Streamlined the downstream build pipeline by [adding a pull-request pipeline for the full spark-operator on main](https://redhat.atlassian.net/browse/RHAIENG-7261) and [removing the inherited ODH push pipeline](https://redhat.atlassian.net/browse/RHAIENG-7262), reducing pipeline complexity inherited from the midstream.
- Completed this week's [upstream-to-midstream sync](https://redhat.atlassian.net/browse/RHAIENG-6385), keeping the ODH midstream current with upstream development.

## Suggested Addition to Risks/Issues Section

- Spark Operator [scaling guidelines for OpenShift AI](https://redhat.atlassian.net/browse/RHAISTRAT-2591) remain in refinement with no published guidance yet. Field teams asking for production sizing recommendations continue to lack official documentation; this is now a second week without resolution.

## Suggested Addition to Associates Section

- Shruthi Sankepelly drove all five 3.5 GA RC3 sign-off tracks this week, including disconnected bare metal install, disconnected upgrade, ROSA HCP smoke tests, full test matrix execution, and documentation sign-off, a high-volume delivery that cleared the team's GA release gate obligations.

---

## Raw Bullets (for editing)

### DATA_PROCESSING

- Cleared all 3.5 GA RC3 release gate requirements, completing [test matrix execution, ROSA HCP smoke tests, disconnected bare metal install, and disconnected upgrade from 3.4 to 3.5](https://redhat.atlassian.net/browse/RHOAIENG-88072) across OCP 4.21 and 4.22. Documentation sign-off for [3.5 GA](https://redhat.atlassian.net/browse/RHOAIENG-74581) was also closed this week.
- Following last week's 3.6 EA1 Week 1 test execution, completed the [Week 2 test matrix run](https://redhat.atlassian.net/browse/RHOAIENG-82901), advancing the team's EA1 release gate obligations through the second validation cycle.
- Added [weekly scheduled CI runs on the midstream main branch](https://github.com/opendatahub-io/spark-operator/pull/172) with failure notifications, giving the team continuous visibility into regressions between release cycles.
- Resolved a [noisy CI issue](https://redhat.atlassian.net/browse/RHOAIENG-85763) where unrelated tests were being triggered and attributed to Spark E2E runs, improving signal quality in test reporting.
- Updated [PySpark to version 4.0.4](https://redhat.atlassian.net/browse/RHAIENG-6956) in the downstream build, keeping the downstream aligned with the latest upstream PySpark release.
- Streamlined the downstream build pipeline by [adding a pull-request pipeline for the full spark-operator on main](https://redhat.atlassian.net/browse/RHAIENG-7261) and [removing the inherited ODH push pipeline](https://redhat.atlassian.net/browse/RHAIENG-7262), reducing pipeline complexity inherited from the midstream.
- Completed this week's [upstream-to-midstream sync](https://redhat.atlassian.net/browse/RHAIENG-6385), keeping the ODH midstream current with upstream development.

### RISKS

- Spark Operator [scaling guidelines for OpenShift AI](https://redhat.atlassian.net/browse/RHAISTRAT-2591) remain in refinement with no published guidance yet. Field teams asking for production sizing recommendations continue to lack official documentation; this is now a second week without resolution.

### ASSOCIATES

- Shruthi Sankepelly drove all five 3.5 GA RC3 sign-off tracks this week, including disconnected bare metal install, disconnected upgrade, ROSA HCP smoke tests, full test matrix execution, and documentation sign-off, a high-volume delivery that cleared the team's GA release gate obligations.

---

## Source Data Summary

- Jira: 15 completed by team, 27 in progress
  (4 additional completed on the Data Processing component but assigned outside the team roster, excluded from this report)
- GitHub: 9 PRs merged, 1 by team
- Sections: DATA_PROCESSING, RISKS, ASSOCIATES
