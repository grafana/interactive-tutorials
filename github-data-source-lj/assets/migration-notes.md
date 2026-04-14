---
status: complete
package: github-data-source-lj
type: path
steps: 6
date: 2026-04-07
---

# Migration Notes: github-data-source-lj

## Overview

Migrated learning path `github-data-source-lj` (6 steps) to Pathfinder package format.

## Files Created

- `github-data-source-lj/manifest.json` — path-level manifest (type: path)
- `github-data-source-lj/content.json` — path-level cover page (new, derived from website _index.md)
- `github-data-source-lj/business-value/manifest.json` — step 1
- `github-data-source-lj/advantages-github-datasource/manifest.json` — step 2
- `github-data-source-lj/create-github-token/manifest.json` — step 3
- `github-data-source-lj/install-github-plugin/manifest.json` — step 4
- `github-data-source-lj/config-github-datasource/manifest.json` — step 5
- `github-data-source-lj/end-journey/manifest.json` — step 6

## Files NOT Modified

All 6 pre-existing step `content.json` files verified byte-identical by SHA-256 before and after writes.
No path-level `content.json` existed prior to migration.
`index.json` was not modified (not present in this worktree; read from source repo).
No files outside `github-data-source-lj/` were touched.

## Sources Consulted

### content.json (per step)
- Used for `id` and `title` fields in each step manifest.

### Website markdown
- Path: `/Users/davidallen/hax/website/content/docs/learning-paths/github-data-source/`
- `_index.md`: title, description, journey.group (data-availability), journey.links.to (github-visualize)
- All 6 step `index.md` files: weight, step number, pathfinder_data, description, side_journeys
- All steps had `pathfinder_data` frontmatter — no directory name fallback needed.

### Recommender rules
- File: `connections-cloud.json`
- Matched rule: type "learning-journey", URL `https://grafana.com/docs/learning-journeys/github-data-source/`
- Match expression: `{"urlPrefix": "/add-new-connection"}`
- Description from recommender: "A learning journey that shows you how to connect GitHub repository data in Grafana Cloud."
- Used recommender description for path manifest (higher priority than website _index.md).

### index.json
- No matching entry found for `github-data-source-lj` (expected — index.json does not contain learning-journey entries).

### journeys.yaml
- Entry found: `id: github-data-source`, `category: data-availability`, `links.to: visualize-github-data`

### CODEOWNERS
- `/github-data-source-lj/` owned by `@chri2547` — used for `author.name` on all manifests.

## Step Ordering (by website weight)

| Weight | Step | Directory | content.json id |
|--------|------|-----------|-----------------|
| 100 | 2 | business-value | github-data-source-business-value |
| 200 | 3 | advantages-github-datasource | github-data-source-advantages |
| 300 | 4 | create-github-token | github-data-source-create-token |
| 400 | 5 | install-github-plugin | github-data-source-install |
| 500 | 6 | config-github-datasource | github-data-source-config |
| 600 | 7 | end-journey | github-data-source-end-journey |

Note: Website `step` numbering starts at 2 (step 1 is the _index.md landing page). Weight ordering is authoritative.

## Metadata Conflicts

### journeys.yaml vs _index.md: links.to mismatch
- `journeys.yaml` has `links.to: visualize-github-data`
- `_index.md` has `journey.links.to: github-visualize`
- Used `_index.md` value (`github-visualize` -> `github-visualize-lj`) as authoritative per derivation rules.
- Website team should reconcile this inconsistency.

## Dangling References

- `recommends: ["github-visualize-lj"]` on path manifest — directory may not yet be migrated. This is expected; the CLI catches dangling refs at build time.
- `suggests: ["github-visualize-lj"]` on end-journey step — same note.

## side_journeys Resolution

- `business-value/index.md` has `side_journeys` with link `/docs/grafana-cloud/introduction/what-is-observability/` — this is an external docs link, not a learning path. Not mappable to a package ID. Ignored.
- `end-journey/index.md` has `related_journeys` with link `/docs/learning-paths/github-visualize/` — resolved to `github-visualize-lj`. Added to step `suggests`.

## Duplicate Description Check

No duplicate descriptions found among sibling steps.

## Validation Results

- `validate --package github-data-source-lj`: PASSED
- `validate --package business-value`: PASSED
- `validate --package advantages-github-datasource`: PASSED
- `validate --package create-github-token`: PASSED
- `validate --package install-github-plugin`: PASSED
- `validate --package config-github-datasource`: PASSED
- `validate --package end-journey`: PASSED

All 7 packages passed validation. Step-level warnings about missing `targeting` and `startingLocation` are expected (targeting lives at path level).

## testEnvironment Derivation

Recommender match has no `source` or `targetPlatform` fields — only `urlPrefix`. Per inference rules, this defaults to `{ "tier": "cloud" }` (minimum default, no match expression contains cloud/oss indicators). Applied to path and all steps.
