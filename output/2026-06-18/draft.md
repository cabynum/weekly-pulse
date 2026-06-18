# Data Processing - Weekly Highlights Draft
Generated: 2026-06-18 19:50

## Suggested Section for AAET Weekly Pulse Check

**Data Processing** (Chris Bynum) - 24 issues completed

Highlights:

- Shipped [3.5 EA1 product and documentation sign-off](https://redhat.atlassian.net/browse/RHOAIENG-61873), completing RC2 test execution and closing out the EA1 release cycle for the team.
- Fixed Spark UI accessibility by eliminating the need for manual port-forwarding to view running jobs. Enabled secure browser access by [implementing driverIngressOptions with TLS](https://redhat.atlassian.net/browse/RHOAIENG-64770) and published [documentation for the port-forwarding workflow](https://redhat.atlassian.net/browse/RHOAIENG-60634) in the interim.
- Replaced the tini init system with catatonit across Spark operator containers, resolving [licensing and supportability concerns for productization](https://redhat.atlassian.net/browse/RHAIENG-5328).
- Landed [E2E tests covering Kueue admission, quota enforcement, and reclamation](https://redhat.atlassian.net/browse/RHAIENG-5289) for SparkApplications, with active review underway on fair-sharing, priority scheduling, preemption, multi-tenancy, and gang-scheduling scenarios.
- Delivered the [File Processors API into the downstream OGX operator](https://redhat.atlassian.net/browse/RHAISTRAT-1410), including beta-status markers, disconnected/air-gapped support, FIPS and license validation, and CRD extensions for file processor configuration.
- Shipped updated [docling container images for EA2](https://redhat.atlassian.net/browse/RHAISTRAT-1409): refreshed the SDK image with new package versions and models, and built the new GPU-accelerated serve image, with both pending registry push.
- Upgraded KFP to 2.16.1 and [increased pipeline timeout](https://github.com/opendatahub-io/data-processing/pull/127) to reduce flaky test failures in CI.
- Expanded upstream Spark operator test coverage with [webhook subPath parity and drift tests](https://redhat.atlassian.net/browse/RHAIENG-5563), and increased E2E timeouts to [reduce CI flakiness](https://redhat.atlassian.net/browse/RHAIENG-5561).

## Suggested Addition to Associates Section

- Rishabh Singh drove both docling container image deliverables for EA2 and led the upstream webhook drift test expansion, spanning productization, image pipeline work, and upstream community contribution in a single sprint.

---

## Raw Bullets (for editing)

### DATA_PROCESSING

- Shipped [3.5 EA1 product and documentation sign-off](https://redhat.atlassian.net/browse/RHOAIENG-61873), completing RC2 test execution and closing out the EA1 release cycle for the team.
- Fixed Spark UI accessibility by eliminating the need for manual port-forwarding to view running jobs. Enabled secure browser access by [implementing driverIngressOptions with TLS](https://redhat.atlassian.net/browse/RHOAIENG-64770) and published [documentation for the port-forwarding workflow](https://redhat.atlassian.net/browse/RHOAIENG-60634) in the interim.
- Replaced the tini init system with catatonit across Spark operator containers, resolving [licensing and supportability concerns for productization](https://redhat.atlassian.net/browse/RHAIENG-5328).
- Landed [E2E tests covering Kueue admission, quota enforcement, and reclamation](https://redhat.atlassian.net/browse/RHAIENG-5289) for SparkApplications, with active review underway on fair-sharing, priority scheduling, preemption, multi-tenancy, and gang-scheduling scenarios.
- Delivered the [File Processors API into the downstream OGX operator](https://redhat.atlassian.net/browse/RHAISTRAT-1410), including beta-status markers, disconnected/air-gapped support, FIPS and license validation, and CRD extensions for file processor configuration.
- Shipped updated [docling container images for EA2](https://redhat.atlassian.net/browse/RHAISTRAT-1409): refreshed the SDK image with new package versions and models, and built the new GPU-accelerated serve image, with both pending registry push.
- Upgraded KFP to 2.16.1 and [increased pipeline timeout](https://github.com/opendatahub-io/data-processing/pull/127) to reduce flaky test failures in CI.
- Expanded upstream Spark operator test coverage with [webhook subPath parity and drift tests](https://redhat.atlassian.net/browse/RHAIENG-5563), and increased E2E timeouts to [reduce CI flakiness](https://redhat.atlassian.net/browse/RHAIENG-5561).

### ASSOCIATES

- Rishabh Singh drove both docling container image deliverables for EA2 and led the upstream webhook drift test expansion, spanning productization, image pipeline work, and upstream community contribution in a single sprint.

---

## Source Data Summary

- Jira: 24 completed, 89 in progress
- GitHub: 9 PRs merged, 3 by team
- Sections: DATA_PROCESSING, ASSOCIATES
