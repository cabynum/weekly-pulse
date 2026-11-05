# Data Processing - Weekly Highlights Draft
Generated: 2026-11-05 18:01

## Suggested Section for AAET Weekly Pulse Check

**Data Processing** (Chris Bynum) - 10 issues completed

Highlights:

- Shipped [NetworkPolicy coverage for Kubeflow Spark Operator operands](https://redhat.atlassian.net/browse/RHOAIENG-93732), closing a blocker-priority gap in network isolation for 3.6 GA. This completes the work started several weeks ago with pod inventory and policy scoping.
- Enabled TLS-compliant secure metrics on the midstream Spark Operator by [configuring HTTPS for metrics endpoints](https://github.com/opendatahub-io/spark-operator/pull/205) and [restoring Prometheus scraping via PodMonitors](https://github.com/opendatahub-io/spark-operator/pull/221) after a regression introduced by the TLS change. Added a [TLS-Scanner CI step](https://redhat.atlassian.net/browse/RHOAIENG-95821) to catch compliance drift automatically going forward.
- Updated the [docling-serve version in the container image](https://redhat.atlassian.net/browse/RHAIENG-7670), a blocker-priority fix that keeps the document conversion pipeline current ahead of 3.6 GA.
- Completed [research into tooling and approach selection](https://redhat.atlassian.net/browse/RHAIENG-6958) for downstream productization requirements, laying the groundwork for the document conversion reference architecture.
- Fixed a [Spark Connect E2E test failure](https://github.com/opendatahub-io/spark-operator/pull/216) caused by client dependencies installing into a read-only directory, keeping the midstream CI pipeline green.
- Added [environment specification to the sync job](https://github.com/opendatahub-io/spark-operator/pull/217) in the midstream repo, improving consistency of automated syncing between streams.
- Wrapped up the Spark Operator controller tuning benchmark series, completing [multiple benchmark variants](https://redhat.atlassian.net/browse/RHAIENG-7842) at scale (51 apps) covering worker counts, resource-version polling, and combined tuning. Results are [documented on Confluence](https://redhat.atlassian.net/browse/RHAIENG-7844) and surfaced in an [interactive Grafana dashboard](https://redhat.atlassian.net/browse/RHAIENG-7846), advancing the official scaling guidelines effort toward published guidance for 3.6 GA.

## Suggested Addition to Associates Section

- Vedant Deshpande published a [blog post on job scheduling with Spark Operator and Kueue on OpenShift AI](https://redhat.atlassian.net/browse/RHAIENG-7425), contributing community-facing content that documents a key 3.6 feature for practitioners.

---

## Raw Bullets (for editing)

### DATA_PROCESSING

- Shipped [NetworkPolicy coverage for Kubeflow Spark Operator operands](https://redhat.atlassian.net/browse/RHOAIENG-93732), closing a blocker-priority gap in network isolation for 3.6 GA. This completes the work started several weeks ago with pod inventory and policy scoping.
- Enabled TLS-compliant secure metrics on the midstream Spark Operator by [configuring HTTPS for metrics endpoints](https://github.com/opendatahub-io/spark-operator/pull/205) and [restoring Prometheus scraping via PodMonitors](https://github.com/opendatahub-io/spark-operator/pull/221) after a regression introduced by the TLS change. Added a [TLS-Scanner CI step](https://redhat.atlassian.net/browse/RHOAIENG-95821) to catch compliance drift automatically going forward.
- Updated the [docling-serve version in the container image](https://redhat.atlassian.net/browse/RHAIENG-7670), a blocker-priority fix that keeps the document conversion pipeline current ahead of 3.6 GA.
- Completed [research into tooling and approach selection](https://redhat.atlassian.net/browse/RHAIENG-6958) for downstream productization requirements, laying the groundwork for the document conversion reference architecture.
- Fixed a [Spark Connect E2E test failure](https://github.com/opendatahub-io/spark-operator/pull/216) caused by client dependencies installing into a read-only directory, keeping the midstream CI pipeline green.
- Added [environment specification to the sync job](https://github.com/opendatahub-io/spark-operator/pull/217) in the midstream repo, improving consistency of automated syncing between streams.
- Wrapped up the Spark Operator controller tuning benchmark series, completing [multiple benchmark variants](https://redhat.atlassian.net/browse/RHAIENG-7842) at scale (51 apps) covering worker counts, resource-version polling, and combined tuning. Results are [documented on Confluence](https://redhat.atlassian.net/browse/RHAIENG-7844) and surfaced in an [interactive Grafana dashboard](https://redhat.atlassian.net/browse/RHAIENG-7846), advancing the official scaling guidelines effort toward published guidance for 3.6 GA.

### ASSOCIATES

- Vedant Deshpande published a [blog post on job scheduling with Spark Operator and Kueue on OpenShift AI](https://redhat.atlassian.net/browse/RHAIENG-7425), contributing community-facing content that documents a key 3.6 feature for practitioners.

---

## Source Data Summary

- Jira: 10 completed by team, 17 in progress
  (1 additional completed on the Data Processing component but assigned outside the team roster, excluded from this report)
- GitHub: 6 PRs merged, 4 by team
- Sections: DATA_PROCESSING, ASSOCIATES
