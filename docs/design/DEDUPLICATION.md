# Recommendation Deduplication

## Background

We are underway with a package migration plan; read [MIGRATION.md](MIGRATION.md) for critical context.

## Problem

After package migration completes, every learning journey will have **two independent sources of recommendation rules** that overlap:

1. **Static recommender rules** — JSON files in `grafana-recommender/internal/configs/state_recommendations/*.json` containing `"type": "learning-journey"` entries. These are the current production recommendation source. Each rule has a `match` expression (URL prefix, platform, etc.) and a `url` pointing to `https://grafana.com/docs/learning-journeys/<slug>/` or `https://grafana.com/docs/learning-paths/<slug>/`.

2. **Package manifest targeting** — `targeting.match` in each `manifest.json` within `interactive-tutorials`. During migration, these match expressions are *derived from* the recommender rules (the migration skill copies them verbatim). When the Pathfinder system consumes `repository.json`, it evaluates these match expressions to make contextual recommendations.

The recommender's `/api/v1/recommend` endpoint already consumes package repositories and evaluates manifest targeting alongside its static rules. A dev deployment is already serving both sources, which is how the duplication was discovered: users in a matching context receive the same learning journey recommended twice — once from the static rules and once from the package targeting.

## Scale of the overlap

Current state of the recommender's static learning-journey rules:

- **61 total rule entries** across 10 JSON files
- **36 unique URLs** (some journeys appear in multiple files with different match contexts)
- All 36 URLs point to pages on `grafana.com/docs/learning-journeys/` or `grafana.com/docs/learning-paths/`

(THIS SHOULD BE RE-VERIFIED PRIOR TO ANY DE-DUPLICATION WORK, AS NEW ITEMS COME IN ALL THE TIME)

Current state of the `interactive-tutorials` repo:

- **19 learning journey directories** (`*-lj/`)
- **22 standalone guides** with `manifest.json` (some already migrated)
- Standalone guides also have targeting in `index.json` (22 rules), which will move into manifests

(THIS SHOULD BE RE-VERIFIED PRIOR TO ANY DE-DUPLICATION WORK, AS NEW ITEMS COME IN ALL THE TIME)

After full migration, every one of the unique recommender LJ URLs will have a corresponding package manifest with an equivalent `targeting.match`. The `index.json` standalone-guide rules (22 entries) will similarly be duplicated by manifest targeting.

## Why the duplication exists

The duplication is structural, not accidental:

- The **recommender** was built first. Docs partners added static rules to `state_recommendations/*.json` to wire learning journeys and docs pages to specific URL contexts within Grafana.
- The **package system** was designed later. It puts targeting into `manifest.json` alongside the content, so each package is self-describing. The migration skill deliberately copies recommender match expressions into manifests to preserve the same routing behavior.
- During migration, both systems coexist by design (the [MIGRATION.md](MIGRATION.md) "Coexistence" strategy). The recommender's v1 endpoint already merges both sources, so the duplication is a live problem in the dev environment and will be a production problem as soon as packages are deployed.

## What needs deduplication

### Learning journeys (primary concern)

Every `"type": "learning-journey"` rule in the recommender's static JSON files has (or will have) a corresponding `manifest.json` with equivalent targeting. These are the bulk of the problem: 61 rule entries across 10 files.

### Standalone interactive guides (secondary concern)

The 22 rules in `index.json` are the current targeting source for standalone guides. After migration, each guide's `manifest.json` carries its own `targeting.match` (copied from the `index.json` rule). Once the Pathfinder system is the sole recommendation source, `index.json` becomes redundant for targeting purposes (though it may still be needed for other consumers like the CDN publication pipeline).

## Proposed approach: migrate-then-deduplicate

### Phase 1: Complete all package migrations (current work)

Migrate all remaining guides and learning journeys to the package format. Each manifest gets its `targeting.match` derived from the recommender rules (for LJs) or `index.json` (for standalone guides). Both the old and new targeting sources coexist.

No changes to the recommender repo during this phase.

