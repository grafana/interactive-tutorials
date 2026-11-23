# Catalog targeting audit — 20 October 2026

This change recommends learning paths as single units and matches lessons to product discovery pages and the current Grafana task. It contains no guide-ID boosts, curated defaults, ordering list, telemetry changes or Pathfinder UI changes. It is independent of Pathfinder PR #2184.

## Scope and evidence

The baseline is tutorials main `ae282c99d260664c78b1fb703e678fe5098c814f`.

| Inventory | Count | Disposition |
|---|---:|---|
| Learning paths | 74 | 73 recommendable; alerting-with-Terraform remains direct-only |
| Standalone guides/tours | 97 | 89 recommendable; 8 explicitly direct-only |
| Path modules/supporting lessons | 554 | Never independently recommendable |
| Total packages | 725 | Every package manifest and content file inventoried |

The 554 includes 483 declared milestone members and 71 additional lessons physically nested under paths. Foundations use `milestones`; the current schema additionally supports `tracks[].guides`. The traversal unions both and supports shared membership; this baseline has no tracks or shared members. The three nested Grafana Play tours are standalone guides under a collection cover, not path modules. The extra `shared/snippets/case-for-o11y/content.json` is reusable snippet content, not an independently recommendable package; it is validated with the shared catalog. No package in this baseline is explicitly marked archived; untargeted demos/supporting lessons are retained with explicit dispositions, not deleted.

- [Candidate review by product area](candidates.md): review the 171 paths and standalone items without wading through module counts.
- [Complete inventory](inventory.json): source paths and content hashes, task excerpts/sections, page requirements, parent graph, launch location, product category, dependencies and before/after rules for all 725 packages. Hashes establish which content was audited; this is a targeting review, not a full execution audit of every guide.
- [Decisions](decisions.json): explicit changes and deferred cases; remaining rules retain their product/demo context.
- [Scenarios](scenarios.json): fixed positive and negative expectations, plus the cross-product matrix. These are synthetic contexts without user data.
- [Results](results.json): ordered real-server results, evidence metadata and accuracy before/after, at caps 3, 10 and 10000.
- [Validation](validation.json): pinned CLI validation and reproducible generation.

## Main changes

**Connections:** remove generic catalog exposure for backend-specific paths. Configure data sources on their backend-specific catalog detail route, or on `/connections/datasources/edit/` with the observed backend type, using the actual plugin IDs for PostgreSQL and ClickHouse. Standard Admin eligibility reflects data-source creation permissions. Integration paths use their own setup tiles. Remote write, PDC, host integrations and OTLP setup no longer compete indiscriminately on every connection page.

**Dashboards:** panel authoring requires dashboard creation or observed editing. Visualization paths use the selected backend instead of requiring a panel choice on the dashboard listing. In particular, logs aggregation can produce a time series: a `panel-type:logs` requirement was not justified. Visualization-specific labs require an observed panel choice, including on new dashboards. Viewing an existing dashboard no longer recommends editing transformations, saved queries or conditional display rules.

**Explore:** DPM requires an observed Prometheus selection, Elasticsearch querying requires Elasticsearch, and the demo trace path requires Tempo and its original demo-host restriction. Generic Explore tours remain available without a selection. Installed Prometheus/Loki alone never establishes the active query task.

**Product pages:** retain workflow targeting and add deliberate discovery on the relevant product entry pages. Cardinality and usage alerts also appear on billing/Usage; IRM and SLO appear on Alerts & IRM; Home offers platform orientation and administrator onboarding. Keep broad product-equivalent peers when no trustworthy signal distinguishes them; do not manufacture intent.

**Modules:** remove recommendation targeting from all six previously targeted k6 modules/supporting lessons. Their IDs, content, launch locations and path membership are unchanged. Confirmed downstream lessons move from `recommends` to `suggests`, so the ranker does not mistake further learning for prerequisites. Genuine prerequisites remain, and two stale dependency IDs are corrected. No content file or frozen `index.json` changes.

## Before / after

Counts below are package eligibility before the server cap, on Cloud as Admin. Installed Prometheus and Loki are present in both contexts except the panel example, which explicitly observes Loki and Stat while editing.

| Context | Before | After | Outcome |
|---|---:|---:|---|
| Home | 3 | 3 | Explicit orientation/onboarding rules; partial AND leakage remains removed |
| Dashboards listing | 9 | 4 | Playlist discovery restored; UI/SDK/Terraform distinction remains unresolved |
| Existing dashboard view | 8 | 1 | Snapshot sharing remains; edit-only lessons excluded |
| Explore, no observed selection | 9 | 3 | General Explore tours only |
| Explore, selected Loki | 9 | 3 | Prometheus DPM and backend setup no longer leak in |
| Connection catalog | 17 | 3 | Connect existing data, instrument an application, or monitor a host |
| k6 | 12 | 9 | Partial leakage removed; methodology ties remain |
| Edit panel, observed Stat + Loki | 9 | 9 | Stat lab and logs visualization outrank route-only candidates |

