# Data Processing - Weekly Highlights Draft
Generated: 2026-07-23 17:01
Enriched: 2026-07-23 17:10 (Slack)

## Suggested Section for AAET Weekly Pulse Check

**Data Processing** (Chris Bynum) - 18 issues completed

Highlights:

- Completed the team's [3.5 EA2 release gate requirements](https://redhat.atlassian.net/browse/RHOAIENG-75005), executing RC1 and RC2 test matrices plus an OCP 4.21 disconnected install validation. Also cleared [Week 2 of the 3.5 GA test matrix](https://redhat.atlassian.net/browse/RHOAIENG-74360), keeping the GA timeline on track.
- Following last week's upstream sync strategy work, [executed Phase 1 of the upstream sync](https://redhat.atlassian.net/browse/RHOAIENG-74889), merging the latest kubeflow/spark-operator changes into the ODH midstream repo.
- Shipped the [Kueue and Spark Operator integration guide](https://github.com/opendatahub-io/spark-operator/pull/125) to the midstream docs site, covering both admin setup and user workflows. This closes out the [validation and documentation work](https://redhat.atlassian.net/browse/RHAIENG-5288) for the Kueue integration feature. After RHBoK 1.4 landed, E2E was re-validated on a RHOAI cluster and a [release scope exception](https://redhat.atlassian.net/browse/RHAISTRAT-1477) was secured so the feature stays on the 3.5 GA train (docs and tests only, no bundle impact).
- Added [Spark Connect documentation for RHOAI workbenches](https://github.com/opendatahub-io/spark-operator/pull/149) and [comprehensive Spark observability guidance](https://github.com/opendatahub-io/spark-operator/pull/133) to the midstream docs site, covering interactive job management and the Spark UI with history server.
- Landed [SparkApplication in the Kueue frameworkMapping](https://redhat.atlassian.net/browse/RHOAIENG-63982) for the opendatahub-operator, enabling Kueue to natively recognize and schedule Spark jobs without manual configuration.
- Advanced Spark Operator modularization: module controller and Konflux Tekton pipeline for the module image are merged, and the [platform operator handler PR](https://github.com/opendatahub-io/opendatahub-operator/pull/3836) is open to move Spark from in-tree to the out-of-tree module model.
- Resolved four [critical CVEs in the odh-spark-operator-rhel9 image](https://redhat.atlassian.net/browse/RHOAIENG-77030) for 3.4, covering Eclipse Vert.x information disclosure, Apache Commons Configuration denial of service, and two containerd security bypass vulnerabilities.

## Suggested Addition to Associates Section

- Vedant Deshpande delivered the [admin and user guide for the Kueue and Spark Operator integration](https://github.com/opendatahub-io/spark-operator/pull/125), completed RHBoK 1.4 E2E validation on RHOAI, and drove the [3.5 GA release scope exception](https://redhat.atlassian.net/browse/RHAISTRAT-1477) after the Kueue dependency unblocked. *(already published to Week of Jul 23)*
- Rishabh Singh co-authored [5 Anti-Patterns That Cause Kubernetes Operator Vulnerabilities](https://developers.redhat.com/articles/2026/07/06/5-anti-patterns-cause-kubernetes-operator-vulnerabilities) on the Red Hat Developer Blog. He then applied that guidance against Spark Operator and landed the upstream [controller-runtime cache hardening](https://github.com/kubeflow/spark-operator/pull/3032) against OOMKill. *(published to Week of Jul 23)*

---

## Raw Bullets (for editing)

### DATA_PROCESSING

- Completed the team's [3.5 EA2 release gate requirements](https://redhat.atlassian.net/browse/RHOAIENG-75005), executing RC1 and RC2 test matrices plus an OCP 4.21 disconnected install validation. Also cleared [Week 2 of the 3.5 GA test matrix](https://redhat.atlassian.net/browse/RHOAIENG-74360), keeping the GA timeline on track.
- Following last week's upstream sync strategy work, [executed Phase 1 of the upstream sync](https://redhat.atlassian.net/browse/RHOAIENG-74889), merging the latest kubeflow/spark-operator changes into the ODH midstream repo.
- Shipped the [Kueue and Spark Operator integration guide](https://github.com/opendatahub-io/spark-operator/pull/125) to the midstream docs site, covering both admin setup and user workflows. This closes out the [validation and documentation work](https://redhat.atlassian.net/browse/RHAIENG-5288) for the Kueue integration feature. After RHBoK 1.4 landed, E2E was re-validated on a RHOAI cluster and a [release scope exception](https://redhat.atlassian.net/browse/RHAISTRAT-1477) was secured so the feature stays on the 3.5 GA train (docs and tests only, no bundle impact).
- Added [Spark Connect documentation for RHOAI workbenches](https://github.com/opendatahub-io/spark-operator/pull/149) and [comprehensive Spark observability guidance](https://github.com/opendatahub-io/spark-operator/pull/133) to the midstream docs site, covering interactive job management and the Spark UI with history server.
- Landed [SparkApplication in the Kueue frameworkMapping](https://redhat.atlassian.net/browse/RHOAIENG-63982) for the opendatahub-operator, enabling Kueue to natively recognize and schedule Spark jobs without manual configuration.
- Advanced Spark Operator modularization: module controller and Konflux Tekton pipeline for the module image are merged, and the [platform operator handler PR](https://github.com/opendatahub-io/opendatahub-operator/pull/3836) is open to move Spark from in-tree to the out-of-tree module model.
- Resolved four [critical CVEs in the odh-spark-operator-rhel9 image](https://redhat.atlassian.net/browse/RHOAIENG-77030) for 3.4, covering Eclipse Vert.x information disclosure, Apache Commons Configuration denial of service, and two containerd security bypass vulnerabilities.

### ASSOCIATES

- Vedant Deshpande delivered the [admin and user guide for the Kueue and Spark Operator integration](https://github.com/opendatahub-io/spark-operator/pull/125), completed RHBoK 1.4 E2E validation on RHOAI, and drove the [3.5 GA release scope exception](https://redhat.atlassian.net/browse/RHAISTRAT-1477) after the Kueue dependency unblocked. *(already published)*
- Rishabh Singh co-authored [5 Anti-Patterns That Cause Kubernetes Operator Vulnerabilities](https://developers.redhat.com/articles/2026/07/06/5-anti-patterns-cause-kubernetes-operator-vulnerabilities) on the Red Hat Developer Blog. He then applied that guidance against Spark Operator and landed the upstream [controller-runtime cache hardening](https://github.com/kubeflow/spark-operator/pull/3032) against OOMKill. *(published)*

---

## Source Data Summary

- Jira: 18 completed, 100 in progress
- GitHub: 9 PRs merged, 3 by team
- Slack: 131 messages across 5 team members
- Sections: DATA_PROCESSING, ASSOCIATES
- Enrichment: RHBoK 1.4 / RHAISTRAT-1477 exception context; Spark modularization progress (Risks omitted by request)
- Correction: removed RHAIRFE-2736/2737 (Closed/Obsolete, no PR; not shipped)
- Published Associates append: Rishabh blog + OOMKill follow-through (Vedant left untouched)
