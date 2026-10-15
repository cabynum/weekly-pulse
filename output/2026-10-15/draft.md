# Data Processing - Weekly Highlights Draft
Generated: 2026-10-15 17:01

## Suggested Section for AAET Weekly Pulse Check

**Data Processing** (Chris Bynum) - 11 issues completed

Highlights:

- Completed the 3.6 EA2 [product sign-off and RC1 test execution](https://redhat.atlassian.net/browse/RHOAIENG-92384) gate requirements, clearing the team's release obligations for this milestone.
- Wrapped up a full P0 benchmarking campaign for the Spark Operator on OpenShift AI, covering [baseline throughput](https://redhat.atlassian.net/browse/RHAIENG-7485), [namespace-density comparison](https://redhat.atlassian.net/browse/RHAIENG-7486), and [artifact retention](https://redhat.atlassian.net/browse/RHAIENG-7487) for further analysis. Results feed directly into the official Spark Operator scaling guidelines effort targeting 3.6 GA.
- Fixed a [webhook namespace-selector bug](https://redhat.atlassian.net/browse/RHAIENG-7751) in the upstream Spark Operator that caused incorrect behavior in multi-tenant Helm installs, landing the fix in the upstream kubeflow repo.
- Resolved a [CI failure in the ODH Spark Pi Kustomize E2E suite](https://redhat.atlassian.net/browse/RHAIENG-7778) where operator deployments were timing out in KIND clusters, restoring CI reliability for midstream validation.
- Fixed a [CI image/config version skew issue](https://github.com/opendatahub-io/spark-operator/pull/200) in the midstream repo by switching to source builds on push, preventing mismatches between the operator image and its configuration on every commit.
- Added [Konflux package rules on main](https://redhat.atlassian.net/browse/RHAIENG-7613) to automatically track each new release branch, reducing manual overhead in the downstream build pipeline.
- Reviewed and approved [NetworkPolicy additions](https://github.com/opendatahub-io/spark-operator/pull/198) for operator egress and webhook ingress in ODH/RHOAI overlays, building on last week's Prometheus metrics NetworkPolicy to round out operator network isolation.

## Suggested Addition to Risks/Issues Section

- TLS compliance for 3.6 GA ([RHAISTRAT-2826](https://redhat.atlassian.net/browse/RHAISTRAT-2826)) remains in progress and is assigned outside the team. Given the Critical priority and GA timeline, this dependency should be tracked closely.

## Suggested Addition to Associates Section

- Rishabh Singh led the full P0 Spark Operator benchmarking effort end-to-end, from [adapting the upstream benchmark workflow to OpenShift AI](https://redhat.atlassian.net/browse/RHAIENG-7273) through execution and artifact retention, producing the data needed to publish official scaling guidelines.
- Shruthi Sankepelly completed the 3.6 EA2 [product sign-off and test execution matrix](https://redhat.atlassian.net/browse/RHOAIENG-92384), fulfilling the team's critical release gate obligations for this milestone.

---

## Raw Bullets (for editing)

### DATA_PROCESSING

- Completed the 3.6 EA2 [product sign-off and RC1 test execution](https://redhat.atlassian.net/browse/RHOAIENG-92384) gate requirements, clearing the team's release obligations for this milestone.
- Wrapped up a full P0 benchmarking campaign for the Spark Operator on OpenShift AI, covering [baseline throughput](https://redhat.atlassian.net/browse/RHAIENG-7485), [namespace-density comparison](https://redhat.atlassian.net/browse/RHAIENG-7486), and [artifact retention](https://redhat.atlassian.net/browse/RHAIENG-7487) for further analysis. Results feed directly into the official Spark Operator scaling guidelines effort targeting 3.6 GA.
- Fixed a [webhook namespace-selector bug](https://redhat.atlassian.net/browse/RHAIENG-7751) in the upstream Spark Operator that caused incorrect behavior in multi-tenant Helm installs, landing the fix in the upstream kubeflow repo.
- Resolved a [CI failure in the ODH Spark Pi Kustomize E2E suite](https://redhat.atlassian.net/browse/RHAIENG-7778) where operator deployments were timing out in KIND clusters, restoring CI reliability for midstream validation.
- Fixed a [CI image/config version skew issue](https://github.com/opendatahub-io/spark-operator/pull/200) in the midstream repo by switching to source builds on push, preventing mismatches between the operator image and its configuration on every commit.
- Added [Konflux package rules on main](https://redhat.atlassian.net/browse/RHAIENG-7613) to automatically track each new release branch, reducing manual overhead in the downstream build pipeline.
- Reviewed and approved [NetworkPolicy additions](https://github.com/opendatahub-io/spark-operator/pull/198) for operator egress and webhook ingress in ODH/RHOAI overlays, building on last week's Prometheus metrics NetworkPolicy to round out operator network isolation.

### RISKS

- TLS compliance for 3.6 GA ([RHAISTRAT-2826](https://redhat.atlassian.net/browse/RHAISTRAT-2826)) remains in progress and is assigned outside the team. Given the Critical priority and GA timeline, this dependency should be tracked closely.

### ASSOCIATES

- Rishabh Singh led the full P0 Spark Operator benchmarking effort end-to-end, from [adapting the upstream benchmark workflow to OpenShift AI](https://redhat.atlassian.net/browse/RHAIENG-7273) through execution and artifact retention, producing the data needed to publish official scaling guidelines.
- Shruthi Sankepelly completed the 3.6 EA2 [product sign-off and test execution matrix](https://redhat.atlassian.net/browse/RHOAIENG-92384), fulfilling the team's critical release gate obligations for this milestone.

---

## Source Data Summary

- Jira: 11 completed by team, 28 in progress
  (4 additional completed on the Data Processing component but assigned outside the team roster, excluded from this report)
- GitHub: 8 PRs merged, 1 by team
- Sections: DATA_PROCESSING, RISKS, ASSOCIATES
