# Interactive guide E2E failures — 16 November 2026

Source: ops Grafana, `grafanacloud-logs`, `{service_namespace="pathfinder-e2e-platform",service_name="orchestrator"} | event_name="guide_execution"`, preceding 24 hours as queried around 14:11 UTC. Latest `ended_at` per guide cross-checked against an aggregate `max_over_time` query.

**379 observed executed leaf guides: 280 passed, 99 failed.** All observed executions are non-canary, ending between 01:02 and 04:43 UTC on 16 November. This is observed execution coverage, not a claim that every catalogue guide ran. Journey milestones count individually. Failed prerequisites can prevent later milestones from executing.

Task telemetry also contains 18 infrastructure-exhausted tasks and 6 non-executions; these are separate from the 99 observed failed guide executions. All ten selected failures belong to terminal guide-failure tasks.

[Guide health dashboard](https://ops.grafana-ops.net/d/lekzbhd/pathfinder-guide-health-detail)

## Priority repair batch

Ranked by broadly reusable workflows and shared repair opportunities, not usage analytics.

| Rank | Guide | Reason |
|---|---|---|
| 1 | `sm-setting-up-your-first-check` | Create HTTP uptime checks; stale navigation completion |
| 2 | `sm-dns-check-tutorial` | DNS availability; shared navigation repair |
| 3 | `sm-tcp-check-tutorial` | TCP availability; shared navigation repair |
| 4 | `first-dashboard-cloud` | First dashboard; collapsed navigation menu |
| 5 | `alerting-first-rule-set-evaluation-behavior` | First alert; evaluation group setup |
| 6 | `connect-prometheus-metrics` | Connect Prometheus metrics; catalog navigation |
| 7 | `loki-data-source-add` | Connect logs; catalog navigation and rename |
| 8 | `postgresql-data-source-add` | Connect PostgreSQL; catalog navigation and rename |
| 9 | `mysql-data-source-add` | Connect MySQL; catalog navigation and rename |
| 10 | `create-availability-slo-configure-targets` | Create availability SLO; actionable wizard steps |

The initial shortlist also included LogQL 101, advanced Prometheus, Logs/Metrics Drilldown, and generic connect-data onboarding. Their saved pages show unfilled learner inputs, absent data, or an unselected external system. Those need runner/fixture work; bypassing their checks would hide failures. The repair batch above focuses on broadly useful guides with confirmed content defects.

## All latest failures

| Guide | Local content | Failed step |
|---|---|---|
| `adaptive-logs-review-apply` | [adaptive-logs-lj/review-apply/content.json](../../adaptive-logs-lj/review-apply/content.json) | `__standalone__-step-u9zyug` |
| `adaptive-metrics-rules-exemptions` | [adaptive-metrics-lj/rules-exemptions/content.json](../../adaptive-metrics-lj/rules-exemptions/content.json) | `__standalone__-step-1u5eg52` |
| `alerting-first-rule-set-evaluation-behavior` | [alerting-first-rule-lj/set-evaluation-behavior/content.json](../../alerting-first-rule-lj/set-evaluation-behavior/content.json) | `section-set-evaluation-behavior-step-13hzsxy` |
| `alerting-query-language-set-evaluation-behavior` | [alerting-query-language-lj/set-evaluation-behavior/content.json](../../alerting-query-language-lj/set-evaluation-behavior/content.json) | `section-set-evaluation-behavior-step-13hzsxy` |
| `application-observability-investigate-service` | [application-observability-investigate-service/content.json](../../application-observability-investigate-service/content.json) | `open-instrumented-service` |
| `attribute-cost-by-team-create-team-pipeline` | [attribute-cost-by-team-lj/create-team-pipeline/content.json](../../attribute-cost-by-team-lj/create-team-pipeline/content.json) | `section-create-team-pipeline-step-1dz5n4r` |
| `billing-usage-navigate-to-billing-dashboard` | [billing-usage-lj/navigate-to-billing-dashboard/content.json](../../billing-usage-lj/navigate-to-billing-dashboard/content.json) | `section-open-the-app-step-1pkyzex` |
| `categorize-collector-fleet-navigate-to-fleet` | [categorize-collector-fleet-lj/navigate-to-fleet/content.json](../../categorize-collector-fleet-lj/navigate-to-fleet/content.json) | `section:blocks[1]-step-1tz4u0c` |
| `clickhouse-data-source-add` | [clickhouse-data-source-lj/add-data-source/content.json](../../clickhouse-data-source-lj/add-data-source/content.json) | `section:blocks[2]-step-a7xjtd` |
| `connect-agent-to-agent-observability-enable-agent-observability` | [connect-agent-to-agent-observability-lj/enable-agent-observability/content.json](../../connect-agent-to-agent-observability-lj/enable-agent-observability/content.json) | `section-enable-agent-observability-step-1ljcvmy` |
| `connect-prometheus-direct-cloud` | [connect-prometheus-direct-cloud/content.json](../../connect-prometheus-direct-cloud/content.json) | `connect-prometheus-direct-cloud-step-7` |
| `connect-prometheus-metrics` | [connect-prometheus-metrics/content.json](../../connect-prometheus-metrics/content.json) | `section-add-connection-step-2i05v7` |
| `connect-prometheus-pdc-cloud` | [connect-prometheus-pdc-cloud/content.json](../../connect-prometheus-pdc-cloud/content.json) | `create-private-network` |
| `create-availability-slo-configure-targets` | [create-availability-slo-lj/configure-targets/content.json](../../create-availability-slo-lj/configure-targets/content.json) | `section:blocks[2]-step-n2w0kx` |
| `create-new-scripted-synthetics-check-tutorial` | [sm-scripted-check-tutorial/content.json](../../sm-scripted-check-tutorial/content.json) | `section:blocks[2]-step-lche00` |
| `create-usage-alert` | [create-usage-alert/content.json](../../create-usage-alert/content.json) | `section-configure-alert-step-qpzbga` |
| `dashboard-snapshot-guide` | [dashboard-snapshot-guide/content.json](../../dashboard-snapshot-guide/content.json) | `find-panel-snapshot-header` |
| `data-transformation-lp-add-field-from-calculation` | [data-transformation-lp/add-field-from-calculation/content.json](../../data-transformation-lp/add-field-from-calculation/content.json) | `section:blocks[0].whenFalse[2]-step-19iamkr` |
| `data-transformation-lp-export-transformations` | [data-transformation-lp/export-transformations/content.json](../../data-transformation-lp/export-transformations/content.json) | `section:blocks[0].whenFalse[2]-step-1hdnjhm` |
| `data-transformation-lp-filter-by-value` | [data-transformation-lp/filter-by-value/content.json](../../data-transformation-lp/filter-by-value/content.json) | `section:blocks[0].whenFalse[2]-step-19iamkr` |
| `data-transformation-lp-group-by` | [data-transformation-lp/group-by/content.json](../../data-transformation-lp/group-by/content.json) | `section:blocks[0].whenFalse[2]-step-19iamkr` |
| `data-transformation-lp-join-by-field` | [data-transformation-lp/join-by-field/content.json](../../data-transformation-lp/join-by-field/content.json) | `section:blocks[0].whenFalse[2]-step-19iamkr` |
| `data-transformation-lp-organize-by-fields` | [data-transformation-lp/organize-by-fields/content.json](../../data-transformation-lp/organize-by-fields/content.json) | `section:blocks[0].whenFalse[2]-step-19iamkr` |
| `dpm-explore-up-metric` | [dpm-explore-up-metric/content.json](../../dpm-explore-up-metric/content.json) | `section-choose-prometheus-datasource-step-1xdyge6` |
| `drilldown-logs-view-logs` | [drilldown-logs-lj/view-logs/content.json](../../drilldown-logs-lj/view-logs/content.json) | `section:blocks[1]-step-7pxzlj` |
| `drilldown-metrics-analyze-data` | [drilldown-metrics-lj/analyze-data/content.json](../../drilldown-metrics-lj/analyze-data/content.json) | `section:blocks[1]-step-kt5u4o` |
| `drilldown-profiles-explore-services` | [drilldown-profiles-lj/explore-services/content.json](../../drilldown-profiles-lj/explore-services/content.json) | `conditional-false:blocks[1]-step-1sj8mt6` |
| `drilldown-traces-view-distribution` | [drilldown-traces-lj/view-distribution/content.json](../../drilldown-traces-lj/view-distribution/content.json) | `section:blocks[3]-step-1t57rkk` |
| `elasticsearch-data-source-add` | [elasticsearch-data-source-lj/add-data-source/content.json](../../elasticsearch-data-source-lj/add-data-source/content.json) | `section:blocks[1]-step-x5sofb` |
| `elasticsearch-logs-configure-log-display` | [elasticsearch-logs-lj/configure-log-display/content.json](../../elasticsearch-logs-lj/configure-log-display/content.json) | `section:blocks[1]-step-s7y1ix` |
| `find-and-fix-slow-query-choose-and-open` | Not found in checkout | `section-choose-and-open-step-10ox0ys` |
| `find-transformations` | [transform-data/content.json](../../transform-data/content.json) | `section-guide-section-34209-step-1am283n` |
| `first-dashboard-cloud` | [first-dashboard-cloud/content.json](../../first-dashboard-cloud/content.json) | `section-datasource-setup-step-t5lsxb` |
| `fleet-mgt-monitor-health-determine-config` | [fleet-mgt-monitor-health-lj/determine-config/content.json](../../fleet-mgt-monitor-health-lj/determine-config/content.json) | `section:blocks[2]-step-1c6y2fa` |
| `fleet-mgt-staged-rollout-verify-env-attributes` | [fleet-mgt-staged-rollout-lj/verify-env-attributes/content.json](../../fleet-mgt-staged-rollout-lj/verify-env-attributes/content.json) | `section-check-collector-attributes-step-11jg9q9` |
| `get-started-connect-data` | [get-started-connect-data/content.json](../../get-started-connect-data/content.json) | `section-add-your-data-source-step-1sl5g5c` |
| `get-started-demo-data` | [get-started-demo-data/content.json](../../get-started-demo-data/content.json) | `section-install-the-demo-step-1sp30i` |
| `get-started-instrument-app` | [get-started-instrument-app/content.json](../../get-started-instrument-app/content.json) | `section-create-a-token-and-copy-the-config-step-uwja2f` |
| `get-started-k6-test-builder` | [get-started-k6-test-builder/content.json](../../get-started-k6-test-builder/content.json) | `section-open-the-test-builder-step-qjgi09` |
| `get-started-monitor-host` | [get-started-monitor-host/content.json](../../get-started-monitor-host/content.json) | `section-set-up-the-collector-step-1fa4dxa` |
| `get-started-send-data` | [get-started-send-data/content.json](../../get-started-send-data/content.json) | `section-create-a-token-and-copy-the-config-step-sunkoi` |
| `git-sync-dashboards-create-new-dashboard` | [git-sync-dashboards-lj/create-new-dashboard/content.json](../../git-sync-dashboards-lj/create-new-dashboard/content.json) | `section:blocks[3]-step-2oooyr` |
| `git-sync-setup` | [git-sync-setup/content.json](../../git-sync-setup/content.json) | `section-guide-section-configure-repository-step-bv7s77` |
| `github-data-source-install` | [github-data-source-lj/install-github-plugin/content.json](../../github-data-source-lj/install-github-plugin/content.json) | `section:blocks[4]-step-rb6wuv` |
| `github-visualize-build-issues-panel` | [github-visualize-lj/build-issues-panel/content.json](../../github-visualize-lj/build-issues-panel/content.json) | `section:blocks[1]-step-ybxq1z` |
| `google-sheets-data-source-install` | [google-sheets-data-source-lj/install-plugin/content.json](../../google-sheets-data-source-lj/install-plugin/content.json) | `section:blocks[3]-step-1d80a7k` |
| `grafana-cloud-onboarding-setup-billing-alerts` | [grafana-cloud-onboarding-lj/setup-billing-alerts/content.json](../../grafana-cloud-onboarding-lj/setup-billing-alerts/content.json) | `section-create-usage-alert-step-1a9kpdx` |
| `grafana-irm-configuration-create-on-call-schedule` | [grafana-irm-configuration-lj/create-on-call-schedule/content.json](../../grafana-irm-configuration-lj/create-on-call-schedule/content.json) | `section-create-new-schedule-step-1kz0eqe` |
| `grafana-k8s-tour` | [grafana-k8s-tour/content.json](../../grafana-k8s-tour/content.json) | `overview-datasource` |
| `haproxy-load-balancer-configure-integration` | [haproxy-load-balancer-lj/configure-integration/content.json](../../haproxy-load-balancer-lj/configure-integration/content.json) | `section:blocks[1]-step-kkmzle` |
| `how-to-setup-secrets-tutorial` | [how-to-setup-secrets-tutorial/content.json](../../how-to-setup-secrets-tutorial/content.json) | `section-performace-multistep-guided-step-z0ljak` |
| `ihub-install-alloy-k8s` | [ihub-install-alloy-k8s/content.json](../../ihub-install-alloy-k8s/content.json) | `step-choose-setup-standard` |
| `iis-web-server-verify-metrics` | [iis-web-server-lj/verify-metrics/content.json](../../iis-web-server-lj/verify-metrics/content.json) | `section:blocks[1]-step-150ysr8` |
| `infinity-csv-add-data-source` | [infinity-csv-lj/add-data-source/content.json](../../infinity-csv-lj/add-data-source/content.json) | `section:blocks[2]-step-136s9ed` |
| `influxdb-data-source-add` | [influxdb-data-source-lj/add-data-source/content.json](../../influxdb-data-source-lj/add-data-source/content.json) | `section:blocks[1]-step-x5sofb` |
| `infrastructure-alerting-build-your-query` | [infrastructure-alerting-lj/build-your-query/content.json](../../infrastructure-alerting-lj/build-your-query/content.json) | `section:blocks[2]-step-cfj0m0` |
| `interactive-dashboards-create-query-variable` | [interactive-dashboards-lj/create-query-variable/content.json](../../interactive-dashboards-lj/create-query-variable/content.json) | `section:blocks[3]-step-imjn8t` |
| `irm-configuration` | [irm-configuration/content.json](../../irm-configuration/content.json) | `section-create-on-call-rotation-step-1qslqhb` |
| `k8s-connect-first-cluster` | [k8s-connect-first-cluster/content.json](../../k8s-connect-first-cluster/content.json) | `section-open-configuration-step-1ajh0ik` |
| `k8s-cpu` | [k8s-cpu/content.json](../../k8s-cpu/content.json) | `section-namespace-cpu-detail-step-16tatr6` |
| `k8s-mem` | [k8s-mem/content.json](../../k8s-mem/content.json) | `section-namespace-detail-step-1gfa53n` |
| `kafka-monitoring-install-grafana-alloy` | [kafka-monitoring-lj/install-grafana-alloy/content.json](../../kafka-monitoring-lj/install-grafana-alloy/content.json) | `section:blocks[2]-step-140rgjy` |
| `knowledge-graph-explore-service-relationships` | [knowledge-graph-explore-service-relationships/content.json](../../knowledge-graph-explore-service-relationships/content.json) | `section-read-graph-step-1eik4oq` |
| `linux-server-integration-configure-alloy` | [linux-server-integration-lj/configure-alloy/content.json](../../linux-server-integration-lj/configure-alloy/content.json) | `section:blocks[2]-step-nlxzo3` |
| `logql-101` | [logql-101/content.json](../../logql-101/content.json) | `section-select-datasource-step-mwd2e4` |
| `loki-data-source-add` | [loki-data-source-lj/add-data-source/content.json](../../loki-data-source-lj/add-data-source/content.json) | `section:blocks[1]-step-1ivn75v` |
| `macos-integration-configure-alloy` | [macos-integration-lj/configure-alloy/content.json](../../macos-integration-lj/configure-alloy/content.json) | `section:blocks[1]-step-kkmzle` |
| `monitor-aws-resources-create-scrape-job` | [monitor-aws-resources-lj/create-scrape-job/content.json](../../monitor-aws-resources-lj/create-scrape-job/content.json) | `section:blocks[3]-step-1fi85vc` |
| `monitor-azure-resources-verify-data-collection` | [monitor-azure-resources-lj/verify-data-collection/content.json](../../monitor-azure-resources-lj/verify-data-collection/content.json) | `section:blocks[1]-step-1mi8i7t` |
| `mysql-data-source-add` | [mysql-data-source-lj/add-data-source/content.json](../../mysql-data-source-lj/add-data-source/content.json) | `section:blocks[2]-step-1h15kww` |
| `mysql-db-olly-configure-alloy` | [mysql-db-olly-lj/configure-alloy/content.json](../../mysql-db-olly-lj/configure-alloy/content.json) | `section:blocks[3]-step-exl5i5` |
| `mysql-integration-test-connection` | [mysql-integration-lj/test-connection/content.json](../../mysql-integration-lj/test-connection/content.json) | `section:blocks[1]-step-uulvt3` |
| `open-a-query-on-queries-overview` | Not found in checkout | `section-open-one-query-step-jiwyh8` |
| `play-chicago-l-trains-tour` | [play-chicago-l-trains-tour/content.json](../../play-chicago-l-trains-tour/content.json) | `section-the-api-query-step-19n5hi4` |
| `postgresql-data-source-add` | [postgresql-data-source-lj/add-data-source/content.json](../../postgresql-data-source-lj/add-data-source/content.json) | `section:blocks[1]-step-1ivn75v` |
| `postgresql-db-olly-configure-alloy` | [postgresql-db-olly-lj/configure-alloy/content.json](../../postgresql-db-olly-lj/configure-alloy/content.json) | `section:blocks[3]-step-exl5i5` |
| `postgresql-integration-configure-alloy` | [postgresql-integration-lj/configure-alloy/content.json](../../postgresql-integration-lj/configure-alloy/content.json) | `section:blocks[2]-step-1fmi0ia` |
| `private-data-source-connect-select-installation-method` | [private-data-source-connect-lj/select-installation-method/content.json](../../private-data-source-connect-lj/select-installation-method/content.json) | `section:blocks[1]-step-rzd5o3` |
| `prom-remote-write-configure` | [prom-remote-write-lj/configure-prom-remote-write/content.json](../../prom-remote-write-lj/configure-prom-remote-write/content.json) | `section-create-a-token-and-copy-the-config-step-yt40j7` |
| `prometheus-add-data-source` | [prometheus-lj/add-data-source/content.json](../../prometheus-lj/add-data-source/content.json) | `section-add-prometheus-data-source-step-3oqs47` |
| `prometheus-advanced-queries` | [prometheus-advanced-queries/content.json](../../prometheus-advanced-queries/content.json) | `choose-prometheus` |
| `rca-demo` | [rca-demo/content.json](../../rca-demo/content.json) | `section-rca-orientation-step-16uffjj` |
| `rca-demo-ops` | [rca-demo-ops/content.json](../../rca-demo-ops/content.json) | `section-go-to-rca-workbench-step-1r4dumt` |
| `rca-workbench-investigation-navigate-to-workbench` | [rca-workbench-investigation-lj/navigate-to-workbench/content.json](../../rca-workbench-investigation-lj/navigate-to-workbench/content.json) | `section-navigate-to-rca-step-18sn5ya` |
| `read-a-trace-open-a-trace` | [read-a-trace-lj/open-a-trace/content.json](../../read-a-trace-lj/open-a-trace/content.json) | `section:blocks[1]-step-84v889` |
| `saved-queries-panel-edit` | [saved-queries-panel-edit/content.json](../../saved-queries-panel-edit/content.json) | `saved-query-editor-ready` |
| `semantic-layer-data-model-config` | [semantic-layer-data-model-config/content.json](../../semantic-layer-data-model-config/content.json) | `section-data-model-exploration-step-1w8gz2` |
| `send-logs-alloy-loki-install-alloy` | [send-logs-alloy-loki-lj/install-alloy/content.json](../../send-logs-alloy-loki-lj/install-alloy/content.json) | `section:blocks[3]-step-1xblqgf` |
| `show-hide-rules-1l2h` | [show-hide-rules-1l2h/content.json](../../show-hide-rules-1l2h/content.json) | `section:blocks[1]-step-1x937jp` |
| `sm-dns-check-tutorial` | [sm-dns-check-tutorial/content.json](../../sm-dns-check-tutorial/content.json) | `section-navigate-synthetics-step-fb5im0` |
| `sm-first-reachability-slo` | [sm-first-reachability-slo/content.json](../../sm-first-reachability-slo/content.json) | `sm-slo-search-check-optional` |
| `sm-setting-up-your-first-check` | [sm-setting-up-your-first-check/content.json](../../sm-setting-up-your-first-check/content.json) | `section-navigate-synthetics-step-fb5im0` |
| `sm-tcp-check-tutorial` | [sm-tcp-check-tutorial/content.json](../../sm-tcp-check-tutorial/content.json) | `section-navigate-synthetics-step-fb5im0` |
| `tempo-data-source-add` | [tempo-data-source-lj/add-data-source/content.json](../../tempo-data-source-lj/add-data-source/content.json) | `section:blocks[1]-step-1ayyzjq` |
| `visualization-logs-add-visualization` | [visualization-logs-lp/add-visualization/content.json](../../visualization-logs-lp/add-visualization/content.json) | `section:blocks[3]-step-2oooyr` |
| `visualization-metrics-write-query` | [visualization-metrics-lj/write-query/content.json](../../visualization-metrics-lj/write-query/content.json) | `section:blocks[3]-step-1ermedq` |
| `visualization-traces-add-traces-table` | [visualization-traces-lj/add-traces-table/content.json](../../visualization-traces-lj/add-traces-table/content.json) | `section:blocks[2]-step-x7ng86` |
| `welcome-to-play-visualization` | [welcome-to-play/visualization-page/content.json](../../welcome-to-play/visualization-page/content.json) | `section-flame-graphs-viz-step-vcqkt9` |
| `windows-integration-install-dashboards-alerts` | [windows-integration-lp/install-dashboards-alerts/content.json](../../windows-integration-lp/install-dashboards-alerts/content.json) | `section:blocks[3]-step-sug0pq` |

## Validation on learn.grafana.net

All 11 changed packages pass strict Pathfinder CLI validation. Ten failed guide flows are repaired; the SLO flow also requires executable ratio-query inputs in its preceding milestone, so it changes two content files. No completion checks were removed to manufacture passes.

| Flow | Verification result |
|---|---|
| HTTP Synthetic Monitoring | Stock E2E: 19 passed, 1 optional initialization skipped, 0 failed; saved check visible |
| DNS Synthetic Monitoring | Stock E2E: 21 passed, 1 optional initialization skipped, 0 failed; saved check visible |
| TCP Synthetic Monitoring | Stock E2E: 21 passed, 1 optional initialization skipped, 0 failed; saved check visible |
| Connect Prometheus metrics | Stock E2E: 4 passed, 0 failed; reached hosted Prometheus configuration |
| First dashboard | Corrected catalog navigation checked against live UI; full E2E blocked during discovery by an already-completed, collapsed TestData section |
| First alert evaluation | Stock E2E: 4 passed, 1 absent optional evaluation-mode selector skipped, 0 failed; all 18 prerequisite navigation/query/folder steps passed |
| Loki data source | Catalog navigation/search pass in stock E2E; native UI creation and rename verified. Automated creation remains unsuccessful |
| PostgreSQL data source | Catalog navigation/search pass in stock E2E; native UI creation and rename verified. Automated creation remains unsuccessful |
| MySQL data source | Catalog navigation/search pass in stock E2E; native UI creation verified. Automated creation remains unsuccessful |
| Availability SLO | Native UI creation verified, then independently read through gcx: authored OpenTelemetry ratio queries, 99.9% objective, 28-day window |

The three data-source reruns stop at creation despite the same catalog actions succeeding with the signed-in user. A Loki rerun captured HTTP 500 after clicking the card. Mandatory creation verification remains in place; these are not reported as passing E2Es. A legacy data-source API probe succeeded, which does not establish that the newer creation API or subsequent permission reload works for the test account.

The SLO stock chain returned nominal passes while screenshots still showed loading and the wizard never created a resource; those results are rejected as proof. The first-dashboard runner hung while trying to discover hidden steps inside an already-completed section. Neither issue is bypassed with weakened guide requirements.

Test checks, data sources, and SLOs were deleted after verification. No external database credentials were entered and no alert rules were saved. Raw reports, screenshots and signed evidence URLs remain outside the repository; signed URLs and temporary credentials are not included in this report.
