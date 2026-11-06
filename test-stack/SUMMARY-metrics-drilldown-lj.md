# Seeding a shared test stack for learning paths: pilot summary for engineering

Written 2026-11-02. Covers the work on grafana/interactive-tutorials#666 ("Populate the test stack with prerequisites and data for all learning paths", part of #665) with `drilldown-metrics-lj` as the main worked example. Everything here is from the pilot's own logs. Nothing is committed: all files are untracked in `test-stack/`.

Detailed logs: [PROCESS.md](PROCESS.md) (step-by-step), [drilldown-metrics-lj-notes.md](drilldown-metrics-lj-notes.md) (path-level notes), [e2e-findings.md](e2e-findings.md) (automated runner findings), [discovery.md](discovery.md) (stack discovery), [audit.md](audit.md) (path audit), [inventory-summary.md](inventory-summary.md) (AI-generated needs).

## 1. Summary

- **Goal:** find out whether a pre-seeded shared Grafana Cloud stack (`docsteam.grafana.net`, Grafana 13.3.0, Pathfinder plugin 2.25.0) can support end-to-end testing of docs learning paths.
- **Constraints:** no budget, and we cannot host external infrastructure (databases, VMs, collectors). The pre-seeded stack is all there is.
- **Result:** `drilldown-metrics-lj` runs end to end on the seeded stack. Seeding is two scripts run immediately before a test. The path passes, but has guide issues worth fixing (section 8).
- **What worked:** seeding Prometheus metrics (Influx line protocol and Prometheus remote write), running the real guide in the Pathfinder panel, and cleaning up per run.
- **What did not work:** the Pathfinder CLI's automated E2E runner could not authenticate its browser on this stack, so all path testing so far was manual or semi-manual.
- **Biggest open questions for engineering:** runner browser auth on a Cloud stack; how to reset state between runs on a shared stack.

## 2. Context and scope

- **Population:** 75 packages with `type: path` on `origin/main` at 6a8356f6 (65 `-lj`, 10 `-lp`). The proposal's scope was multi-milestone paths (the `-lj` family).
- **Audit result** ([audit.md](audit.md)): 33 testable on the seeded stack alone, 41 need something hosted or supplied externally, 1 unclear (`git-sync-use-lp`). `connect-agent-to-agent-observability-lj` is on a branch only and was excluded.
- **How the audit was made:** AI agents read each path's manifest and content and produced a per-path needs list (`inventory/*.json`, 65 files; 64 of 75 read in depth, the other 11 judged from their "Before you begin" text). **Nothing is verified against the stack or reviewed by a writer.** "Testable" means the stated needs look satisfiable with Cloud configuration and data, not that a test passed.
- **External-infrastructure paths:** the inventory groups them as hosted systems (databases, services), third-party or secret-bearing, CLI or local tools, collector fleets, and public endpoints. The recommendation is to exempt those paths from stack testing, pending stakeholder buy-in. That proposal is written up in the Google proposal doc and is not yet agreed.
- **The Google doc numbers are slightly out of date** against the audit (about 30 testable and 35 exempt, versus 33 and 41 including `-lp`).

## 3. Why we chose `drilldown-metrics-lj`

`drilldown-metrics-lj` is the worked example of the pilot, which was meant to use paths that are not too hard but representative.

`drilldown-metrics-lj` was chosen because it clearly needs seeded data and nothing outside the stack:
- Its "Before you begin" declares "Prometheus metrics sent to Grafana Cloud", a data requirement, not just an account.
- The stack's default data source (`grafanacloud-prom`) existed but held no metric data at all.
- The only gap was metrics data, which a script can write. It needs no external infrastructure.
- It has a sibling family (`drilldown-logs-lj`, `drilldown-traces-lj`, `drilldown-profiles-lj`) so the method can be reused. Many other paths in the audit also depend on seeded data.

## 4. Stack baseline and what the path needs

Needs from the AI inventory (unreviewed): a Prometheus-compatible data source (guide selects `grafanacloud-prom`), several metrics with related prefixes and labels in it, and `grafana-metricsdrilldown-app` enabled.

Baseline findings (read-only discovery, [discovery.md](discovery.md)):
- The data source's display name is `grafanacloud-docsteam-prom`, its **uid is `grafanacloud-prom`**. Guides use the uid-style name. Use the uid in API calls.
- It was empty. The Metrics Drilldown app was installed and enabled.
- Other data sources on the stack are not a substitute: the guide selects `grafanacloud-prom`.
- The manifest for this path declares only `testEnvironment: {tier: cloud}` and no `prerequisites`. The real needs exist only in prose and in the guide's selectors. **If `testEnvironment.datasources` or similar fields were filled in, tooling could read the needs instead of an AI inferring them.**

## 5. What was built to seed

All scripts are stdlib-only Python, dry run by default, and never print credentials.

| Script | What it does |
|---|---|
| `scripts/seed-metrics.py` | Writes synthetic series in Influx line protocol to the stack's Grafana Cloud Prometheus. `--send` writes; otherwise prints a dry run. |
| `scripts/seed-remote-write.py` | Writes series whose names contain colons, using Prometheus remote write. |
| `scripts/extract-dossiers.py` | Builds per-path evidence files (`dossiers/`) from manifests and content, input to the AI inventory. |

