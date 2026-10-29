# Data Processing - Weekly Highlights Draft
Generated: 2026-10-29 17:22

## Suggested Section for AAET Weekly Pulse Check

**Data Processing** (Chris Bynum) - 1 issues completed

Highlights:

- Landed a [network policy pod inventory](https://github.com/opendatahub-io/spark-operator/pull/207) in the ODH midstream repo, building on last week's network isolation work by cataloging all pods that need policy coverage for egress and webhook ingress.
- Fixed a [Deployment selector label regression](https://github.com/opendatahub-io/spark-operator/pull/212) in the midstream Spark Operator module that would have broken in-place upgrades from 3.5 to 3.6, preserving upgrade continuity for existing deployments.
- Enabled [early-gate testing to run automatically on PRs](https://github.com/opendatahub-io/spark-operator/pull/213) in the midstream repo, shifting validation left so issues surface before merge rather than after.
- Wrapped up [research into OpenShift CI approaches](https://redhat.atlassian.net/browse/RHOAIENG-74892) for RHOAI testing, completing the Phase 3a investigation that will inform how the team structures CI going forward.
- The [official Spark Operator scaling guidelines](https://redhat.atlassian.net/browse/RHAISTRAT-2591) effort continues, building on last week's P0 benchmarking results. Work is in progress to translate benchmark data into published guidance for 3.6 GA.
- The [high-fidelity document conversion reference example](https://redhat.atlassian.net/browse/RHAISTRAT-1951) for policy documents, transcripts, and wikis is in review, with the docling-based pipeline targeting structured clean text output on OpenShift AI.
- The [structured information extraction from cheques](https://redhat.atlassian.net/browse/RHAISTRAT-1787) phased reference example remains in progress, a Critical-priority deliverable for 3.6 GA.

---

## Raw Bullets (for editing)

### DATA_PROCESSING

- Landed a [network policy pod inventory](https://github.com/opendatahub-io/spark-operator/pull/207) in the ODH midstream repo, building on last week's network isolation work by cataloging all pods that need policy coverage for egress and webhook ingress.
- Fixed a [Deployment selector label regression](https://github.com/opendatahub-io/spark-operator/pull/212) in the midstream Spark Operator module that would have broken in-place upgrades from 3.5 to 3.6, preserving upgrade continuity for existing deployments.
- Enabled [early-gate testing to run automatically on PRs](https://github.com/opendatahub-io/spark-operator/pull/213) in the midstream repo, shifting validation left so issues surface before merge rather than after.
- Wrapped up [research into OpenShift CI approaches](https://redhat.atlassian.net/browse/RHOAIENG-74892) for RHOAI testing, completing the Phase 3a investigation that will inform how the team structures CI going forward.
- The [official Spark Operator scaling guidelines](https://redhat.atlassian.net/browse/RHAISTRAT-2591) effort continues, building on last week's P0 benchmarking results. Work is in progress to translate benchmark data into published guidance for 3.6 GA.
- The [high-fidelity document conversion reference example](https://redhat.atlassian.net/browse/RHAISTRAT-1951) for policy documents, transcripts, and wikis is in review, with the docling-based pipeline targeting structured clean text output on OpenShift AI.
- The [structured information extraction from cheques](https://redhat.atlassian.net/browse/RHAISTRAT-1787) phased reference example remains in progress, a Critical-priority deliverable for 3.6 GA.

---

## Source Data Summary

- Jira: 1 completed by team, 8 in progress
- GitHub: 9 PRs merged, 3 by team
- Sections: DATA_PROCESSING
