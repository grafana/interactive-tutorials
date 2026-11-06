# E2E findings

## alerting-first-rule-lj, run 1 (2026-10-29)

Runner: Pathfinder CLI 2.25.0 (35a0e40), target `docsteam.grafana.net` (Grafana 13.3.0), shared-stack mode with mutations allowed for that host.

Result: **0 of 8 guides passed.** Milestone 1 (`install-datasources`) failed with 0 steps executed; milestones 2 to 8 were skipped because their prerequisite failed. Pre-flight checks passed (auth valid, Pathfinder plugin installed).

### Likely cause (SUPERSEDED, see run 2 below: this hypothesis was wrong)
Milestone 1 is a guided step that clicks `button[data-testid='install-quickpizza']` and requires that button to exist (`exists-reftarget`). The QuickPizza data sources were already installed by hand beforehand, so the button is probably gone and the step cannot run. The runner gave no step-level detail and wrote no failure artifacts, so this is inferred from the guide, not observed.

### What it shows
Seeding a prerequisite that a path itself performs can make the path fail. This is the shared-stack state problem named in the proposal: the stack's state must match what the guide expects at the start of the run, not only what it needs at the end.

### Stack state after the run
- No folder `QuickPizza alerts` and no alert rules were created (milestone 1 failed first).
- The runner's temporary service account was created and deleted. No leftovers.

### Options
1. Uninstall the demo data and rerun, so the path's own install step performs it. The next run would fail again unless the stack is reset first.
2. Keep the demo data seeded and make the install step conditional in the guide (author decision).
3. Exclude milestone 1 from the test and treat the data sources as a seeded prerequisite.

## alerting-first-rule-lj, run 2 (after Remove, Install button visible again)

Same result: 0 of 8, milestone 1 failed with 0 steps.

The report shows the real error, which I had not read in run 1: `outcome: infrastructure_error`, `errorCode: REPORT_MISSING`, message `locator.waitFor: Timeout 15000ms exceeded` while waiting for **any interactive step element to become visible**.

So the guide's steps never rendered in the browser. The Install button was not the cause, and my run 1 diagnosis was wrong. The failure happens before any step is attempted, so nothing was created on the stack in either run.

Open questions: why the guide does not render on `docsteam.grafana.net` (the plugin version on the stack, how a local package is loaded into the Pathfinder panel, or an auth or panel-opening issue). Next step is a run with `--always-screenshot --trace --headed` to see what the browser shows.

## alerting-first-rule-lj, run 3 (diagnostic: --always-screenshot --trace --headed)

Same result (`infrastructure_error`, `REPORT_MISSING`, 0 steps). No screenshots or traces were saved: tracing is disabled for bearer-token auth ("traces can contain credentials") and artifacts are only written once a step runs.

What the source shows: the runner navigates to the path's `startingLocation` (`/alerting`), opens the Pathfinder docs panel, then dispatches a `pathfinder-auto-open-docs` event with the guide URL `bundled:e2e-test` and waits up to 15 s for an interactive step to render. Pre-flight passes (auth valid, `grafana-pathfinder-app` 2.25.0 installed and enabled, same version as the runner). The stack's Pathfinder plugin has no saved configuration (`jsonData: null`).

Not yet known: what the browser shows at the moment of the timeout. Candidates: the docs panel not opening on `/alerting`, the plugin not accepting the injected guide on a Cloud stack, or a page-level error.

Nothing was created on the stack in any of the three runs. Runner service accounts were created and deleted each time.

## Run 4 and diagnosis: the browser is not signed in

Run 4 (headed): Taylor saw the stack open at the **login page**.

Confirmed with read-only requests: on `docsteam.grafana.net`, API calls accept a service-account bearer token (`/api/org`, `/api/user` return 200), but a **page load** with the same token is treated as signed out (`/alerting` boot data says `"isSignedIn": false`, identical to an unauthenticated request). The runner authenticates its browser by adding the bearer header to requests to the target, so the browser lands on the login page, the Pathfinder panel never opens, and no steps render. That matches the 15 s `waitFor` timeout and `REPORT_MISSING`.

