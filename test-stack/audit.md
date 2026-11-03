# Learning path audit: what can the seeded test stack alone support?

Scope: every path with `type: path` on `origin/main` at 6a8356f6 (2026-10-21): **75** (65 `-lj`, 10 `-lp`). Standalone guides (94) are out of scope.

- Testable on the seeded stack alone: **33**
- Needs something hosted or supplied externally: **41**
- Unclear, needs a closer look: **1** (`git-sync-use-lp`)

## Confidence
- 64 of the 75 were read in depth by AI agents (`inventory/*.json`); the other 11 (all `-lp`, plus `k6-script-authoring-assistant-lj`) were judged only from their 'Before you begin' text.
- **Nothing here has been verified against the stack or reviewed by a writer.** 'Testable' means the guide's stated needs look satisfiable with Grafana Cloud config and data; it does not mean the test has passed.
- `connect-agent-to-agent-observability-lj` is inventoried but is not on main (it is on branch journey/intro-to-agent-olly) and is excluded.

## Testable on the seeded stack alone (33)

| Path | Why |
|---|---|
| adaptive-logs-lj | in-Cloud only |
| adaptive-metrics-lj | in-Cloud only |
| alerting-first-rule-lj | in-Cloud only |
| alerting-query-language-lj | in-Cloud only |
| billing-usage-lj | in-Cloud only |
| categorize-collector-fleet-lj | needs collectors seeded |
| core-grafana-concepts-lj | in-Cloud only |
| create-availability-slo-lj | in-Cloud only |
| data-transformation-lp | needs a data source and dashboard |
| detect-outages-synthetic-monitoring-lj | in-Cloud only |
| drilldown-logs-lj | in-Cloud only |
| drilldown-metrics-lj | in-Cloud only |
| drilldown-profiles-lj | needs seeded endpoint or guide fix; verify |
| drilldown-traces-lj | in-Cloud only |
| fleet-mgt-monitor-health-lj | needs collectors seeded |
| fleet-mgt-staged-rollout-lj | needs collectors seeded |
| get-started-grafana-assistant-lj | in-Cloud only |
| grafana-cloud-onboarding-lj | in-Cloud only |
| grafana-cloud-tour-lj | in-Cloud only |
| grafana-irm-configuration-lj | in-Cloud only |
| infinity-csv-lj | needs seeded endpoint or guide fix; verify |
| infinity-json-lj | needs seeded endpoint or guide fix; verify |
| infrastructure-alerting-lj | in-Cloud only |
| interactive-dashboards-lj | in-Cloud only |
| intro-to-assistant-watchers-lj | in-Cloud only |
| k6-script-authoring-assistant-lj | Cloud only; local k6 optional |
| loki-data-source-lj | needs seeded endpoint or guide fix; verify |
| rca-workbench-investigation-lj | in-Cloud only |
| read-a-trace-lj | in-Cloud only |
| tempo-data-source-lj | needs seeded endpoint or guide fix; verify |
| visualization-logs-lp | needs Loki logs ingested |
| visualization-metrics-lj | in-Cloud only |
| visualization-traces-lj | in-Cloud only |

## Needs additional setup hosted outside the stack (41)

| Path | Reason |
|---|---|
| automate-k6-cicd-lj | C: terminal, CLI or local code |
| beyla-tempo-lj | A: a system the learner hosts |
| build-dashboard-sdk-lp | C: terminal, CLI or local code (Go/Node SDK) |
| clickhouse-data-source-lj | A: a system the learner hosts |
| cloudwatch-data-source-lj | B: third-party account or secret |
| configure-grafana-terraform-lp | C: Terraform CLI plus identity provider (Okta) |
| deploy-alert-terraform-lj | C: terminal, CLI or local code |
| deploy-dashboard-terraform-lp | C: terminal, CLI or local code (Terraform) |
| elasticsearch-data-source-lj | A: a system the learner hosts |
| elasticsearch-logs-lj | A: a system the learner hosts |
| establish-k6-baseline-lj | C: terminal, CLI or local code |
| find-k6-limits-lj | C: terminal, CLI or local code |
| git-sync-dashboards-lj | B: third-party account or secret |
| github-data-source-lj | B: third-party account or secret |
| github-visualize-lj | B: third-party account or secret |
| google-sheets-data-source-lj | B: third-party account or secret |
| haproxy-load-balancer-lj | A: a system the learner hosts |
| iis-web-server-lj | A: a system the learner hosts |
| influxdb-data-source-lj | A: a system the learner hosts |
| k6-soak-testing-lj | C: terminal, CLI or local code |
| k6-spike-testing-lp | C: terminal, CLI or local code (k6) |
| kafka-monitoring-lj | A: a system the learner hosts |
| kubernetes-lp | A: a system the learner hosts (Kubernetes cluster, Helm) |
| linux-server-integration-lj | A: a system the learner hosts |
| macos-integration-lj | A: a system the learner hosts |
| mongodb-integration-lj | A: a system the learner hosts |
| monitor-aws-resources-lj | B: third-party account or secret |
| monitor-azure-resources-lj | B: third-party account or secret |
| mysql-data-source-lj | A: a system the learner hosts |
| mysql-db-olly-lj | A: a system the learner hosts |
| mysql-integration-lj | A: a system the learner hosts |
| postgresql-data-source-lj | A: a system the learner hosts |
| postgresql-db-olly-lj | A: a system the learner hosts |
| postgresql-integration-lj | A: a system the learner hosts |
| private-data-source-connect-lj | A: a system the learner hosts |
| prom-remote-write-lj | A: a system the learner hosts |
| prometheus-lj | A: a system the learner hosts |
| run-first-k6-test-lj | C: terminal, CLI or local code |
| send-logs-alloy-loki-lj | A: a system the learner hosts |
| send-traces-alloy-lp | A: a system the learner hosts (Alloy host) |
| windows-integration-lp | A: a system the learner hosts (Windows host) |

## Unclear (1)

- git-sync-use-lp: prerequisites text did not state requirements; Git Sync likely needs a GitHub repo (group B). Check.
