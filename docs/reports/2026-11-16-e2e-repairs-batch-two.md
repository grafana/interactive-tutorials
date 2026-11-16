# Interactive guide E2E repairs — batch two, 16 November 2026

This batch follows [PR #743](https://github.com/grafana/interactive-tutorials/pull/743) and repairs ten different failed guides. A fresh gcx query on ops returned 99 failed executions across 99 distinct guides in the preceding 24 hours. These are the same overnight failures as the [full inventory](2026-11-16-e2e-failures.md), not a post-deployment measurement of either repair batch. No reduction in scheduled failures is claimed yet.

Source: `grafanacloud-logs`, `{service_namespace="pathfinder-e2e-platform",service_name="orchestrator"} | event_name="guide_execution" | outcome="failed"`. Reports and failure DOM were inspected for each selected guide. [Guide health dashboard](https://ops.grafana-ops.net/d/lekzbhd/pathfinder-guide-health-detail).

## Selected repairs

Selected for broad usefulness and confirmed content defects, not usage analytics. All ten changed packages declare Cloud testing. The Prometheus learning path here connects a backend to Grafana Cloud; it is not the separate OSS `prometheus-grafana-101` guide. The OSS dashboard, Prometheus and Loki guides are unchanged.

| Guide | Confirmed problem and repair |
|---|---|
| `prometheus-add-data-source` | Add-data-source now opens an assistant/manual menu. Navigate to the catalog and retain mandatory creation verification. |
| `tempo-data-source-add` | Same catalog transition; replace stale name input with the current editable-title control. |
| `elasticsearch-data-source-add` | Search was attempted while the new menu was still open. Open the catalog, scope search to that page, and verify creation. |
| `clickhouse-data-source-add` | New add menu prevented reaching the catalog. Preserve plugin prerequisites and verify the catalog route. |
| `infinity-csv-add-data-source` | Same catalog transition and stale rename control. Keep creation verification and use the editable title. |
| `create-new-scripted-synthetics-check-tutorial` | Brittle navigation and positional tab/probe controls. Use current controls, wait for a loaded script editor, preserve the exact HTTP assertion, and require saved-check proof. |
| `alerting-query-language-set-evaluation-behavior` | The old ungrouped interval input is absent in grouped mode. Create the one-minute group atomically, confirm its selection, and configure pending/keep-firing durations. |
| `visualization-logs-add-visualization` | Panel creation/configuration existed only as prose. Add executable panel setup, handle optional onboarding, and use the current visualization tab. |
| `find-transformations` | Panel controls were hidden until the edit sidebar opened; the visualization selector was positional. Use current setup controls, select Line chart, and scope help/removal to the field filter. |
| `create-usage-alert` | Create usage alert was replaced by Create alert plus a product menu. Open All Products atomically, require product/budget configuration, and keep final notification activation explicitly manual. |

## Validation

All ten changed contents and packages pass strict Pathfinder CLI validation. Diff checks pass. IDs and platform targeting are preserved. An independent review checked the datasource, scripted and transformation changes. The transformation button prose was corrected from Configure to Edit visualization after its passing run; its tested selectors and actions are unchanged.

| Guide(s) | Live verification on learn.grafana.net |
|---|---|
| Query-language alert evaluation | Stock chain passed. Selected milestone: 4 mandatory steps passed, 1 unavailable optional mode selector skipped. Group creation and selection were exercised; no alert rule was saved. |
| Logs visualization | Stock E2E: 7 passed, 1 absent optional onboarding step skipped, 0 failed. Created an unsaved panel and selected Logs. Choosing the intended Loki source remains a manual prerequisite; this does not validate the following LogQL milestone. |
| Data transformations | Stock E2E: 15 passed, 1 absent optional onboarding step skipped, 0 failed. Final proof requires the calculation to remain and the filter to be absent. Dashboard remained unsaved. |
| Usage alert | Stock E2E: 8 passed, 0 failed. Exercised the product menu and budget configuration. Contact-point selection and Create alerts remain manual; no notifications were enabled. |
| Prometheus, Tempo, Elasticsearch, ClickHouse, Infinity | Each stock run reaches the corrected catalog but fails mandatory creation completion. Native UI creation succeeded for all five, independently confirmed through gcx; Tempo and Infinity rename controls were exercised. These are not reported as passing E2Es. |
| Scripted check | Stock execution reaches the scripted editor but prior step completion resets before script insertion. Native UI creation succeeded, and gcx confirmed the saved script matches the guide byte-for-byte, one probe is selected, and test alerts are off. Saved-check link and five-second dashboard refresh were verified. This is not a passing stock E2E. |

The data-source creation discrepancy between signed-in native UI and test-account execution remains unresolved. Required creation checks were retained. Script insertion and saved-check proof likewise remain mandatory; the runner failure was not bypassed with skips.

## Cleanup and exclusions

Deleted the five data sources created during native verification and confirmed the datasource UID set exactly matches the pre-test baseline. Deleted the single scripted test check and the one newly created, empty alerting folder. Revoked the temporary test service account. No existing resources were removed, no dashboard was saved, and no standalone alert rule was created. Private reports and signed artifact URLs remain outside the repository.

Direct Prometheus connection was excluded because its saved failure page has an empty required server URL. Snapshot/query-library guides lacked their required existing-panel setup. Reachability SLO lacked a check, and PDC needs a connected external agent. Those require explicit fixtures or broader workflow changes; they were not counted as repaired by weakening checks.
