# JSON Schema Requirements

This document defines the structure and field requirements for `content.json` files.

---

## Root-Level Schema (REQUIRED)

**CRITICAL:** Every `content.json` file MUST include these top-level fields:

```json
{
  "id": "[learning-path-slug]-[milestone-slug]",
  "title": "[Milestone Title]",
  "blocks": [
    // ... content blocks here
  ]
}
```

### Field Specifications:

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `schemaVersion` | string | Optional | Omit it and the parser defaults to `"1.1.0"`. If you include it, the value MUST be `"1.1.0"` — any other value (for example `"1.0.0"`) fails validation. | `"1.1.0"` |
| `id` | string | ✅ Yes | Format: `[learning-path-slug]-[milestone-slug]` (kebab-case) | `"billing-usage-navigate-to-billing-dashboard"` |
| `title` | string | ✅ Yes | Human-readable milestone title from source markdown | `"Navigate to the billing dashboard"` |
| `blocks` | array | ✅ Yes | Array of content blocks (see below) | `[{...}, {...}]` |

### Complete Example:

```json
{
  "id": "billing-usage-business-value",
  "title": "Understand the business value",
  "blocks": [
    {
      "type": "markdown",
      "content": "Understanding your Grafana Cloud billing and usage..."
    },
    {
      "type": "interactive",
      "action": "highlight",
      "reftarget": "a[href='/dashboards']",
      "content": "Navigate to **Dashboards**."
    },
    {
      "type": "markdown",
      "content": "---\n\n### More to explore (optional)\n\n- [Cost management docs](/docs/grafana-cloud/cost-management-and-billing/)"
    }
  ]
}
```

---

## Block Types

| Type | Purpose | Has "Do it"? | When to Use |
|------|---------|--------------|-------------|
| `markdown` | Explanatory text, instructions | No | Conceptual content, external actions, conditional UI |
| `interactive` | Automated actions with "Show me" / "Do it" | Yes | Single UI interactions (click, fill, hover) |
| `multistep` | Sequential navigation (shows "▶ Run N steps") | Yes | Multi-step navigation through menus |
| `section` | Groups steps for sequential numbering | N/A | Wrap related interactive/noop steps so they render as numbered steps |
| `guided` | User performs manually, no automation | No | Manual actions that can't be automated |

---

## Interactive Action Types

| Action | Use Case | `reftarget` Value | Additional Fields |
|--------|----------|-------------------|-------------------|
| `highlight` | Click element by CSS selector | CSS selector | - |
| `button` | Click button by visible text | Button text | - |
| `formfill` | Enter text in field | CSS selector | `targetvalue` |
| `hover` | Reveal hover-dependent UI | CSS selector | - |
| `navigate` | Change pages | URL path | - |
| `noop` | Non-interactive numbered step (no automation) | Not used | - |

### The `noop` Action

Use `noop` only for steps that should be **numbered** within a `section` but must **not** tell the learner to click, type, open, or fill UI. Prefer `markdown` for instructions without a stable selector. Prefer a real interactive action (`highlight`, `button`, `formfill`, `guided`) when you have a `reftarget`.

**When to use `noop`:**
- Intentional numbered pause that is not a click/type instruction (e.g. “Wait for the query to finish”, “Confirm the preview looks right before you continue”)
- Optional look-at context with a `reftarget` where the copy does not instruct a click

**When NOT to use `noop`:**
- Learner actions without a selector (“Open a dashboard…”, “Enter the username…”, “Click **Save**”) → use `markdown`, or restore a real interactive step if you have a stable selector
- Flaky-selector fallback → use `markdown` (or `highlight` + `doIt: false` when a selector exists)
- Observation / confirmation / pure explanation that should not be numbered → use `markdown`
- Content outside a `section` → use `markdown`

```json
{
  "type": "interactive",
  "action": "noop",
  "content": "Wait for the query preview to finish loading before you continue."
}
```

For a manual UI instruction without a working highlight, use markdown instead:

```json
{
  "type": "markdown",
  "content": "In the **Label** field, enter a user-friendly display name.\n\nFor example, for the variable named `environment`, enter the label `Environment`."
}
```

### The `doIt` Property

Add `"doIt": false` to any interactive block where the user should perform the action manually. This hides the "Do it" button while keeping the "Show me" highlight.

**When to use `doIt: false`:**
- The step involves user-specific input (e.g., selecting their own data source, entering a custom name)
- The automated action could cause unintended side effects
- The step highlights an element but the user should decide when/how to interact

```json
{
  "type": "interactive",
  "action": "formfill",
  "reftarget": "[data-testid='data-testid Data source settings page name input field']",
  "targetvalue": "My Infinity Data Source",
  "content": "Enter a name for the data source.",
  "doIt": false
}
```

---

## Field Reference

### IMPORTANT: Use Correct Field Names

