# Test dashboards for authoring on learn.grafana.net

Some learning paths open dashboards on Grafana Play (`play.grafana.org`). Authors test paths in the Pathfinder Block Editor on `learn.grafana.net`, where those dashboards may not exist. A step that opens a missing dashboard shows "Dashboard not found", and the highlight steps after it can't find their panels.

This folder holds copies of Play dashboards that can be imported into a test stack. They are for checking path steps only. Learners run the paths on Grafana Play, so nothing here is published.

## account-service.json

A copy of **Account Service** from Grafana Play (uid `appenv-svc-account`, folder Retail Banking). It was saved from Play on 2026-11-06. Play's own last-saved date for the dashboard is 2026-10-29.

The `read-dashboard-panels` path uses it in the section "All three RED measurements", where it highlights the **Request Rate**, **Error Ratio**, and **Latency P50 / P95 / P99** panels (panel ids 5, 6, and 7).

To import it:

1. In Grafana, go to **Dashboards**, then **New**, then **Import**.
2. Upload `account-service.json`.
3. Keep the uid `appenv-svc-account`. The path's steps open `/d/appenv-svc-account/account-service`.
4. Choose any folder.

The panels will show no data or a data source error, because the queries use the Prometheus data source on Play. The path's steps highlight the panels themselves, so the steps can still be tested. The copy is not kept in sync with Play.
