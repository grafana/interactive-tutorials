# JSON Schema Reference for Learning-Path Guides

> **Canonical reference:** For the full block type catalog, action types, and properties, see
> [`docs/json-guide-reference.md`](../../../../docs/json-guide-reference.md).
> For all requirement types (fixed and parameterized), see
> [`docs/requirements-reference.md`](../../../../docs/requirements-reference.md).
>
> This file documents only the **LJ-specific content rules** that differ from or extend the
> canonical reference — root-level field conventions, milestone scaffolding requirements,
> block selection guidance for LJ content, and the supplementary content pattern.

---

## Root-Level Schema

Every `content.json` in a learning path must include these top-level fields:

```json
{
  "id": "[learning-path-slug]-[milestone-slug]",
  "title": "[Milestone Title]",
  "blocks": []
}
```

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `schemaVersion` | string | Optional | Advisory field; not validated against a specific value. Current recommended value is `"1.1.0"`, but `"1.0.0"` and any other string are accepted at runtime. Omit if uncertain — the manifest defaults apply. | `"1.1.0"` |
| `id` | string | ✅ Yes | Format: `[learning-path-slug]-[milestone-slug]` (kebab-case) | `"billing-usage-navigate-to-billing-dashboard"` |
| `title` | string | ✅ Yes | Human-readable milestone title from source markdown | `"Navigate to the billing dashboard"` |
| `blocks` | array | ✅ Yes | Array of content blocks — see [docs/json-guide-reference.md](../../../../docs/json-guide-reference.md) for all block types | `[{...}, {...}]` |

### Complete Example

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

## Block Types for LJ Content

See [`docs/json-guide-reference.md`](../../../../docs/json-guide-reference.md) for the complete reference. The most common blocks in learning-path guides are:

| Type | Purpose | When to Use |
|------|---------|-------------|
| `markdown` | Explanatory text, instructions | Conceptual content, external actions, conditional UI |
| `interactive` | Automated actions with "Show me" / "Do it" | Single UI interactions (click, fill, hover) |
| `multistep` | Sequential navigation (shows "▶ Run N steps") | Multi-step navigation through menus |
| `section` | Groups steps for sequential numbering | Wrap related interactive/noop steps |
| `guided` | User performs manually, no automation | Manual actions that can't be automated |

For all 17 registered block types (plus the runtime-only `challenge` block), see the canonical reference.

---

## Interactive Action Types

See [`docs/interactive-actions.md`](../../../../docs/interactive-actions.md) for the full reference including `popout`. The most common actions in LJ guides:

| Action | Use Case | `reftarget` Value | Additional Fields |
|--------|----------|-------------------|-------------------|
| `highlight` | Click element by CSS selector | CSS selector | - |
| `button` | Click button by visible text | Button text | - |
| `formfill` | Enter text in field | CSS selector | `targetvalue` |
| `hover` | Reveal hover-dependent UI | CSS selector | - |
| `navigate` | Change pages | URL path | - |
| `noop` | Non-interactive numbered step | Not used | - |

### The `noop` Action

Use `noop` for steps that should be **numbered** within a `section` but don't trigger UI automation.

**When to use `noop`:**
- The step is inside a `section` and should be numbered in sequence with interactive steps
- The step is a directive telling the user to do something manually
- The step is instructional but part of a numbered procedure

**When NOT to use `noop`:**
- The content is an observation or confirmation → use `markdown`
- The content is purely explanatory → use `markdown`
- The content is outside a `section` → use `markdown`

```json
{
  "type": "interactive",
  "action": "noop",
  "content": "Enter a title and description for your dashboard, select a folder if applicable, and click **Save**."
}
```

### The `doIt` Property

Add `"doIt": false` to any interactive block where the user should perform the action manually.

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

## Requirements in LJ Guides

See [`docs/requirements-reference.md`](../../../../docs/requirements-reference.md) for the full reference. Common LJ requirements:

| Requirement | When to Use |
|-------------|-------------|
| `exists-reftarget` | Any DOM interaction (highlight, formfill, button, hover) |
| `navmenu-open` | Navigation menu elements |
| `on-page:/path` | Page-specific actions |
| `section-completed:id` | Sequential dependencies between sections |
| `is-admin` | Admin-only features |
| `has-datasource:<identifier>` | When a specific data source is needed |
| `has-plugin:id` | When a specific plugin must be installed |

---

## When to Use Markdown Instead of Interactive

| Scenario | Why Markdown is Better |
|----------|------------------------|
| Steps inside dialogs that require prior user actions | Dialog may not exist yet; automation will fail |
| External actions (run command on another machine) | Can't automate outside the browser |
| Conditional UI (create new vs use existing) | Multiple paths; can't predict user's choice |
| Complex multi-option flows | Better to explain options than force one path |
| Steps after external verification | User must complete real-world action first |

---

## CRITICAL: Scaffold ALL Milestones

**You MUST create content.json for EVERY milestone in the learning path.**

This includes:
- ✅ Milestones with interactive UI steps (use `interactive` blocks)
- ✅ Purely conceptual/educational milestones (use `markdown` blocks)
- ✅ Introduction or overview pages (use `markdown` blocks)
- ✅ Conclusion/outro pages (use `markdown` blocks)
- ✅ External-only actions (use `markdown` or `guided` blocks)

### For Milestones WITHOUT Interactive UI Steps

Convert ALL content to `markdown` blocks:

```json
{
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

The content.json files are the source of truth for learning paths. Extract and include ALL supplementary content from the website milestone's YAML frontmatter as markdown blocks at the END of the `blocks` array.

### Frontmatter Sections to Extract

| Frontmatter Key | Output Block Title | Description |
|------------------|--------------------|-------------|
| `side_journeys` | `### More to explore (optional)` | Links to related documentation |
| `related_journeys` | `### Related paths` | Links to other learning paths |
| `cta.troubleshooting` | `### Troubleshooting` | Links to troubleshooting documentation |

### Formatting Rules

Each supplementary block uses a **horizontal rule divider** (`---`) followed by an **H3 heading** (`###`).

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

### Root-Level Schema
- [ ] File includes `"id"` field with format `[learning-path-slug]-[milestone-slug]`
- [ ] File includes `"title"` field with human-readable milestone title
- [ ] File includes `"blocks"` array at root level

### Block-Level Requirements
- [ ] Every block has a `"type"` field
- [ ] Instruction text uses `"content"` (NOT `"description"`)
- [ ] Formfill actions use `"targetvalue"` (NOT `"formvalue"`)
- [ ] Navigation steps use `"multistep"` blocks
- [ ] Interactive blocks that target a CSS selector include `exists-reftarget` in their requirements array
- [ ] Interactive blocks have empty `"reftarget": ""` (selectors added in Step 5)

### Supplementary Content
- [ ] **`side_journeys` from frontmatter** → included as "More to explore" markdown block (if present)
- [ ] **`related_journeys` from frontmatter** → included as "Related paths" markdown block (if present)
- [ ] **`cta.troubleshooting` from frontmatter** → included as "Troubleshooting" markdown block (if present)

**If any check fails, fix before continuing.**
