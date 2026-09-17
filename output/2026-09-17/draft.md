# Data Processing - Weekly Highlights Draft
Generated: 2026-09-17 17:01

## Suggested Section for AAET Weekly Pulse Check

**Data Processing** (Chris Bynum) - 32 issues completed

Highlights:

- Synced upstream kubeflow/spark-operator v2.5.1 changes [into the ODH midstream](https://github.com/opendatahub-io/spark-operator/pull/181), keeping the midstream current ahead of the 3.6 release cycle.
- Fixed a Helm CI branch fallback bug for [scheduled runs](https://github.com/opendatahub-io/spark-operator/pull/182), resolving an edge case where scheduled pipelines could target the wrong branch.
- Resolved a wave of [critical CVEs in the 3.5.1 GA Spark operator image](https://redhat.atlassian.net/browse/RHOAIENG-81554), covering vulnerabilities across Python, OpenSSH, libvpx, libtiff, libnghttp2, openexr-libs, and vim packages. All 20 CVE tickets are now closed.
- Completed the [3.6 EA1 product and documentation sign-offs](https://redhat.atlassian.net/browse/RHOAIENG-83071) for Data Processing, and executed the [3.6 EA2 test matrix (Week 1)](https://redhat.atlassian.net/browse/RHOAIENG-92120), clearing the team's release gate requirements for both milestones.
- Continuing work on the [GPU-accelerated Docling serve API container image for 3.6 EA2](https://redhat.atlassian.net/browse/RHAISTRAT-2618), with the batch processing image already complete.
- Drafting [official Spark Operator scaling guidelines for OpenShift AI](https://redhat.atlassian.net/browse/RHAISTRAT-2591) to give customers validated recommendations for large-scale deployments.
- Two reference architecture workstreams entered refinement: [structured information extraction from cheques](https://redhat.atlassian.net/browse/RHAISTRAT-1787) and a [continuous indexing and enrichment pipeline for agent and RAG knowledge bases](https://redhat.atlassian.net/browse/RHAISTRAT-1786).

---

## Raw Bullets (for editing)

### DATA_PROCESSING

- Synced upstream kubeflow/spark-operator v2.5.1 changes [into the ODH midstream](https://github.com/opendatahub-io/spark-operator/pull/181), keeping the midstream current ahead of the 3.6 release cycle.
- Fixed a Helm CI branch fallback bug for [scheduled runs](https://github.com/opendatahub-io/spark-operator/pull/182), resolving an edge case where scheduled pipelines could target the wrong branch.
- Resolved a wave of [critical CVEs in the 3.5.1 GA Spark operator image](https://redhat.atlassian.net/browse/RHOAIENG-81554), covering vulnerabilities across Python, OpenSSH, libvpx, libtiff, libnghttp2, openexr-libs, and vim packages. All 20 CVE tickets are now closed.
- Completed the [3.6 EA1 product and documentation sign-offs](https://redhat.atlassian.net/browse/RHOAIENG-83071) for Data Processing, and executed the [3.6 EA2 test matrix (Week 1)](https://redhat.atlassian.net/browse/RHOAIENG-92120), clearing the team's release gate requirements for both milestones.
- Continuing work on the [GPU-accelerated Docling serve API container image for 3.6 EA2](https://redhat.atlassian.net/browse/RHAISTRAT-2618), with the batch processing image already complete.
- Drafting [official Spark Operator scaling guidelines for OpenShift AI](https://redhat.atlassian.net/browse/RHAISTRAT-2591) to give customers validated recommendations for large-scale deployments.
- Two reference architecture workstreams entered refinement: [structured information extraction from cheques](https://redhat.atlassian.net/browse/RHAISTRAT-1787) and a [continuous indexing and enrichment pipeline for agent and RAG knowledge bases](https://redhat.atlassian.net/browse/RHAISTRAT-1786).

---

## Source Data Summary

- Jira: 32 completed by team, 57 in progress
  (4 additional completed on the Data Processing component but assigned outside the team roster, excluded from this report)
- GitHub: 5 PRs merged, 2 by team
- Sections: DATA_PROCESSING