Not known: why this stack ignores the bearer token for page loads, and how the runner's cloud shared-stack path is meant to authenticate the browser (it is documented for `learn.grafana.net`). Possibilities: a Grafana Cloud edge or auth-proxy behaviour specific to this stack, a missing stack setting, or the runner's mechanism needing something we did not provide.

Nothing was created on the stack in any run.

### Draft question for Pathfinder engineering (not sent)
> We're running `pathfinder-cli e2e --tier cloud --cloud-url https://docsteam.grafana.net/ --cloud-instance-admin-token docsteam.grafana.net=... --allow-cloud-instance-mutations docsteam.grafana.net` (CLI 2.25.0, stack Pathfinder 2.25.0, Grafana 13.3.0). Pre-flight passes but the headed browser lands on the login page, and the run ends with `infrastructure_error / REPORT_MISSING` after a 15 s wait for the first step. API calls with the minted service-account token return 200, but page loads with the same bearer token return `isSignedIn: false`. How is the browser meant to authenticate on a shared Cloud stack, and is there stack-level configuration docsteam needs?

## Signed-in browser check (Taylor signed in to the built-in browser; read-only, nothing changed)

- **Pathfinder works when signed in.** The Help button opens the "Interactive learning, help, and documentation" panel with suggested guides. So the plugin and panel are fine; the runner failure is about browser authentication only.
- **Contact points:** one contact point exists, named `empty`, with "No integrations configured", used by 1 notification policy. The default `grafana-default-email` does not exist. The guide's contact-point step highlights the first option in the list and does not name one, so `empty` is probably selectable. Whether the rule saves and fires with an empty contact point is untested.
- Alert rules: 0 (unchanged).

## Manual walkthrough of alerting-first-rule-lj in the signed-in browser (2026-10-30)

Taylor signed in to the built-in browser and asked me to walk the path by hand. Not an automated E2E run: the query was entered in Code mode (a builder shortcut), and my own typing mistakes in the editor cost time and are not guide defects. The goal was to check the guide against the stack's real state.

**Result: the rule was created and saved.** Every milestone could be completed on the seeded stack.

### Guide vs stack findings
| Milestone | Finding |
|---|---|
| 1. Install | `button[data-testid='install-quickpizza']` exists and works. Install refreshed to the QuickPizza dashboards folder, as the guide says. With dashboards removed and data sources left, the app shows a "removed all dashboards but data sources are still present" notice and a "Clean up datasources" button, plus Install Dashboards for Weather and QuickPizza. |
| 2. Navigate / name | `/alerting/new/alerting` and the name field work. |
| 3. Query | Data source `grafanacloud-play-prom` selects. The metric exists. The target query `sum(increase(quickpizza_server_http_requests_total{status=~"5.."}[5m]))` runs without error. **Result is "No data"**: QuickPizza series exist (159 in the last 30 days) but have **no samples in the last 5 minutes**, so the rule can never fire. The guide's wording about confirming the alert fires cannot be satisfied right now. |
| 4. Folder and labels | New folder `QuickPizza alerts` and label `severity=critical` work. |
| 5. Evaluation | **Guide defect on Grafana 13.3.0:** the guide fills `#evaluate-every-no-group`, which does not exist. The UI requires creating an evaluation group via "New evaluation group" (interval field is `#eval-every-input`). The guide has no step to create a group. Pending period (1m) and keep firing (0s) defaults match the guide. |
| 6. Contact point | The only option is `empty` (no integrations). The guide only highlights the first option, so it works. |
| 7. Save | Saved successfully. |

### Created on the shared stack (for cleanup decisions; nothing deleted)
- Demo dashboards folder reinstalled: "Grafana QuickPizza Demo Dashboards" (4 dashboards).
- Folder `QuickPizza alerts`.
- Evaluation group `quickpizza-1m` (1m interval) in that folder.
- Alert rule `QuickPizza server errors` (uid fg2t0qwbw5jwgb), label `severity=critical`, contact point `empty`.
- Earlier: 4 `grafanacloud-play-*` data sources (installed before this walkthrough, still present).

### Implication for E2E and seeding
- Seeding needed for this path: the Demo Data app (installed), a live QuickPizza feed if the alert must be able to fire, and a contact point (any).
- Reruns will collide: the folder `QuickPizza alerts` and the rule already exist. Cleanup or a reset is needed between runs.

