---
name: migrate-guide
description: Migrate a standalone guide or learning path to the Pathfinder package format by generating manifest.json (and path-level content.json for LJs). Reads content.json, index.json, and optionally website markdown to derive all manifest fields. Use when the user wants to migrate a guide directory to the package format, or asks to create a manifest.json for a guide.
---

# Migrate Guide to Package Format

Migrate a single guide directory or a learning path (`*-lj`) to the Pathfinder two-file package model (`content.json` + `manifest.json`). The skill is invoked on one directory at a time and is safe to run in parallel across different directories.

**Read these reference documents on demand** for field-level detail:
- `docs/manifest-reference.md` — authoritative derivation rules, templates, naming conventions, fallbacks
- `.cursor/authoring-guide.mdc` — guide content conventions (for path-level content.json authoring)

Keep this skill focused on workflow/orchestration. Do not duplicate field derivation tables from `docs/manifest-reference.md`.

---

## Safety Invariants

These rules are **inviolable** — the skill must never break them:

1. **Never modify an existing `content.json`.** The skill may *create* a new `content.json` (path-level cover page) but must never modify one that already exists.
2. **Never modify `index.json`.** Read it as a data source; never write to it.
3. **Verify after writing.** Before any writes, snapshot every in-scope pre-existing `content.json` as raw bytes (or SHA-256). After writes, confirm each snapshot is byte-identical.

---

## Mode Detection

Determine the mode from the target directory:

| Condition | Mode |
|-----------|------|
| Directory name ends with `-lj` OR a directory contains other nested directories with `content.json` | **Mode 2: Learning path** |
| Otherwise | **Mode 1: Standalone guide** |

---

## Data Sources

### index.json (read-only)

Location: `index.json` (repo root)

Each rule has: `title`, `url`, `description`, `type`, `match`. Match a rule to a guide by:
1. Strip any trailing `/content.json` from the rule's `url`
2. Extract the last path segment (e.g., `alerting-101`)
3. Compare against the guide's directory name or `content.json` `id`

If no rule matches, the guide has no targeting — omit the `targeting` field.

### Website learning path markdown (read-only, optional)

Location: `/Users/davidallen/hax/website/content/docs/learning-paths/`

Map `*-lj` directory names to website paths by stripping the `-lj` suffix (e.g., `prometheus-lj` → `prometheus`). Step directory names are identical in both repos. The website markdown `pathfinder_data` frontmatter provides the authoritative mapping.

If the website repo is unavailable, apply fallback rules from `docs/manifest-reference.md` under "When website markdown is unavailable" and flag affected fields for manual review.

### journeys.yaml (read-only, optional)

Location: `/Users/davidallen/hax/website/content/docs/learning-paths/journeys.yaml`

Provides inter-journey category and relationship data.

---

## Mode 1: Standalone Guide

Invoked on a guide directory (e.g., `alerting-101/`).

### Steps

#### 1. Read content.json

Read `{dir}/content.json` and extract the `id` and `title` fields. **Do not modify this file.**

#### 2. Look up matching index.json rule

Read `index.json` from the repo root. Find the rule whose `url` path segment matches the directory name or the `content.json` `id`. Record:
- `description` from the rule
- `match` object from the rule
- `startingLocation`: traverse the `match` expression depth-first, left-to-right and pick the first URL-bearing leaf (`urlPrefix` value or first entry of `urlPrefixIn`). Falls back to `"/"`.

If no rule matches, record that targeting is absent.

#### 3. Check for website markdown (if step is inside a `*-lj`)

If this guide directory is a direct child of a `*-lj` directory, look up the parent path's website markdown `_index.md` and extract `journey.group` for the `category` field. Otherwise, `category` defaults to `"general"`.

#### 4. Derive testEnvironment

Apply these rules against the `match` expression (most-specific-first):

| Condition | Result |
|-----------|--------|
| `match` contains `source: "play.grafana.org"` at any depth | `{ "tier": "play", "instance": "play.grafana.org" }` |
| `match` contains a `source` rule (non-play) at any depth | `{ "tier": "cloud", "instance": "<source value>" }` |
| `match` contains `"targetPlatform": "cloud"` (without `source`) | `{ "tier": "cloud" }` |
| Otherwise | `{ "tier": "local" }` |

#### 5. Generate manifest.json

Write `{dir}/manifest.json` with the derived fields:

```json
{
  "id": "<from content.json>",
  "type": "guide",
  "description": "<from index.json rule, or flag for manual entry>",
  "category": "<from journey.group if inside *-lj, else 'general'>",
  "author": { "team": "interactive-learning" },
  "startingLocation": "<first URL from match, or '/'>",
  "targeting": {
    "match": { "<copied verbatim from index.json rule>" }
  },
  "testEnvironment": {
    "tier": "<local|cloud|play>",
    "instance": "<if applicable>"
  }
}
```

