# Data Processing - Weekly Highlights Draft
Generated: 2026-06-14 17:58

## Suggested Section for AAET Weekly Pulse Check

**Data Processing** (Chris Bynum) - 12 issues completed

Highlights:

- Completed 3.5 EA1 [test plan sign-off and RC1 test execution](https://redhat.atlassian.net/browse/RHOAIENG-61812), clearing the release gate for the Data Processing team.
- Fixed Spark UI accessibility by eliminating the need for manual port-forwarding to view running jobs. Enabled secure browser access by [implementing driverIngressOptions with TLS](https://redhat.atlassian.net/browse/RHOAIENG-64770), superseding the previous sparkUIOptions approach.
- Replaced the tini init system with catatonit across Spark operator containers, resolving [licensing and supportability concerns](https://redhat.atlassian.net/browse/RHAIENG-5328) for productization. Also replaced BuildKit bind mounts with standard COPY instructions to improve Dockerfile portability.
- Shipped [unified deployment documentation](https://redhat.atlassian.net/browse/RHAIENG-3740) and kustomize-based installation instructions for the Spark operator, reducing onboarding friction for new users.
- Removed stale Tekton CI pipeline files to [resolve Konflux configuration conflicts](https://redhat.atlassian.net/browse/RHOAIENG-67538) that were blocking the build pipeline.
- Expanded upstream Kubeflow Spark Operator test coverage: [increased e2e timeouts to reduce CI flakiness](https://redhat.atlassian.net/browse/RHAIENG-5561) and added [webhook subPath parity checks with drift detection](https://redhat.atlassian.net/browse/RHAIENG-5563).
- Wrapped up [evaluation of Unstructured.io as a File Processor backend](https://redhat.atlassian.net/browse/RHAIENG-2473), informing the upcoming Docling integration work for the OGX operator.

In progress: 41 active issues.

Feature watch: [RHAISTRAT-1477](https://redhat.atlassian.net/browse/RHAISTRAT-1477) Kueue support for Kubeflow Spark Operator (KSO) - testing and docs  (Green) TV:rhoai-3.5; [RHAISTRAT-1410](https://redhat.atlassian.net/browse/RHAISTRAT-1410) Include File Processors API in OGX (previously Llama Stack) Operator downstream (Green) TV:rhoai-3.5; [RHAISTRAT-1409](https://redhat.atlassian.net/browse/RHAISTRAT-1409) Docling container image updates (new package versions, models) and push to registry.redhat every EA2 release (Green) TV:rhoai-3.5; [RHAISTRAT-1408](https://redhat.atlassian.net/browse/RHAISTRAT-1408) Test & document using the Spark Application UI and spark-history mcp server for logs (Green) TV:rhoai-3.5

## Suggested Addition to Associates Section

- Sahana Sreeram submitted her [first open-source contribution](https://redhat.atlassian.net/browse/RHAIENG-5273) to the upstream OGX project as part of her internship, completing her first mentor-picked issue in weeks 4-5.

---

## Raw Bullets (for editing)

### DATA_PROCESSING

- Completed 3.5 EA1 [test plan sign-off and RC1 test execution](https://redhat.atlassian.net/browse/RHOAIENG-61812), clearing the release gate for the Data Processing team.
- Fixed Spark UI accessibility by eliminating the need for manual port-forwarding to view running jobs. Enabled secure browser access by [implementing driverIngressOptions with TLS](https://redhat.atlassian.net/browse/RHOAIENG-64770), superseding the previous sparkUIOptions approach.
- Replaced the tini init system with catatonit across Spark operator containers, resolving [licensing and supportability concerns](https://redhat.atlassian.net/browse/RHAIENG-5328) for productization. Also replaced BuildKit bind mounts with standard COPY instructions to improve Dockerfile portability.
- Shipped [unified deployment documentation](https://redhat.atlassian.net/browse/RHAIENG-3740) and kustomize-based installation instructions for the Spark operator, reducing onboarding friction for new users.
- Removed stale Tekton CI pipeline files to [resolve Konflux configuration conflicts](https://redhat.atlassian.net/browse/RHOAIENG-67538) that were blocking the build pipeline.
- Expanded upstream Kubeflow Spark Operator test coverage: [increased e2e timeouts to reduce CI flakiness](https://redhat.atlassian.net/browse/RHAIENG-5561) and added [webhook subPath parity checks with drift detection](https://redhat.atlassian.net/browse/RHAIENG-5563).
- Wrapped up [evaluation of Unstructured.io as a File Processor backend](https://redhat.atlassian.net/browse/RHAIENG-2473), informing the upcoming Docling integration work for the OGX operator.

### ASSOCIATES

- Sahana Sreeram submitted her [first open-source contribution](https://redhat.atlassian.net/browse/RHAIENG-5273) to the upstream OGX project as part of her internship, completing her first mentor-picked issue in weeks 4-5.

---

## Source Data Summary

- Jira: 12 completed, 41 in progress
- GitHub: 10 PRs merged, 6 by team
- Sections: DATA_PROCESSING, ASSOCIATES
