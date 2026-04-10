# Package Migration Record

Historical record of the migration from bare `content.json` guides to the Pathfinder two-file package format (`content.json` + `manifest.json`). This project ran from approximately March–April 2026 and is now complete.

**This document is a historical reference, not a working plan.** For current package authoring guidance, see [`docs/manifest-reference.md`](../manifest-reference.md).

---

## What was done

Every guide and learning path in this repository was migrated to the Pathfinder package format. Migration was additive-only: a `manifest.json` was added alongside each existing `content.json`. No existing `content.json` or `index.json` files were modified.

After migration, recommendation rules that had been duplicated between the static recommender (`grafana-recommender`) and the new package manifests were deduplicated by removing the static rules, leaving `manifest.json` targeting as the single source of truth.

### Key outcomes

| Outcome | Detail |
|---------|--------|
| Packages migrated | 62 (12 standalone guides, 21 learning paths, 3 special cases, plus previously migrated guides) |
| `repository.json` entries | 250 (includes learning path steps) |
| Post-migration validation | 0 errors, 62 packages valid |
| CI enforcement | `manifest.json` required for every `content.json` (`.github/workflows/validate-json.yml`) |
| Recommender deduplication | All `"type": "learning-journey"` static rules removed from `grafana-recommender` |
| `index.json` | Frozen — CI guard blocks changes; serves legacy `/recommend` endpoint only until retirement |

---

## Design decisions worth preserving

1. **Additive-only migration.** No existing `content.json` was ever modified. This eliminated merge conflicts with ongoing authoring work and made rollback trivial (just revert the commit adding manifest files).

2. **Coexistence during migration.** Three recommendation sources overlapped during the transition: `index.json`, `manifest.json` targeting, and `grafana-recommender` static rules. All were retained until migration was complete, then deduplicated.

3. **`repository.json` is CI-generated, never committed.** CI generates it on every push; the deploy pipeline publishes it to the CDN. Paths in `repository.json` are relative to the CDN publication root.

4. **Two CDN paths.** Legacy `guides/` (driven by `index.json`) and new `packages/` (driven by `repository.json`) are published independently. The `packages/` copy is a full directory tree (not JSON-only) to support non-JSON assets referenced by relative path.

5. **Wave-based batch execution.** Migrations ran in parallel waves using isolated worktrees — one agent per guide, one PR per migration. Waves were reviewed between batches to catch systemic issues early.

6. **Migration skill.** A reusable skill (`.cursor/skills/migrate-guide/SKILL.md`) performed each migration. It derived manifest fields from `content.json`, `index.json`, website markdown, and recommender rules, with conflict flagging rather than silent resolution.

---

## PR tracking

### Umbrella PR