Field omission rules:
- Omit `repository` (schema default `"interactive-tutorials"` applies)
- Omit `language` (schema default `"en"` applies)
- Omit `targeting` entirely if no index.json rule matched
- Omit `testEnvironment.instance` if tier is `"local"`
- Omit `depends`, `recommends`, `suggests`, `provides` when empty (standalone guides generally have no dependency info unless explicitly known)

#### 6. Validate

- Confirm `id` matches between `content.json` and `manifest.json`
- Confirm the generated JSON is syntactically valid
- Confirm no existing `content.json` was modified by byte-level comparison against the pre-write snapshot (raw bytes or SHA-256)

#### 7. Run package validation (required)

Run:

```bash
node dist/cli/cli/index.js validate --package <dir>
```

This validation attempt is required for Phase 1 migration. If the command cannot run (CLI missing/unbuilt), treat this as an incomplete migration and explicitly report the blocker.

#### 8. Report

Tell the user:
- Which manifest was created
- Which fields were derived from which sources
- Result of `validate --package`
- Any fields that need manual review (e.g., no index.json rule found, fallback used)

---

## Mode 2: Learning Path

Invoked on a `*-lj` directory (e.g., `prometheus-lj/`).

### Steps

#### 1. Locate website markdown

Map the directory name to the website path by stripping `-lj` (e.g., `prometheus-lj` → `prometheus`). Check for `/Users/davidallen/hax/website/content/docs/learning-paths/<path-name>/`.

If not found, apply fallback rules and flag for manual review.

#### 2. Read path-level metadata

Read `_index.md` from the website path. Extract from frontmatter:
- `title` — for path-level content.json and manifest
- `description` — for manifest
- `journey.group` — for `category`
- `journey.skill` — note but defer (not in current schema)
- `journey.links.to` — for `recommends`
- `related_journeys.items` — for `suggests` (default) or `depends` (only if unambiguously prerequisite)

Extract from body content:
- All prose, learning objectives, prerequisites — for path-level content.json blocks

#### 3. Read step metadata

Build a canonical step map from website markdown. For each `<website-step>/index.md` in the website path, extract:
- `weight` — for ordering within the `steps` array
- `step` — step number (redundant with weight ordering, use as cross-check)
- `pathfinder_data` — authoritative mapping to the interactive-tutorials directory (e.g., `prometheus-lj/add-data-source`)
- `description` — for step manifest
- `side_journeys` — for step `suggests`

Canonical mapping rules:
- Treat `pathfinder_data` as authoritative for mapping website steps to interactive-tutorials step directories.
- Validate each `pathfinder_data` target exists under the `*-lj` directory and has `content.json`.
- Build the path manifest `steps` array from this map, ordered by `weight`.
- Do not derive step order from local directory listing.

#### 4. Migrate each step (Mode 1)

For each mapped step in canonical `weight` order:

