# Step 3: Write JSON and Website Markdown

Create content.json files for the Pathfinder interactive experience and corresponding website `index.md` files with Hugo front matter.

---

## Tutorial Mode Introduction

```
**Step 3: Write JSON and Website Markdown**

I'll create two sets of files for each milestone plus a welcome page:
- content.json (schemaVersion 1.0.0) with interactive blocks and markdown content
- website index.md with Hugo front matter and {{< pathfinder/json >}} body
- welcome/content.json for the path landing page (intro, objectives, prerequisites)

Ready to proceed? (Y/N)
```

Wait for confirmation, then write.

---

## Expert Mode

Write immediately without introduction.

---

## Before Starting

> Read `build-interactive-lj/reference/json-schema.md` for content.json schema, block types, and field reference.
> Read `reference/frontmatter-schema.md` for website front matter fields, CTA types, and paired examples.
> Read `build-interactive-lj/reference/proven-patterns.md` for reusable patterns.

---

## Directory Structure

Create the learning path directory in interactive-tutorials:

```
interactive-tutorials/
  [slug]-lj/
    welcome/content.json          ← path landing page (intro, objectives, prerequisites)
    business-value/content.json
    install-alloy/content.json
    configure-alloy/content.json
    ...
    end-journey/content.json
```

Create the corresponding website directory:

```
website/
  content/docs/learning-paths/[slug]/
    _index.md                     ← front matter + {{< pathfinder/json >}} → welcome
    business-value/index.md
    install-alloy/index.md
    configure-alloy/index.md
    ...
    end-journey/index.md
```

Use the milestone folder names from the approved plan (Step 2). The website slug drops the `-lj` suffix (e.g., `linux-server-integration-lj` → `linux-server-integration`).

---

## Part A: Write content.json Files

For EACH milestone in the approved plan:

### 1. Create the Root Structure

```json
{
  "schemaVersion": "1.0.0",
  "id": "[path-slug]-[milestone-slug]",
  "title": "[Milestone Title from plan]",
  "blocks": [ ... ]
}
```

### 2. Write the Blocks

Convert the plan's step descriptions into blocks:

| Plan content | Block type |
|---|---|
| Introductory/explanatory text | `markdown` |
| Click a specific UI element | `interactive` with `action: "highlight"` |
| Navigate through menus | `multistep` with sequential steps |
| Fill in a form field | `interactive` with `action: "formfill"` |
| Click a button by text | `interactive` with `action: "button"` |
| User performs action outside browser | `markdown` or `guided` |
| Multi-option flow (create new vs use existing) | `markdown` with table |
| Sequential UI steps in a group | `section` wrapping multiple blocks |

### 3. Leave Selectors Empty

For interactive blocks, set `"reftarget": ""` — selectors are discovered in Step 5.

Exception: nav menu items use a known pattern and can be filled immediately:
```json
"reftarget": "a[data-testid='data-testid Nav menu item'][href='/path']"
```

### 4. Set Requirements

| UI context | Requirement |
|---|---|
| Nav menu element | `["navmenu-open"]` |
| Page-specific action | `["on-page:/path"]` |
| Depends on previous section | `["section-completed:id"]` |
| No special context | Omit or use `[]` |

Never add `"exists-reftarget"` — it's auto-applied.

---

## Part B: Write Website Milestone Markdown

For EACH milestone, create a corresponding `index.md` in the website repo at:

```
website/content/docs/learning-paths/[slug]/[milestone]/index.md
```

### Structure

Each milestone `index.md` consists of Hugo front matter followed by the Pathfinder shortcode:

```markdown
---
menuTitle: [Short nav title]
title: [Full milestone title]
description: [1-2 sentence description starting with action verb]
keywords:
  - [keyword1]
  - [keyword2]
weight: [ordering weight, increments of 100]
step: [step number in sequence]
layout: single-journey
cta:
  type: [continue|success|conclusion]
pathfinder_data: [slug]-lj/[milestone]
---

{{< pathfinder/json >}}
```

### Front Matter Field Reference

