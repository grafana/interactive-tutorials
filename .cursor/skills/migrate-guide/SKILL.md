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

Map `*-lj` directory names to website paths by stripping the `-lj` suffix (e.g., `prometheus-lj` → `prometheus`). Step directory names are identical in both repos. The website markdown `pathfinder_data` frontmatter provides the authoritative mapping when present, but most steps lack it — fall back to directory name matching (see step 3 canonical mapping rules).

If the website repo is unavailable, apply fallback rules from `docs/manifest-reference.md` under "When website markdown is unavailable" and flag affected fields for manual review.

### journeys.yaml (read-only, optional)

Location: `/Users/davidallen/hax/website/content/docs/learning-paths/journeys.yaml`

Provides inter-journey category and relationship data.

---

## Description Conventions

The `description` field is a **compact, one-line summary** suitable for a course catalog listing. It is not introductory prose — that belongs in the `content.json` markdown blocks.

**Priority for resolving `description`:**

1. **`index.json` rule** — if the guide has a matching rule, use its `description` verbatim. These are already written in catalog style.
2. **Summarize available sources** — if no `index.json` rule exists, collect all available description sources (website markdown frontmatter `description`, `content.json` title, path-level metadata) and boil them down into a single sentence. Write it in the style of the `index.json` descriptions (e.g., "Hands-on guide: Learn how to...").
3. **Ask the user** — if no sources exist at all, stop and request a description. Do not invent one.

---

## Author Conventions

The `author` field has a `team` value that depends on content type:

| Content type | `author.team` |
|-------------|---------------|
| Learning path (`type: "path"`) | `"Grafana Documentation"` |
| Step within a learning path (inside a `*-lj` directory) | `"Grafana Documentation"` |
| Standalone guide (not inside a `*-lj` directory) | `"interactive-learning"` |

`"interactive-learning"` is the fallback default when content type is unknown. If you know the content is a learning path or a step within one, always use `"Grafana Documentation"`.

The `author.name` field is optional. To derive it:
1. Look at all git revisions since the `content.json` file was created (use `git log --follow` to track renames)
2. Extract the GitHub handles (not full names) of all commit authors
3. Exclude any obvious automation or bot authors (e.g., `dependabot`, `renovate`, `github-actions`, `bot`, etc.)
4. If multiple authors remain, comma-separate their GitHub handles
5. If no authors remain after filtering bots, or if unsure, omit `name` entirely

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
- `startingLocation`: traverse the `match` expression recursively, collect all URL-bearing leaves (`urlPrefix` values and entries from `urlPrefixIn` arrays), then pick the first one. If no URL can be extracted, omit `startingLocation` entirely — a missing value is preferable to a wrong one.

If no rule matches, record that targeting is absent.

#### 3. Check for website markdown (if step is inside a `*-lj`)

If this guide directory is a direct child of a `*-lj` directory, look up the parent path's website markdown `_index.md` and extract `journey.group` for the `category` field. Otherwise, `category` defaults to `"general"`.

#### 4. Derive testEnvironment

**`testEnvironment` must NEVER be omitted.** Every manifest must include it.

Apply these rules in order:

**IF match expression exists (and is not empty):**
- **IF** `match` contains `source` at any depth (any host, including `play.grafana.org`) → `{ "tier": "cloud", "instance": "<source value>" }`
- **ELSE IF** `match` contains `"targetPlatform": "cloud"` → `{ "tier": "cloud" }`
- **ELSE** → `{ "tier": "local" }`

**ELSE (no match expression or match expression is empty):**
- → `{ "tier": "cloud" }` (minimum default)

Note: An empty match expression (`match: {}`) is treated the same as no match expression — both default to `"cloud"`.

#### 5. Generate manifest.json

Write `{dir}/manifest.json` with the derived fields:

```json
{
  "id": "<from content.json>",
  "type": "guide",
  "description": "<compact one-line summary; see Description Conventions>",
  "category": "<from journey.group if inside *-lj, else 'general'>",
  "author": { "team": "<see Author Conventions>" },
  "startingLocation": "<first URL from match, if derivable>",
  "targeting": {
    "match": { "<copied verbatim from index.json rule>" }
  },
  "testEnvironment": {
    "tier": "<local|cloud|play>",
    "instance": "<if applicable>"
  },
  "depends": [],
  "recommends": [],
  "suggests": [],
  "provides": []
}
```