1. Read the step's `content.json` to get `id` and `title` (**do not modify**)
2. Check if the step has its own `index.json` entry (most steps don't — targeting lives at the path level)
3. Resolve description source in priority order:
   - Website step `index.md` `description`
   - Matching step-level `index.json` rule `description` (if present)
   - If neither exists: **stop and request manual description** for that step (required field; do not guess)
4. Generate `{step-dir}/manifest.json`:

```json
{
  "id": "<from step content.json>",
  "type": "guide",
  "description": "<from step index.md description>",
  "category": "<from parent path journey.group>",
  "author": { "team": "interactive-learning" },
  "depends": ["<previous-step-id>"],
  "recommends": ["<next-step-id>"]
}
```

Step dependency rules:
- First step: omit `depends`
- Step N+1: `depends` on step N's `id`
- Last step: omit `recommends` (no next step)
- Step N: `recommends` step N+1's `id`
- If the step has `side_journeys`, map them to `suggests`

Omit `targeting` unless the step has its own `index.json` entry.

#### 5. Check for metadata conflicts

Compare metadata across sources (website markdown frontmatter, `index.json` rule if present, `journeys.yaml`). A conflict exists when the same field has different string values in two sources.

**Flag conflicts for the user** — present both values and ask which to use. Do not silently pick one.

#### 6. Look up path-level index.json rule

Check if the `*-lj` directory name (or a URL containing it) has an entry in `index.json`. Extract `match` for `targeting` and derive `startingLocation` and `testEnvironment` using the same rules as Mode 1.

#### 7. Generate path-level manifest.json

Write `{lj-dir}/manifest.json`:

```json
{
  "id": "<lj-directory-name>",
  "type": "path",
  "description": "<from _index.md description>",
  "category": "<from journey.group>",
  "author": { "team": "interactive-learning" },
  "startingLocation": "<from index.json match, or '/'>",
  "targeting": {
    "match": { "<from index.json rule if exists>" }
  },
  "testEnvironment": {
    "tier": "<from index.json rule>"
  },
  "steps": [
    "<step-1-id>",
    "<step-2-id>",
    "..."
  ],
  "recommends": ["<from journey.links.to>"],
  "suggests": ["<from related_journeys>"]
}
```

Omit `targeting` if no index.json rule exists for the path.
Omit `recommends`/`suggests`/`depends` when empty.

#### 8. Create path-level content.json

**Only if `{lj-dir}/content.json` does not already exist.** If it exists, do not touch it.

Derive from `_index.md` body content:

```json
{
  "id": "<lj-directory-name>",
  "title": "<from _index.md title>",
  "blocks": [
    {
      "type": "markdown",
      "content": "<body content with Hugo shortcodes stripped>"
    }
  ]
}
```

Content transformation rules:
- Strip Hugo shortcode tags (`{{< ... >}}`, `{{< /... >}}`)
- For wrapping shortcodes (e.g., `{{< admonition >}}...{{< /admonition >}}`), strip tags but preserve inner content
- Convert remaining markdown into one or more `markdown` blocks
- Preserve learning objectives, prerequisites, and descriptive prose
- Images referenced via markdown syntax can be retained as-is
- Do NOT add a markdown title (`## Title`) — the `title` field handles that

#### 9. Validate

- Confirm `id` consistency: path manifest `id` matches the directory name, step manifest `id` matches step `content.json` `id`
- Confirm `steps` array in path manifest references valid step IDs that exist in step content.json files
- Confirm step ordering matches website `weight` ordering
- Confirm no pre-existing `content.json` in scope was modified by byte-level comparison against pre-write snapshots (including existing path-level `content.json`, if present)
- Confirm all generated JSON is syntactically valid

#### 10. Run package validation (required)

Run:

```bash
node dist/cli/cli/index.js validate --package <lj-dir>
```

If you created step-level manifests, also run `validate --package <step-dir>` for each created/updated step package.

This validation attempt is required for Phase 1 migration. If the command cannot run (CLI missing/unbuilt), treat this as an incomplete migration and explicitly report the blocker.

#### 11. Report

Tell the user:
- Path-level manifest and content.json created
- N step manifests created (list them)
- Fields derived from each source
- Results of all `validate --package` commands
- Any conflicts flagged
- Any fields that need manual review
- Any fallbacks used due to missing website markdown

---

## Reference-First Derivation

For all field derivation logic and fallback rules, use `docs/manifest-reference.md` as the authoritative source:
- `startingLocation` extraction
- `testEnvironment` tier inference
- website-markdown fallback behavior

Only include migration-specific orchestration logic in this skill. If this skill and `docs/manifest-reference.md` disagree, follow `docs/manifest-reference.md` and report the mismatch.

---

## Post-Migration Validation

After generating all files, run this checklist:

- [ ] Every `manifest.json` has a matching `content.json` in the same directory
- [ ] `id` matches between each `manifest.json` and `content.json` pair
- [ ] No pre-existing `content.json` was modified (byte-level check against pre-write snapshots)
- [ ] `index.json` was not modified
- [ ] Path manifests have `type: "path"` and a `steps` array
- [ ] Step manifests have `type: "guide"`
- [ ] Step `depends`/`recommends` chains are consistent (no broken references)
- [ ] JSON is syntactically valid in all generated files
- [ ] `node dist/cli/cli/index.js validate --package <dir>` was run for each generated package (or a blocker was explicitly reported)

---

## Error Handling

### No index.json rule found
Generate the manifest without `targeting`, `startingLocation` defaults to `"/"`, `testEnvironment` defaults to `{ "tier": "local" }`. Flag for user review — the guide may be path-only (reachable via learning path, not contextual recommendation).

### Website markdown not found
Apply fallback rules. Clearly state which fields used fallback values and need manual review.

### Missing required step description during LJ fallback
Try, in order:
1. Website step `index.md` `description`
2. Step-level `index.json` rule `description` (if any)
3. If still missing, stop and ask the user for that step's description (required manifest field). Do not invent one.

### content.json missing in a step directory
This is unexpected. Report the missing file and skip that step. Do not create a content.json for a step — that is the content author's responsibility, not the migration skill's.

### Metadata conflict between sources
Present both values to the user, state which source each came from, and ask the user to choose. Do not guess.

---

## Example Invocations

### Standalone guide
> "Migrate `alerting-101/` to the package format"

The skill reads `alerting-101/content.json` (id: `alerting-101`), finds the matching `index.json` rule, and generates `alerting-101/manifest.json`.

### Learning path
> "Migrate `prometheus-lj/` to the package format"

The skill reads all 9 step `content.json` files, the website markdown at `learning-paths/prometheus/`, and the index.json. It generates:
- `prometheus-lj/manifest.json` (type: path, 9 steps)
- `prometheus-lj/content.json` (path-level cover page from website markdown)
- 9 step-level `manifest.json` files