The full matrix covers Cloud/OSS, Viewer/Editor/Admin, empty contexts, unrelated routes, home, listings, new/existing dashboards, no-selection Explore, selected backends, connection setup/configuration, alerting and every product represented by a recommendable path. Each candidate has a positive case and unrelated-route rejection. Task-, role-, platform- and source-constrained alternatives also have missing/wrong-evidence rejection cases. All 1,247 contexts are evaluated before and after at all three caps.

## Product discovery follow-up

The initial audit over-weighted the active workflow: users should not have to discover a feature before its introduction can be recommended. Twenty candidate manifests now add exact entry-page alternatives. These alternatives are normal route evidence, without ID boosts, default lists, installed-backend assumptions or fabricated edit signals. Existing deeper workflow matches remain. Home onboarding requires Admin; playlist discovery requires Editor or Admin; Cloud-only discovery keeps its platform gate. Modules and demo-host restrictions remain excluded from this widening.

Signed-in Chrome inspection on 20 October confirmed the current navigation destinations and the content of Home, Connections, Drilldown, Observability, Alerts & IRM, billing/Usage and Adaptive Telemetry. The AI entry link was verified in navigation. Observability specifically presents Knowledge Graph/RCA and Kubernetes/application monitoring. A Learn-only Knowledge Graph tour was retained unchanged; the general RCA path provides discovery instead.

| Entry page | Discovery opportunity | Eligible on Cloud as Admin, without observed task/data |
|---|---|---:|
| Home `/` | Concepts, Cloud capabilities, account setup | 3 |
| Dashboards | Create dashboards; discover playlists | 4 |
| Connections | Connect data, instrument applications, monitor hosts, existing infrastructure introduction | 4 |
| Add new connection | Choose between connecting data, application telemetry and host monitoring | 3 |
| Data sources | Discover private connectivity alongside connection setup | 2 |
| Drilldown | Overview plus metrics/logs/traces/profiles learning paths | 5 |
| Observability | Kubernetes tour, application instrumentation, RCA investigation | 3 |
| Alerts & IRM | Alerting, SLOs and incident response | 3 |
| Adaptive Telemetry | Logs and metrics optimization | 2 |
| Cost Management / Usage | Understand billing, investigate cardinality, set usage alerts | 3 |
| AI | Assistant onboarding | 1 |

The 140 added scenarios cover entry pages, trailing slashes, unrelated routes, arbitrary descendants and similarly named neighbors, plus platform/role rejection where applicable. Each discovery positive is also asserted at cap 10. Exact entry matching avoids exposing these introductions on all nested workflows. The existing catalog task-negative cases still pass. No user tenure, empty-state or available-telemetry signal is inferred; guide prerequisites still apply.

Server caps remain a visibility limit: cap 3 omits playlists behind existing dashboard-authoring candidates, and omits profiles/traces behind the Drilldown overview/logs/metrics peers. All fit at cap 10. The audit records this honestly rather than adding editorial boosts. Testing & synthetics already offers overview, first-check and test-builder discovery, so its rules did not need widening. Existing Admin/Terraform discovery also remains; demo-only guides and backend-specific setup are not promoted to unrelated product hubs. No suitable general guide was established for Bookmarks, Notebooks, Workflows, Pages or Machine learning, so no speculative cross-product rules were added there.

## Engine contract and reproducibility

The harness imports no replacement matcher or ranker. It copies a small test adapter into a disposable archive of these exact revisions and invokes the actual code:

- Recommender `b9adce44e8474441223c80d22ffcc92e6d465a55`: `V1RecommendationsHandler`, `EvalWithCriteria`, relevance v1 and server ranking/capping. Existing internal recommender tests and server relevance/prerequisite tests run alongside the catalog matrix.
- Pathfinder `37a9e12aa19ac269812242ddfba8b0d54ffa0a30`: real client ranking, legacy response handling, fail-closed local matching and context event bus tests. Catalog responses are also ranked with and without completion.
- Validation CLI `8262a2562c41c8a0a626a6f9e7d7f2405e4a31db`: the revision pinned by this repository's CI.

