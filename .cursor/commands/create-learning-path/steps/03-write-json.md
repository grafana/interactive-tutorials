# Step 3: Write Enriched JSON

Create content.json files with both interactive blocks and website metadata.

---

## Tutorial Mode Introduction

```
**Step 3: Write Enriched JSON**

I'll create content.json files for each milestone:
- schemaVersion 2.0.0 with the `website` key for Hugo metadata
- Interactive blocks with empty selectors (filled in Step 5)
- Markdown blocks for conceptual content

Ready to proceed? (Y/N)
```

Wait for confirmation, then write.

---

## Expert Mode

Write immediately without introduction.

---

## Before Starting

> Read `reference/enriched-json-schema.md` for the complete field reference.
> Read `build-interactive-lj/reference/json-schema.md` for block type details.
> Read `build-interactive-lj/reference/proven-patterns.md` for reusable patterns.

---

## Directory Structure

Create the learning path directory:

```
interactive-tutorials/
  [slug]-lj/
    business-value/content.json
    install-alloy/content.json
    configure-alloy/content.json
    ...
    end-journey/content.json
```

Use the milestone folder names from the approved plan (Step 2).

---

## Writing Process

For EACH milestone in the approved plan:

### 1. Create the Root Structure

```json
{
  "schemaVersion": "2.0.0",
  "id": "[path-slug]-[milestone-slug]",
  "title": "[Milestone Title from plan]",
  "website": { ... },
  "blocks": [ ... ]
}
```

### 2. Populate the `website` Key

Use the milestone plan to fill in Hugo metadata:

| Plan field | JSON field |
|---|---|
| Milestone title (short) | `website.menuTitle` |
| Description | `website.description` |
| Weight | `website.weight` |
| Step number | `website.step` |
| CTA type | `website.cta.type` |
| Troubleshooting links | `website.cta.troubleshooting` |
| Side journey links | `website.side_journeys` |
| Related paths | `website.related_journeys` |

**Skip the `website` key** for milestones flagged as Hugo-only in the plan.

### 3. Write the Blocks

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

### 4. Leave Selectors Empty

For interactive blocks, set `"reftarget": ""` — selectors are discovered in Step 5.

Exception: nav menu items use a known pattern and can be filled immediately:
```json
"reftarget": "a[data-testid='data-testid Nav menu item'][href='/path']"
```

### 5. Set Requirements

| UI context | Requirement |
|---|---|
| Nav menu element | `["navmenu-open"]` |
| Page-specific action | `["on-page:/path"]` |
| Depends on previous section | `["section-completed:id"]` |
| No special context | Omit or use `[]` |

Never add `"exists-reftarget"` — it's auto-applied.

---

## Milestone Type Templates

### Business Value Milestone

```json
{
  "schemaVersion": "2.0.0",
  "id": "[slug]-business-value",
  "title": "The value of [feature]",
  "website": {
    "menuTitle": "The value of [feature]",
    "description": "Learn about [feature] and how it helps you [outcome]",
    "weight": 100,
    "step": 2,
    "cta": { "type": "continue" },
    "side_journeys": { ... }
  },
  "blocks": [
    { "type": "markdown", "content": "[Problem statement and solution benefits]" },
    { "type": "markdown", "content": "[Feature advantages list]" }
  ]
}
```

### Interactive Navigation Milestone

```json
{
  "schemaVersion": "2.0.0",
  "id": "[slug]-navigate-to-[location]",
  "title": "Navigate to [location]",
  "website": {
    "menuTitle": "[Short location name]",
    "description": "Learn how to navigate to [location]",
    "weight": 200,
    "step": 3
  },
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

### Verification Milestone

```json
{
  "schemaVersion": "2.0.0",
  "id": "[slug]-test-connection",
  "title": "Test the connection",
  "website": {
    "menuTitle": "Test connection",
    "description": "Verify that [component] is working correctly",
    "weight": 500,
    "step": 6,
    "cta": {
      "type": "success",
      "troubleshooting": {
        "title": "Explore the following troubleshooting topics if you need help:",
        "items": [
          { "title": "[Problem]", "link": "/docs/.../troubleshoot/#issue" }
        ]
      }
    }
  },
  "blocks": [ ... ]
}
```

### Conclusion Milestone

```json
{
  "schemaVersion": "2.0.0",
  "id": "[slug]-end-journey",
  "title": "Destination reached!",
  "website": {
    "menuTitle": "Destination reached!",
    "description": "Your journey concludes",
    "weight": 900,
    "step": 10,
    "cta": {
      "type": "conclusion",
      "image": {
        "src": "/media/docs/learning-journey/journey-conclusion-header-1.svg",
        "width": 735,
        "height": 175
      }
    },
    "related_journeys": { ... },
    "side_journeys": { ... }
  },
  "blocks": [
    { "type": "markdown", "content": "Congratulations on completing this journey!..." }
  ]
}
```

---

## Path Overview (`_index.md`)

The path overview page uses Hugo shortcodes that can't be represented in JSON. Write it as hand-crafted markdown in:

```
website/content/docs/learning-paths/[slug]/_index.md
```

Use the template from `website/.github/learning-paths/templates/path-index-frontmatter.yaml` and `path-index-content.md`.

---

## Verification Checklist

Before proceeding to Step 4:

- [ ] Every milestone has a `content.json` file
- [ ] Every file has `"schemaVersion": "2.0.0"`
- [ ] Every file has `"id"` in `[path-slug]-[milestone-slug]` format
- [ ] Every file has `"title"` matching the plan
- [ ] Interactive milestones have `"website"` key with required fields
- [ ] Hugo-only milestones have NO `"website"` key
- [ ] Interactive blocks use `"content"` (NOT `"description"`)
- [ ] Formfill actions use `"targetvalue"` (NOT `"formvalue"`)
- [ ] Interactive blocks have `"reftarget": ""` (selectors in Step 5)
- [ ] `"exists-reftarget"` is NOT manually added
- [ ] `_index.md` is written in the website repo

---

## Display

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Step 3 complete: JSON Files Written

Created [N] content.json files:
├── [slug]-lj/milestone-1/content.json ([N] blocks, website ✅)
├── [slug]-lj/milestone-2/content.json ([N] blocks, website ✅)
├── [slug]-lj/milestone-3/content.json ([N] blocks, website ❌ Hugo-only)
└── ...

Also created:
└── website/.../[slug]/_index.md (path overview)

Verification: All checks passed ✓

⏳ Next: Step 4 - Recommender Mapping
   Ready to proceed? (Y/N)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
