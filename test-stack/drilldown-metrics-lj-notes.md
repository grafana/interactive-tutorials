# drilldown-metrics-lj: seeding and test notes (for eng)

Purpose: record, step by step, how we seed the shared stack `docsteam.grafana.net` for `drilldown-metrics-lj` and test the path, so the same method can be repeated or automated for other paths. Part of grafana/interactive-tutorials#666.

Status legend: DONE, PENDING. Dates are when a step was performed.

## 0. What the path needs

From the AI inventory (`inventory/drilldown-metrics-lj.json`, reviewed by a human: no):

| Need | Kind | Declared in "Before you begin" |
|---|---|---|
| A Prometheus-compatible data source (guide selects `grafanacloud-prom`) | datasource | yes |
| Several metrics with related name prefixes and labels in that data source | telemetry-data | yes |
| `grafana-metricsdrilldown-app` enabled | plugin-or-app | no (implied by `startingLocation`) |

Manifest facts: `startingLocation` `/a/grafana-metricsdrilldown-app/drilldown`, 5 milestones (search-metrics, analyze-data, open-metrics-explore, add-metric-dashboard, end-journey), `testEnvironment.tier` cloud, no `prerequisites`.

## 1. Baseline (stack before seeding) (DONE, read-only discovery before 2026-10-29; see discovery.md)

- Data source `grafanacloud-prom` (display name `grafanacloud-docsteam-prom`, default) exists and is **empty**: no metric data at all.
- Metrics Drilldown app is installed and enabled.
- The `grafanacloud-play-*` (QuickPizza) data sources are not a substitute: the guide selects `grafanacloud-prom`.

Lesson: the stack had the right data source but no data. "Has a Prometheus data source" is not the same as "has the metrics the guide shows".

## 2. Seeding method (DONE 2026-10-31)

Script: `scripts/seed-metrics.py`. Writes synthetic series in Influx line protocol to the stack's Grafana Cloud Prometheus. Dry run by default; `--send` writes.

- Series: `up`, `node_cpu_online`, `node_cpu_hourly_cost`, `node_cpu_seconds_total`, `node_cpu_guest_seconds_total`, `node_cpu_usage_seconds_total`, `http_requests_total`, `node_memory_MemAvailable_bytes`, `node_filesystem_avail_bytes`. 6 instances in 4 environment/cluster/region groups, 30 s resolution, about 120 series.
- Counters are monotonic (a first version made them decrease; fixed).
- Credential: Cloud access policy `pathfinder-seed-metrics-write`, scope `metrics:write` only, 7-day token, stored outside the repo in `~/.config/grafana-docsteam-metrics.env` (METRICS_USER is the non-secret Prometheus instance id). The policy form had no realm field, so it may not be pinned to this stack.
- Result: HTTP 204. Verified read-only through the data source proxy: `up{job="node"}` 6 series, `node_cpu_seconds_total` 48, `environment` values development/production/staging.
- **Samples are only queryable for a short recent window.** Reseed immediately before each test run. Seeded metrics cannot be deleted; they age out.

Limits found:
- Influx ingestion rewrites colons in names to underscores (`asserts:resource:threshold` arrived as `asserts_resource_threshold`, a stray series left on the stack by our test; it ages out).

Remote write for colon names (DONE 2026-11-02): `scripts/seed-remote-write.py`, stdlib only. Hand-encoded protobuf `WriteRequest` plus snappy literal blocks (valid snappy, no compression), POST to `https://prometheus-prod-05-gb-south-0.grafana.net/api/prom/push` with the same Basic auth and `metrics:write` token, headers `Content-Encoding: snappy`, `Content-Type: application/x-protobuf`, `X-Prometheus-Remote-Write-Version: 0.1.0`. Server returned 200; `asserts:resource:threshold` queryable with 4 series (cpu:usage and memory:usage, warning and critical). Names with colons (recording-rule style) are therefore seedable. Dry run by default; run `seed-metrics.py --send` and `seed-remote-write.py --send` together before each test.

## 3. Test run: guide vs stack (DONE once as a selector check, 2026-10-31)