## Why the QuickPizza metrics are stale (investigated 2026-10-30, read-only)

- `grafanacloud-play-prom` is not seeded data on our stack. It is a read-only data source created by the Demo Data Dashboards app that points at a Grafana-run shared backend (`prometheus-prod-10-prod-us-central-0.grafana.net`). Sibling sources `-play-logs`, `-play-traces`, `-play-profiles` point at other shared Grafana endpoints.
- `quickpizza_server_http_requests_total` has samples 31 to 90 days ago (about 60 to 90 series per sampled day) and **none in the last ~30 days**. The whole `quickpizza_*` family is gone, not only this metric (no live series match `quickpizza_*`). No `quickpizza*` spans in play-traces in the last hour.
- Other data on the same backend is live (`up`, `kube_pod_info`, span metrics, synthetic-monitoring logs), so the data source works. The QuickPizza demo app that feeds it appears to have stopped sending around 30 days ago.
- Cause is upstream and not visible from here. We cannot fix it from our stack: the data source is read-only and shared.
- **Impact beyond the test stack:** any learner who clicks Install gets the same stale demo data, so guides that depend on live QuickPizza data (the alerting paths, Explore, golden signals; 61 references across 8 paths) have the same issue for real users.
- Not blocking for E2E on this path: the guide only requires the rule to save, which works with no data.

## drilldown-metrics-lj manual walkthrough (2026-10-31, selector check; nothing saved)

Seeded with `scripts/seed-metrics.py` (Influx line protocol, 204 accepted). Signed-in built-in browser. Steps were checked against the live page; the final Save was not clicked to avoid writing to the shared stack.

| Milestone | Finding |
|---|---|
| 1. search-metrics | Data source variable resolves to `grafanacloud-prom` (display name `grafanacloud-docsteam-prom`). Label filter input exists. Nav menu item not checked (menu closed on that page). |
| 2. analyze-data | **Gap:** step 1 highlights `button[data-testid='select-action-asserts:resource:threshold']`; that metric does not exist on this stack. Influx ingestion rewrites colons to underscores (test write became `asserts_resource_threshold`), so it cannot be seeded this way; remote write would be needed. The metric is also Asserts-specific, so the guide would break for any learner without Asserts. Time picker, Breakdown and Related metrics tabs work on a seeded metric (`node_cpu_seconds_total`). |
| 3. open-metrics-explore | `button[title='Menu']` and `Panel menu item Explore` exist. Explore opens in a new browser tab (blocked in the built-in pane, a tooling limit, not a guide defect). |
| 4. add-metric-dashboard | Explore toolbar 4th button is `Add`; `Add to dashboard` menu item and `Open dashboard` button exist. Opens `/dashboard/new` (unsaved). |
| 5. Save | `button[data-testid='data-testid Save dashboard button']` exists. Not clicked. |

Side effect: one stray series `asserts_resource_threshold` written by the colon experiment (job="node"). Metrics cannot be deleted; it ages out.

## Recommender does not suggest alerting-first-rule-lj (2026-11-02)

On `https://docsteam.grafana.net/alerting/list` as a signed-in Admin, the Pathfinder panel's Suggested guides shows 1 item, the documentation page "Grafana Alerting"; the learning path is not suggested. Taylor can find the path by search, so it is published.

Checked and ruled out:
- Published manifest on origin/main targets `urlPrefix /alerting` AND `targetPlatform cloud` AND `userRoleIn [Editor, Admin]`. Taylor is Admin on a Cloud stack.
- Deploy workflow runs on main succeed; the newest main commit (1e6c8fbc, 2026-10-30) deployed to prod.
- The stack uses the production recommender (`recommender.grafana.com`): the dev recommender is chosen only for `*.grafana-dev.net` hosts.
- The plugin's custom guide repository is empty (`guides: []`), so suggestions come from the online recommender.
- The recommender call is not visible in the browser's network log, so the response could not be inspected.

Not determined: why the recommender omits the path. Open question for Pathfinder engineering (recommender index refresh lag, how it scores the manifest, or paths appearing somewhere other than Suggested guides). Cheap discriminating test: see whether another published path (for example drilldown-metrics-lj at `/a/grafana-metricsdrilldown-app/drilldown`) is suggested on its own page.
