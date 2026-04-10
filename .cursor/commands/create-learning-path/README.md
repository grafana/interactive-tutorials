# /create-learning-path

Create a complete interactive learning path from scratch — plan, write JSON, wire up the website, and test.

This is the **unified command** that replaces the two-pass workflow (write markdown first, then convert to JSON). You author `content.json` files (schemaVersion 1.0.0) for the interactive Pathfinder experience, and write the corresponding website milestone `index.md` files with Hugo front matter directly.

---

## What It Does

1. Plans the learning path structure and gets user approval
2. Writes `content.json` files (schemaVersion 1.0.0) with interactive blocks, and website milestone `index.md` files with Hugo front matter
3. Generates `manifest.json` files for the path and every milestone (package format)
4. Creates the recommender mapping and wires targeting into the path manifest
5. Discovers CSS selectors by walking the Grafana UI
6. Tests interactivity collaboratively with the user
7. Verifies website markdown is complete and correct
8. Verifies factual claims against live Grafana documentation
9. Produces a final report

---

## Prerequisites

See `build-interactive-lj/SETUP.md` for environment setup:
- Three repos in workspace: `website`, `interactive-tutorials`, `grafana-recommender`
- Playwright MCP configured
- GitHub CLI authenticated (`gh auth login`)

---

## Input

The user provides:
- **Feature or product goal** — what they want the learning path to teach
- **Target audience** — who is this for (typically Grafana beginners)

No markdown source files needed. This command creates everything from a description.

---

## Mode

Ask the user their mode preference at the start:

| Mode | Behavior |
|------|----------|
| **Tutorial** | Explain what each step does, confirm before proceeding |
| **Expert** | Run each step immediately, minimal prompts |

Default to **Tutorial** if not specified.

---

## Steps

### Step 1: Environment Validation
> File: `build-interactive-lj/steps/01-environment.md`

Verify repos and Playwright are available. Same as the existing command.

### Step 2: Plan Learning Path ★ NEW
> File: `steps/02-plan.md`

Propose 2-4 path options, outline milestones, get user approval. Adapted from the learning path skill's planning phase.

### Step 3: Write JSON and Website Markdown
> File: `steps/03-write-json.md`

Create `content.json` files (schemaVersion 1.0.0) with interactive blocks and markdown content. Also write the corresponding website milestone `index.md` files with Hugo front matter and `{{< pathfinder/json >}}` body, and the path overview `_index.md`. The path cover page is a root-level `content.json` (not `welcome/content.json`).

### Step 4: Generate Manifest Files
> File: `steps/04-manifest.md`

Generate `manifest.json` for the path (type `"path"` with milestones array) and for each milestone (type `"guide"` with depends/recommends chain). Targeting fields are left empty for Step 5.

### Step 5: Create Recommender Mapping
> File: `build-interactive-lj/steps/03-recommender.md`

Create the recommender mapping so Pathfinder surfaces the learning path. After the rule is created, wire `startingLocation` and `targeting.match` into the path-level `manifest.json`.

### Step 6: Selector Discovery
> File: `build-interactive-lj/steps/05-selectors.md`

Use Playwright to walk the Grafana UI and discover CSS selectors for each interactive block. Same as the existing command.

### Step 7: Test in Pathfinder
> File: `build-interactive-lj/steps/06-testing.md`

Collaboratively test each milestone in the Block Editor. User imports JSON, clicks through interactions, reports failures. AI fixes selectors. Same as the existing command.

### Step 8: Verify Website Markdown
> File: `steps/08-verify-website-markdown.md`

Verify that every milestone has a corresponding website `index.md` with correct front matter and that the path overview `_index.md` is present.

### Step 8b: Verify Documentation Accuracy (MANDATORY)
> File: `steps/08b-verify-docs-accuracy.md`

Cross-check all factual claims in the learning path content against live Grafana documentation. Fetches canonical docs pages and compares navigation paths, feature names, capability descriptions, platform availability, and prerequisites.

### Step 9: Report and Next Steps
> File: `steps/09-report.md`

Summary of created files (including manifest.json), quality metrics, and PR guidance.

---

## Session Planning

For paths with 7+ milestones, plan for two sessions. The natural break point is after file creation, manifest generation, and recommender mapping (Steps 1–5) and before selector discovery (Steps 6–9). All artifacts are on disk at the break point, so the second session reads the existing files and resumes at selector discovery.

For paths with fewer milestones, a single session is usually sufficient.

---

## Reference Documentation

| Document | Purpose |
|----------|---------|
| `reference/frontmatter-schema.md` | Website front matter field reference, CTA types, and paired examples |
| `build-interactive-lj/reference/json-schema.md` | content.json schema (v1.0.0), block types, action types, and field reference |
| `docs/manifest-reference.md` | manifest.json field reference, derivation rules, and templates |
| `.cursor/proven-patterns.mdc` | Reusable interactive patterns (loaded automatically for content.json) |
| `build-interactive-lj/reference/selector-patterns.md` | Selector stability rules and anti-patterns |

---

## Relationship to Existing Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| **`/create-learning-path`** (this) | Create a new learning path from scratch | Starting from zero — no markdown exists |
| **`/build-interactive-lj`** | Add interactivity to an existing markdown learning path | A learning path already exists in the website repo |

The existing `/build-interactive-lj` remains useful for retrofitting existing markdown-first paths. This command is for net-new paths where JSON-first is the better approach.

---

## File Layout

After completion, the learning path spans two repositories:

```
interactive-tutorials/
  [slug]-lj/
    content.json                ← path cover page (intro, objectives, prerequisites)
    manifest.json               ← type: "path", milestones, targeting
    milestone-1/
      content.json              ← Pathfinder interactive content
      manifest.json             ← type: "guide", depends/recommends
    milestone-2/
      content.json
      manifest.json
    ...

website/
  content/docs/learning-paths/[slug]/
    _index.md                   ← front matter + {{< pathfinder/json >}} → path cover page
    milestone-1/index.md        ← front matter + {{< pathfinder/json >}}
    milestone-2/index.md        ← front matter + {{< pathfinder/json >}}
    ...

grafana-recommender/
  internal/configs/state_recommendations/
    [area]-cloud.json           ← mapping entry added
```

