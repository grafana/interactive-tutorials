# Test stack: prerequisite inventory summary

Generated from `inventory/*.json` (AI-extracted, 65 paths, **not yet human-reviewed**). Tiering below is a first-pass judgment to be confirmed with writers.

| Group | Paths | What it takes |
|---|---|---|
| A-hosted-system | 21 | A real server or host the stack can reach (database, load balancer, OS host, Kafka, Elasticsearch, Prometheus). Needs hosting and an owner. |
| B-third-party-account-or-secret | 7 | A real cloud or SaaS account, or a secret (AWS/Azure/GitHub/Google). Needs credential storage decisions. |
| C-local-cli-or-agent-code | 7 | Terminal, CLI, CI or local-code steps a browser E2E cannot drive. |
| D-collector-fleet-seeding | 3 | Registered Alloy collectors in Fleet Management. Feasible with a few containers. |
| E-public-endpoint-or-portable-url | 5 | Public demo endpoints or URLs that may only need a seeded data source or guide fix. |

Paths with any external-infra need: 43 of 65. Paths needing only in-Cloud seeding or nothing: 22.

## A-hosted-system (21)

- beyla-tempo-lj
- clickhouse-data-source-lj
- elasticsearch-data-source-lj
- elasticsearch-logs-lj
- haproxy-load-balancer-lj
- iis-web-server-lj
- influxdb-data-source-lj
- kafka-monitoring-lj
- linux-server-integration-lj
- macos-integration-lj
- mongodb-integration-lj
- mysql-data-source-lj
- mysql-db-olly-lj
- mysql-integration-lj
- postgresql-data-source-lj
- postgresql-db-olly-lj
- postgresql-integration-lj
- private-data-source-connect-lj
- prom-remote-write-lj
- prometheus-lj
- send-logs-alloy-loki-lj

## B-third-party-account-or-secret (7)

- cloudwatch-data-source-lj
- git-sync-dashboards-lj
- github-data-source-lj
- github-visualize-lj
- google-sheets-data-source-lj
- monitor-aws-resources-lj
- monitor-azure-resources-lj

## C-local-cli-or-agent-code (7)

- automate-k6-cicd-lj
- connect-agent-to-agent-observability-lj
- deploy-alert-terraform-lj
- establish-k6-baseline-lj
- find-k6-limits-lj
- k6-soak-testing-lj
- run-first-k6-test-lj

## D-collector-fleet-seeding (3)

- categorize-collector-fleet-lj
- fleet-mgt-monitor-health-lj
- fleet-mgt-staged-rollout-lj

## E-public-endpoint-or-portable-url (5)

- drilldown-profiles-lj
- infinity-csv-lj
- infinity-json-lj
- loki-data-source-lj
- tempo-data-source-lj

## Notes
- `loki-data-source-lj` has an external-infra need but its agent set `externalInfraDependent: false`; treated as group E.
- `github-visualize-lj` PAT is a secret, not a server (group B).
- `k6-script-authoring-assistant-lj` has fewer than two milestones and is out of scope.
- 'entitlement' was tagged on 41 paths and is mostly permissions/admin role; treat as unreliable until reviewed.