**Common mistakes to avoid:**
- ❌ `description` → ✅ `content`
- ❌ `formvalue` → ✅ `targetvalue`
- ❌ `title` on interactive blocks (not needed)

### Optional Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `doIt` | boolean | `true` | Set to `false` to hide the "Do it" button while keeping "Show me" |

---

## JSON Structure Examples

### Highlight Action (Correct)

```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "[data-testid=\"my-element\"]",
  "content": "Click **Button** to do the thing.",
  "requirements": ["exists-reftarget"]
}
```

### Button Action (Correct)

Uses button text, not CSS selector:

```json
{
  "type": "interactive",
  "action": "button",
  "reftarget": "Install",
  "content": "Click **Install** to add the dashboards.",
  "requirements": ["exists-reftarget"]
}
```

### Formfill Action (Correct)

```json
{
  "type": "interactive",
  "action": "formfill",
  "reftarget": "[aria-label=\"Search connections by name\"]",
  "targetvalue": "value to enter",
  "content": "Enter the value.",
  "requirements": ["exists-reftarget"]
}
```

### Hover Action (Correct)

For revealing hover-dependent UI:

```json
{
  "type": "interactive",
  "action": "hover",
  "reftarget": "[data-testid=\"hover-target\"]",
  "content": "Hover over this element to reveal options.",
  "requirements": ["exists-reftarget"]
}
```

### Section Block (Correct)

Wraps interactive/noop steps so they render as a numbered sequence. All `interactive` and `noop` blocks inside a section are assigned step numbers (1, 2, 3...). `markdown` and `image` blocks inside a section are unnumbered.

```json
{
  "type": "section",
  "blocks": [
    {
      "type": "interactive",
      "action": "noop",
      "content": "Sign in to your Grafana environment."
    },
    {
      "type": "multistep",
      "content": "Navigate to **Connections > Add new connection**.",
      "requirements": ["navmenu-open"],
      "steps": [
        { "action": "highlight", "reftarget": "a[data-testid='data-testid Nav menu item'][href='/connections']" },
        { "action": "highlight", "reftarget": "a[data-testid='data-testid Nav menu item'][href='/connections/add-new-connection']" }
      ]
    },
    {
      "type": "markdown",
      "content": "You should see the connections page."
    }
  ]
}
```

> **Key rule:** A `section` with only one step should be a plain `interactive` block instead. Don't wrap a single step in a section.

### Multistep Block (Correct)

For navigation sequences:

```json
{
  "type": "multistep",
  "content": "Navigate to **X > Y > Z**.",
  "requirements": ["navmenu-open"],
  "steps": [
    { "action": "highlight", "reftarget": "[aria-label=\"Expand section: Connections\"]" },
    { "action": "highlight", "reftarget": "a[href=\"/connections/add-new-connection\"]" }
  ]
}
```

### Guided Block (Correct)

User performs action manually, no "Do it" button:

```json
{
  "type": "guided",
  "content": "Copy the installation command and run it on your server.",
  "requirements": []
}
```

### Markdown Block (Correct)

```json
{
  "type": "markdown",
  "content": "This is explanatory text. Use markdown formatting:\n\n- Bullet points\n- **Bold text**\n- `Code snippets`"
}
```

---

## Requirements Reference

| Requirement | When to Use | Notes |
|-------------|-------------|-------|
| `exists-reftarget` | Any DOM interaction (highlight, formfill, button, hover) | Include for selector-targeting steps |
| `navmenu-open` | Navigation menu elements (ensures menu is expanded) | — |
| `on-page:/path` | Page-specific actions (checks current URL) | — |
| `section-completed:id` | Sequential dependencies between sections | — |
| `is-admin` | Admin-only features | — |
| `has-datasource:type` | When a specific data source is needed | — |
| `has-plugin:id` | When a specific plugin must be installed | — |

> `exists-reftarget` is the standard convention for selector-targeting steps. Include it in the `requirements` array for any block or step with a `reftarget`.

---

## When to Use Markdown Instead of Interactive

Some steps are better as plain `markdown` blocks rather than `interactive`:

| Scenario | Why Markdown is Better |
|----------|------------------------|
| Steps inside dialogs that require prior user actions | Dialog may not exist yet; automation will fail |
| External actions (run command on another machine) | Can't automate outside the browser |
| Conditional UI (create new vs use existing) | Multiple paths; can't predict user's choice |
| Complex multi-option flows | Better to explain options than force one path |
| Steps after external verification | User must complete real-world action first |

### Example from Windows Integration

The "Test Alloy connection" button only appears after the user has actually installed Alloy on their Windows machine. Since automation can't do that, the step is markdown:

```json
{
  "type": "markdown",
  "content": "After installing Alloy, click **Test Alloy connection** to verify the installation."
}
```

---

## Scaffolding Rules

### CRITICAL: Scaffold ALL Milestones

**You MUST create content.json for EVERY milestone in the learning path.**