Field omission rules:
- Omit `repository` (schema default `"interactive-tutorials"` applies)
- Omit `language` (schema default `"en"` applies)
- Omit `targeting` entirely if no index.json rule matched
- Omit `startingLocation` if no URL can be derived from the match expression — do not fall back to `"/"`. A missing value is preferable to a wrong one.
- **Never omit `testEnvironment`.** Minimum is `{ "tier": "cloud" }`. Omit `instance` when no instance value is available.
- Always include `depends`, `recommends`, `suggests`, and `provides` — even when empty (`[]`). This makes the fields visible to authors so they know they can fill them out later. Never invent values; use `[]` when no information is available.

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

#### 8. Write migration notes

Write `{dir}/assets/migration-notes.md` following the [migration notes convention](#migration-notes). Include:
- Which manifest was created and when
- Which fields were derived from which sources
- Result of `validate --package`
- Any fields that need manual review (e.g., no index.json rule found, fallback used)
- Any dangling references
- Any surprises or unexpected situations

#### 9. Report

Tell the user:
- Which manifest was created
- Which fields were derived from which sources
- Result of `validate --package`
- Any fields that need manual review
- Summary of migration notes written

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
- `description` — a source for the manifest description (apply [Description Conventions](#description-conventions): if there is an `index.json` rule for this path, prefer its description; otherwise condense the `_index.md` description into a compact one-line catalog summary)
- `journey.group` — for `category`
- `journey.skill` — note but defer (not in current schema)
- `journey.links.to` — for `recommends`
- `related_journeys.items` — for `suggests` (default) or `depends` (only if unambiguously prerequisite). **Relationship strength heuristic:** when the `related_journeys.heading` text says "before" or "prerequisite" but the body content qualifies the relationship (e.g., "while not required"), use `suggests`. The body-level qualification takes precedence over the heading-level framing. Only use `depends` when both the heading *and* the body unambiguously describe a hard prerequisite with no "optional" or "recommended" qualifier.

Extract from body content:
- All prose, learning objectives, prerequisites — for path-level content.json blocks

#### 3. Read step metadata

Build a canonical step map from website markdown. For each `<website-step>/index.md` in the website path, extract:
- `weight` — for ordering within the `steps` array
- `step` — step number (redundant with weight ordering, use as cross-check)
- `pathfinder_data` — authoritative mapping to the interactive-tutorials directory (e.g., `prometheus-lj/add-data-source`)
- `description` — for step manifest
- `side_journeys` — for step `suggests` (see step 3a below for URL-to-ID resolution)

Canonical mapping rules:
- When present, treat `pathfinder_data` as authoritative for mapping website steps to interactive-tutorials step directories. Validate each target exists under the `*-lj` directory and has `content.json`.
- **When `pathfinder_data` is absent** (common — most steps lack it), fall back to directory name matching: website step directory names are identical to interactive-tutorials step directory names within the same path. Confirm the match by verifying the directory exists and has `content.json`. Note which steps used name-matching fallback in the migration notes.
- Build the path manifest `steps` array from this map, ordered by `weight`.
- Do not derive step order from local directory listing.

#### 3a. Resolve side_journeys URLs to package IDs

For each step's `side_journeys.items`, check whether any link matches the pattern `/docs/learning-paths/<name>/`. If so, resolve `<name>` to `<name>-lj` and check whether that directory exists in this repo. If the directory exists, add its ID to the step's `suggests` array. If the directory does not exist, the reference is still included (it may point to a not-yet-migrated path) — note it as a dangling reference in the migration notes.

Links that do not match the learning path URL pattern (external docs, YouTube URLs, etc.) are not mappable to package IDs and should be ignored.

#### 4. Migrate each step (Mode 1)

For each mapped step in canonical `weight` order:

1. Read the step's `content.json` to get `id` and `title` (**do not modify**)
2. Check if the step has its own `index.json` entry (most steps don't — targeting lives at the path level)
3. Resolve description following the [Description Conventions](#description-conventions):
   1. Matching step-level `index.json` rule `description` (first priority — already catalog-style)
   2. Website step `index.md` `description` — if multi-sentence or verbose, condense to one line
   3. Summarize from step `content.json` title + any other available context into a single catalog-style sentence
   4. If no sources exist at all: **stop and request manual description** (required field; do not guess)
4. Generate `{step-dir}/manifest.json`:

```json
{
  "id": "<from step content.json>",
  "type": "guide",
  "description": "<compact one-line summary; see Description Conventions>",
  "category": "<from parent path journey.group>",
  "author": { "team": "Grafana Documentation" },
  "testEnvironment": {
    "tier": "<inherited from path, or 'cloud' minimum>"
  },
  "depends": ["<previous-step-id>"],
  "recommends": ["<next-step-id>"],
  "suggests": [],
  "provides": []
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

#### 5a. Cross-validate journey.links.to against journeys.yaml

Read `journeys.yaml` and find the entry whose `id` maps to the current learning path (e.g., `prom-data-source` for `prometheus-lj`). Compare the `links.to` values from `journeys.yaml` against the `journey.links.to` values from the `_index.md` frontmatter. If the IDs differ (e.g., `metrics-drilldown` in journeys.yaml vs `drilldown-metrics` in `_index.md`), flag the mismatch as a data quality issue in the migration notes. Use the `_index.md` value as authoritative (it maps to actual directory names in this repo) but record both values so the website team can reconcile the inconsistency.

#### 5b. Duplicate description sanity check

After resolving descriptions for all steps, compare them pairwise. If two or more sibling steps within the same path have identical `description` values, flag this as a likely copy-paste error in the website markdown. Record it in the migration notes. Still use the values as-is (they come from the authoritative source), but the duplicate should be reviewed and corrected upstream.

#### 6. Look up path-level index.json rule

Check if the `*-lj` directory name (or a URL containing it) has an entry in `index.json`. Extract `match` for `targeting` and derive `startingLocation` (traverse recursively, collect all URL-bearing leaves, pick the first) and `testEnvironment` (apply the IF/ELSE tier inference rules from Mode 1) using the same rules as Mode 1.

#### 7. Generate path-level manifest.json

Write `{lj-dir}/manifest.json`:

```json
{
  "id": "<lj-directory-name>",
  "type": "path",
  "description": "<compact one-line summary; see Description Conventions>",
  "category": "<from journey.group>",
  "author": { "team": "Grafana Documentation" },
  "startingLocation": "<from index.json match, if derivable>",
  "targeting": {
    "match": { "<from index.json rule if exists>" }
  },
  "testEnvironment": {
    "tier": "<from index.json rule, or 'cloud' minimum>"
  },
  "steps": [
    "<step-1-id>",
    "<step-2-id>",
    "..."
  ],
  "depends": [],
  "recommends": ["<from journey.links.to>"],
  "suggests": ["<from related_journeys>"],
  "provides": []
}
```

Omit `targeting` if no index.json rule exists for the path.
Omit `startingLocation` if no URL can be derived — do not fall back to `"/"`.
**Never omit `testEnvironment`.** Minimum is `{ "tier": "cloud" }`.
Always include `depends`, `recommends`, `suggests`, and `provides` — use `[]` when no data is available.

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
- For non-wrapping shortcodes with a `heading` attribute (e.g., `{{< docs/icon-heading heading="## Here's what to expect" >}}`), extract and preserve the heading value as a markdown header in the output
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

#### 11. Write migration notes

Write `{lj-dir}/assets/migration-notes.md` following the [migration notes convention](#migration-notes). Include:
- Path-level manifest and content.json created
- N step manifests created (list them)
- Fields derived from each source
- Results of all `validate --package` commands
- Any metadata conflicts flagged (including journeys.yaml cross-validation mismatches)
- Any duplicate descriptions detected
- Any dangling references in `recommends`, `suggests`, or `depends` (these are expected and preferred — the CLI catches them)
- Any side_journeys URLs resolved (or not resolved) to package IDs
- Any fields that need manual review
- Any fallbacks used due to missing website markdown
- Any surprises or unexpected situations

#### 12. Report

Tell the user:
- Path-level manifest and content.json created
- N step manifests created (list them)
- Fields derived from each source
- Results of all `validate --package` commands
- Any conflicts flagged
- Any fields that need manual review
- Any fallbacks used due to missing website markdown
- Summary of migration notes written

---

## Reference-First Derivation

For all field derivation logic and fallback rules, use `docs/manifest-reference.md` as the authoritative source:
- `startingLocation` extraction (traverse recursively, collect all URL-bearing leaves, pick the first)
- `testEnvironment` tier inference (IF/ELSE logic: source → cloud, targetPlatform: cloud → cloud, else → local; no match/empty match → cloud)
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
- [ ] Step `depends`/`recommends` chains are consistent (no broken references within the current migration scope)
- [ ] Dangling references (IDs in `depends`/`recommends`/`suggests` that point to directories not yet in the repo) are acceptable and **preferred** — always include them when the underlying data supports the reference. The Pathfinder CLI (`validate --package`) knows how to detect and report dangling references, so they will be caught during validation. It is better to produce more dangling references (which the CLI catches) than to silently drop relationships that exist in the source data. Record each dangling reference in the migration notes.
- [ ] JSON is syntactically valid in all generated files
- [ ] `node dist/cli/cli/index.js validate --package <dir>` was run for each generated package (or a blocker was explicitly reported)

---

## Error Handling

### No index.json rule found
Generate the manifest without `targeting`. Omit `startingLocation` (do not default to `"/"`). `testEnvironment` defaults to `{ "tier": "cloud" }` (the minimum acceptable value — this applies when no match expression exists or when the match expression is empty). Flag for user review — the guide may be path-only (reachable via learning path, not contextual recommendation).

### Website markdown not found
Apply fallback rules. Clearly state which fields used fallback values and need manual review.

### Missing required step description during LJ fallback
Follow the [Description Conventions](#description-conventions) priority:
1. Step-level `index.json` rule `description` (first priority — already catalog-style)
2. Website step `index.md` `description` — condense to one line if verbose
3. Summarize from step `content.json` title and any available context into a single catalog-style sentence
4. If no sources exist at all, stop and ask the user for that step's description (required manifest field). Do not invent one.

### content.json missing in a step directory
This is unexpected. Report the missing file and skip that step. Do not create a content.json for a step — that is the content author's responsibility, not the migration skill's.

### Metadata conflict between sources
Present both values to the user, state which source each came from, and ask the user to choose. Do not guess.

---

## Migration Notes

Every migration produces a leave-behind document recording findings, decisions, surprises, and TODO items specific to that guide or path. This follows the `assets/` directory convention from `.cursor/skills/skill-memory.md`.

### Location

- Standalone guide: `{dir}/assets/migration-notes.md`
- Learning path: `{lj-dir}/assets/migration-notes.md` (one file for the entire path, covering path-level and all steps)

### Format

```markdown
---
disclaimer: Auto-generated by migrate-guide. Do not edit manually.
notice: To regenerate, re-run the migration skill on this directory.
migrated_at: "<ISO 8601 timestamp>"
---

# Migration Notes: <directory-name>

## Files Created

- `manifest.json` — <brief description of what was generated>
- (for paths) `content.json` — path-level cover page
- (for paths) `<step>/manifest.json` — one per step

## Field Derivation Summary

| Field | Source | Value |
|-------|--------|-------|
| ... | ... | ... |

## Flags for Manual Review

- <any fields that used fallback values>
- <any missing descriptions that were requested from the user>

## Dangling References

- <any suggests/recommends/depends IDs that point to non-existent directories>
- (Dangling references are expected and preferred — the Pathfinder CLI catches them during validation)

## Data Quality Issues

- <any journeys.yaml vs _index.md mismatches>
- <any duplicate step descriptions>
- <any side_journeys URLs that could not be resolved>

## Surprises / Notes

- <anything unexpected encountered during migration>

## TODO

- [ ] <actionable items for follow-up>
```

Omit any section that has no entries (e.g., if there are no dangling references, omit that section entirely). The goal is a concise, scannable document — not a verbose log.

Path migration (Mode 2) produces significantly more complex notes than standalone guides (Mode 1) because of the variety of special circumstances that can arise: metadata conflicts across sources, step ordering nuances, shortcode stripping edge cases, relationship mapping ambiguities, and cross-repo data inconsistencies. The migration notes capture these per-path specifics so they are not lost.

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
