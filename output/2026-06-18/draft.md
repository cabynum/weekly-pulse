# Data Processing - Weekly Highlights Draft
Generated: 2026-06-18 19:53

## Suggested Section for AAET Weekly Pulse Check

**Data Processing** (Chris Bynum) - 24 issues completed

Highlights:

- Shipped [Spark Operator v2.5.1](https://github.com/opendatahub-io/spark-operator/pull/115), including TLS version and cipher suite configuration flags and a Kubernetes dependency bump to v1.35.4 with controller-runtime v0.23.3, keeping the operator current with upstream and hardening cluster security posture.
- Released odh-3.5.0-ea.2, completing the [3.5 EA1 RC2 test execution matrix, documentation sign-off, and product sign-off](https://redhat.atlassian.net/browse/RHOAIENG-61873) ahead of the milestone.
- Added [E2E test coverage for Kueue integration with SparkApplication](https://redhat.atlassian.net/browse/RHAIENG-5289), validating basic admission, quota enforcement, and resource reclamation. Active review underway on additional scenarios covering fair sharing, priority scheduling, and preemption.
- Delivered both [docling container images for EA2](https://redhat.atlassian.net/browse/RHAISTRAT-1409): the SDK image (batch document processing) updated with new package versions and models, and a new CUDA/UBI9 serve image for the REST API, with both pushed to the Red Hat registry on the EA2 cadence.
- Landed the [File Processors API into the downstream OGX Operator](https://redhat.atlassian.net/browse/RHAISTRAT-1410), completing air-gapped environment support, FIPS and license validation, beta API labeling, CRD extension, and provider integration across five linked tickets.
- Resolved [upstream webhook subPath parity and expanded drift test coverage](https://redhat.atlassian.net/browse/RHAIENG-5563) in the Kubeflow Spark Operator, and increased E2E test timeouts to [reduce CI flakiness](https://redhat.atlassian.net/browse/RHAIENG-5561) blocking upstream contributors.
- Documented the [Spark UI port-forwarding workflow](https://github.com/opendatahub-io/spark-operator/pull/107) to support users until the driverIngressOptions TLS-based browser access lands in a future release.
- Upgraded KFP to [2.16.1 and increased pipeline timeout](https://github.com/opendatahub-io/data-processing/pull/127) to reduce intermittent test failures in the data-processing integration suite.

## Suggested Addition to Associates Section

- Rishabh Singh drove delivery of both docling container images and the [RHAISTRAT-1409](https://redhat.atlassian.net/browse/RHAISTRAT-1409) registry publication pipeline, a blocker-priority item, while simultaneously landing upstream webhook and drift test improvements.

---

## Raw Bullets (for editing)

### DATA_PROCESSING

- Shipped [Spark Operator v2.5.1](https://github.com/opendatahub-io/spark-operator/pull/115), including TLS version and cipher suite configuration flags and a Kubernetes dependency bump to v1.35.4 with controller-runtime v0.23.3, keeping the operator current with upstream and hardening cluster security posture.
- Released odh-3.5.0-ea.2, completing the [3.5 EA1 RC2 test execution matrix, documentation sign-off, and product sign-off](https://redhat.atlassian.net/browse/RHOAIENG-61873) ahead of the milestone.
- Added [E2E test coverage for Kueue integration with SparkApplication](https://redhat.atlassian.net/browse/RHAIENG-5289), validating basic admission, quota enforcement, and resource reclamation. Active review underway on additional scenarios covering fair sharing, priority scheduling, and preemption.
- Delivered both [docling container images for EA2](https://redhat.atlassian.net/browse/RHAISTRAT-1409): the SDK image (batch document processing) updated with new package versions and models, and a new CUDA/UBI9 serve image for the REST API, with both pushed to the Red Hat registry on the EA2 cadence.
- Landed the [File Processors API into the downstream OGX Operator](https://redhat.atlassian.net/browse/RHAISTRAT-1410), completing air-gapped environment support, FIPS and license validation, beta API labeling, CRD extension, and provider integration across five linked tickets.
- Resolved [upstream webhook subPath parity and expanded drift test coverage](https://redhat.atlassian.net/browse/RHAIENG-5563) in the Kubeflow Spark Operator, and increased E2E test timeouts to [reduce CI flakiness](https://redhat.atlassian.net/browse/RHAIENG-5561) blocking upstream contributors.
- Documented the [Spark UI port-forwarding workflow](https://github.com/opendatahub-io/spark-operator/pull/107) to support users until the driverIngressOptions TLS-based browser access lands in a future release.
- Upgraded KFP to [2.16.1 and increased pipeline timeout](https://github.com/opendatahub-io/data-processing/pull/127) to reduce intermittent test failures in the data-processing integration suite.

### ASSOCIATES

- Rishabh Singh drove delivery of both docling container images and the [RHAISTRAT-1409](https://redhat.atlassian.net/browse/RHAISTRAT-1409) registry publication pipeline, a blocker-priority item, while simultaneously landing upstream webhook and drift test improvements.

---

## Source Data Summary

- Jira: 24 completed, 89 in progress
- GitHub: 9 PRs merged, 3 by team
- Sections: DATA_PROCESSING, ASSOCIATES