This includes:
- ✅ Milestones with interactive UI steps (use `interactive` blocks)
- ✅ Purely conceptual/educational milestones (use `markdown` blocks)
- ✅ Introduction or overview pages (use `markdown` blocks)
- ✅ Conclusion/outro pages (use `markdown` blocks)
- ✅ External-only actions (use `markdown` or `guided` blocks)

**Why scaffold everything?**
- Pathfinder needs a content.json for every milestone to track progress through the learning path
- Even non-interactive milestones need to be represented so users can mark them complete
- Skipping milestones breaks the learning path flow
- **The content.json is the source of truth** — all milestone content must live here

### For Milestones WITH Interactive UI Steps:

- Numbered steps that reference Grafana UI → `interactive` blocks with `action: "highlight"` and empty `reftarget`
- Sequential navigation steps (e.g., "Navigate to X > Y > Z") → `multistep` blocks
- Explanatory text between steps → `markdown` blocks

### For Milestones WITHOUT Interactive UI Steps:

Convert ALL content to `markdown` blocks:

```json
{
  "schemaVersion": "1.0.0",
  "id": "learning-path-milestone-slug",
  "title": "Milestone Title",
  "blocks": [
    {
      "type": "markdown",
      "content": "[Full milestone content converted from markdown]"
    }
  ]
}
```

---

## CRITICAL: Include ALL Supplementary Content from Frontmatter

**The content.json files are the source of truth for learning paths.** You MUST extract and include
ALL supplementary content from the website milestone's YAML frontmatter. These appear as markdown
blocks at the END of the `blocks` array.

### Frontmatter Sections to Extract

| Frontmatter Key | Output Block Title | Description |
|------------------|--------------------|-------------|
| `side_journeys` | `### More to explore (optional)` | Links to related documentation |
| `related_journeys` | `### Related paths` | Links to other learning paths |
| `cta.troubleshooting` | `### Troubleshooting` | Links to troubleshooting documentation |

### Formatting Rules

Each supplementary block uses a **horizontal rule divider** (`---`) followed by an **H3 heading** (`###`). This visually separates supplementary content from the main body and renders the heading at a larger, more readable size than bold text.

### Block Ordering

Supplementary blocks MUST appear at the end of the `blocks` array, in this order:

1. Main body content (markdown, interactive, multistep blocks)
2. Transition text (e.g., "In the next milestone, you'll...")
3. **More to explore** (from `side_journeys`)
4. **Related paths** (from `related_journeys`)
5. **Troubleshooting** (from `cta.troubleshooting`)

### Examples

**More to explore** (from `side_journeys`):
```json
{
  "type": "markdown",
  "content": "---\n\n### More to explore (optional)\n\nAt this point in your journey, you can explore the following paths:\n\n- [Labels and Fields](/docs/grafana-cloud/visualizations/simplified-exploration/logs/labels-and-fields/)"
}
```

**Related paths** (from `related_journeys`):
```json
{
  "type": "markdown",
  "content": "---\n\n### Related paths\n\nConsider taking the following paths after you complete this journey.\n\n- [Explore metrics using Metrics Drilldown](/docs/learning-paths/drilldown-metrics/)"
}
```

**Troubleshooting** (from `cta.troubleshooting`):
```json
{
  "type": "markdown",
  "content": "---\n\n### Troubleshooting\n\nExplore the following troubleshooting topics if you need help:\n\n- [Failed to install Alloy for Windows](/docs/cloud-onboarding/next/troubleshoot/install-troubleshooting-windows-alloy/#error-failed-to-install-alloy-for-windows)"
}
```

---

## Verification Checklist

Before proceeding to selector discovery, verify EACH content.json file:

### Root-Level Schema:
- [ ] File includes `"schemaVersion": "1.0.0"` at root level
- [ ] File includes `"id"` field with format `[learning-path-slug]-[milestone-slug]`
- [ ] File includes `"title"` field with human-readable milestone title
- [ ] File includes `"blocks"` array at root level

### Block-Level Requirements:
- [ ] Every block has a `"type"` field
- [ ] Instruction text uses `"content"` (NOT `"description"`)
- [ ] Formfill actions use `"targetvalue"` (NOT `"formvalue"`)
- [ ] Navigation steps use `"multistep"` blocks
- [ ] Interactive blocks that target a CSS selector include `exists-reftarget` in their requirements array (repo convention)
- [ ] Interactive blocks have empty `"reftarget": ""` (selectors added in Step 5)

### Supplementary Content:
- [ ] **`side_journeys` from frontmatter** → included as "More to explore" markdown block (if present)
- [ ] **`related_journeys` from frontmatter** → included as "Related paths" markdown block (if present)
- [ ] **`cta.troubleshooting` from frontmatter** → included as "Troubleshooting" markdown block (if present)

**If any check fails, fix before continuing.**