| Field | Required | Description |
|-------|----------|-------------|
| `menuTitle` | Yes | Short nav title (under 20 chars) |
| `title` | Yes | Full milestone title (matches content.json `title`) |
| `description` | Yes | 1-2 sentence description starting with action verb |
| `keywords` | No | SEO keywords (3-5 terms) |
| `weight` | Yes | Ordering weight (increments of 100) |
| `step` | Yes | Step number in the learning path sequence |
| `layout` | Yes | Always `single-journey` |
| `cta` | Yes | Call-to-action configuration (see reference doc) |
| `side_journeys` | No | Optional exploration links |
| `related_journeys` | No | Related learning paths (typically conclusion only) |
| `pathfinder_data` | Yes | Path to the content.json directory: `[slug]-lj/[milestone]` |

### CTA Types

**Continue** (default for intermediate steps):
```yaml
cta:
  type: continue
```

**Success** (verification milestones):
```yaml
cta:
  type: success
  troubleshooting:
    title: 'Explore the following troubleshooting topics if you need help:'
    items:
      - title: Problem description
        link: /docs/grafana-cloud/.../troubleshoot/#specific-issue
```

**Conclusion** (final milestone):
```yaml
cta:
  type: conclusion
  image:
    src: /media/docs/learning-journey/journey-conclusion-header-1.svg
    width: 735
    height: 175
```

### Side Journeys

```yaml
side_journeys:
  title: More to explore (optional)
  heading: 'At this point in your journey, you can explore the following paths:'
  items:
    - title: Link title
      link: /docs/...
```

### Related Journeys (Conclusion Milestones)

```yaml
related_journeys:
  title: Related paths
  heading: Consider taking the following paths after you complete this journey.
  items:
    - title: Path title
      link: /docs/learning-paths/path-name/
```

---

## Part C: Write Welcome Page

The welcome page is the learning path landing page. It consists of two files:

### 1. Create `welcome/content.json`

This file contains the path introduction, objectives, prerequisites, and boilerplate as markdown blocks:

```json
{
  "schemaVersion": "1.0.0",
  "id": "[slug]-welcome",
  "title": "[Path Title]",
  "blocks": [
    {
      "type": "markdown",
      "content": "[Welcome paragraph introducing the path and what users will learn.]\n\n[Second paragraph with more context about the technology or product.]"
    },
    {
      "type": "markdown",
      "content": "## Here's what to expect\n\nWhen you complete this path, you'll be able to:\n\n- [Objective 1]\n- [Objective 2]\n- [Objective 3]"
    },
    {
      "type": "markdown",
      "content": "## Before you begin\n\nBefore you [action], ensure you have:\n\n- [Prerequisite 1]\n- [Prerequisite 2]\n- [Prerequisite 3]"
    },
    {
      "type": "markdown",
      "content": "## Troubleshooting\n\nIf you get stuck, we've got your back! Where appropriate, troubleshooting information is just a click away."
    },
    {
      "type": "markdown",
      "content": "## More to explore\n\nWe understand you might want to explore other capabilities not strictly on this path. We'll provide you opportunities where it makes sense."
    }
  ]
}
```

### 2. Create `_index.md` in the website repo

The `_index.md` uses `{{< pathfinder/json >}}` as its body, with `pathfinder_data` pointing to the welcome content.json. The front matter contains path-level metadata that Hugo needs for navigation and theming:

```markdown
---
menuTitle: [Short path name]
title: [Full path title]
description: [1-2 sentence path description]
weight: [ordering weight among all learning paths]
journey:
  group: [data-availability|getting-started|...]
  skill: [Beginner|Intermediate|Advanced]
  source: Docs & blog posts
  logo:
    src: [path to logo image]
    background: '[hex color]'
    width: [number]
    height: [number]
step: 1
layout: single-journey
cascade:
  layout: single-journey
cta:
  type: start
  title: Are you ready?
  cta_text: Let's go!
keywords:
  - [keyword1]
  - [keyword2]
related_journeys:
  title: Related paths
  heading: Consider taking the following paths before you start this path.
  items:
    - title: [Related path title]
      link: /docs/learning-paths/[related-path]/
pathfinder_data: [slug]-lj/welcome
---

{{< pathfinder/json >}}
```

### `_index.md` Front Matter Fields (Path-Level Only)

