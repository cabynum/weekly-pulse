# Data Processing - Weekly Highlights Draft
Generated: 2026-06-14 18:06

## Suggested Section for AAET Weekly Pulse Check

**Data Processing** (Chris Bynum) - 12 issues completed

Highlights:

- Completed 3.5 EA1 [test plan sign-off and RC1 test execution](https://redhat.atlassian.net/browse/RHOAIENG-61812), clearing the release gate for the Data Processing team.
- Fixed Spark UI accessibility by eliminating the need for manual port-forwarding to view running jobs. Enabled secure browser access by [implementing driverIngressOptions with TLS](https://redhat.atlassian.net/browse/RHOAIENG-64770) in the upstream Kubeflow Spark Operator.
- Replaced the tini init system with catatonit across Spark operator containers, resolving [licensing and supportability concerns for productization](https://redhat.atlassian.net/browse/RHAIENG-5328). Change landed in both the upstream and downstream Dockerfiles.
- Resolved a Dockerfile build compatibility issue by [replacing BuildKit bind mounts with standard COPY instructions](https://github.com/opendatahub-io/spark-operator/pull/112), improving portability across build environments.
- Shipped [unified deployment documentation](https://redhat.atlassian.net/browse/RHAIENG-3740) and [kustomize-based installation instructions](https://github.com/kubeflow/spark-operator/pull/2951) to the upstream readme, reducing setup friction for new users.
- Wrapped up an [evaluation of Unstructured.io as a file processor provider](https://redhat.atlassian.net/browse/RHAIENG-2473), informing the upcoming Docling integration work for the File Processor API.
- Expanded upstream webhook subPath parity coverage and [broadened drift detection tests](https://redhat.atlassian.net/browse/RHAIENG-5563) to catch configuration regressions earlier in CI.
- Increased e2e test timeouts in the upstream Kubeflow Spark Operator to [reduce intermittent CI failures](https://redhat.atlassian.net/browse/RHAIENG-5561) that were obscuring real test signal.

## Suggested Addition to Risks/Issues Section

- Old Tekton pipeline files in the repo were [conflicting with Konflux CI](https://redhat.atlassian.net/browse/RHOAIENG-67538) and have been removed. Teams relying on those pipelines should confirm they have migrated to Konflux.
- Docling container image updates targeting 3.5 EA2 are [marked Blocker priority](https://redhat.atlassian.net/browse/RHAISTRAT-1409) and actively in progress. Any delays in registry access or build system onboarding could slip EA2 readiness.

## Suggested Addition to Associates Section

- Sahana Sreeram submitted her [first open-source contribution](https://redhat.atlassian.net/browse/RHAIENG-5273) to the upstream project as part of the OGX onboarding program, completing her weeks 4-5 milestone ahead of schedule.

---

## Raw Bullets (for editing)

### DATA_PROCESSING

- Completed 3.5 EA1 [test plan sign-off and RC1 test execution](https://redhat.atlassian.net/browse/RHOAIENG-61812), clearing the release gate for the Data Processing team.
- Fixed Spark UI accessibility by eliminating the need for manual port-forwarding to view running jobs. Enabled secure browser access by [implementing driverIngressOptions with TLS](https://redhat.atlassian.net/browse/RHOAIENG-64770) in the upstream Kubeflow Spark Operator.
- Replaced the tini init system with catatonit across Spark operator containers, resolving [licensing and supportability concerns for productization](https://redhat.atlassian.net/browse/RHAIENG-5328). Change landed in both the upstream and downstream Dockerfiles.
- Resolved a Dockerfile build compatibility issue by [replacing BuildKit bind mounts with standard COPY instructions](https://github.com/opendatahub-io/spark-operator/pull/112), improving portability across build environments.
- Shipped [unified deployment documentation](https://redhat.atlassian.net/browse/RHAIENG-3740) and [kustomize-based installation instructions](https://github.com/kubeflow/spark-operator/pull/2951) to the upstream readme, reducing setup friction for new users.
- Wrapped up an [evaluation of Unstructured.io as a file processor provider](https://redhat.atlassian.net/browse/RHAIENG-2473), informing the upcoming Docling integration work for the File Processor API.
- Expanded upstream webhook subPath parity coverage and [broadened drift detection tests](https://redhat.atlassian.net/browse/RHAIENG-5563) to catch configuration regressions earlier in CI.
- Increased e2e test timeouts in the upstream Kubeflow Spark Operator to [reduce intermittent CI failures](https://redhat.atlassian.net/browse/RHAIENG-5561) that were obscuring real test signal.

### RISKS

- Old Tekton pipeline files in the repo were [conflicting with Konflux CI](https://redhat.atlassian.net/browse/RHOAIENG-67538) and have been removed. Teams relying on those pipelines should confirm they have migrated to Konflux.
- Docling container image updates targeting 3.5 EA2 are [marked Blocker priority](https://redhat.atlassian.net/browse/RHAISTRAT-1409) and actively in progress. Any delays in registry access or build system onboarding could slip EA2 readiness.

### ASSOCIATES

- Sahana Sreeram submitted her [first open-source contribution](https://redhat.atlassian.net/browse/RHAIENG-5273) to the upstream project as part of the OGX onboarding program, completing her weeks 4-5 milestone ahead of schedule.

---

## Source Data Summary

- Jira: 12 completed, 41 in progress
- GitHub: 10 PRs merged, 6 by team
- Sections: DATA_PROCESSING, RISKS, ASSOCIATES
