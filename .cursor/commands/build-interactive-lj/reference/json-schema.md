# JSON Schema Requirements

This document defines the structure and field requirements for `content.json` files.

---

## Root-Level Schema (REQUIRED)

**CRITICAL:** Every `content.json` file MUST include these top-level fields:

```json
{
  "schemaVersion": "1.0.0",
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
| `schemaVersion` | string | ✅ Yes | Always `"1.0.0"` | `"1.0.0"` |
| `id` | string | ✅ Yes | Format: `[learning-path-slug]-[milestone-slug]` (kebab-case) | `"billing-usage-navigate-to-billing-dashboard"` |
| `title` | string | ✅ Yes | Human-readable milestone title from source markdown | `"Navigate to the billing dashboard"` |
| `blocks` | array | ✅ Yes | Array of content blocks (see below) | `[{...}, {...}]` |

### Complete Example:

```json
{
  "schemaVersion": "1.0.0",
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

---

## Field Reference

### IMPORTANT: Use Correct Field Names

**Common mistakes to avoid:**
- ❌ `description` → ✅ `content`
- ❌ `formvalue` → ✅ `targetvalue`
- ❌ `title` on interactive blocks (not needed)

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

| Requirement | When to Use | Auto-Applied? |
|-------------|-------------|---------------|
| `exists-reftarget` | Any DOM interaction (highlight, formfill, button, hover) | ✅ Yes (don't add manually) |
| `navmenu-open` | Navigation menu elements (ensures menu is expanded) | No |
| `on-page:/path` | Page-specific actions (checks current URL) | No |
| `section-completed:id` | Sequential dependencies between sections | No |
| `is-admin` | Admin-only features | No |
| `has-datasource:type` | When a specific data source is needed | No |
| `has-plugin:id` | When a specific plugin must be installed | No |

> ⚠️ **Important:** `exists-reftarget` is auto-applied by Pathfinder. Never add it manually to interactive blocks.

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

### For Milestones WITH Interactive UI Steps:

- Numbered steps that reference Grafana UI → `interactive` blocks with `action: "highlight"` and empty `reftarget`
- Sequential navigation steps (e.g., "Navigate to X > Y > Z") → `multistep` blocks
- Explanatory text between steps → `markdown` blocks

### For Milestones WITHOUT Interactive UI Steps:

Convert ALL content to `markdown` blocks with proper root-level schema:

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
- [ ] Interactive blocks do NOT have `"requirements": ["exists-reftarget"]` (it's auto-applied)
- [ ] Interactive blocks have empty `"reftarget": ""` (selectors added in Step 5)

**If any check fails, fix before continuing.**
