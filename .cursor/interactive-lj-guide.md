# Interactive Learning Journey JSON Guide

> A guide for creating `content.json` files that add interactivity (Show me / Do it) to Learning Journeys.

---

## Prerequisites

### Step 1: Clone the Required Repositories

If you haven't already, clone these three repositories:

```bash
cd ~/Documents/repositories  # or your preferred location

# Interactive tutorials - where you'll create the content
git clone https://github.com/grafana/interactive-tutorials.git

# Website - contains the LJ markdown source files
git clone https://github.com/grafana/website.git

# Grafana Recommender - contains Pathfinder recommendation rules
git clone https://github.com/grafana/grafana-recommender.git
```

### Step 2: Create a Cursor Workspace

Create a workspace in Cursor that includes all three repos:

1. Open Cursor
2. **File → Add Folder to Workspace** → Select `interactive-tutorials`
3. **File → Add Folder to Workspace** → Select `website`
4. **File → Add Folder to Workspace** → Select `grafana-recommender`
5. **File → Save Workspace As** → Name it (e.g., `lj-interactivity.code-workspace`)

---

## Table of Contents

1. [Core Principle](#core-principle)
2. [Workflow Overview](#workflow-overview)
3. [JSON Structure](#json-structure)
4. [Block Types](#block-types)
5. [Finding Selectors](#finding-selectors)
6. [Common Patterns](#common-patterns)
7. [Troubleshooting Selectors](#troubleshooting-selectors)
8. [Tracking Broken Selectors](#tracking-broken-selectors)

---

## Core Principle

> **CRITICAL: Always keep JSON content aligned with the markdown source.**

The markdown (`index.md`) is the source of truth. When creating `content.json`:

1. **Include ALL content** from the source markdown — intro text, bullet lists, insights, images, videos, closing paragraphs
2. Match the content text to what's in the markdown
3. Find the correct selector for UI elements
4. **Never** change the content text to match a selector you found

> ⚠️ **IMPORTANT:** If a milestone requires a `content.json` (because it has interactive steps), you **MUST** bring over ALL content from the source `index.md`. The JSON is used to render the Learning Journey on the website — missing content means missing content for users.

If a selector doesn't exist for an element described in the markdown, either:
- Record a new selector
- Convert that step to markdown (non-interactive)
- Track it as needing a testID from the dev team

---

## Workflow Overview

### 1. Verify Workspace Setup

Confirm that all three required repos are in your Cursor workspace:
- `interactive-tutorials` ✓
- `website` ✓
- `grafana-recommender` ✓

If any are missing, see the [Prerequisites](#prerequisites) section above.

### 2. Verify Recommender Mapping

Verify the LJ is mapped in the `grafana-recommender` repo:

```bash
cd grafana-recommender
grep -r "{lj-name}" internal/configs/state_recommendations/
```

Look for a rule that maps the LJ URL to the relevant Grafana UI pages:

```json
{
  "title": "Monitor a macOS system in Grafana Cloud",
  "url": "https://grafana.com/docs/learning-journeys/macos-integration/",
  "type": "learning-journey",
  "match": {
    "and": [
      { "urlPrefixIn": ["/connections/add-new-connection/macos-node"] },
      { "targetPlatform": "cloud" }
    ]
  }
}
```

If no mapping exists, create a branch and add the rule:

```bash
cd grafana-recommender
git checkout main && git pull
git checkout -b add-lj-{lj-name}
```

Add the rule to the appropriate file in `internal/configs/state_recommendations/` (usually `connections-cloud.json` for integrations).

**Verify the rule before committing:**
- **title**: Does it accurately describe the LJ? (e.g., "Monitor a MySQL database in Grafana Cloud")
- **url**: Does it point to the correct LJ path? (e.g., `https://grafana.com/docs/learning-journeys/mysql-integration/`)
- **urlPrefixIn**: Does it match the Grafana UI page(s) where users should see this LJ? (e.g., `/connections/add-new-connection/mysql`)

Once verified, commit and push to create a PR.

### 3. Create a Branch in interactive-tutorials

Each Learning Journey gets its own branch in the `interactive-tutorials` repo:

```bash
cd interactive-tutorials
git checkout main && git pull
git checkout -b interactive-lj-{lj-name}
```

**Important**: No branch is needed in the `website` repo. Interactive content lives only in `interactive-tutorials`.

### 4. Initial Scaffolding (AI-assisted)

1. Read the milestone's `index.md` from the website repo
2. **Copy ALL content** — intro, bullet lists, insights, images, videos, closing text
3. Check `interactive-tutorials` repo for existing selectors in `shared/snippets/`
4. Create `content.json` directly in `interactive-tutorials/{lj-name}-lj/{milestone}/`
5. Convert actionable steps to interactive blocks; keep explanatory content as markdown blocks
6. Use known-good selectors or TODO placeholders

**Skip milestones with no Grafana UI interactions:**
- If a milestone only involves terminal commands, external configuration, or reading information — don't create a `content.json` for it
- Only create content for milestones where users interact with the Grafana Cloud UI

> ⚠️ **Remember:** If you create a JSON, you must include ALL content from the source markdown. The JSON renders the milestone on the website.

### 5. Recording Selectors (Manual)

1. Open Pathfinder Block Editor in Grafana Cloud (`?pathfinderDev=true`)
2. Navigate to the correct page
3. Use **Record mode** or **Element Picker** to capture selectors
4. Test with "Show me" / "Do it" buttons
5. Update the `content.json` file with refined selectors

### 6. Iteration & Testing

1. Test the full guide end-to-end
2. Fix any broken selectors
3. Log problematic selectors in `selector-issue-tracker/issues.md`
4. Convert problematic steps to markdown if needed

### 7. Push & Create PR

```bash
git add {lj-name}-lj/
git commit -m "Add interactive content for {LJ Name} Learning Journey"
git push -u origin interactive-lj-{lj-name}
```

---

## JSON Structure

### Basic Structure

```json
{
  "id": "journey-name-milestone-name",
  "title": "Milestone Title",
  "blocks": [
    // Array of block objects
  ]
}
```

### File Location

Interactive JSON files live in the `interactive-tutorials` repo, **not** the website repo:

```
interactive-tutorials/
  {journey-name}-lj/           ← Add "-lj" suffix
    {milestone-name}/
      content.json             ← Always named content.json
```

**Example:**
```
interactive-tutorials/
  linux-server-integration-lj/
    select-platform/
      content.json
    install-alloy/
      content.json
    configure-alloy/
      content.json
```

The website repo contains only the markdown source:
```
website/content/docs/learning-journeys/
  linux-server-integration/
    select-platform/
      index.md                 ← Source markdown (read this)
```

---

## Block Types

### Markdown Block

Non-interactive text content.

```json
{
  "type": "markdown",
  "content": "Sign in to your Grafana Cloud environment."
}
```

**Use for:**
- Introductory text
- Steps that don't need interactivity
- Conditional steps ("If you have multiple...")
- Closing/transitional text

### Interactive Block

A single interactive step with Show me / Do it.

```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "button[aria-label='Save']",
  "content": "Click **Save** to save your changes.",
  "requirements": ["exists-reftarget"],
  "doIt": false
}
```

**Properties:**
| Property | Required | Description |
|----------|----------|-------------|
| `type` | Yes | Always `"interactive"` |
| `action` | Yes | `"highlight"`, `"button"`, `"formfill"`, `"hover"`, `"navigate"` |
| `reftarget` | Yes | CSS selector, button text, or URL |
| `content` | Yes | Markdown text describing the step |
| `requirements` | No | Array: `["exists-reftarget"]`, `["navmenu-open"]` |
| `doIt` | No | Set to `false` for "Show me" only (no "Do it" button) |
| `targetvalue` | For formfill | Value to enter in the field |

**Important:** Do NOT use the `tooltip` field for Learning Journeys. Put all helpful text in the `content` field or as a separate markdown block.

### Multistep Block

Multiple actions executed in sequence as one step.

```json
{
  "type": "multistep",
  "content": "Click **Drilldown > Logs** to open Logs Drilldown.",
  "steps": [
    {
      "action": "highlight",
      "reftarget": "button[aria-label='Expand section: Drilldown']"
    },
    {
      "action": "highlight",
      "reftarget": "a[data-testid='data-testid Nav menu item'][href='/a/grafana-lokiexplore-app/explore']"
    }
  ]
}
```

**Use for:**
- Multi-click navigation (expand menu → click item)
- Sequential actions that belong together conceptually
- When markdown describes it as one step (e.g., "Click X > Y")

### Section Block

Groups related blocks together.

```json
{
  "type": "section",
  "blocks": [
    // Array of blocks
  ]
}
```

### Image Block

Include images from the source markdown — the JSON also renders the LJ on the website.

```json
{
  "type": "image",
  "src": "/media/docs/learning-journey/metrics-drilldown/cpu-usage.png",
  "alt": "Metrics Drilldown dashboards showing CPU performance"
}
```

**Important:** Since the `content.json` is used to render the Learning Journey on the Grafana website, images from the markdown source **must** be included in the JSON.

### Video Block

Include videos from the source markdown — typically YouTube embeds using the `docs/video` shortcode.

```json
{
  "type": "video",
  "src": "https://www.youtube.com/embed/VIDEO_ID",
  "provider": "youtube",
  "title": "Video Title"
}
```

**Properties:**
| Property | Required | Description |
|----------|----------|-------------|
| `type` | Yes | Always `"video"` |
| `src` | Yes | Video URL (use embed URL for YouTube) |
| `provider` | No | `"youtube"` (default) or `"native"` for HTML5 video |
| `title` | No | Video title for accessibility |

**Hugo shortcode to JSON conversion:**

The website uses `{{< docs/video >}}` shortcodes with these attributes:
```markdown
{{< docs/video id="VIDEO_ID" start="00" end="57" align="right" >}}
Content wrapped by video...
{{< /docs/video >}}
```

Convert to JSON video block:
```json
{
  "type": "video",
  "src": "https://www.youtube.com/embed/VIDEO_ID?start=0&end=57",
  "provider": "youtube",
  "title": "Descriptive title based on context"
}
```

**Note:** The `start` and `end` parameters from the shortcode become URL query parameters in the embed URL.

**Important:** Like images, videos from the markdown source **must** be included in the JSON for proper website rendering.

---

## Finding Selectors

### 1. Check interactive-tutorials Repo First

Clone and search for existing selectors:

```bash
git clone https://github.com/grafana/interactive-tutorials.git /tmp/interactive-tutorials
```

**Key locations:**
- `shared/snippets/` — Reusable selector patterns
- `explore-drilldowns-101/content.json` — Drilldown selectors
- `first-dashboard/content.json` — Dashboard selectors

### 2. Known-Good Selector Patterns

**Navigation menu items:**
```
a[data-testid='data-testid Nav menu item'][href='/path/here']
```

**Expand menu section:**
```
button[aria-label='Expand section: SectionName']
```

**Data source picker:**
```
label[data-testid*="Data source"]
```

**Run query button:**
```
button[data-testid='data-testid RefreshPicker run button']
```

**Save dashboard:**
```
input[aria-label='Save dashboard title field']
```

### 3. Recording New Selectors

If no existing selector works:

1. Open Block Editor in Pathfinder (add `?pathfinderDev=true` to URL)
2. Click **Record** (red circle) on the block
3. Perform the action in Grafana
4. Press **Stop** or **Escape**
5. Or use **Element Picker** (crosshairs) to click directly on elements

### 4. Selector Priority

Prefer selectors in this order (most stable to least):

1. `data-testid` attributes — Intentionally stable
2. `aria-label` attributes — Accessibility-focused, fairly stable
3. Semantic attributes (`href`, `placeholder`) — Usually stable
4. Class names — Often auto-generated, avoid if possible

### 5. Dynamic Selectors (IMPORTANT)

⚠️ **Watch for selectors that include dynamic content.** These will break across environments.

**Red flags to watch for:**
- Numbers in testIDs: `Panel menu Log volume (3K)` — the count changes
- User/instance-specific values: `grafanacloud-mystack-logs`
- Timestamps or dates
- Index-based selectors that depend on data: `button:nth-match(5)`

**Solution: Use wildcard matching (`*=` contains)**

```
❌ Bad:  button[data-testid='data-testid Panel menu Log volume (3K)']
✅ Good: button[data-testid*='Panel menu Log volume']
```

**CSS selector operators:**
| Operator | Meaning | Example |
|----------|---------|---------|
| `=` | Exact match | `[data-testid='exact-value']` |
| `*=` | Contains | `[data-testid*='partial-value']` |
| `^=` | Starts with | `[data-testid^='prefix-']` |
| `$=` | Ends with | `[data-testid$='-suffix']` |

When in doubt, use `*=` (contains) for any testID that might include dynamic content.

---

## Common Patterns

### Navigation to a Feature

```json
{
  "type": "multistep",
  "content": "Click **Drilldown > Logs**.",
  "steps": [
    {
      "action": "highlight",
      "reftarget": "button[aria-label='Expand section: Drilldown']"
    },
    {
      "action": "highlight",
      "reftarget": "a[data-testid='data-testid Nav menu item'][href='/a/grafana-lokiexplore-app/explore']"
    }
  ]
}
```

### Dropdown/Picker (Show me only)

```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "label[data-testid*=\"Data source\"]",
  "content": "Select the **Data source** you want to query.",
  "doIt": false
}
```

### Form Input

```json
{
  "type": "interactive",
  "action": "formfill",
  "reftarget": "input[placeholder='Search metrics']",
  "targetvalue": "cpu",
  "content": "Enter `cpu` in the search field."
}
```

### Conditional Step (Use Markdown)

When a step only applies sometimes, use markdown instead of interactive:

```json
{
  "type": "markdown",
  "content": "If you have multiple data sources, select the one you want to query."
}
```

---

## Troubleshooting Selectors

### "Element not found"

- Is the nav menu open? Add `"requirements": ["navmenu-open"]`
- Is the element on screen? May need to scroll or navigate first
- Has the selector changed? Check interactive-tutorials for updates

### Tiny highlight area

- Selector is targeting an `<input>` inside a container
- Need a testID on the parent/container element
- Track as needing dev team fix

### Wrong element highlighted

- Selector is too generic
- Add more specificity: `:first-of-type`, `[href='...']`
- Use Element Picker to get exact selector

---

## Tracking Broken Selectors

Maintain a tracking file for selectors that need dev team fixes:

**Location:** `interactive-tutorials/selector-issue-tracker/issues.md`

**Format:**

```markdown
## Issue N: {Element Name}

**Learning Journey:** {lj-name}
**Milestone:** {milestone-name}

### Description
{What's wrong with the selector}

### Details
- **Instance:** learn.grafana.net (or specific instance)
- **Page URL:** /path/to/page
- **Steps to record:** Navigate to X, click Y

### Current JSON
```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "current-selector",
  "content": "Step description"
}
```

### Observed Behavior
{What happens when you test}

### Expected Behavior
{What should happen}

### Severity
- [ ] Blocking (cannot complete LJ)
- [x] Degraded (works but looks wrong)
- [ ] Minor (cosmetic)
```

**Share with:**
- Pathfinder team (`#proj-grafana-pathfinder`)
- Relevant UI teams

---

## Two Experiences: Markdown vs JSON

| Format | Location | Purpose |
|--------|----------|---------|
| `index.md` | `website` repo | Source markdown with Hugo shortcodes |
| `content.json` | `interactive-tutorials` repo | Website rendering + Pathfinder interactivity |

- Keep them **aligned in meaning and steps**
- JSON **must include ALL content** from the markdown:
  - Introductory paragraphs and explanations
  - Bullet lists (benefits, insights, etc.)
  - Images and videos
  - Closing/transitional paragraphs
- JSON content can be slightly more concise (no Hugo shortcodes)
- **Never** drift on the actual instructions

> ⚠️ The `content.json` is used to render the Learning Journey on the Grafana website. If you create a JSON for a milestone, it **replaces** the markdown rendering. Missing content = missing content for users.

---

## Quick Reference: Repo Separation

| What | Where |
|------|-------|
| LJ markdown content | `website/content/docs/learning-journeys/{lj-name}/` |
| Interactive JSON | `interactive-tutorials/{lj-name}-lj/{milestone}/content.json` |
| Reusable snippets | `interactive-tutorials/shared/snippets/` |
| Selector issues | `interactive-tutorials/selector-issue-tracker/issues.md` |
| AI reference docs | `interactive-tutorials/.cursor/` |

---

*Last updated: January 27, 2026*