These fields appear only on `_index.md`, not on milestone `index.md` files:

| Field | Required | Description |
|-------|----------|-------------|
| `journey` | Yes | Path metadata: group, skill level, source, logo |
| `cascade` | Yes | Always `{ layout: single-journey }` — propagates to child pages |
| `cta.type` | Yes | Always `start` for the landing page |
| `cta.title` | Yes | Prompt text (typically "Are you ready?") |
| `cta.cta_text` | Yes | Button text (typically "Let's go!") |

---

## Page and Milestone Templates

### Welcome Page

**welcome/content.json:**
```json
{
  "schemaVersion": "1.0.0",
  "id": "[slug]-welcome",
  "title": "[Full Path Title]",
  "blocks": [
    {
      "type": "markdown",
      "content": "Welcome to the Grafana learning path that [describes what the path teaches].\n\n[Second paragraph with product/technology context.]"
    },
    {
      "type": "markdown",
      "content": "## Here's what to expect\n\nWhen you complete this path, you'll be able to:\n\n- [Objective 1]\n- [Objective 2]\n- [Objective 3]"
    },
    {
      "type": "markdown",
      "content": "## Before you begin\n\nBefore you [action], ensure you have:\n\n- A Grafana Cloud account. To create an account, refer to [Grafana Cloud](https://grafana.com/signup/cloud/connect-account).\n- [Prerequisite 2]\n- [Prerequisite 3]"
    },
    {
      "type": "markdown",
      "content": "## Troubleshooting\n\nIf you get stuck, we've got your back! Where appropriate, troubleshooting information is just a click away."
    },
    {
      "type": "markdown",
      "content": "## More to explore\n\nWe understand you might want to explore other capabilities not strictly on this path. We'll provide you opportunities where it makes sense."
    }
  ]
}
```

**_index.md:**
```markdown
---
menuTitle: [Short path name]
title: [Full Path Title]
description: [1-2 sentence path description]
weight: [ordering weight]
journey:
  group: [data-availability|getting-started|...]
  skill: Beginner
  source: Docs & blog posts
  logo:
    src: /static/img/menu/grafana2.svg
    background: '#0068FF'
    width: 46
    height: 55
step: 1
layout: single-journey
cascade:
  layout: single-journey
cta:
  type: start
  title: Are you ready?
  cta_text: Let's go!
keywords:
  - [keyword1]
  - [keyword2]
related_journeys:
  title: Related paths
  heading: Consider taking the following paths before you start this path.
  items:
    - title: [Related path title]
      link: /docs/learning-paths/[related-path]/
pathfinder_data: [slug]-lj/welcome
---

{{< pathfinder/json >}}
```

### Business Value Milestone

**content.json:**
```json
{
  "schemaVersion": "1.0.0",
  "id": "[slug]-business-value",
  "title": "The value of [feature]",
  "blocks": [
    { "type": "markdown", "content": "[Problem statement and solution benefits]" },
    { "type": "markdown", "content": "[Feature advantages list]" }
  ]
}
```

**index.md:**
```markdown
---
menuTitle: The value of [feature]
title: The value of [feature]
description: Learn about [feature] and how it helps you [outcome]
weight: 100
step: 2
layout: single-journey
cta:
  type: continue
side_journeys:
  title: More to explore (optional)
  heading: 'At this point in your journey, you can explore the following paths:'
  items:
    - title: Related docs link
      link: /docs/...
pathfinder_data: [slug]-lj/business-value
---

{{< pathfinder/json >}}
```

### Interactive Navigation Milestone

**content.json:**
```json
{
  "schemaVersion": "1.0.0",
  "id": "[slug]-navigate-to-[location]",
  "title": "Navigate to [location]",
  "blocks": [
    { "type": "markdown", "content": "Introduction..." },
    {
      "type": "section",
      "blocks": [
        {
          "type": "interactive",
          "action": "highlight",
          "reftarget": "",
          "content": "Click **[menu item]** in the nav menu.",
          "requirements": ["navmenu-open"]
        }
      ]
    }
  ]
}
```