**Series seeded** (about 124 series, 30 s resolution, last 10 minutes written per run): `up`, `node_cpu_online`, `node_cpu_hourly_cost`, `node_cpu_seconds_total`, `node_cpu_guest_seconds_total`, `node_cpu_usage_seconds_total`, `http_requests_total`, `node_memory_MemAvailable_bytes`, `node_filesystem_avail_bytes`. Six instances in four environment/cluster/region groups (production, staging, development). Counters are monotonic (an early version let them decrease; fixed). Remote write adds 4 series of `asserts:resource:threshold`.

**Why two scripts:** Grafana Cloud's Influx endpoint turns colons in metric names into underscores (a test of `asserts:resource:threshold` arrived as `asserts_resource_threshold`). The guide's milestone 2 highlights the button for the colon name, so remote write was needed. The remote-write script hand-encodes the protobuf `WriteRequest` and uses snappy literal blocks (valid snappy without compression) to avoid dependencies. Endpoint: the stack's `/api/prom/push`, Basic auth, headers `Content-Encoding: snappy`, `Content-Type: application/x-protobuf`, `X-Prometheus-Remote-Write-Version: 0.1.0`. The server returned 200. Influx path: the stack's `/api/v1/push/influx/write`, returned 204.

**Credentials (all outside the repo, in `~/.config/`):**
- Read-only Viewer service account token, for discovery and verification queries.
- Admin service account token, 7-day expiry, for runner attempts and for deleting objects after runs.
- A Grafana Cloud **access policy token with only `metrics:write`**, 7-day expiry, used by both seed scripts. The policy form in the portal had no realm field, so the policy may not be pinned to this stack. The Prometheus instance id used as the username is not a secret.

**Verification after writing** (read-only token, query through the data source proxy): `up{job="node"}` 6 series, `node_cpu_seconds_total` 48, `node_cpu_hourly_cost` 6, `asserts:resource:threshold` 4; label values include `environment` = development/production/staging.

**Limits:** metrics cannot be deleted (they age out), and samples are only queryable for a short recent window, so **both scripts must run immediately before each test**.

## 6. How I tested

1. **Automated E2E runner (failed, infrastructure).** Built the Pathfinder CLI (v2.25.0 from commit 35a0e40) and ran `e2e` against the stack in shared-stack mode with mutations allowed. Four runs against the stack all failed with `infrastructure_error / REPORT_MISSING` after a 15 s wait for the first step. Cause: the runner adds a bearer token to requests, and on this stack API calls accept it but **page loads are treated as signed out** (`isSignedIn: false`), so the browser lands on the login page and the guide panel never opens. Not known: whether this is stack configuration, a Cloud edge behaviour, or the runner's expected auth mechanism. A question for Pathfinder engineering is drafted in [e2e-findings.md](e2e-findings.md) but **has not been sent**. My first diagnosis was wrong; the real error was in the report's `errorCode`, which I had not read.
2. **Selector check.** In a signed-in browser, the manifest selectors for milestones 1 to 5 were checked against the live page.
3. **In-panel run.** The real guide was started from the Pathfinder panel (suggested on the Drilldown page) and driven with each step's Show me / Do it. Reseeded first with both scripts.

Results:

| Milestone | Result |
|---|---|
| 1. Search and filter metrics | Pass. Step 1 needs the nav menu docked; the guide's "Fix this" button handled it. |
| 2. Investigate the data | Pass, including the `asserts:resource:threshold` step (needed the remote-write seed). Steps 5 and 6 need a metric selected first (section 8). |
| 3. Open in Explore | Partial. The two-part Menu then Explore step ran and showed Completed, but Explore opens in a new tab, which the built-in browser pane blocks for automation, so the opened page was not seen. Explore was verified separately by loading the same query by URL. Tooling limit, not a guide defect. |
| 4. Add to dashboard | Pass. Opened an unsaved dashboard and the Save dialog. I cancelled the dialog, so nothing was written. |
| 5. End journey | Not run (closing text). |

## 7. How Taylor tested manually

After a fresh reseed, Taylor went through the whole path end to end in their own browser. That run saved one dashboard (`New dashboard`, uid `tang567`, one panel on `asserts:resource:threshold`). I confirmed it came from that run (created that day, General folder), deleted it by uid with the admin token, and verified the lookup returns 404, with 0 alert rules, only the `GrafanaCloud` folder, and 16 data sources left. Stock Cloud dashboards were untouched.

Conclusion: with two reseed commands and no other setup, the path can be completed end to end. Per-run cleanup is one dashboard if the learner saves.

## 8. Shortcomings and issues found

