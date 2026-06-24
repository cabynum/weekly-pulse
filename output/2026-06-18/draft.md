# Data Processing - Weekly Highlights Draft

Generated: 2026-06-18 19:53

## Suggested Section for AAET Weekly Pulse Check

**Data Processing** (Chris Bynum) - 24 issues completed

Highlights:

- Synced [upstream Spark Operator v2.5.1](https://github.com/opendatahub-io/spark-operator/pull/115) into the ODH midstream fork, picking up TLS configuration flags and a Kubernetes dependency bump.
- Completed [3.5 EA1 RC2 test execution, documentation sign-off, and product sign-off](https://redhat.atlassian.net/browse/RHOAIENG-61873), closing out the team's EA1 release gate requirements.
- Added [E2E test coverage for Kueue integration with SparkApplication](https://redhat.atlassian.net/browse/RHAIENG-5289), validating admission, quota enforcement, and resource reclamation. Fair sharing, priority scheduling, and preemption scenarios are in active review.
- Delivered both [docling container images for EA2](https://redhat.atlassian.net/browse/RHAISTRAT-1409): the batch processing image with updated packages and models, and a new CUDA/UBI9 serve image for the REST API.
- Landed the [File Processors API in the downstream OGX Operator](https://redhat.atlassian.net/browse/RHAISTRAT-1410), completing air-gapped support, FIPS validation, beta API labeling, and CRD extensions across five linked tickets.
- Resolved [upstream webhook subPath parity and expanded drift test coverage](https://redhat.atlassian.net/browse/RHAIENG-5563) in the Kubeflow Spark Operator, and [increased E2E test timeouts](https://redhat.atlassian.net/browse/RHAIENG-5561) to reduce CI flakiness.
- Upgraded KFP to [2.16.1 and increased pipeline timeout](https://github.com/opendatahub-io/data-processing/pull/127) to reduce intermittent test failures in the data-processing integration suite.

---

## Raw Bullets (for editing)

### DATA_PROCESSING

- Synced [upstream Spark Operator v2.5.1](https://github.com/opendatahub-io/spark-operator/pull/115) into the ODH midstream fork, picking up TLS configuration flags and a Kubernetes dependency bump.
- Completed [3.5 EA1 RC2 test execution, documentation sign-off, and product sign-off](https://redhat.atlassian.net/browse/RHOAIENG-61873), closing out the team's EA1 release gate requirements.
- Added [E2E test coverage for Kueue integration with SparkApplication](https://redhat.atlassian.net/browse/RHAIENG-5289), validating admission, quota enforcement, and resource reclamation. Fair sharing, priority scheduling, and preemption scenarios are in active review.
- Delivered both [docling container images for EA2](https://redhat.atlassian.net/browse/RHAISTRAT-1409): the batch processing image with updated packages and models, and a new CUDA/UBI9 serve image for the REST API.
- Landed the [File Processors API in the downstream OGX Operator](https://redhat.atlassian.net/browse/RHAISTRAT-1410), completing air-gapped support, FIPS validation, beta API labeling, and CRD extensions across five linked tickets.
- Resolved [upstream webhook subPath parity and expanded drift test coverage](https://redhat.atlassian.net/browse/RHAIENG-5563) in the Kubeflow Spark Operator, and [increased E2E test timeouts](https://redhat.atlassian.net/browse/RHAIENG-5561) to reduce CI flakiness.
- Upgraded KFP to [2.16.1 and increased pipeline timeout](https://github.com/opendatahub-io/data-processing/pull/127) to reduce intermittent test failures in the data-processing integration suite.

### ASSOCIATES

- Rishabh Singh drove delivery of both docling container images and the [RHAISTRAT-1409](https://redhat.atlassian.net/browse/RHAISTRAT-1409) registry publication pipeline, a blocker-priority item, while simultaneously landing upstream webhook and drift test improvements.

---

## Source Data Summary

- Jira: 24 completed, 89 in progress
- GitHub: 9 PRs merged, 3 by team
- Sections: DATA_PROCESSING, ASSOCIATES
