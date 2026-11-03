# Step 1: read-only discovery of docsteam.grafana.net

Run with a Viewer-level service account token, GET requests only. Nothing was changed. Grafana 13.3.0.

## What exists
- **Data sources (12):** grafanacloud-prom (default, Prometheus), grafanacloud-logs (Loki), grafanacloud-traces (Tempo), grafanacloud-profiles (Pyroscope), grafanacloud-graphite, grafanacloud-infinity, grafanacloud-k6, grafanacloud-usage (Prometheus), plus alert-state-history, cardinality-management, knowledgegraph, usage-insights.
- **Apps enabled:** grafana-metricsdrilldown-app 3.1.0, grafana-lokiexplore-app 3.1.0, grafana-pyroscope-app 3.1.0.
- **Folders:** GrafanaCloud (built-in usage and cardinality dashboards), Shared with me. Dashboards are the stock Cloud ones only.
- **Alert rules:** 0.
- **Prometheus (grafanacloud-prom):** the API works but the data source is **empty**: 0 metric names, no `up` series.

## Gaps per pilot path

| Need | alerting-first-rule-lj | drilldown-metrics-lj | interactive-dashboards-lj |
|---|---|---|---|
| Prometheus data source | Needs one named `grafanacloud-play-prom` (QuickPizza). Not present. | `grafanacloud-prom` exists | `grafanacloud-prom` exists |
| Metrics in it | `quickpizza_server_http_requests_total` with a `status` label. **Missing, source is empty.** | Several metrics with shared name prefixes and labels. **Missing.** | Series `up` with `environment` and `cluster` labels. **Missing.** |
| App enabled | n/a | grafana-metricsdrilldown-app **enabled** | n/a |
| Saved dashboard with a Prometheus panel | n/a | n/a | **Missing** (only stock Cloud dashboards exist) |
| Demo Data Dashboards app (installs QuickPizza sources) | Unknown. Could not confirm from this token. | n/a | n/a |
| Contact point | Provisioning API returned none. Unverified: the token cannot read the Alertmanager config. | n/a | n/a |
| Folder `QuickPizza alerts` | Absent (good, the path creates it) | n/a | n/a |

## What the token could not tell us
- Alertmanager config and whether the default contact point exists (needs `alert.notifications.config-history:read`).
- Whether the Demo Data Dashboards app is installed (not listed in the plugin API response).
- Whether the user the E2E tests run as has Editor or Admin. Check separately.

## Main finding
The default Prometheus data source has **no metric data at all**. All three pilot paths, and most metric-based paths, depend on seeded series. The key seeding question is how to get metrics in, covered in the next step.

## Follow-up: Demo Data Dashboards app (option 1 check, read-only)
- The app **`grafana-demodashboards-app` 1.18.0 is installed and enabled** on the stack.
- Its QuickPizza data sources are **not installed**: no `grafanacloud-play-prom`, `-play-traces`, `-play-logs` or `-play-profiles` exist. The guide describes an **Install** action inside the app that creates them.
- `alerting-first-rule-lj` opens with that install step, so the path may seed itself. The inventory flagged this as unclear ("only needed if data sources are not installed"). Needs a test run to confirm.
- The app creates its own `grafanacloud-play-*` data sources. It does **not** put data into `grafanacloud-prom`, so it does not help `drilldown-metrics-lj` or `interactive-dashboards-lj`.
- The `grafanacloud-play-*` names are referenced by 61 `content.json` blocks across 8 guides/paths (alerting, quickpizza, Explore, golden signals, demo-data), so installing the app's data sources is likely the most reusable seed.
- The install action is a write. It was not run.

## After installing the QuickPizza demo data (UI install by Taylor; re-checked read-only)
- **Created:** data sources `grafanacloud-play-prom`, `-play-logs`, `-play-traces`, `-play-profiles` (16 data sources total) and folder "Grafana QuickPizza Demo Dashboards" with 4 dashboards (Business Health, Logs Demo Dashboard, Overview, Performance Stats).
- **`grafanacloud-play-prom` has live data:** 3,596 metric names, including `quickpizza_server_http_requests_total` (with a `status` label), `up`, and `node_cpu_usage_seconds_total`. `cluster` values: `appenv-grafana-play-cluster`, `play-db-cluster`.

| Path | Status after install |
|---|---|
| alerting-first-rule-lj | **Data needs met** (data source and metric present). Still unverified: a contact point to select (provisioning API shows none; token cannot read Alertmanager config). Folder `QuickPizza alerts` still absent, as expected. |
| drilldown-metrics-lj | **Not met.** The guide's dashboard variable selects `grafanacloud-prom-input`, the default Cloud data source, which is still empty. `grafanacloud-play-prom` has the metrics but is not what the guide selects. |
| interactive-dashboards-lj | **Not met.** The guide queries `label_values(up, environment)` and uses a `region` label. `up` in play-prom has no `environment` label (it has `deployment_environment` and `cluster`). Also needs a saved dashboard with a Prometheus panel. |

## Open question for the two unmet paths
Either seed `grafanacloud-prom` with series that match the guides, or adjust the guides to use the play data source and labels that really exist. The second is a content change that affects real users, so it belongs to the authors.
