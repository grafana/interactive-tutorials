# Seeding the shared test stack: process log

This file records how we seed `https://docsteam.grafana.net/` so that learning paths can be tested end to end. It is written step by step as the work happens. Each step says what we did, why, and what it allows.

Status: pilot. Three paths: `alerting-first-rule-lj`, `drilldown-metrics-lj`, `interactive-dashboards-lj`.

## Ground rules

- The stack is shared. Anything written to it is visible to everyone who uses it.
- We talk each step through before doing it. No changes to the stack without agreement.
- Read first, write second. We look at what exists before seeding anything.
- Seeding must be idempotent (safe to rerun), because the stack may be wiped on a schedule.
- Credentials never go in this repository, in chat, or in command output.

## Step 0: Access token

### What it is
A Grafana service account token for `docsteam.grafana.net`. A service account is a non-human identity inside Grafana. Its token lets scripts call the Grafana HTTP API with only the permissions the account's role grants.

### Why we need it
We want to inspect and later seed the stack through its API rather than by clicking through the UI. The API is faster and repeatable, and it leaves a record of exactly what was created. Without a token, every seeding step would be manual.

### What it lets us do
- **Read-only token (Viewer role), used first:** list data sources, dashboards, folders, alert rules, contact points and installed apps; run queries to check whether a metric exists. It cannot change anything.
- **Write token (Editor or Admin role), created later and only when we agree to seed:** create folders, dashboards and data sources, and enable apps. We will use a separate token so that discovery cannot modify the stack.

### What it does not let us do
- It does not give access to the Grafana Cloud portal (billing, stack settings, other stacks).
- A Viewer token cannot create or edit anything.

### How it is handled
- The token is created by a person with admin access to the stack and stored in `~/.config/grafana-docsteam.env` (outside the repo, permissions `600`).
- Commands load it from that file. The value is never printed or committed.
- Tokens are revoked when the pilot ends, or on the stack's reset schedule if the account does not survive a wipe.

### Setup steps (done by the stack admin)
1. In `docsteam.grafana.net`, open **Administration > Users and access > Service accounts**.
2. Create a service account named `pathfinder-seed-readonly` with the **Viewer** role.
3. Add a token with an expiry (7 days is enough for the pilot) and copy it once.
4. Save it locally without putting it in shell history:
   ```bash
   mkdir -p ~/.config && umask 077
   read -rs "GRAFANA_TOKEN?Paste token: " && echo
   printf 'GRAFANA_URL=https://docsteam.grafana.net\nGRAFANA_TOKEN=%s\n' "$GRAFANA_TOKEN" > ~/.config/grafana-docsteam.env
   unset GRAFANA_TOKEN
   ```
5. Verify, without printing the token:
   ```bash
   set -a; . ~/.config/grafana-docsteam.env; set +a
   curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $GRAFANA_TOKEN" "$GRAFANA_URL/api/org"
   ```
   `200` means the token works.

## Step 1: Read-only discovery (next)

Done. Results in [discovery.md](discovery.md). The default Prometheus data source is empty, which blocks all three pilot paths.


## Step 2: Install QuickPizza demo data (done)

Taylor clicked Install in the Demo Data Dashboards app (`/a/grafana-demodashboards-app`). Re-checked read-only: see the "After installing" section of [discovery.md](discovery.md). The only write to the stack so far.

## Step 3: Build the Pathfinder CLI (done)

Cloned grafana/grafana-pathfinder-app at 35a0e40 (v2.25.0 prep) into the session scratchpad. Installed with `npm ci --ignore-scripts` and built with `npm run build:cli`. No contact with the stack.

## Step 4: First E2E run, alerting-first-rule-lj

Dry run (no write flag): all 8 milestones skipped as unsafe on a shared stack, as designed. Real run with `--allow-cloud-instance-mutations docsteam.grafana.net`: milestone 1 (install-datasources) failed, 0 steps executed, remaining 7 skipped. Runner service account was created and deleted. See [findings](e2e-findings.md).

## Step 5: Manual walkthrough of alerting-first-rule-lj (done)

Signed-in built-in browser. Rule created. Details, guide defect and cleanup list in [e2e-findings.md](e2e-findings.md).

## Standing rule: clean up after every test run

**Frequent cleanup of the shared stack is imperative.** Learning paths create objects (folders, evaluation groups, alert rules, dashboards, data sources) that persist after a run. The next run of the same path then collides with them (duplicate folder names, a missing Install button), and different paths can interfere with each other. Observed on 2026-10-30: after one manual pass through `alerting-first-rule-lj`, a rerun would have collided with the `QuickPizza alerts` folder and the saved rule.

- Clean up after every run, not on a weekly schedule. Better still, reset the stack to a known baseline before each run.
- Delete only the objects the run created, identified by uid, and verify the stack state afterwards.
- Record what each path creates so cleanup can be scripted.

Cleanup performed 2026-10-30: deleted alert rule `QuickPizza server errors` and folder `QuickPizza alerts` (with its evaluation group), then used the Demo Data app's Remove to delete the QuickPizza dashboards. The four `grafanacloud-play-*` data sources were left in place. Verified read-only: 0 alert rules, no folders besides GrafanaCloud and Shared with me, 16 data sources, no leftover runner service accounts.

