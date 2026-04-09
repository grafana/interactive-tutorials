# Post-batch validation report

**Generated:** 2026-04-09  
**Repository:** `interactive-tutorials` (local workspace)  
**Pathfinder CLI:** `/Users/davidallen/hax/grafana-pathfinder-app` — `npm run build:cli` (TypeScript compile to `dist/cli/cli/index.js`)

## Commands run

```bash
cd /Users/davidallen/hax/grafana-pathfinder-app && npm run build:cli

cd /Users/davidallen/hax/interactive-tutorials
node /Users/davidallen/hax/grafana-pathfinder-app/dist/cli/cli/index.js validate --packages .
node /Users/davidallen/hax/grafana-pathfinder-app/dist/cli/cli/index.js build-repository . -o repository.json
node /Users/davidallen/hax/grafana-pathfinder-app/dist/cli/cli/index.js build-graph interactive-tutorials:repository.json -o graph.json
```

## Artifacts (repo root)

| File | Approx. size | Notes |
|------|----------------|-------|
| `repository.json` | ~166 KB | Denormalized catalog from all `manifest.json` trees |
| `graph.json` | ~240 KB | D3-style dependency graph from `repository.json` |

These paths are listed in `.gitignore` (same pattern as CI artifacts). They are present on disk for local inspection and for equivalence tooling; they are not committed unless you change ignore rules or force-add.

---

## 1. `validate --packages .`

| Metric | Value |
|--------|--------|
| **Exit code** | `0` |
| **Packages validated** | 62 |
| **Invalid** | 0 |
| **Result** | All packages valid |

**Warnings (non-fatal):** 29 lines containing `WARN:` (mostly optional `targeting` / `startingLocation` defaults on some manifests — same class of notices as in CI’s “missing targeting” warnings for packages that intentionally omit or inherit targeting).

---

## 2. `build-repository . -o repository.json`

| Metric | Value |
|--------|--------|
| **Exit code** | `0` |
| **Entries written** | 250 |

The entry count is higher than “62 packages” because `build-repository` discovers **every directory** that contains a `manifest.json`, including nested learning-path step directories. That is expected for a full tree build.

---

## 3. `build-graph interactive-tutorials:repository.json -o graph.json`

| Metric | Value |
|--------|--------|
| **Exit code** | `0` |
| **Nodes** | 250 |
| **Edges** | 600 |
| **Lint** | **0 errors**, **63 warnings** |

### Graph lint summary

1. **Dangling references (25 warnings)**  
   `depends` / `recommends` / `suggests` targets that are not present in this repository as a package ID or virtual capability — for example `kubernetes-lj`, `fleet-mgt-monitor-health-lj`, `private-data-source-connect-lj`, `visualization-logs-lj`, `github-visualize-lj`, `irm-configuration-lj`, `grafana-irm-configuration-lj`, `plugin-enabled:grafana-asserts-app`, etc. These are expected when manifests reference **not-yet-migrated** journeys, external plugins, or IDs that only exist in another catalog.

2. **Cycle in `recommends` (1 warning)**  
   `welcome-to-play-main` → `welcome-to-play-visualization` → `welcome-to-play-main`. Worth a manual content review for the welcome-to-play metapackage.

3. **Orphaned packages (37 warnings)**  
   Packages with no incoming or outgoing graph edges — mostly standalone guides that are not linked into dependency chains. This is informational, not a schema failure.

---

## Overall verdict

- **Package validation:** PASS — no blocking errors across the tree.  
- **Aggregate build:** PASS — `repository.json` and `graph.json` generated successfully.  
- **Follow-ups:** Graph warnings do not fail the CLI; they flag **graph hygiene** (external references, one cycle, orphans). Use this output as input to [DEDUPLICATION.md](DEDUPLICATION.md) Phase 2 (equivalence) and to any cleanup of `welcome-to-play` / cross-repo `suggests` IDs.

---

## Reproduce

Regenerate after pulling latest `main`:

```bash
cd /Users/davidallen/hax/grafana-pathfinder-app && npm run build:cli
cd /Users/davidallen/hax/interactive-tutorials
node /Users/davidallen/hax/grafana-pathfinder-app/dist/cli/cli/index.js validate --packages .
node /Users/davidallen/hax/grafana-pathfinder-app/dist/cli/cli/index.js build-repository . -o repository.json
node /Users/davidallen/hax/grafana-pathfinder-app/dist/cli/cli/index.js build-graph interactive-tutorials:repository.json -o graph.json
```
