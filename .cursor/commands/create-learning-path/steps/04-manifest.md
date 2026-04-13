# Step 4: Generate Manifest Files

Generate `manifest.json` files for the path and every milestone to complete the package format.

---

## Tutorial Mode Introduction

```
**Step 4: Generate Manifest Files**

I'll create manifest.json files for the package format:
- A path-level manifest with milestones, category, and author
- A step-level manifest for each milestone with depends/recommends chain
- Targeting and startingLocation are populated later (Step 5: Recommender)

Ready to proceed? (Y/N)
```

Wait for confirmation, then generate.

---

## Expert Mode

Generate immediately without introduction.

---

## Before Starting

> Read `docs/manifest-reference.md` for the complete field reference, derivation rules, and templates.
> The content.json files created in Step 3 are the source for `id`, `title`, and milestone ordering.
> The website `_index.md` created in Step 3 is the source for `category` (from `journey.group`) and `description`.

---

## What Gets Generated

Every package directory needs a `manifest.json` alongside its `content.json`:

```
[slug]-lj/
  content.json        ← created in Step 3
  manifest.json       ← type: "path" (created now)
  business-value/
    content.json      ← created in Step 3
    manifest.json     ← type: "guide" (created now)
  install-alloy/
    content.json
    manifest.json
  ...
```

---

## Part A: Generate Path-Level Manifest

Create `[slug]-lj/manifest.json` with the following fields:

```json
{
  "id": "[slug]-lj",
  "type": "path",
  "description": "[from _index.md description or plan]",
  "category": "[from _index.md journey.group]",
  "author": {
    "name": "[from CODEOWNERS or git history]",
    "team": "Grafana Documentation"
  },
  "testEnvironment": {
    "tier": "cloud"
  },
  "milestones": [
    "[slug]-business-value",
    "[slug]-install-alloy",
    "[slug]-configure-alloy",
    "..."
  ],
  "depends": [],
  "recommends": [],
  "suggests": [],
  "provides": []
}
```

### Field Derivation

| Field | Source | Rule |
|-------|--------|------|
| `id` | Directory name | The `[slug]-lj` directory name. Must match the `id` in the path-level `content.json`. |
| `type` | — | Always `"path"`. |
| `description` | Website `_index.md` | Condense the `description` frontmatter to a compact one-line catalog summary. |
| `category` | Website `_index.md` | From `journey.group` (e.g., `"data-availability"`, `"getting-started"`). |
| `author.name` | CODEOWNERS / git | Check `.github/CODEOWNERS` for the directory owner, or use `git log` on the content.json files. |
| `author.team` | — | Always `"Grafana Documentation"` for learning paths. |
| `testEnvironment` | — | Default to `{ "tier": "cloud" }`. Adjusted in Step 5 if the recommender rule targets a different platform. |
| `milestones` | Step content.json files | Ordered array of step `id` values, matching the milestone order from the plan (Step 2). |
| `suggests` | Website `_index.md` | From `related_journeys` items. Convert website URL slugs to `[slug]-lj` package IDs (e.g., `/docs/learning-paths/drilldown-metrics/` becomes `drilldown-metrics-lj`). |
| `depends` | — | Leave empty unless the plan explicitly identifies prerequisites. |
| `recommends` | — | Leave empty unless the plan explicitly identifies recommended prior paths. |
| `provides` | — | Leave empty. Populate manually when semantic outcomes are defined. |

### Fields Left Empty for Step 5

The following fields are populated after the recommender mapping is created in Step 5:

- `startingLocation` — derived from the recommender match expression
- `targeting.match` — copied from the recommender rule

Do **not** add placeholder values. These fields are simply omitted until Step 5 fills them in.

---

## Part B: Generate Step-Level Manifests

For EACH milestone subdirectory, create a `manifest.json`:

```json
{
  "id": "[slug]-[milestone]",
  "type": "guide",
  "description": "[from step content.json title or website index.md description]",
  "category": "[same as path category]",
  "author": {
    "name": "[same as path author]",
    "team": "Grafana Documentation"
  },
  "testEnvironment": {
    "tier": "cloud"
  },
  "depends": ["[previous-step-id]"],
  "recommends": ["[next-step-id]"],
  "suggests": [],
  "provides": []
}
```

### Step Dependency Chain

Steps form a linear chain: each step depends on the previous one and recommends the next one.

| Step position | `depends` | `recommends` |
|---------------|-----------|--------------|
| First step | `[]` | `["<second-step-id>"]` |
| Middle steps | `["<previous-step-id>"]` | `["<next-step-id>"]` |
| Last step | `["<previous-step-id>"]` | `[]` |

### Field Derivation

| Field | Source | Rule |
|-------|--------|------|
| `id` | Step `content.json` | Copy the `id` field verbatim. Must match the `content.json` `id`. |
| `type` | — | Always `"guide"`. |
| `description` | Step `content.json` title, then website `index.md` | Use the website `index.md` `description` frontmatter if available. Otherwise, use the `content.json` `title` as a short description. |
| `category` | Path manifest | Same `category` as the parent path. |
| `author` | Path manifest | Same `author` as the parent path. |
| `testEnvironment` | Path manifest | Same `testEnvironment` as the parent path. |
| `depends` | Step ordering | Previous step's `id`. Empty for the first step. |
| `recommends` | Step ordering | Next step's `id`. Empty for the last step. |
| `suggests` | Website `index.md` | From `side_journeys` items if they reference other learning paths. Otherwise empty. |
| `provides` | — | Leave empty. |

---

## Verification Checklist (REQUIRED)

Before proceeding to Step 5, verify:

- [ ] `[slug]-lj/manifest.json` exists with `"type": "path"`
- [ ] Path manifest `id` matches the directory name and the path-level `content.json` `id`
- [ ] Path manifest `milestones` array contains all step IDs in the correct order
- [ ] Path manifest has `category`, `author`, `description`, and `testEnvironment`
- [ ] Path manifest does NOT have `startingLocation` or `targeting` (added in Step 5)
- [ ] Every milestone subdirectory has a `manifest.json` with `"type": "guide"`
- [ ] Every step manifest `id` matches its `content.json` `id`
- [ ] Step dependency chain is correct: first step has empty `depends`, last step has empty `recommends`
- [ ] All manifests use consistent `category`, `author`, and `testEnvironment` values

**If any check fails, fix before continuing.**

---

## Completion

Display a summary showing: path manifest (with milestone count), step manifests created (with depends/recommends chain), and verification status. Ask the user if they're ready for Step 5 (Recommender Mapping).