**index.md:**
```markdown
---
menuTitle: '[Short location name]'
title: Navigate to [location]
description: Learn how to navigate to [location]
weight: 200
step: 3
layout: single-journey
cta:
  type: continue
pathfinder_data: [slug]-lj/navigate-to-[location]
---

{{< pathfinder/json >}}
```

### Verification Milestone

**content.json:**
```json
{
  "schemaVersion": "1.0.0",
  "id": "[slug]-test-connection",
  "title": "Test the connection",
  "blocks": [
    { "type": "markdown", "content": "Introduction..." },
    {
      "type": "section",
      "blocks": [
        {
          "type": "interactive",
          "action": "button",
          "reftarget": "",
          "content": "Click **Save & test**."
        }
      ]
    }
  ]
}
```

**index.md:**
```markdown
---
menuTitle: Test connection
title: Test the connection
description: Verify that [component] is working correctly
weight: 500
step: 6
layout: single-journey
cta:
  type: success
  troubleshooting:
    title: 'Explore the following troubleshooting topics if you need help:'
    items:
      - title: '[Problem]'
        link: /docs/.../troubleshoot/#issue
pathfinder_data: [slug]-lj/test-connection
---

{{< pathfinder/json >}}
```

### Conclusion Milestone

**content.json:**
```json
{
  "schemaVersion": "1.0.0",
  "id": "[slug]-end-journey",
  "title": "Destination reached!",
  "blocks": [
    { "type": "markdown", "content": "Congratulations on completing this journey!..." }
  ]
}
```

**index.md:**
```markdown
---
menuTitle: Destination reached!
title: Destination reached!
description: Your journey concludes
weight: 900
step: 10
layout: single-journey
cta:
  type: conclusion
  image:
    src: /media/docs/learning-journey/journey-conclusion-header-1.svg
    width: 735
    height: 175
related_journeys:
  title: Related paths
  heading: Consider taking the following paths after you complete this journey.
  items:
    - title: Explore data using Metrics Drilldown
      link: /docs/learning-paths/drilldown-metrics/
side_journeys:
  title: More to explore (optional)
  heading: 'The world is your oyster! Read more about how you can:'
  items:
    - title: Monitor alerts
      link: /docs/grafana-cloud/alerting-and-irm/alerting/monitor-status
pathfinder_data: [slug]-lj/end-journey
---

{{< pathfinder/json >}}
```

---

## Verification Checklist

Before proceeding to Step 4:

- [ ] `welcome/content.json` exists with intro, objectives, prerequisites
- [ ] Every milestone has a `content.json` file
- [ ] Every file has `"schemaVersion": "1.0.0"`
- [ ] Every file has `"id"` in `[path-slug]-[milestone-slug]` format
- [ ] Every file has `"title"` matching the plan
- [ ] content.json files have NO `"website"` key
- [ ] Interactive blocks use `"content"` (NOT `"description"`)
- [ ] Formfill actions use `"targetvalue"` (NOT `"formvalue"`)
- [ ] Interactive blocks have `"reftarget": ""` (selectors in Step 5)
- [ ] `"exists-reftarget"` is NOT manually added
- [ ] Every milestone has a corresponding `index.md` in the website repo
- [ ] Every `index.md` has `layout: single-journey` in front matter
- [ ] Every `index.md` has `pathfinder_data` pointing to `[slug]-lj/[milestone]`
- [ ] Every `index.md` body is `{{< pathfinder/json >}}`
- [ ] `_index.md` exists with `pathfinder_data: [slug]-lj/welcome` and `{{< pathfinder/json >}}` body
- [ ] `_index.md` has `journey`, `cascade`, and `cta.type: start` in front matter

---

## Display

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Step 3 complete: JSON and Website Markdown Written

content.json files (interactive-tutorials):
├── [slug]-lj/welcome/content.json (welcome page)
├── [slug]-lj/milestone-1/content.json ([N] blocks)
├── [slug]-lj/milestone-2/content.json ([N] blocks)
└── ...

Website markdown (website repo):
├── [slug]/_index.md → welcome/content.json ✅
├── [slug]/milestone-1/index.md ✅
├── [slug]/milestone-2/index.md ✅
└── ...

Verification: All checks passed ✓

⏳ Next: Step 4 - Recommender Mapping
   Ready to proceed? (Y/N)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