### Phase 2: Validate equivalence

Before removing anything, verify that the package targeting covers the same ground as the static rules:

1. **Build `repository.json`** from all migrated packages.
2. **Extract all match expressions** from `repository.json` entries.
3. **Compare against recommender rules**: For each `"type": "learning-journey"` rule in the recommender, confirm there is a package in `repository.json` with an equivalent match expression and the same (or better) URL routing.
4. **Compare against `index.json`**: For each `"type": "interactive"` rule, confirm the corresponding manifest carries equivalent targeting.
5. **Flag gaps**: Any recommender rule with no corresponding package targeting is a gap that must be resolved before deduplication.

This could be a script that reads both sources and produces a coverage report. It would be a natural extension of the recommender's existing `cmd/coverage-report` tool.

### Phase 3: Deduplicate the recommender (PR to grafana-recommender)

Submit a PR to `grafana-recommender` that removes all `"type": "learning-journey"` rule entries from `state_recommendations/*.json` that are now covered by package manifest targeting.

**What gets removed:**
- All `"type": "learning-journey"` entries in `state_recommendations/*.json` where a matching package exists in `repository.json` with equivalent targeting.

**What stays:**
- All `"type": "docs-page"` entries — these point to documentation pages, not interactive content. They are not migrated.
- Any `"type": "learning-journey"` entries where the equivalence check found a gap (these need investigation, not blind removal).
- Any rules that serve a purpose beyond Pathfinder's scope (e.g., rules consumed by other systems).

**The PR should include:**
- A full audit table: for every `"type": "learning-journey"` rule entry removed, there should be a link to a corresponding real file on the main branch
of `interactive-tutorials` that corresponds, so that humans and agents can audit that the matches are equivalent and warranted.
- Agents working on deduplication should carefully check their work, as the intent is not to introduce (or remove) any net-new recommendations, relative
to how the recommender works holistically.

**Scope of the change:** This is a large but low-risk PR. The recommender's CI validates all rule JSON files, and the coverage report tool can verify that no recommendation gaps are introduced.

### Phase 4: Freeze index.json

After deduplication and cutover to the v1 endpoint:

1. **Stop accepting new changes** to `index.json` in this repo.
2. **Leave `index.json` in place** — the legacy `/recommend` endpoint still ingests it and will continue to run for some months until it is retired.
3. `index.json` is not actively deduplicated; it becomes a frozen artifact serving the legacy endpoint only.

Removal of `index.json` happens later, when the legacy `/recommend` endpoint is fully retired. That is out of scope for this plan.

## Risks and mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Removing a recommender rule that has no package equivalent | Users lose a recommendation | Phase 2 equivalence check catches this before any removal |
| Package manifest match expression diverges from recommender rule over time | Subtle routing differences after dedup | Run equivalence check as close to the dedup PR as possible; consider a CI check |
| Other systems consume recommender LJ rules | Removing rules breaks those systems | Audit recommender consumers before the dedup PR; the recommender team knows the consumer list |
| `index.json` removal breaks legacy endpoint | Legacy `/recommend` stops working | `index.json` is frozen, not removed — legacy endpoint runs until explicitly retired |

## Preconditions

* On the pathfinder repo, [PR 697](https://github.com/grafana/grafana-pathfinder-app/pull/697) is important because it introduces the machinery 
needed for pathfinder to use the new recommendation endpoint and display those recommendations in the front-end.  This deduplication work should
not be done until after that PR is merged, or subsequent indicated PR that does the same is merged.  This PR creates the trigger condition where
users can actually see duplication.

## Documented Assumptions

1. There are no further learning journey or learning path repos that are not either here or in the static rules of recommender. So our scope is known to be complete.
2. The equivalence check will be a one-time de-duplication at the conclusion of migration, not an ongoing CI process.
3. The legacy /recommend endpoint will continue to run indefinitely after cutover. We will monitor access to this endpoint with prometheus metrics, and the
endpoint will be sunset when the traffic is minimal or non-existent.  This determines how long `index.json` remains frozen.
