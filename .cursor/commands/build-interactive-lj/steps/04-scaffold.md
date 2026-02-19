# Step 4: Scaffold Content Files

Create the content.json structure for each milestone.

---

## Tutorial Mode Introduction

```
**Step 4: Scaffold Content Files**

I'll create the content.json structure for each milestone:
- Read the source markdown from the website repo
- Create directories in interactive-tutorials/[slug]-lj/
- Convert steps to interactive blocks (with empty selectors for now)

Ready to proceed? (Y/N)
```

Wait for confirmation, then scaffold.

---

## Expert Mode

Scaffold immediately without introduction.

---

## Before Starting

> 💡 **Important:** Before scaffolding, consult `reference/proven-patterns.md` for reusable JSON 
> structures that match common Grafana UI elements (navigation, forms, buttons, etc.).

> 📖 **Critical:** Read `reference/json-schema.md` for complete JSON structure requirements and 
> field reference. This ensures you use correct field names (`content` not `description`, 
> `targetvalue` not `formvalue`).

---

## CRITICAL: Scaffold ALL Milestones

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

---

## Scaffolding Process

**For each milestone:**

1. Read `website/content/docs/learning-paths/[slug]/[milestone]/index.md`
2. Create `interactive-tutorials/[slug]-lj/[milestone]/content.json`
3. Convert content using these rules:

### For Milestones WITH Interactive UI Steps:

- Numbered steps that reference Grafana UI → `interactive` blocks with `action: "highlight"` and empty `reftarget`
- Sequential navigation steps (e.g., "Navigate to X > Y > Z") → `multistep` blocks
- Explanatory text between steps → `markdown` blocks

### For Milestones WITHOUT Interactive UI Steps:

Convert ALL content to `markdown` blocks. Use a single markdown block with the full milestone content.

---

## JSON Schema Requirements

**CRITICAL:** Every content.json file MUST include these top-level fields:

```json
{
  "schemaVersion": "1.0.0",
  "id": "[learning-path-slug]-[milestone-slug]",
  "title": "[Milestone Title from index.md]",
  "blocks": [
    {
      "type": "markdown",
      "content": "[Full milestone content converted from markdown]"
    }
  ]
}
```

### Field Specifications:

- **`schemaVersion`**: Always `"1.0.0"` (string, required)
- **`id`**: Format: `[learning-path-slug]-[milestone-slug]` (string, required, kebab-case)
  - Example: `"billing-usage-navigate-to-billing-dashboard"`
- **`title`**: Human-readable milestone title from the source markdown (string, required)
  - Example: `"Navigate to the billing dashboard"`
- **`blocks`**: Array of content blocks (array, required)

### Example Complete File:

```json
{
  "schemaVersion": "1.0.0",
  "id": "billing-usage-business-value",
  "title": "Understand the business value",
  "blocks": [
    {
      "type": "markdown",
      "content": "Understanding your Grafana Cloud billing..."
    }
  ]
}
```

---

## Verification Checklist (REQUIRED)

Before proceeding to Step 5, verify EACH content.json file:

- [ ] File includes `"schemaVersion": "1.0.0"` at root level
- [ ] File includes `"id"` field with format `[learning-path-slug]-[milestone-slug]`
- [ ] File includes `"title"` field with human-readable milestone title
- [ ] File includes `"blocks"` array
- [ ] Every block has a `"type"` field
- [ ] Instruction text uses `"content"` (NOT `"description"`)
- [ ] Formfill actions use `"targetvalue"` (NOT `"formvalue"`)
- [ ] Navigation steps use `"multistep"` blocks
- [ ] Interactive blocks do NOT have `"requirements": ["exists-reftarget"]` (it's auto-applied)
- [ ] Interactive blocks have empty `"reftarget": ""` (selectors added in Step 5)

**If any check fails, fix before continuing.**

---

## Display

Use this exact format:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Step 4 complete: Scaffold

Created [N] content.json files:
├── [slug]-lj/milestone-1/content.json ([N] blocks)
├── [slug]-lj/milestone-2/content.json ([N] blocks)
└── ...

Verification: All checks passed ✓

⏳ Next: Step 5 - Selector Discovery
   Ready to open the test environment?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
