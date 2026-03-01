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

## Phase 0: Documentation

**Goal:** Authors and agents have a reference for writing `manifest.json` in this repository, with field derivation rules specific to this repo's conventions.

### Deliverables

- [ ] **`docs/manifest-reference.md`** — Manifest field reference adapted for this repository. Covers:
  - Package directory structure (`content.json` + `manifest.json`)
  - Field-by-field reference for `manifest.json` with types, required/optional, defaults
  - Field derivation rules for migration (where each field's data comes from — see [field derivation rules](#field-derivation-rules) below)
  - Targeting: how to translate an `index.json` rule into `targeting.match`
  - testEnvironment: tier inference rules (local, cloud, play)
  - Learning path manifests: `type: "path"`, `steps` array, path-level `content.json`
  - Dependency fields: `depends`, `recommends`, `suggests`, `provides`
  - Copy-paste templates for standalone guide and learning path

  The canonical manifest schema can be obtained at any time by running `node dist/cli/cli/index.js schema manifest` from a pathfinder-app checkout. `docs/manifest-reference.md` should reference this as the authoritative schema source rather than duplicating it.

- [ ] **Update `.cursor/authoring-guide.mdc`** — Add a documentation map entry pointing to `docs/manifest-reference.md` and a brief section on manifest authoring.

- [ ] **Update `AGENTS.md`** — Add task routing entries for manifest authoring and migration.

### Field derivation rules

These rules codify where each manifest field's data comes from during migration. The principle is **maximally complete from existing data, no guessing or inventing**.

| Field | Source | Derivation |
|-------|--------|------------|
| `id` | `content.json` | Copy the `id` field verbatim |
| `type` | Directory structure | `"guide"` for standalone guides and LJ steps; `"path"` for `*-lj` directories |
| `repository` | Constant | `"interactive-tutorials"` (the schema default; can be omitted) |
| `description` | `index.json` rule | Copy the `description` field from the matching rule. For LJ steps without an index.json entry, derive from the website markdown frontmatter `description` field |
| `category` | Website markdown | For learning paths: `journey.group` from the path-level `_index.md` frontmatter (e.g., `journey: { group: data-availability }` → `"data-availability"`). For standalone guides: use the learning path's `journey.group` if the guide belongs to one, otherwise default to `"general"` and note the default |
| `author` | Constant for pilot | `{ "team": "interactive-learning" }` — all content in this repo is currently authored by the same team |
| `language` | Constant | `"en"` (the default; can be omitted) |
| `startingLocation` | `index.json` rule | Recursively traverse the `match` expression (`and`/`or` combinators) and pick the first URL-bearing leaf (`urlPrefix` value or first entry of `urlPrefixIn`). If the best choice is ambiguous from context, pick the first one found and note the choice in the generated `manifest.json`. Falls back to `"/"` if no URL rule exists |
| `targeting.match` | `index.json` rule | Copy the `match` object from the matching rule verbatim |
| `testEnvironment.tier` | `index.json` rule | If the `match` expression contains a `source` rule (at any nesting depth), then `"cloud"`. If `match` contains `"targetPlatform": "cloud"` (without a `source` rule), then `"cloud"`. Otherwise `"local"`. If ambiguous, note the ambiguity in the generated manifest |
| `testEnvironment.instance` | `index.json` rule | If the `match` expression contains a `source` rule, set to that value (e.g., `"play.grafana.org"`). Otherwise omit |
| `depends` | Website markdown | For LJ steps: step N+1 `depends` on step N (first step has no `depends`). For standalone guides: leave empty unless explicit |
| `recommends` | Website markdown | For LJ steps: step N `recommends` step N+1 (last step has no `recommends`). At the path level: from `journey.links.to` in `_index.md`. At the step level: also from `side_journeys` in step markdown |
| `suggests` | Website markdown | From `related_journeys` in path-level `_index.md` |
| `provides` | Guide semantics | Infer from what the guide accomplishes (e.g., a data source setup guide provides `"datasource-configured"`). Leave empty when not obvious |
| `steps` | Website markdown | For `type: "path"`: ordered list of step package IDs, derived from the step markdown `weight` field ordering. The `pathfinder_data` frontmatter field maps each markdown step to its `interactive-tutorials` directory |

### Matching index.json rules to guides

The `index.json` `url` field contains the CDN URL for the guide (e.g., `https://interactive-learning.grafana.net/guides/alerting-101`). Some URLs have a trailing `/content.json` — strip it before matching. The guide directory name is the last path segment after stripping. Packages are identified by directory, not by file; either `content.json` or `manifest.json` can be resolved within the directory.

Match by comparing the guide's `id` (from `content.json`) against the directory name extracted from each rule's `url`.

For learning journey steps, individual steps typically don't have their own `index.json` entries — targeting lives at the path level. Step-level manifests have no `targeting` field unless the step has its own `index.json` entry. Step-level `description` comes from the website markdown.

---

## Phase 1: Migration skill

**Goal:** A reusable agent skill that atomically migrates one guide or one learning path to the package format.

### Skill design principles

- **References, not duplication.** The skill focuses on migration logic — field mapping, data source lookup, conflict detection. It does not duplicate documentation on manifest format, guide authoring rules, or content conventions. Instead, it references the Phase 0 docs (`docs/manifest-reference.md`) and the existing authoring guide (`.cursor/authoring-guide.mdc`) by inclusion. This follows the repo's tiered context access pattern.

- **Parallel-safe.** The skill operates on a single directory in isolation. It reads shared resources (`index.json`, website markdown) but never modifies them. Multiple agents can run the skill on different guides simultaneously without risk of stepping on each other.

- **Never modifies existing content.json.** The skill may create a new `content.json` (e.g., a path-level cover page) but must never modify an existing one. As a verification step, the skill confirms that every `content.json` in scope was either pre-existing (unchanged) or newly created.

- **Never modifies index.json.** The skill reads `index.json` for targeting data but never writes to it.

### Deliverables

- [ ] **`.cursor/skills/migrate-guide/SKILL.md`** — Single skill with two modes:

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

  **Metadata conflict resolution:** The website markdown `_index.md` is the authoritative source for path-level metadata (title, description, category, learning objectives, prerequisites). However, metadata may exist in multiple places — `index.json`, `journeys.yaml`, the markdown frontmatter, and the markdown body. If any path-level metadata in `_index.md` differs from or contradicts what is found elsewhere (e.g., a different description in `index.json`, a different category in `journeys.yaml`), the skill must **flag the conflict for manual resolution** by the user rather than silently picking one source. The agent should present both values and ask the user which to use.

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
   - Strip Hugo shortcodes (`{{< ... >}}`, `{{< /... >}}`) — these are rendering directives, not content
   - Convert the remaining markdown body into one or more `markdown` blocks
   - Preserve learning objectives, prerequisites, and descriptive prose — these provide value as the path's introductory page
   - Images referenced via markdown syntax (`![alt](url)`) can be retained as-is in the markdown block content; the Pathfinder renderer will handle them

**Example:** For `prometheus-lj`, the path-level `content.json` would contain the title "Connect to a Prometheus data source in Grafana Cloud" and markdown blocks covering: what Prometheus is, what the journey teaches, learning objectives (the 5-point list), and prerequisites.

---

## Phase 2: Pilot migration (content)

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

- [ ] **Standalone guide manifests** — Run the migration skill on each pilot guide. Each produces a `manifest.json` alongside the existing `content.json`.

- [ ] **Learning path migration** — Run the migration skill on `prometheus-lj/`. Produces:
  - `prometheus-lj/manifest.json` (`type: "path"`, `steps` array with 9 entries)
  - `prometheus-lj/content.json` (path-level descriptive content from website markdown)
  - `prometheus-lj/<step>/manifest.json` for each of the 9 steps

- [ ] **Validation** — All migrated packages pass `validate --package` / `validate --packages`

- [ ] **index.json unchanged** — Existing entries remain; no entries removed or modified

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

## Phase 3: CI integration

**Goal:** CI validates packages and generates `repository.json` on every push/PR.

### Deliverables

- [ ] **Extend `validate-json.yml`** with a new job (or extend the existing `validate-guides` job):
  - After building the pathfinder CLI, run `validate --packages .` to validate all package directories (those with `manifest.json`)
  - Run `build-repository . -o repository.json` to generate `repository.json` from all packages
  - Run `build-graph` for dependency visualization (informational, not blocking)
  - Upload `repository.json` as a CI artifact for inspection

- [ ] **Validation scope** — `validate --packages` validates only directories that contain `manifest.json`. Directories with only `content.json` (un-migrated guides) are still validated by the existing per-file validation loop. Both validations coexist.

- [ ] **repository.json paths** — The `build-repository` command produces entries with paths relative to the repository root (e.g., `"path": "alerting-101/"`). These are also relative to the CDN publication root since the deploy step copies the repo structure into the `guides/` bucket prefix.

### CI job ordering

```
validate-recommender-rules (index.json)     ← existing, unchanged
validate-guides (content.json per-file)      ← existing, unchanged
validate-packages (manifest.json packages)   ← new
build-repository (repository.json)           ← new
```

The `validate-packages` and `build-repository` jobs depend on the pathfinder CLI being built, which the existing `validate-guides` job already does. They can share that build step or run in the same job.

---

## Phase 4: Deploy pipeline

**Goal:** The deploy pipeline publishes `repository.json` to the CDN alongside guide content.

### Deliverables

- [ ] **Extend `deploy.yml`** to include a build + publish step for `repository.json`:
  1. Checkout pathfinder-app and build CLI (same pattern as validate-json.yml)
  2. Run `build-repository . -o guides/repository.json`
  3. The existing "Prepare tutorial files" step already copies guide directories into `guides/`
  4. `repository.json` is published alongside `index.json` at the bucket root: `guides/repository.json`

- [ ] **Verify relative paths** — `repository.json` entries use paths relative to the publication root. For example, `"path": "alerting-101/"` resolves to `https://interactive-learning.grafana.net/guides/alerting-101/content.json` when the CDN base URL is `https://interactive-learning.grafana.net/guides/`.

- [ ] **Manifest files deployed** — The existing deploy step copies `*.json` from guide directories, which already includes `manifest.json` files. Verify that `manifest.json` files are deployed alongside `content.json`.

- [ ] **Future: simplify deploy to copy entire repo** — In a later stage, the deploy pipeline should be upgraded to copy the near-entirety of the repo to the CDN (all `*.json`, all `assets/*`, `repository.json`) rather than discovering files individually. This removes the need for the pipeline to track which files each package includes. The current `find` + `cp *.json` approach works for the pilot but won't scale to packages with assets.

### CDN structure after deploy

```
interactive-learning-{env}/guides/
├── index.json                     ← existing
├── repository.json                ← new
├── shared/                        ← existing
├── alerting-101/
│   ├── content.json
│   └── manifest.json              ← new
├── prometheus-lj/
│   ├── content.json               ← new (path cover page)
│   ├── manifest.json              ← new
│   ├── add-data-source/
│   │   ├── content.json
│   │   └── manifest.json          ← new
│   └── ...
└── ... (all other guides, unchanged)
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

---

## Appendix: Data sources for migration

### index.json

Location: `interactive-tutorials/index.json`

Each rule provides: `title`, `url`, `description`, `type`, `match` (targeting expression). The `url` field's path segment identifies which guide the rule belongs to.

### Website learning path markdown

Location: `/Users/davidallen/hax/website/content/docs/learning-paths/`

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

The general rule for mapping between repos is **strip the `-lj` suffix** from the `interactive-tutorials` directory name to get the corresponding `website/content/docs/learning-paths/` directory name (e.g., `prometheus-lj` → `prometheus`, `linux-server-integration-lj` → `linux-server-integration`).

The full set of `*-lj` directories is ongoingly changing — authors continue to write new learning journeys on parallel branches during this migration. This is why we pilot on a subset and create a generic, reusable migration skill for the rest.

Within paths, step directory names are identical in both repos. The website markdown `pathfinder_data` frontmatter field is the authoritative link: e.g., `pathfinder_data: prometheus-lj/add-data-source` maps the website step to the `interactive-tutorials/prometheus-lj/add-data-source/` directory.