### Guide issues in `drilldown-metrics-lj` (for authors; the path passes but these should be addressed)
1. **Milestone 2 step 2 depends on an Asserts-only metric (medium).** It highlights the Select button for `asserts:resource:threshold`, which exists only on stacks with Asserts. On any other stack the step's `exists-reftarget` is never met and a learner cannot complete it. We only passed it by seeding that metric. Suggest a metric every Prometheus stack has, or a conditional step.
2. **That step only highlights, so later steps are blocked (medium).** Steps 5 and 6 (Breakdown, Related metrics) show "The target element must be visible and available on the page" until a metric is actually selected. Learners who follow the text will click Select; anyone using the buttons, and any automated run, gets stuck. Suggest a click action.
3. **Probable metric-name typo (low).** The milestone 2 prose says `node_cpu_guest_seconds`; the node exporter metric ends in `_total`. Seen in panel text only, not checked in the source.
4. **Milestone 1 step 1 needs the nav menu docked (low).** "Fix this" resolves it, but a first-time learner sees a failed requirement first.

### Seeding and environment limitations
- Metrics cannot be deleted and are only queryable for a short window, so the stack never holds a stable state; seeding must be rerun every time.
- Pathfinder progress is saved per user (milestones show complete, a "Badge unlocked" popup appears). A rerun starts partway through unless the progress is reset by hand.
- The built-in browser pane cannot follow actions that open new tabs (Explore), so those steps need a person.
- The seeded data is synthetic. It matches the guides' names and labels, but guides that say what the data "shows" were not read for that.

### Process gaps
- The AI inventory is unreviewed; 52 of 65 entries carry a "needs human review" flag.
- The runner question and the authors' defect reports have not been sent.

## 9. Lessons for building a test environment for learning paths

1. **Separate declared needs from real needs.** The drilldown path declares metrics in its "Before you begin", and the stack held none; that is easy to miss when needs live only in prose. Fill in `testEnvironment` fields so tooling can read needs; do not rely on AI inference.
2. **State collides across runs.** Saved objects persist (here, a dashboard saved at the end of the run). A rerun, or a different path, can collide with leftovers. **Clean up after every run and delete only what the run created, by uid.** Prefer a reset-to-baseline step before each run. Record what each path creates.
3. **Seeding must be idempotent and time-aware.** Anything time-series needs reseeding right before a test. A scheduler or a pre-run hook should do it, not a person.
4. **Data presence and selectors are the usual failure.** `exists-reftarget` steps fail when the data behind them is missing; a seeded stack needs the exact metric, label and data source names the guide uses (check both the display name and the uid).
5. **Some data cannot be seeded the obvious way.** Influx ingestion rewrites names; remote write is more faithful. Plan for both, and check names on the stack after writing.
6. **Credentials.** Use separate, short-lived, least-privilege tokens for discovery (read-only), seeding (`metrics:write` only), and cleanup (admin). Store them outside the repo and load them from files. A token was once pasted into chat during setup; avoid that, and revoke it.
7. **Run guides the way a learner does.** Starting the real guide in the Pathfinder panel found things selector checks missed (the blocked steps, the nav-menu requirement, progress persistence).
8. **Tooling constraints matter.** The runner's browser auth on Cloud is the main blocker to automation here. New-tab actions need a person or a different browser harness.
9. **Verify with a read-only token after every write.** It is cheap and catches rewritten names and empty series.

## 10. How to reproduce the drilldown run

1. Create a Cloud access policy with scope `metrics:write` only (7-day token) and save `METRICS_USER` (the Prometheus instance id) and `METRICS_TOKEN` to `~/.config/grafana-docsteam-metrics.env`.
2. `python3 test-stack/scripts/seed-metrics.py --send` then `python3 test-stack/scripts/seed-remote-write.py --send` (both dry-run without `--send`).
3. Verify `up{job="node"}`, `node_cpu_seconds_total` and `asserts:resource:threshold` return series through the `grafanacloud-prom` data source.
4. In a signed-in browser, open `/a/grafana-metricsdrilldown-app/drilldown`, open the Help panel, start "Explore data using Metrics Drilldown", reset any saved progress first.
5. After the run, delete any saved dashboard by uid and verify the stack.

## 11. Open items and suggested next steps

- Send the runner-authentication question to Pathfinder engineering and decide how E2E should authenticate on a shared Cloud stack.
- Raise the drilldown issues in section 8 with the guide authors.
- Decide on the exemption of the external-infrastructure paths; get stakeholder buy-in and a writer review of the AI inventory.
- Next pilot candidates: `drilldown-logs-lj` (tests a second data type through the same scheme with a `logs:write` credential) or `visualization-metrics-lj` (reuses the metrics already seeded). Not started.
- Decide how to reset Pathfinder progress and shared-stack state between runs, and how often.
- At the end of the pilot, revoke the metrics access policy and token, and the read-only and admin service account tokens.

## 12. File index

Docs: `PROCESS.md`, `drilldown-metrics-lj-notes.md`, `e2e-findings.md`, `discovery.md`, `audit.md`, `inventory-summary.md`, this file. Data: `dossiers/` (66), `inventory/` (65). Scripts: `scripts/extract-dossiers.py`, `scripts/seed-metrics.py`, `scripts/seed-remote-write.py`. Outside the repo: the Google proposal doc, and credential files in `~/.config/`.