Method: signed-in browser, selectors from the manifest checked against the live page. The automated runner cannot be used (see `e2e-findings.md`: the runner's browser lands on the login page on this stack).

| Milestone | Result |
|---|---|
| 1. search-metrics | Data source variable resolves to `grafanacloud-prom`; label filter exists. Nav menu step not checked. |
| 2. analyze-data | **Gap:** step 1 highlights `select-action-asserts:resource:threshold`, an Asserts-only metric that cannot be seeded via Influx. Time picker, Breakdown and Related metrics tabs work. |
| 3. open-metrics-explore | Panel Menu and Explore item exist. Explore opens in a new tab, which the built-in browser pane blocks (tooling limit). |
| 4. add-metric-dashboard | Add menu, Add to dashboard item and Open dashboard button exist. |
| 5. Save | Save dashboard button exists. Not clicked. |

## 4. Run from the top (PENDING)

Plan, agreed step by step before any write:
1. Reseed metrics (stale after hours) and verify with the read-only token.
2. Walk milestones 1 to 5 in the signed-in browser, including saving the dashboard this time.
3. Decide how to handle the milestone 2 Asserts step (record as a guide gap, or attempt remote write).
4. Log every guide-vs-stack difference below.
5. Clean up and verify.

Run log: (empty)

## 5. Cleanup (PENDING after step 4)

Standing rule: frequent cleanup is imperative. Delete only objects the run created, identified by uid, and verify afterwards.

Expected objects from this path: one saved dashboard (from milestone 5). Metrics cannot be deleted.

Pilot teardown: delete access policy `pathfinder-seed-metrics-write` and its token; revoke the read-only and admin service account tokens.

### Run log, 2026-11-02 (in-panel run, signed-in built-in browser)

Method: started the real guide in the Pathfinder panel and used each step's Show me / Do it, so the guide itself drives the page. Reseeded with `seed-metrics.py --send` and `seed-remote-write.py --send` first.

- **Recommender:** on `/a/grafana-metricsdrilldown-app/drilldown` the panel's Suggested guides lists the learning path "Explore data using Metrics Drilldown" (5 milestones), with Start path. The alerting path was not suggested on `/alerting`, so the recommender serves some paths on this stack and not others.
- **Milestone 1 (search-metrics): PASS.** Step 1 needed the nav menu docked; the guide's "Fix this" button did it, then Do it completed. Steps 3 (data source) and 4 (filter) passed with Show me. Complete milestone worked; a "Badge unlocked" popup appeared (progress is saved to the user's Pathfinder storage, so a second run starts with milestone 1 already done unless reset).
- **Milestone 2 (analyze-data):** the guide text names `node_cpu_online`, `node_cpu_guest_seconds`, `node_cpu_seconds_total`, `node_cpu_usage_seconds_total`, all seeded. Step 2 (Select on `asserts:resource:threshold`) now **PASSES** with the remote-write seed; it was the failing step before. Remaining steps: pending.
- **Milestone 2 (analyze-data): PASS** (all 5 steps and Complete milestone). Step 2's Show me only highlights the Select button; steps 5 and 6 need a metric actually selected (the Breakdown and Related metrics tabs only exist on a metric page) and show "The target element must be visible and available on the page" until a learner clicks Select as step 2 says. Not a guide defect, but it means an automated run must perform the click, not just highlight it. After selecting `node_cpu_seconds_total` and Retry, both steps passed.
- **Milestone 3 (open-metrics-explore): not yet run.** Expected obstacle: the guide's Menu > Explore click opens Explore in a new browser tab, which the built-in browser pane blocks for automation (a user's own click is allowed).
- **Milestone 3 (open-metrics-explore): PARTIAL.** The guide's two-part step ("Run 2 steps": panel Menu, then Explore) ran and was marked Completed, but Explore opened in a new tab that the built-in browser pane blocks, so we could not see the Explore page open from the guide. Verified Explore separately by loading the same query by URL. Milestone marked complete with Mark section as complete and Complete milestone. Tooling limit, not a guide defect.
- **Milestone 4 (add-metric-dashboard): PASS.** Loaded Explore directly with the node_cpu_seconds_total query (the Pathfinder panel reopened by itself with the guide state intact). "Run 3 steps" (Add, Add to dashboard, Open dashboard) opened `/dashboard/new` with the panel, and "Do it" on Save dashboard opened the Save dialog. We cancelled the dialog, so nothing was written to the stack (dashboard count unchanged, 13 stock dashboards). The guide itself never asks the learner to confirm the dialog.
- **Milestone 5 (end-journey): not run** (closing text milestone).
- **Result so far:** with both seed scripts run first, milestones 1, 2 and 4 pass end to end in the real guide; milestone 3 passes except for the new-tab limit of our browser. The only seeding the path needed was Prometheus metrics, including the Asserts-style colon metric via remote write.
- **Cleanup for this run:** nothing to delete on the stack. Seeded metrics age out. The Pathfinder progress for this user is stored (milestones 1 to 4 marked complete) and should be reset before a rerun, using the milestone Redo or Reset section buttons.

### Manual run by Taylor, 2026-11-02 (after fresh reseed of both scripts)

Taylor went through the whole path end to end in their own browser (including clicking Explore, which opens in a new tab). The run saved one dashboard, `New dashboard` (uid `tang567`, General folder, one panel on `asserts:resource:threshold`), which was deleted by uid with the admin token and verified gone. Nothing else was left on the stack: 0 alert rules, only the `GrafanaCloud` folder, 16 data sources. Stock Cloud dashboards untouched.

Conclusion: `drilldown-metrics-lj` can be run end to end on the seeded stack with two reseed commands and no other setup. Cleanup per run is one dashboard.

## Issues to address (drilldown-metrics-lj passes end to end, but these should be looked at)

Result: the path passes on the seeded stack. These are problems found while running it, for the guide authors and Pathfinder team. Severity is my judgement; not yet reviewed by a writer.

1. **Milestone 2 step 2 depends on an Asserts-only metric (medium).** It highlights the Select button for `asserts:resource:threshold`, which exists only on stacks with Asserts enabled. On a stack without it the step's `exists-reftarget` requirement is never met, so a learner cannot complete the step. We could only pass it by seeding that metric through Prometheus remote write. Suggest pointing the step at a metric every Prometheus stack has, or making the step conditional.
2. **Milestone 2 step 2 only highlights; steps 5 and 6 need a metric actually selected (medium).** Step 2 is a highlight action, so using Show me or Do it does not click Select. Steps 5 and 6 (Breakdown and Related metrics tabs) then show "The target element must be visible and available on the page" until the learner selects a metric manually. Learners who follow the text will click Select, but anyone driving the guide with the buttons, and any automated run, gets stuck. Suggest making step 2 a click action.
3. **Metric name in the guide text is probably missing `_total` (low).** The milestone 2 prose names `node_cpu_guest_seconds`; the Prometheus node exporter metric is `node_cpu_guest_seconds_total`. Check against the real metric name.
4. **Milestone 1 step 1 needs the nav menu docked (low).** The guide's own "Fix this" button handles it, so it works, but a first-time learner sees a failed requirement before the step can run.

Not guide issues, for context: Explore opens in a new tab that the built-in browser pane blocks (tooling limit), and the recommender suggests this path on its own page but not the alerting path on `/alerting` (Pathfinder question).
