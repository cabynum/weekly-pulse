# Data Processing - Weekly Highlights Draft

Generated: 2026-06-12 (v3 - final review)

## Suggested Section for AAET Weekly Pulse Check

**Data Processing** (Chris Bynum) - 8 issues completed

Highlights:

- Completed 3.5 EA1 [test plan sign-off and RC1 test execution](https://redhat.atlassian.net/browse/RHOAIENG-61812)
- Fixed Spark UI accessibility by eliminating the need for manual port-forwarding to view running jobs. Enabled secure browser access by [implementing driverIngressOptions with TLS](https://redhat.atlassian.net/browse/RHOAIENG-64770).
- Replaced tini init system with catatonit across Spark operator containers, resolving [licensing and supportability concerns for RHOAI productization](https://redhat.atlassian.net/browse/RHAIENG-5328).
- Added [Kustomize deployment documentation](https://redhat.atlassian.net/browse/RHAIENG-3740) to upstream Spark Operator, which previously only had Helm instructions. Gives GitOps users a supported installation path without relying on downstream docs.
- Completed E2E testing of [Kueue + Spark Operator integration](https://redhat.atlassian.net/browse/RHAISTRAT-1477) covering admission, quota, preemption, and multi-tenancy. PRs in review, documentation to follow.
- Building two [docling container images for 3.5 EA2](https://redhat.atlassian.net/browse/RHAIENG-5259): one for batch document processing, one for the REST API. First image pipeline passing, working through build system access for the second.
- File Processors API [air-gapped environment support](https://redhat.atlassian.net/browse/RHAIENG-5123) and [downstream OGX distribution integration](https://redhat.atlassian.net/browse/RHAIENG-5119) both in review, targeting 3.5 EA2.

## Suggested Addition to Associates Section

- Rishabh Singh was approved as a Maintainer of the Kubeflow Spark Operator, recognizing his upstream contributions in testing, code review, and community engagement.
- Rishabh Singh co-authored [Protect your Kubernetes operator from OOMKill](https://developers.redhat.com/articles/2026/06/01/protect-your-kubernetes-operator-oomkill) on the Red Hat Developer Blog, detailing a systemic vulnerability found across controller-runtime operators.
