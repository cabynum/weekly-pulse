# Data Processing - Weekly Highlights Draft
Generated: 2026-06-18 19:43

## Suggested Section for AAET Weekly Pulse Check

**Data Processing** (Chris Bynum) - 24 issues completed

Highlights:

- Shipped [3.5 EA1 product, documentation, and RC2 sign-offs](https://redhat.atlassian.net/browse/RHOAIENG-61873), closing out the EA1 release milestone for the team.
- Replaced the tini init system with catatonit across Spark operator containers, resolving [licensing and supportability concerns](https://redhat.atlassian.net/browse/RHAIENG-5328) that blocked productization.
- Fixed Spark UI accessibility by eliminating the need for manual port-forwarding to view running jobs. Enabled secure browser access by [implementing driverIngressOptions with TLS](https://redhat.atlassian.net/browse/RHOAIENG-64770), and [documented the port-forwarding workflow](https://redhat.atlassian.net/browse/RHOAIENG-60634) as a fallback reference.
- Landed [E2E tests covering Kueue admission, quota enforcement, and reclamation](https://redhat.atlassian.net/browse/RHAIENG-5289) for the Spark operator. Additional coverage for fair-sharing, priority scheduling, and preemption is in active review.
- Delivered the File Processors API into the downstream LlamaStack operator, including [CRD extension](https://redhat.atlassian.net/browse/RHAIENG-5120), [beta status labeling](https://redhat.atlassian.net/browse/RHAIENG-5121), [air-gapped environment support](https://redhat.atlassian.net/browse/RHAIENG-5123), and [FIPS and license validation](https://redhat.atlassian.net/browse/RHAIENG-5122). Release is pending for EA2.
- Built and published both [docling container images](https://redhat.atlassian.net/browse/RHAISTRAT-1409) for EA2: the batch document processing image (updated packages and models) and the new [CUDA UBI9 serve image](https://redhat.atlassian.net/browse/RHAIENG-5263) for the REST API.
- Upgraded KFP to [2.16.1](https://github.com/opendatahub-io/data-processing/pull/127) and increased pipeline timeout to improve reliability in long-running pipeline scenarios.

## Suggested Addition to Associates Section

- Rishabh Singh expanded upstream Spark operator test coverage by [adding webhook subPath parity tests and drift detection](https://redhat.atlassian.net/browse/RHAIENG-5563), and [increased E2E test timeouts](https://redhat.atlassian.net/browse/RHAIENG-5561) to reduce CI flakiness across the upstream project.

---

## Raw Bullets (for editing)

### DATA_PROCESSING

- Shipped [3.5 EA1 product, documentation, and RC2 sign-offs](https://redhat.atlassian.net/browse/RHOAIENG-61873), closing out the EA1 release milestone for the team.
- Replaced the tini init system with catatonit across Spark operator containers, resolving [licensing and supportability concerns](https://redhat.atlassian.net/browse/RHAIENG-5328) that blocked productization.
- Fixed Spark UI accessibility by eliminating the need for manual port-forwarding to view running jobs. Enabled secure browser access by [implementing driverIngressOptions with TLS](https://redhat.atlassian.net/browse/RHOAIENG-64770), and [documented the port-forwarding workflow](https://redhat.atlassian.net/browse/RHOAIENG-60634) as a fallback reference.
- Landed [E2E tests covering Kueue admission, quota enforcement, and reclamation](https://redhat.atlassian.net/browse/RHAIENG-5289) for the Spark operator. Additional coverage for fair-sharing, priority scheduling, and preemption is in active review.
- Delivered the File Processors API into the downstream LlamaStack operator, including [CRD extension](https://redhat.atlassian.net/browse/RHAIENG-5120), [beta status labeling](https://redhat.atlassian.net/browse/RHAIENG-5121), [air-gapped environment support](https://redhat.atlassian.net/browse/RHAIENG-5123), and [FIPS and license validation](https://redhat.atlassian.net/browse/RHAIENG-5122). Release is pending for EA2.
- Built and published both [docling container images](https://redhat.atlassian.net/browse/RHAISTRAT-1409) for EA2: the batch document processing image (updated packages and models) and the new [CUDA UBI9 serve image](https://redhat.atlassian.net/browse/RHAIENG-5263) for the REST API.
- Upgraded KFP to [2.16.1](https://github.com/opendatahub-io/data-processing/pull/127) and increased pipeline timeout to improve reliability in long-running pipeline scenarios.

### ASSOCIATES

- Rishabh Singh expanded upstream Spark operator test coverage by [adding webhook subPath parity tests and drift detection](https://redhat.atlassian.net/browse/RHAIENG-5563), and [increased E2E test timeouts](https://redhat.atlassian.net/browse/RHAIENG-5561) to reduce CI flakiness across the upstream project.

---

## Source Data Summary

- Jira: 24 completed, 89 in progress
- GitHub: 9 PRs merged, 3 by team
- Sections: DATA_PROCESSING, ASSOCIATES
