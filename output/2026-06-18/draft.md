# Data Processing - Weekly Highlights Draft
Generated: 2026-06-18 19:18

## Suggested Section for AAET Weekly Pulse Check

**Data Processing** (Chris Bynum) - 21 issues completed

Highlights:

- Completed [3.5 EA1 RC2 test execution, documentation sign-off, and product sign-off](https://redhat.atlassian.net/browse/RHOAIENG-61873), closing out all EA1 release gate requirements for the team.
- Shipped both [docling container images for EA2](https://redhat.atlassian.net/browse/RHAISTRAT-1409): updated the existing batch processing image and created a new CUDA-enabled serve image, with both queued for push to the Red Hat registry on EA2 release.
- Validated FIPS compliance and [air-gapped environment support](https://redhat.atlassian.net/browse/RHAIENG-5123) for the File Processors API, and [integrated the API and Docling provider into the downstream llama-stack-distribution](https://redhat.atlassian.net/browse/RHAIENG-5119), with scheduler support for the Docling serve execution model also closed out.
- Added [E2E tests covering Kueue admission, quota enforcement, and reclamation](https://github.com/opendatahub-io/spark-operator/pull/109) for SparkApplications, with fair-sharing, priority scheduling, and preemption scenarios currently in review.
- Fixed Spark UI accessibility by [documenting the port-forwarding workflow](https://github.com/opendatahub-io/spark-operator/pull/107) as an interim measure while the driverIngressOptions TLS solution progresses toward release.
- Replaced the tini init system with catatonit across Spark operator containers, resolving [licensing and supportability concerns for productization](https://redhat.atlassian.net/browse/RHAIENG-5328).
- Upgraded KFP to 2.16.1 and [increased pipeline timeouts](https://github.com/opendatahub-io/data-processing/pull/127) to reduce intermittent test failures in the data-processing pipeline.

## Suggested Addition to Customers Section

- Resolved a [merge conflict in the python package index](https://redhat.atlassian.net/browse/RHAIENG-5035) introduced during the main-to-rhoai-3.5 branch sync, preventing a build break that would have affected downstream consumers of the Spark operator.

## Suggested Addition to Associates Section

- Rishabh Singh expanded upstream Kubeflow Spark Operator test coverage by landing [webhook subPath parity and drift test additions](https://redhat.atlassian.net/browse/RHAIENG-5563), and reduced CI flakiness by [increasing E2E test timeouts](https://redhat.atlassian.net/browse/RHAIENG-5561) in the upstream repo.

---

## Raw Bullets (for editing)

### DATA_PROCESSING

- Completed [3.5 EA1 RC2 test execution, documentation sign-off, and product sign-off](https://redhat.atlassian.net/browse/RHOAIENG-61873), closing out all EA1 release gate requirements for the team.
- Shipped both [docling container images for EA2](https://redhat.atlassian.net/browse/RHAISTRAT-1409): updated the existing batch processing image and created a new CUDA-enabled serve image, with both queued for push to the Red Hat registry on EA2 release.
- Validated FIPS compliance and [air-gapped environment support](https://redhat.atlassian.net/browse/RHAIENG-5123) for the File Processors API, and [integrated the API and Docling provider into the downstream llama-stack-distribution](https://redhat.atlassian.net/browse/RHAIENG-5119), with scheduler support for the Docling serve execution model also closed out.
- Added [E2E tests covering Kueue admission, quota enforcement, and reclamation](https://github.com/opendatahub-io/spark-operator/pull/109) for SparkApplications, with fair-sharing, priority scheduling, and preemption scenarios currently in review.
- Fixed Spark UI accessibility by [documenting the port-forwarding workflow](https://github.com/opendatahub-io/spark-operator/pull/107) as an interim measure while the driverIngressOptions TLS solution progresses toward release.
- Replaced the tini init system with catatonit across Spark operator containers, resolving [licensing and supportability concerns for productization](https://redhat.atlassian.net/browse/RHAIENG-5328).
- Upgraded KFP to 2.16.1 and [increased pipeline timeouts](https://github.com/opendatahub-io/data-processing/pull/127) to reduce intermittent test failures in the data-processing pipeline.

### CUSTOMERS

- Resolved a [merge conflict in the python package index](https://redhat.atlassian.net/browse/RHAIENG-5035) introduced during the main-to-rhoai-3.5 branch sync, preventing a build break that would have affected downstream consumers of the Spark operator.

### ASSOCIATES

- Rishabh Singh expanded upstream Kubeflow Spark Operator test coverage by landing [webhook subPath parity and drift test additions](https://redhat.atlassian.net/browse/RHAIENG-5563), and reduced CI flakiness by [increasing E2E test timeouts](https://redhat.atlassian.net/browse/RHAIENG-5561) in the upstream repo.

---

## Source Data Summary

- Jira: 21 completed, 89 in progress
- GitHub: 9 PRs merged, 3 by team
- Sections: DATA_PROCESSING, CUSTOMERS, ASSOCIATES
