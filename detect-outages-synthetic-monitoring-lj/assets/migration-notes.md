---
status: complete
migration_date: 2026-04-07
directory: detect-outages-synthetic-monitoring-lj
type: learning-path
step_count: 7
---

# Migration Notes: detect-outages-synthetic-monitoring-lj

## Sources Consulted

### content.json (per step)
- All 7 step `content.json` files read for `id` and `title` fields.
- No pre-existing root `content.json` — created new path-level cover page.

### index.json
- No matching rule found in `index.json` for this learning journey (index.json contains only `type: "interactive"` entries).

### Recommender rules
- **File:** `testing-synthetics-cloud.json`
- **Rule matched:** `type: "learning-journey"`, URL `https://grafana.com/docs/learning-paths/detect-outages-synthetic-monitoring/`
- **Match expression:** `{"and": [{"urlPrefix": "/a/grafana-synthetic-monitoring-app/home"}, {"targetPlatform": "cloud"}]}`
- **Description from rule:** "Step-by-step guide: Detect customer-visible outages using Synthetic Monitoring."
- Also checked `featured.json` — no matching learning-journey rules.

### Website markdown
- **Path:** `/Users/davidallen/hax/website/content/docs/learning-paths/detect-outages-synthetic-monitoring/`
- **_index.md:** Read successfully. Extracted `journey.group: data-availability`, title, description.
- **Step index.md files:** All 7 steps read. Extracted weight, description, pathfinder_data, side_journeys.
- No `journey.links.to` in _index.md frontmatter (no recommends at path level).
- No `related_journeys` in _index.md frontmatter (no suggests at path level).

### journeys.yaml
- No entry found for `detect-outages-synthetic-monitoring` in journeys.yaml.

### CODEOWNERS
- Directory-scoped rule found: `/detect-outages-synthetic-monitoring-lj/ @heitortsergent`
- `author.name` set to `heitortsergent` (from CODEOWNERS).

## Field Derivation

### Path-level manifest
| Field | Source | Value |
|-------|--------|-------|
| id | directory name | `detect-outages-synthetic-monitoring-lj` |
| type | convention | `path` |
| description | recommender rule (testing-synthetics-cloud.json) | "Step-by-step guide: Detect customer-visible outages using Synthetic Monitoring." |
| category | website _index.md `journey.group` | `data-availability` |
| author.name | CODEOWNERS | `heitortsergent` |
| author.team | convention (learning path) | `Grafana Documentation` |
| startingLocation | recommender match `urlPrefix` | `/a/grafana-synthetic-monitoring-app/home` |
| targeting.match | recommender rule (testing-synthetics-cloud.json) | `{"and": [{"urlPrefix": "/a/grafana-synthetic-monitoring-app/home"}, {"targetPlatform": "cloud"}]}` |
| testEnvironment.tier | match contains `targetPlatform: cloud` | `cloud` |
| milestones | website step weights | 7 steps in weight order |
| recommends | _index.md (no journey.links.to) | `[]` |
| suggests | _index.md (no related_journeys) | `[]` |

### Step manifests
- Descriptions sourced from website step `index.md` frontmatter `description` fields.
- Category: `data-availability` (from parent path `journey.group`).
- Dependency chain: step N depends on step N-1, recommends step N+1.
- First step (value-of-synthetic-monitoring): no depends. Last step (end-journey): no recommends.

## Step Ordering (by website weight)

| Weight | Step Directory | content.json ID |
|--------|---------------|-----------------|
| 100 | value-of-synthetic-monitoring | detect-outages-synthetic-monitoring-value-of-synthetic-monitoring |
| 200 | navigate-to-synthetic-monitoring | detect-outages-synthetic-monitoring-navigate-to-synthetic-monitoring |
| 300 | initialize-plugin | detect-outages-synthetic-monitoring-initialize-plugin |
| 400 | create-ping-check | detect-outages-synthetic-monitoring-create-ping-check |
| 500 | select-probe-locations | detect-outages-synthetic-monitoring-select-probe-locations |
| 600 | view-check-dashboard | detect-outages-synthetic-monitoring-view-check-dashboard |
| 800 | end-journey | detect-outages-synthetic-monitoring-end-journey |

## Path-level content.json
- Created from website `_index.md` body content.
- Hugo shortcodes (`docs/box`, `docs/icon-heading`) stripped.
- Preserved: introductory paragraph, learning objectives list, prerequisites section.

## Validation Results
- `validate --package` passed for path-level package and all 7 step packages.
- Warning: `content.json` unknown field `description` at root (expected for path-level content.json — non-blocking).
- Step warnings: `targeting` and `startingLocation` not specified (expected — targeting lives at path level).

## Safety Invariants
- All 7 pre-existing step `content.json` files verified byte-identical (SHA-256 before/after).
- `index.json` verified unchanged (SHA-256 before/after).
- No files outside `detect-outages-synthetic-monitoring-lj/` were modified.

## Dangling References
- No dangling references. All dependency chain IDs point to steps within this path.