[#227 — Pathfinder package format: mass migration base](https://github.com/grafana/interactive-tutorials/pull/227)

### Standalone guides

| Directory | PR |
|-----------|-----|
| `dynamic-dashboards-tour` | [#228](https://github.com/grafana/interactive-tutorials/pull/228) |
| `enable-coda` | [#229](https://github.com/grafana/interactive-tutorials/pull/229) |
| `fleet-management-onboarding` | [#230](https://github.com/grafana/interactive-tutorials/pull/230) |
| `how-to-import-external-alerting-resource-5e08` | [#231](https://github.com/grafana/interactive-tutorials/pull/231) |
| `how-to-setup-secrets-tutorial` | [#232](https://github.com/grafana/interactive-tutorials/pull/232) |
| `otel-fleet-management` | [#234](https://github.com/grafana/interactive-tutorials/pull/234) |
| `play-carbon-intensity` | [#233](https://github.com/grafana/interactive-tutorials/pull/233) |
| `semantic-layer-tutorial` | [#237](https://github.com/grafana/interactive-tutorials/pull/237) |
| `slo-quickstart` | [#235](https://github.com/grafana/interactive-tutorials/pull/235) |
| `sm-dns-check-tutorial` | [#236](https://github.com/grafana/interactive-tutorials/pull/236) |
| `sm-ping-check-tutorial` | [#239](https://github.com/grafana/interactive-tutorials/pull/239) |
| `sm-tcp-check-tutorial` | [#238](https://github.com/grafana/interactive-tutorials/pull/238) |

### Learning paths

| Directory | PR |
|-----------|-----|
| `adaptive-logs-lj` | [#263](https://github.com/grafana/interactive-tutorials/pull/263) |
| `billing-usage-lj` | [#240](https://github.com/grafana/interactive-tutorials/pull/240) |
| `create-availability-slo-lj` | [#241](https://github.com/grafana/interactive-tutorials/pull/241) |
| `detect-outages-synthetic-monitoring-lj` | [#248](https://github.com/grafana/interactive-tutorials/pull/248) |
| `drilldown-logs-lj` | [#245](https://github.com/grafana/interactive-tutorials/pull/245) |
| `drilldown-metrics-lj` | [#242](https://github.com/grafana/interactive-tutorials/pull/242) |
| `drilldown-traces-lj` | [#243](https://github.com/grafana/interactive-tutorials/pull/243) |
| `github-data-source-lj` | [#249](https://github.com/grafana/interactive-tutorials/pull/249) |
| `grafana-cloud-tour-lj` | [#244](https://github.com/grafana/interactive-tutorials/pull/244) |
| `infinity-csv-lj` | [#251](https://github.com/grafana/interactive-tutorials/pull/251) |
| `influxdb-data-source-lj` | [#246](https://github.com/grafana/interactive-tutorials/pull/246) |
| `infrastructure-alerting-lj` | [#254](https://github.com/grafana/interactive-tutorials/pull/254) |
| `kafka-monitoring-lj` | [#250](https://github.com/grafana/interactive-tutorials/pull/250) |
| `linux-server-integration-lj` | [#252](https://github.com/grafana/interactive-tutorials/pull/252) |
| `macos-integration-lj` | [#253](https://github.com/grafana/interactive-tutorials/pull/253) |
| `mysql-data-source-lj` | [#260](https://github.com/grafana/interactive-tutorials/pull/260) |
| `mysql-integration-lj` | [#258](https://github.com/grafana/interactive-tutorials/pull/258) |
| `postgresql-integration-lj` | [#262](https://github.com/grafana/interactive-tutorials/pull/262) |
| `prom-remote-write-lj` | [#247](https://github.com/grafana/interactive-tutorials/pull/247) |
| `visualization-metrics-lj` | [#259](https://github.com/grafana/interactive-tutorials/pull/259) |
| `visualization-traces-lj` | [#261](https://github.com/grafana/interactive-tutorials/pull/261) |

### Special cases

| Directory | PR |
|-----------|-----|
| `visualization-logs` | [#264](https://github.com/grafana/interactive-tutorials/pull/264) |
| `windows-integration` | [#265](https://github.com/grafana/interactive-tutorials/pull/265) |
| `welcome-to-play` | [#266](https://github.com/grafana/interactive-tutorials/pull/266) |

### Pilot guides (migrated before the batch)

`alerting-101`, `explore-drilldowns-101`, `first-dashboard`, `prometheus-lj`

---

## Post-batch validation summary

**Date:** 2026-04-09

| Check | Result |
|-------|--------|
| `validate --packages .` | 62 packages valid, 0 errors |
| `build-repository . -o repository.json` | 250 entries |
| `build-graph` | 250 nodes, 600 edges, 0 errors, 63 warnings (dangling cross-repo refs, orphaned standalone guides — expected) |

---

## Related external work

| Item | Link |
|------|------|
| Pathfinder package design spec | [PATHFINDER-PACKAGE-DESIGN.md](https://github.com/grafana/grafana-pathfinder-app/blob/main/docs/design/PATHFINDER-PACKAGE-DESIGN.md) |
| Pathfinder frontend integration | [grafana-pathfinder-app PR #697](https://github.com/grafana/grafana-pathfinder-app/pull/697) |
| Recommender deduplication PR | [grafana-recommender](https://github.com/grafana/grafana-recommender/pulls) |
| Partner-facing migration guide | [Google Doc](https://docs.google.com/document/d/1LQkqzjZwLibQPCg91SIwxDvYELv4xy2f2Fr9Y1wN0FY/edit?usp=sharing) |

---

## Source documents

This record was consolidated from the following design documents, which were removed from `docs/design/` after the project completed:

- `MIGRATION.md` — phased migration design (Phases 0–4), field derivation rules, safety invariants
- `MASS-MIGRATION-PLAN.md` — batch execution plan, PR conventions, wave scheduling, tracking
- `DEDUPLICATION.md` — recommender rule deduplication plan (Phases 1–4)
- `POST-BATCH-VALIDATION-REPORT.md` — full validation output after all migrations merged
