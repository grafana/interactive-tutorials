# Migration to Pathfinder Package Format

This document describes the phased migration of the `interactive-tutorials` repository from bare `content.json` guides with a centralized `index.json` to the Pathfinder two-file package model (`content.json` + `manifest.json`) with a CI-generated `repository.json`.

**Design references (in grafana-pathfinder-app):**
- [PATHFINDER-PACKAGE-DESIGN.md](https://github.com/grafana/grafana-pathfinder-app/blob/main/docs/design/PATHFINDER-PACKAGE-DESIGN.md) — the package format spec
- [package-authoring.md](https://github.com/grafana/grafana-pathfinder-app/blob/main/docs/developer/package-authoring.md) — manifest field reference and templates
- [CLI_TOOLS.md](https://github.com/grafana/grafana-pathfinder-app/blob/main/docs/developer/CLI_TOOLS.md) — CLI commands: `validate --package/--packages`, `build-repository`, `build-graph`, `schema manifest`

---

## Living document protocol

This is a living document. Each agent tasked with implementing a phase must:

1. **Read the entire document** before starting work — including all completed phases and decisions recorded in them.
2. **Execute the assigned phase.**
3. **Update this document** as a leave-behind: mark the phase complete, record key decisions made, note any deviations from the original specification, and refine later phases if prior-phase decisions affect them.
4. If a prior-phase decision renders a later-phase specification ambiguous or contradictory, **ask questions** to resolve ambiguity before proceeding.

The goal is that this document accumulates the full decision history of the migration, so any agent or human reading it later can understand not just _what_ was done, but _why_.

---

## Starting point

At the time of writing, this repository contains many guides (`content.json`) and 13 learning journey directories (`*-lj`), but no `manifest.json` files and no `repository.json`. The migration adds `manifest.json` alongside existing content; guide counts will change independently as authors continue to write new guides.

---

## Strategy

**Pilot-first.** This branch migrates a representative subset (2–3 standalone guides + 1 learning journey) end-to-end: documentation, manifests, CI, deploy. Full migration is then a matter of reusing the migration skill on the remaining guides.

**Coexistence.** During partial migration, `index.json` continues to serve as the recommendation rules source for all guides. Guides with `manifest.json` carry their own `targeting`, but `index.json` entries are retained for all guides until the recommender consumes `repository.json` directly.

**repository.json is CI-generated.** It is never committed to git. CI generates it on every push and the deploy pipeline publishes it to the CDN alongside guide content. Paths in `repository.json` entries are relative to the CDN publication root (e.g., `alerting-101/` not `/guides/alerting-101/`).

### Safety invariants

These invariants hold throughout the entire migration — pilot and full:

1. **Never modify existing `content.json` files.** Migration writes new `manifest.json` files and may create a new `content.json` where one is missing (e.g., path-level cover pages for `*-lj` directories). It must never modify an existing `content.json`. Content authors own those files; modifying them risks merge conflicts and disrupts ongoing authoring work. The migration skill verifies this: any `content.json` in scope was either already present (unchanged) or newly created — never modified.

2. **Never modify `index.json`.** The migration reads `index.json` as a data source for targeting rules but never writes to it. `index.json` is a shared resource consumed by all guides; modifying it is outside the scope of individual guide migration.

3. **Parallel-safe by design.** Each migration operates on a single directory (one guide or one `*-lj` path). Because the skill only writes files within that directory and reads shared resources (`index.json`, website markdown) without modifying them, multiple agents can migrate different guides simultaneously without risk of conflict.

4. **Rollback is trivial.** Since migration is additive-only (new files, no modifications to existing files), rollback is simply reverting the commit(s) that added manifest files. `repository.json` is CI-generated and never committed, so it disappears automatically when manifests are reverted.

---

## Phase 0: Documentation ✓

**Status: COMPLETE**

**Goal:** Authors and agents have a reference for writing `manifest.json` in this repository, with field derivation rules specific to this repo's conventions.

### Deliverables

- [x] **`docs/manifest-reference.md`** — Manifest field reference adapted for this repository. Covers:
  - Package directory structure (`content.json` + `manifest.json`)
  - Field-by-field reference for `manifest.json` with types, required/optional, defaults
  - Field derivation rules for migration (where each field's data comes from — see [field derivation rules](#field-derivation-rules) below)
  - Targeting: how to translate an `index.json` rule into `targeting.match`
  - testEnvironment: tier inference rules (local, cloud, play)
  - Learning path manifests: `type: "path"`, `steps` array, path-level `content.json`
  - Dependency fields: `depends`, `recommends`, `suggests`, `provides`
  - Copy-paste templates for standalone guide and learning path

  The canonical manifest schema can be obtained at any time by running `node dist/cli/cli/index.js schema manifest` from a pathfinder-app checkout. `docs/manifest-reference.md` should reference this as the authoritative schema source rather than duplicating it.

- [x] **Update `.cursor/authoring-guide.mdc`** — Add a documentation map entry pointing to `docs/manifest-reference.md` and a brief section on manifest authoring.

- [x] **Update `AGENTS.md`** — Add task routing entries for manifest authoring and migration.

### Decisions recorded

1. **`docs/manifest-reference.md` references the CLI schema rather than duplicating it.** The doc points to `node dist/cli/cli/index.js schema manifest` as the authoritative source and serves as a practical companion with repo-specific derivation rules and templates.

2. **Tier inference refined for `play` vs `cloud`.** The testEnvironment section distinguishes `"play"` (when `source` is `play.grafana.org`) from generic `"cloud"` (when `targetPlatform: "cloud"` or `source` is a non-play host). This distinction wasn't explicit in the original field derivation table but follows logically from the existing play vs cloud test environments.

3. **`repository` and `language` marked as omittable.** Since schema defaults (`"interactive-tutorials"` and `"en"`) apply automatically, the templates and derivation rules recommend omitting these fields to reduce noise.

4. **Documentation map entries added to both `.cursor/authoring-guide.mdc` and `AGENTS.md`.** The authoring guide got a new "Manifest Authoring" section at the end plus two entries in the documentation map table. `AGENTS.md` got two new task routing rows (manifest authoring, guide migration) and two new reference documentation rows.

### Field derivation rules

The complete field derivation rules — specifying where each manifest field's data comes from — are defined in [`docs/manifest-reference.md`](manifest-reference.md) under "Field derivation rules." The rules are split into three tables covering standalone guides, learning path steps, and learning paths.

The governing principle is **maximally complete from existing data, no guessing or inventing**.

Guide-to-rule matching and `index.json` URL-to-directory mapping are also documented in [`docs/manifest-reference.md`](manifest-reference.md) under "Matching index.json rules to guides."

---

## Phase 1: Migration skill ✓

**Status: COMPLETE**

**Goal:** A reusable agent skill that atomically migrates one guide or one learning path to the package format.

### Skill design principles

- **References, not duplication.** The skill focuses on migration logic — field mapping, data source lookup, conflict detection. It does not duplicate documentation on manifest format, guide authoring rules, or content conventions. Instead, it references the Phase 0 docs (`docs/manifest-reference.md`) and the existing authoring guide (`.cursor/authoring-guide.mdc`) by inclusion. This follows the repo's tiered context access pattern.

- **Parallel-safe.** The skill operates on a single directory in isolation. It reads shared resources (`index.json`, website markdown) but never modifies them. Multiple agents can run the skill on different guides simultaneously without risk of stepping on each other.

- **Never modifies existing content.json.** The skill may create a new `content.json` (e.g., a path-level cover page) but must never modify an existing one. As a verification step, the skill confirms that every `content.json` in scope was either pre-existing (unchanged) or newly created.

- **Never modifies index.json.** The skill reads `index.json` for targeting data but never writes to it.

### Deliverables

- [x] **`.cursor/skills/migrate-guide/SKILL.md`** — Single skill with two modes:

  **Mode 1: Standalone guide** — invoked on a guide directory (e.g., `alerting-101/`)
  1. Read `content.json` to extract `id` and `title` (do not modify)
  2. Look up the matching `index.json` rule by URL path segment (read-only)
  3. Locate the website markdown equivalent if it exists (at `<website-repo>/content/docs/learning-paths/<name>/`)
  4. Generate `manifest.json` following the field derivation rules in `docs/manifest-reference.md`
  5. Validate: `id` matches between `content.json` and `manifest.json`
  6. Verify: no existing `content.json` was modified
  7. Run `validate --package <dir>` to validate the generated package

  **Mode 2: Learning path** — invoked on a `*-lj` directory (e.g., `prometheus-lj/`)
  1. Locate the website markdown path at `<website-repo>/content/docs/learning-paths/<path-name>/`
  2. Read the path-level `_index.md` for metadata: `title`, `description`, `journey.group` (category), `journey.skill` (difficulty), `journey.links` (recommends), `related_journeys` (suggests/depends)
  3. Read each step's markdown (`<step>/index.md`) for: `weight` (ordering), `step` (number), `pathfinder_data` (directory mapping), `description`, `side_journeys`
  4. For each step subdirectory: run Mode 1 to generate the step's `manifest.json`
  5. Create the path-level `manifest.json` (`type: "path"`) with:
     - `steps` array ordered by `weight` from the markdown
     - `description`, `category`, `author` from path-level markdown
     - `recommends` from `journey.links.to`
     - `suggests` from `related_journeys`
  6. Create the path-level `content.json` derived from the `_index.md` body content (see [path-level content.json authoring](#path-level-contentjson-authoring) below)
  7. Validate cross-file ID consistency and step references
  8. Verify: no existing `content.json` in any step subdirectory was modified

  **Metadata conflict resolution:** The website markdown `_index.md` is the authoritative source for path-level metadata (title, description, category, learning objectives, prerequisites). However, metadata may exist in multiple places — `index.json`, `journeys.yaml`, the markdown frontmatter, and the markdown body. A conflict exists whenever the same field has different string values in two sources, even if the values are semantically similar. The skill must **flag the conflict for manual resolution** by the user rather than silently picking one source. The agent should present both values and ask the user which to use.

  **Website markdown fallback:** If the website repository is not available or a guide has no corresponding website markdown, the skill applies the fallback rules defined in [`docs/manifest-reference.md`](manifest-reference.md) under "When website markdown is unavailable." Fields that cannot be derived are flagged for manual entry rather than guessed.

  **Mapping LJ names to website paths:** The directory names differ between repos. The mapping is:

  | interactive-tutorials | website learning-paths |
  |----------------------|----------------------|
  | `prometheus-lj` | `prometheus` |
  | `linux-server-integration-lj` | `linux-server-integration` |
  | `drilldown-logs-lj` | `drilldown-logs` |
  | (pattern: strip `-lj` suffix) | |

  Within a path, step directories use the same names in both repos. The website markdown `pathfinder_data` frontmatter field provides the authoritative mapping (e.g., `pathfinder_data: prometheus-lj/add-data-source`).

### Path-level content.json authoring

Learning path directories (`*-lj`) typically have no `content.json` at their root — only step subdirectories contain content. The migration creates a path-level `content.json` as a cover page for the path, derived from the website markdown `_index.md`.

**Source:** The `_index.md` file for each learning path (e.g., `website/content/docs/learning-paths/prometheus/_index.md`) contains:
- **Frontmatter:** `title`, `description`, and other metadata (used for `manifest.json`)
- **Body content:** Descriptive prose, learning objectives ("Here's what to expect"), prerequisites ("Before you begin"), and contextual information about the path

**Derivation rules for path-level content.json:**
1. `id` — the `*-lj` directory name (e.g., `"prometheus-lj"`)
2. `title` — from the `_index.md` frontmatter `title` field
3. `blocks` — derived from the `_index.md` body content:
   - Strip Hugo shortcode tags (`{{< ... >}}`, `{{< /... >}}`) — these are rendering directives, not content. For wrapping shortcodes (e.g., `{{< admonition >}}...{{< /admonition >}}`), strip the opening and closing tags but preserve the inner content
   - Convert the remaining markdown body into one or more `markdown` blocks
   - Preserve learning objectives, prerequisites, and descriptive prose — these provide value as the path's introductory page
   - Images referenced via markdown syntax (`![alt](url)`) can be retained as-is in the markdown block content; the Pathfinder renderer will handle them

**Example:** For `prometheus-lj`, the path-level `content.json` would contain the title "Connect to a Prometheus data source in Grafana Cloud" and markdown blocks covering: what Prometheus is, what the journey teaches, learning objectives (the 5-point list), and prerequisites.

### Decisions recorded

1. **Single SKILL.md, no sub-agents.** Unlike the `autogen-guide` skill which uses a multi-phase sub-agent pipeline, the migration skill is a straightforward read-derive-write workflow. All logic is documented inline in `SKILL.md` and executed by a single agent invocation. This keeps the skill simple and predictable — the primary complexity is in the data derivation rules, which are already documented in `docs/manifest-reference.md`.

2. **No skill-memory convention.** The `autogen-guide` skill uses `assets/manifest.yaml` for re-run detection because its input (source code) can drift. Migration input (`content.json`, `index.json`, website markdown) is stable — a guide is migrated once and then maintained by hand. Re-run detection adds complexity with no benefit, so the skill does not implement the skill-memory convention.

3. **Website repo path hardcoded.** The website markdown path (`/Users/davidallen/hax/website/content/docs/learning-paths/`) is documented as a constant in the skill. If the website repo is not at this path, the skill applies fallback rules rather than failing. This matches the existing convention in `docs/manifest-reference.md`.

4. **Conflict flagging over silent resolution.** When metadata differs between sources (e.g., `index.json` description vs website markdown description), the skill flags the conflict and asks the user to choose. This follows the MIGRATION.md specification and avoids the risk of silently picking the wrong value.

5. **Empty dependency arrays.** For migration output the skill's rule applies: empty dependency arrays are included as `[]` so authors see the fields. The skill always includes `depends`, `recommends`, `suggests`, and `provides` (even when empty) rather than omitting them.

---

## Phase 2: Pilot migration (content) ✓

**Status: COMPLETE**

**Goal:** Migrate a representative subset to validate the full pipeline before scaling.

### Pilot candidates

**Standalone guides (2–3):**

| Guide | Why | index.json entry? |
|-------|-----|-------------------|
| `alerting-101` | High-value, has targeting rules, cloud+OSS | Yes |
| `explore-drilldowns-101` | Multi-URL targeting, app-specific | Yes |
| `first-dashboard` | Foundational, simple targeting | Yes |

**Learning path (1):**

| Path | Why |
|------|-----|
| `prometheus-lj` (9 steps) | Good complexity, rich website markdown metadata, `journey.links`, `related_journeys`, multiple step types |

### Deliverables

- [x] **Standalone guide manifests** — Run the migration skill on each pilot guide. Each produces a `manifest.json` alongside the existing `content.json`.

- [x] **Learning path migration** — Run the migration skill on `prometheus-lj/`. Produces:
  - `prometheus-lj/manifest.json` (`type: "path"`, `steps` array with 9 entries)
  - `prometheus-lj/content.json` (path-level descriptive content from website markdown)
  - `prometheus-lj/<step>/manifest.json` for each of the 9 steps

- [x] **Validation** — All migrated packages pass `validate --package` / `validate --packages`

- [x] **index.json unchanged** — Existing entries remain; no entries removed or modified

### Decisions recorded

1. **Execution:** Four sub-agents ran in parallel (one per pilot: alerting-101, explore-drilldowns-101, first-dashboard, prometheus-lj). Each followed `.cursor/skills/migrate-guide/SKILL.md` and wrote leave-behind `assets/migration-notes.md`.

2. **Duplicate step descriptions:** For prometheus-lj, website steps business-value-olly and business-value-prom shared the same description. One agent varied business-value-prom's manifest description to avoid a catalog duplicate. The skill (step 5b) says "Still use the values as-is"; skill wording could be tightened to forbid inventing variants and require using the same value plus flagging for upstream review.

3. **journeys.yaml vs _index.md:** prometheus-lj has `journeys.yaml` `links.to: metrics-drilldown` vs `_index.md` `journey.links.to: drilldown-metrics`. Skill uses _index.md as authoritative (maps to repo directory names). Mismatch recorded in migration notes for website reconciliation.

4. **Path targeting:** prometheus-lj has no index.json rule; path manifest correctly omits `targeting` and `startingLocation`. CLI reports "startingLocation not specified, defaulting to '/'" — that is the validator's default, not a manifest error.

### Expected output structure

```
interactive-tutorials/
├── alerting-101/
│   ├── content.json          ← existing (unchanged)
│   └── manifest.json         ← new
├── explore-drilldowns-101/
│   ├── content.json          ← existing (unchanged)
│   └── manifest.json         ← new
├── first-dashboard/
│   ├── content.json          ← existing (unchanged)
│   └── manifest.json         ← new
├── prometheus-lj/
│   ├── content.json          ← new (path-level cover page)
│   ├── manifest.json         ← new (type: "path", steps: [...])
│   ├── add-data-source/
│   │   ├── content.json      ← existing (unchanged)
│   │   └── manifest.json     ← new
│   ├── business-value-prom/
│   │   ├── content.json      ← existing (unchanged)
│   │   └── manifest.json     ← new
│   └── ... (7 more steps)
├── index.json                ← existing (unchanged)
└── repository.json           ← NOT committed; CI-generated
```

---

## Phase 3: CI integration ✓

**Status: COMPLETE**

**Goal:** CI validates packages and generates `repository.json` on every push/PR.

### Deliverables

- [x] **Extend `validate-json.yml`** with new steps in the existing `validate-guides` job:
  - After building the pathfinder CLI, run `validate --packages .` to validate all package directories (those with `manifest.json`)
  - Run `build-repository . -o repository.json` to generate `repository.json` from all packages
  - Run `build-graph` for dependency visualization (informational, not blocking)
  - Upload `repository.json` as a CI artifact for inspection

- [x] **Validation scope** — `validate --packages` validates only directories that contain `manifest.json`. Directories with only `content.json` (un-migrated guides) are still validated by the existing per-file validation loop. Both validations coexist.

- [x] **repository.json paths** — The `build-repository` command produces entries with paths relative to the repository root (e.g., `"path": "alerting-101/"`). These are also relative to the CDN publication root since the deploy step copies the repo structure into the `guides/` bucket prefix.

- [x] **repository.json excluded from git** — Added `repository.json` to `.gitignore` since it is CI-generated and must never be committed.

### CI job ordering

```
validate-recommender-rules (index.json)     ← existing, unchanged
validate-guides (content.json per-file)      ← existing, unchanged
validate-packages (manifest.json packages)   ← new (same job as validate-guides)
build-repository (repository.json)           ← new (same job as validate-guides)
```

The `validate-packages` and `build-repository` steps are added to the existing `validate-guides` job after the per-file content.json validation. This avoids duplicating the pathfinder-app checkout, Node.js setup, and CLI build steps. The `validate-recommender-rules` job remains a separate parallel job.

### Local verification

Local verification performed successfully against the pathfinder CLI at `/Users/davidallen/hax/grafana-pathfinder-app`:

1. **`validate --packages .`** — All 21 packages valid (13 with manifests, 8 content-only). No errors.
2. **`build-repository . -o repository.json`** — Generated `repository.json` with 13 package entries.
3. **`build-graph interactive-tutorials:repository.json`** — Graph built successfully (13 nodes, 29 edges). 7 warnings:
   - 3 orphaned standalone guides (expected — `alerting-101`, `explore-drilldowns-101`, `first-dashboard` have no inter-package dependencies)
   - 4 unresolved cross-repo references (`drilldown-metrics-lj`, `private-data-source-connect-lj`) — expected since these learning paths have not been migrated yet

### Decisions recorded

1. **Steps in existing job, not separate jobs.** The new `validate-packages`, `build-repository`, `build-graph`, and artifact upload steps are added to the existing `validate-guides` job rather than creating separate jobs. This avoids tripling the pathfinder-app checkout/install/build time. The `validate-recommender-rules` job (which doesn't need the CLI) remains separate and runs in parallel.

2. **`build-graph` uses `continue-on-error: true`.** The dependency graph is informational — lint warnings about orphaned packages or missing cross-repo targets should not fail the CI pipeline. These warnings are expected during partial migration and will resolve as more guides are migrated.

3. **`build-graph` requires `name:path` format.** The CLI's `build-graph` command takes `<name>:<path>` repository entries, not a bare directory. The CI step uses `interactive-tutorials:repository.json` to reference the generated file. This was discovered during local verification (the MIGRATION.md spec used `.` which the CLI rejected).

4. **`repository.json` added to `.gitignore`.** Consistent with the strategy that `repository.json` is CI-generated and never committed to git. The `.gitignore` entry prevents accidental commits from local testing.

5. **Artifact upload with 30-day retention.** The `repository.json` CI artifact uses `actions/upload-artifact@v4` with 30-day retention so it can be inspected on any PR or push without needing to re-run the workflow.

6. **All pilot manifests validate cleanly.** No manifest fixes were needed — the Phase 2 pilot manifests all pass `validate --packages` without errors. The `build-graph` warnings are expected (unresolved cross-repo references, orphaned standalone guides) and do not indicate manifest problems.

---

## Phase 4: Deploy pipeline ✓

**Status: COMPLETE**

**Goal:** The deploy pipeline publishes `repository.json` and all package files to the CDN under a new `packages/` prefix, keeping the legacy `guides/` path unchanged.

### Design decisions

1. **Two separate CDN paths, not one.** The legacy `guides/` copy (driven by `index.json`) continues completely unchanged. A new `packages/` copy is added as a parallel deploy step. This hard-separates the old code path from the new, so neither affects the other during the transition.

2. **`packages/` is a full directory tree copy.** Every guide directory is copied recursively into `packages/` — all `*.json` files, all `assets/` subdirectories, and any other files present. This is required by the open package semantics: a package may include non-JSON files (images, metadata, etc.) that `content.json` or downstream consumers reference by relative path. Copying only `*.json` would silently break those references. The `packages/` copy must never be "optimized" to a JSON-only copy.

3. **Exclude `pathfinder-app/` from the `packages/` copy.** The pathfinder-app repository is checked out into the workspace root as part of the CLI build step (same pattern as `validate-json.yml`). It must be explicitly excluded from the `packages/` copy — it is not a guide package and contains a large amount of source code, bundled guides, and build artifacts that must not be published to the CDN.

4. **`repository.json` is co-located inside `packages/`.** The `build-repository` command is run with `packages/` as both the scan root and the output directory: `build-repository packages/ -o packages/repository.json`. This ensures every `"path"` entry in `repository.json` (e.g., `"path": "alerting-101/"`) is relative to the directory containing `repository.json` itself. Consumers resolve package content as `<base-url-of-repository.json>/<path>`. This invariant must be preserved — running `build-repository` from the repo root and placing `repository.json` elsewhere would break relative path resolution without post-processing.

5. **Un-migrated guides are inert under `packages/`.** A guide that has `content.json` but no `manifest.json` will have its files present under `packages/` but will not appear in `repository.json`. It is undiscoverable by any consumer following the new code path. This is intentional — no filtering of un-migrated guides from the `packages/` copy is needed; discoverability is controlled entirely by `repository.json`.

6. **`packages/` copy is added on every prod deploy.** The `guides/` copy already runs on every deploy; the new `packages/` step runs alongside it every time, so `packages/` is never stale relative to `guides/`.

7. **`push-to-gcs` staging pattern: mirror the `guides/` approach.** The `push-to-gcs` action (`grafana/shared-workflows/actions/push-to-gcs`) has a `parent` input (default `"true"`) that controls whether the local directory name is included in the GCS destination path. The existing step uses `path: guides` with the default `parent: true`, which causes files to land at `bucket/guides/...`. For `packages/`, stage files into a local directory literally named `packages/` and use `path: packages` with default `parent: true` — this causes files to land at `bucket/packages/...`. No `bucket_path` override is needed; the naming convention does the work. This pattern is the simplest and most consistent with the existing step.

   The action also has a `bucket_path` input that prepends a prefix to the bucket destination, but using it would require `parent: "false"` to avoid double-prefixing the local directory name. The staging-directory-naming approach is cleaner.

   **Exclude list for the `packages/` staging copy:** the following must not be copied into the `packages/` staging directory: `pathfinder-app/` (CLI checkout), `.github/`, `docs/`, `.cursor/`, `shared/` (served separately under `guides/`), and any top-level files (`index.json`, `repository.json`, `*.md`, `*.yml`, etc.). Only guide subdirectories (those containing `content.json` or `manifest.json`) should be copied.

### Deliverables

- [x] **Checkout pathfinder-app and build CLI** in `deploy.yml` (same pattern as `validate-json.yml`)

- [x] **Add "Prepare packages" step** to stage the full tree copy:
  1. `mkdir -p packages/`
  2. Copy every guide directory recursively into `packages/`, applying the exclude list above
  3. Run `node pathfinder-app/dist/cli/cli/index.js build-repository packages/ -o packages/repository.json` to generate `repository.json` co-located with the packages. No `--exclude` flag needed here since `pathfinder-app/` is not inside the `packages/` staging directory.
  4. (Optional) Run `build-graph` for informational artifact, `continue-on-error: true`

- [x] **Push `packages/` to GCS** using `path: packages` (default `parent: true`), same `bucket` and `service_account` as the existing `guides/` push

- [x] **Verify relative paths** — `"path": "alerting-101/"` in `repository.json` resolves to `https://interactive-learning.grafana.net/packages/alerting-101/` because `repository.json` and the package directories are siblings under `packages/`

### Decisions recorded

1. **`build-graph` runs inside `packages/` and outputs `graph.json` alongside `repository.json`.** The CLI outputs `graph.json` to the current working directory, so a dedicated "Build dependency graph" step uses `working-directory: packages` to run inside the staging directory. This ensures `graph.json` is staged as a sibling of `repository.json` and deployed to `bucket/packages/graph.json`. Graph warnings (orphaned packages, unresolved cross-repo refs) are expected during partial migration; the step uses `continue-on-error: true` so failures appear as visible warnings in the GitHub Actions UI without blocking the deploy.

2. **Exclude list implemented as an explicit shell loop.** The "Prepare packages" step iterates top-level directories and skips `pathfinder-app`, `.github`, `docs`, `.cursor`, `shared`, `guides`, and `packages`. Top-level files (`.json`, `.md`, `.yml`, etc.) are naturally excluded because the loop only iterates directories (`*/`). This is simpler and less fragile than a `find`-based approach.

3. **`--exclude` flag not used in `build-repository` for deploy.** In `validate-json.yml`, `--exclude pathfinder-app` is needed because the scan root is `.` (the repo root) and `pathfinder-app/` is present there. In `deploy.yml`, the scan root is `packages/` (the staging directory), into which `pathfinder-app/` is never copied. The flag is therefore unnecessary.

4. **Partial migration is safe.** The deploy pipeline produces a valid but incomplete `repository.json` containing only migrated packages (those with `manifest.json`). Un-migrated guides are present under `packages/` but absent from `repository.json` and undiscoverable by consumers. The `guides/` legacy path continues to serve all guides. This means the Phase 4 pipeline can go live while migration is still in progress, enabling downstream component integration testing against real CDN content.

### CDN structure after deploy

```
interactive-learning-{env}/
├── guides/                            ← existing, unchanged
│   ├── index.json
│   ├── shared/
│   ├── alerting-101/
│   │   ├── content.json
│   │   └── manifest.json
│   └── ... (all guides)
└── packages/                          ← new
    ├── repository.json                ← co-located with packages; paths relative to here
    ├── alerting-101/
    │   ├── content.json
    │   ├── manifest.json
    │   └── assets/                    ← full tree; non-JSON files included
    ├── prometheus-lj/
    │   ├── content.json
    │   ├── manifest.json
    │   ├── add-data-source/
    │   │   ├── content.json
    │   │   └── manifest.json
    │   └── ...
    ├── some-unmigrated-guide/
    │   └── content.json               ← present but not in repository.json; unreachable
    └── ... (all guide directories, full tree)
```

---

## Phase 5: Verification and dependent repo testing

**Goal:** Verify end-to-end that the published package structure works with downstream consumers.

### Deliverables

- [ ] **Dev deployment** — Deploy to the `dev` environment via `deploy.yml` workflow dispatch
- [ ] **CDN verification** — Confirm `repository.json` is accessible at the expected CDN URL and contains correct entries for all pilot packages
- [ ] **Recommender integration test** — Configure `grafana-recommender` to fetch `repository.json` from the dev CDN. Verify it resolves pilot package IDs correctly.
- [ ] **Plugin integration test** — Verify the `grafana-pathfinder-app` frontend can load pilot guides through the composite resolver (bundled fallback → recommender resolution)
- [ ] **index.json continuity** — Verify that existing recommendation rules continue to work for all guides (migrated and un-migrated)

---

## Full migration (future work)

After the pilot is validated end-to-end, full migration is a mechanical process:

### Standalone guides

For each un-migrated standalone guide:
1. Run the migration skill
2. Validate
3. Deploy

### Learning paths

For each `*-lj` directory:
1. Run the migration skill (path mode)
2. Validate path-level and all step-level manifests
3. Deploy

### index.json retirement

Once all guides carry their own `targeting` in `manifest.json` and the recommender consumes `repository.json`:
1. Verify the recommender aggregates all `targeting.match` rules from `repository.json`
2. Compare aggregated rules against `index.json` to ensure no rules are lost
3. Remove `index.json` from the repository and deploy pipeline
4. Remove the `validate-recommender-rules` CI job

### Multi-part guides (deferred)

`welcome-to-play/` is a multi-part guide with subdirectories (`main-page`, `visualization-page`, `datasource-page`), each with its own `content.json` and `index.json` entry. It is not a learning path — it will need hand-migration into a metapackage. Defer this from both the pilot and the mechanical full migration; handle it as a separate future task.

### Guides without index.json entries

Some guides have `content.json` but no `index.json` entry (they are not contextually recommended — only reachable via direct link or learning path). These guides still get `manifest.json` with `type`, `description`, `author`, etc. They simply have no `targeting` field. The migration skill handles this: when no matching `index.json` rule is found, `targeting` is omitted.

### CI enforcement: require manifest.json for every package

Once the full migration is complete, add a build step to `validate-json.yml` that **fails the build** if any directory contains a `content.json` without a sibling `manifest.json`. This enforces the invariant that every package is fully migrated and prevents regressions (e.g., new guides committed without a manifest).

**Implementation:** Add a step to the `validate-guides` job after the existing per-file validation loop:

```yaml
- name: Enforce manifest.json for all packages
  run: |
    missing=()
    while IFS= read -r content_file; do
      dir="$(dirname "$content_file")"
      if [ ! -f "$dir/manifest.json" ]; then
        missing+=("$content_file")
      fi
    done < <(find . -name "content.json" -not -path "*/node_modules/*" -not -path "*/.git/*")
    if [ ${#missing[@]} -gt 0 ]; then
      echo "ERROR: content.json found without manifest.json in the following locations:"
      printf '  %s\n' "${missing[@]}"
      exit 1
    fi
    echo "All packages have manifest.json."
```

**When to enable:** Enable this step only after the full migration is complete (all guides have `manifest.json`). Until then, leave it commented out or gated behind a condition, since it would fail on every un-migrated guide. A practical trigger is the completion of `index.json` retirement — at that point the invariant must hold for the recommender to function correctly.

### Legacy deploy cleanup

Once it has been demonstrated that no recommender path depends on `index.json` or the `guides/` prefix on the CDN (i.e., all traffic has moved to `packages/` + `repository.json`):

1. Remove the "Prepare tutorial files" step from `deploy.yml` that stages and publishes the `guides/` tree
2. Remove the `guides/` push-to-GCS step
3. Remove `index.json` from the repository (if not already done as part of `index.json` retirement above)
4. Remove the `validate-recommender-rules` CI job (if not already removed)
5. Optionally, drain the `guides/` bucket prefix on the CDN once confirmed no consumers remain

**Gate:** Do not remove the `guides/` deploy step until you have verified — via recommender logs, CDN access logs, or integration tests — that zero live traffic is fetching from `guides/`. The `packages/` path must be serving successfully in production first.

---

## Appendix: Data sources for migration

### index.json

Location: `interactive-tutorials/index.json`

Each rule provides: `title`, `url`, `description`, `type`, `match` (targeting expression). The `url` field's path segment identifies which guide the rule belongs to.

### Website learning path markdown

Location: `<website-repo>/content/docs/learning-paths/` (default local checkout: `/Users/davidallen/hax/website/content/docs/learning-paths/`)

Structure:
```
learning-paths/
├── _index.md                  ← global learning paths metadata
├── journeys.yaml              ← inter-journey relationships (category, links.to)
├── prometheus/
│   ├── _index.md              ← path-level: title, description, journey.group, journey.links, related_journeys
│   ├── add-data-source/
│   │   └── index.md           ← step-level: weight, step, pathfinder_data, description, side_journeys
│   └── ...
└── ...
```

Key frontmatter fields:

| Level | Field | Maps to |
|-------|-------|---------|
| Path `_index.md` | `title` | Path content.json `title` |
| Path `_index.md` | `description` | manifest `description` |
| Path `_index.md` | `journey.group` | manifest `category` |
| Path `_index.md` | `journey.skill` | (deferred — `difficulty` not in Phase 1 schema) |
| Path `_index.md` | `journey.links.to` | manifest `recommends` |
| Path `_index.md` | `related_journeys.items` | manifest `suggests` or `depends` |
| Path `_index.md` | body content | Path content.json `blocks` (see [path-level content.json authoring](#path-level-contentjson-authoring)) |
| Step `index.md` | `weight` | Step ordering within `steps` array |
| Step `index.md` | `step` | Step number (redundant with weight-based ordering) |
| Step `index.md` | `pathfinder_data` | Maps step markdown to interactive-tutorials directory |
| Step `index.md` | `description` | Step manifest `description` |
| Step `index.md` | `side_journeys` | Step manifest `suggests` |

### journeys.yaml

Location: `learning-paths/journeys.yaml`

Provides inter-journey category and `links.to` relationships at the journey graph level. The `id` field maps to the learning path directory name (with different naming conventions than the `*-lj` suffix used in interactive-tutorials).

---

## Appendix: Naming conventions

See [`docs/manifest-reference.md`](manifest-reference.md) under "Naming conventions" for the directory name mapping rules between repos.

The full set of `*-lj` directories is ongoingly changing — authors continue to write new learning journeys on parallel branches during this migration. This is why we pilot on a subset and create a generic, reusable migration skill for the rest.