The ranking revisions are the open heads of [recommender #283](https://github.com/grafana/grafana-recommender/pull/283) and [Pathfinder #2205](https://github.com/grafana/grafana-pathfinder-app/pull/2205), checked on 20 October 2026. These are local source-level results, not evidence that the ranking revisions are deployed. Live Chrome checks confirmed actual routes; they did not replace the deployed catalog or prove live ranking of this branch.

```sh
python3 scripts/lint-targeting.py
python3 scripts/targeting-audit/run.py --recommender /path/to/grafana-recommender
python3 scripts/targeting-audit/run-client.py /path/to/grafana-pathfinder-app
python3 scripts/targeting-audit/validate.py /path/to/grafana-pathfinder-app
```

The source repositories must contain the pinned revisions. Client/CLI runs reuse the supplied checkout's installed Node dependencies; the archived source itself is pinned. The server uses its archived Go lockfile. Runners leave external repositories unchanged. Inventory, candidate review and results are regenerated from fixed scenarios and the baseline; `decisions.json` and `scenarios.json` are reviewable audit inputs, not runtime policy.

The server matrix proves rejection of partially satisfied required conditions through complete AND alternatives wrapped in a top-level OR. Existing server golden tests establish route/task evidence ahead of installed environment, strongest satisfied OR branch, category deduplication and unchanged literal-prefix semantics. The capped handler tests exercise competing paths and prerequisite ordering. Client tests cover completed/incomplete peers, old responses without ranking metadata and rejection of rich predicates offline. Context event bus tests exercise panel change, navigation away/return and expiry; matrix snapshots test the resulting cleared/observed contexts. The audit introduces no new context emitter.

Stats, repository index, dependency graph and manifest schema are generated into disposable trees. Two independent generations must agree after removing only `generatedAt`. They are not committed because the repository treats these as deployment artifacts. The legacy index remains byte-identical.

## Validation result

- Targeting lint: 162 manifests, no findings.
- Actual server handler: 1,247 before/after scenarios at caps 3, 10 and 10000; all expectations and cap-prefix comparisons passed. Internal engine and server ranking regression tests passed.
- Client: 3 suites / 34 tests passed, including catalog completion/offline checks and the existing ranking/observation tests.
- CI-pinned CLI: 726 content files and 725 packages passed; shared snippets validated. Two independently generated stats/index/graph/schema trees agree.
- Dependency graph: zero errors, 76 warnings (mostly orphaned content, plus existing unresolved `suggests` references such as `send-traces-alloy-lj` and the module reference `data-transformation-lj`). These do not create independent recommendation eligibility. They remain explicit catalog cleanup work, not a clean-graph claim.
- `git diff --check` passed. No `content.json` or frozen `index.json` changes.

## Remaining context gaps

1. **Dashboard authoring method:** `/dashboards` cannot distinguish UI creation, Foundation SDK generation or Terraform deployment. The three candidates remain eligible; no promise is made that the beginner guide wins every peer tie. Their launch location is not task evidence. The untargeted Terraform alerting path stays direct-only rather than gaining a guessed signal.
2. **k6 methodology and collector/database tasks:** product routes do not distinguish baseline, stress, soak, spike or CI authoring, nor database engine selection within DB Observability or all Fleet Management intents. Genuine prerequisite metadata is preserved. Cap 3 intentionally demonstrates some eligible peers being omitted; cap 10 currently fits the nine k6 candidates. This is not an editorial preference solution.
3. **Permissions:** standard roles are a coarse eligibility proxy. Custom RBAC, per-resource permissions, existing resources, actual data availability and external-system access are not available context signals. The guides retain their own requirements. Viewer exclusion is tested where role conditions are authored; it does not prove authorization to perform every guide action.
4. **Observation availability:** an edit-page backend guide appears only after Pathfinder actually observes its type; the specific catalog detail page supplies route intent before that. No installed-data-source fallback or UID/name inference is added. Default Time series rendering is not an observed choice. Rich rules are unavailable to the existing offline matcher; this intentionally fails closed rather than widening OSS fallback eligibility.
5. **Demo prerequisites:** LogQL's named nginx dataset, Cube's particular schema, kiosk content and scripted RCA demos remain direct-only. The existing adaptive-logs standalone walkthrough remains untargeted pending content validation. A generic installed capability cannot establish these prerequisites.
6. **Route aliases and prefix boundaries:** literal prefixes retain their existing starts-with semantics. Neighboring-route tests show that `/explore-extra` and `/dashboards-extra` still match their literal prefixes; these are inherited boundary limitations. Other-backend and unrelated-app neighbors are rejected. Existing product aliases/demo routes are not all available on the development stack. Catalog tile links, dashboard/Explore routes, product navigation and billing/cardinality/usage-alert routes were inspected in signed-in Chrome on `pathfinder.grafana-dev.net`. Retained aliases require release-specific live checks; this audit does not claim every guide was walked live.
7. **Dependencies:** the ranking contract treats `depends`/`recommends` as prerequisites among equally relevant peers. Confirmed further-learning edges were moved to `suggests`; prerequisite edges and module sequencing were retained. No new learning order is invented. The complete dependency metadata is recorded per item; custom RBAC and missing task observations still limit ordering.