## Step 6: Seed the other two pilot paths (drilldown-metrics-lj done, see Step 7; interactive-dashboards-lj not started)

Paths: `drilldown-metrics-lj`, `interactive-dashboards-lj`. Both need data in the stack's own Prometheus (`grafanacloud-prom`, currently empty). The play data sources cannot substitute: the guides expect that data source name, and `up` there has no `environment` or `region` label.

Plan agreed with Taylor:
1. `scripts/seed-metrics.py` writes synthetic series (node_cpu_*, `up` with environment/cluster/region, http and memory/filesystem samples) using Influx line protocol. Dry run by default; `--send` writes. Written, dry run only so far; nothing sent.
2. Needs a new credential: a Grafana Cloud **access policy token with `metrics:write`**, created by Taylor in the Cloud portal (grafana.com), short expiry, saved to `~/.config/grafana-docsteam-metrics.env` with the hidden prompt. Not created yet.
3. Reseed immediately before every test run: samples only stay queryable for a short recent window.
4. Create one seed dashboard with a panel on `grafanacloud-prom` (admin token), and delete it in cleanup.

Done 2026-10-31: Taylor created Cloud access policy `pathfinder-seed-metrics-write` (scope `metrics:write` only; the form had no realm field) and a 7-day token, saved to `~/.config/grafana-docsteam-metrics.env`. `seed-metrics.py --send` wrote 2,520 lines in one chunk; the endpoint returned 204 (Influx line protocol accepted). Verified read-only on the data source with uid `grafanacloud-prom` (display name `grafanacloud-docsteam-prom`): `up{job="node"}` 6 series, `node_cpu_seconds_total` 48, `node_cpu_hourly_cost` 6, `node_cpu_online` 6; `environment` = development, production, staging; `region` = eu-west, us-east; 4 clusters. Not yet done: the seed dashboard (item 4). Cleanup at pilot end: delete the access policy and its token. Seeded metrics cannot be deleted and age out on their own.

Open items to carry into the summary:
- **Guide gap in `interactive-dashboards-lj`:** it starts at `/dashboards` but every step needs an Edit dashboard button, which only exists on a dashboard page. Seeding cannot fix this; pointing `startingLocation` at one seeded dashboard would bake in a stack-specific ID. Authors' decision, not yet raised.
- **New credential and reseed-before-each-run** requirements (items 2 and 3).
- Keep to the standing rule: clean up after every run.

## Step 7: drilldown-metrics-lj seeded and run through the real guide (done 2026-11-02)

Full detail for engineers: [drilldown-metrics-lj-notes.md](drilldown-metrics-lj-notes.md).

- Seeded Prometheus metrics with `scripts/seed-metrics.py` (Influx line protocol) and `scripts/seed-remote-write.py` (Prometheus remote write, for the colon-named `asserts:resource:threshold`). Both use one Cloud access policy token with `metrics:write`. Influx rewrites colons to underscores; remote write keeps them.
- Ran the guide in the Pathfinder panel with Show me / Do it. Milestones 1, 2 and 4 pass; 3 passes except that Explore opens in a new tab the built-in browser pane blocks; 5 not run. Nothing saved to the stack (Save dialog cancelled), so no cleanup was needed.
- **The path passes but has issues that should be addressed** (Asserts-only metric in milestone 2, a highlight step that leaves later steps blocked, a probable metric-name typo, nav-menu requirement): listed in [drilldown-metrics-lj-notes.md](drilldown-metrics-lj-notes.md#issues-to-address-drilldown-metrics-lj-passes-end-to-end-but-these-should-be-looked-at).
- Why this path needed seeding and alerting-first-rule-lj did not: its "Before you begin" declares metrics sent to Grafana Cloud, and the stack's `grafanacloud-prom` held none. Alerting declares only an account and permissions.

## Carry into the final summary

- **Frequent cleanup of the shared stack is imperative** (standing rule above).
- **Reseed before every run:** samples are only queryable for a short recent window. Run both seed scripts right before a test.
- **Credentials to revoke at pilot end:** Cloud access policy `pathfinder-seed-metrics-write` and its token; read-only and admin service account tokens; the token pasted in chat early on.
- **Guide gaps for authors:** `alerting-first-rule-lj` fills `#evaluate-every-no-group`, which does not exist on Grafana 13.3.0 (needs an evaluation-group step); `interactive-dashboards-lj` starts at `/dashboards` but needs a dashboard page; `drilldown-metrics-lj` milestone 2 depends on the Asserts-only metric `asserts:resource:threshold`.
- **Upstream:** QuickPizza demo data feeding `grafanacloud-play-prom` stopped about 30 days before 2026-10-30.
- **Pathfinder questions:** the automated E2E runner's browser lands on the login page on this stack (bearer token works for API, not page loads); the recommender suggests drilldown-metrics-lj on its page but did not suggest alerting-first-rule-lj on `/alerting`.
- **Not started:** `interactive-dashboards-lj`; stakeholder buy-in on exempting the external-infrastructure paths; writer review of the AI inventory.
