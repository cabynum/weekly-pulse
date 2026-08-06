# Data Processing - Weekly Highlights (Enriched)
Generated: 2026-07-09 17:00 | Enriched: 2026-07-10

## Suggested Section for AAET Weekly Pulse Check

**Data Processing** (Chris Bynum) - 11 issues completed

Highlights:

- Completed the 3.5 EA2 [product and documentation sign-offs](https://redhat.atlassian.net/browse/RHOAIENG-68840), clearing 3.5 EA2 release gate requirements.
- Building on last week's module foundation, completed the [Module Operator Controller with tests and finalizer](https://redhat.atlassian.net/browse/RHOAIENG-69116), making the standalone ODH spark-operator module fully operational and verifiable.
- Wired [docling and unstructured into the auto file processor](https://redhat.atlassian.net/browse/RHAIENG-5863), enabling automatic backend selection for document ingestion without requiring manual configuration.
- Added [SparkApplication to Kueue's frameworkMapping in odh-operator](https://redhat.atlassian.net/browse/RHOAIENG-63983), enabling Kueue to manage Spark job scheduling natively within the ODH midstream operator.
- Triaged [15 incoming CVEs](https://redhat.atlassian.net/browse/RHOAIENG-74206) against the spark-operator, closing 10 as non-exploitable. Identified one real vulnerability in the Go stdlib that requires a dependency bump and is coordinating the backport process.
- Resolved a Konflux build failure caused by [file bind mounts in Dockerfile.konflux](https://redhat.atlassian.net/browse/RHOAIENG-72975), unblocking the downstream container build pipeline.
- Started [Konflux onboarding for the spark-operator-module controller](https://redhat.atlassian.net/browse/RHOAIENG-75720) image, creating the Tekton pipeline and filing DevTestOps requests to bring the module to a shippable state for 3.6 EA1.

## Suggested Addition to Risks/Issues Section

- RHBoK 1.4 release delayed from July 8 to July 15 due to an external dependency on rebase 1.36 landing. Team's Kueue testing work is complete, waiting on the upstream team.

