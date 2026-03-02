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
- Include ALL supplementary content (More to explore, Related paths, Troubleshooting)

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
- **The content.json is becoming the source of truth** — all milestone content must live here

---

## CRITICAL: Include ALL Supplementary Content from Frontmatter

**The content.json files are the source of truth for learning paths.** You MUST extract and include
ALL supplementary content from the website milestone's frontmatter. This content appears as
markdown blocks at the END of the `blocks` array, after the main body content.

### Frontmatter Sections to Extract

Parse the YAML frontmatter from each `index.md` file and convert these sections into markdown blocks:

#### 1. `side_journeys` → "More to explore (optional)"

If the frontmatter contains a `side_journeys` section, add a markdown block:

```json
{
  "type": "markdown",
  "content": "**More to explore (optional)**\n\n- [Title 1](/link1)\n- [Title 2](/link2)"
}
```

**Source frontmatter:**
```yaml
side_journeys:
  title: More to explore (optional)
  heading: 'At this point in your journey, you can explore the following paths:'
  items:
    - title: 'Labels and Fields'
      link: '/docs/grafana-cloud/visualizations/simplified-exploration/logs/labels-and-fields/'
```

**Formatting rules:**
- Use the `heading` value as the intro text if present (some milestones have custom headings)
- If no `heading`, just use the bold title followed by the list
- Each item becomes a markdown link: `- [title](link)`

#### 2. `related_journeys` → "Related paths"

If the frontmatter contains a `related_journeys` section, add a markdown block:

```json
{
  "type": "markdown",
  "content": "**Related paths**\n\nConsider taking the following paths after you complete this journey.\n\n- [Title 1](/link1)\n- [Title 2](/link2)"
}
```

**Source frontmatter:**
```yaml
related_journeys:
  title: Related paths
  heading: Consider taking the following paths after you complete this journey.
  items:
    - title: Explore metrics using Metrics Drilldown
      link: '/docs/learning-paths/drilldown-metrics/'
```

**Formatting rules:**
- Include the `heading` value as intro text
- Each item becomes a markdown link: `- [title](link)`

#### 3. `cta.troubleshooting` → "Troubleshooting"

If the frontmatter contains a `cta.troubleshooting` section, add a markdown block:

```json
{
  "type": "markdown",
  "content": "**Troubleshooting**\n\nExplore the following troubleshooting topics if you need help:\n\n- [Title 1](/link1)\n- [Title 2](/link2)"
}
```

**Source frontmatter:**
```yaml
cta:
  type: success
  troubleshooting:
    title: 'Explore the following troubleshooting topics if you need help:'
    items:
      - title: Failed to install Alloy for Windows
        link: /docs/cloud-onboarding/next/troubleshoot/install-troubleshooting-windows-alloy/#error-...
```

**Formatting rules:**
- Use the `title` value from `cta.troubleshooting` as intro text
- Each item becomes a markdown link: `- [title](link)`

### Block Ordering

Supplementary blocks MUST appear at the end of the `blocks` array, in this order:

1. Main body content (markdown, interactive, multistep blocks)
2. Transition text (e.g., "In the next milestone, you'll...")
3. **More to explore** (from `side_journeys`)
4. **Related paths** (from `related_journeys`)
5. **Troubleshooting** (from `cta.troubleshooting`)

### Complete Example

Given this website frontmatter:

```yaml
side_journeys:
  title: More to explore (optional)
  heading: 'At this point in your journey, you can explore the following paths:'
  items:
    - title: 'Grafana Alloy configuration syntax and examples'
      link: '/docs/alloy/latest/reference/config-blocks/'
cta:
  type: success
  troubleshooting:
    title: 'Explore the following troubleshooting topics if you need help:'
    items:
      - title: Common errors when executing Alloy installation script
        link: /docs/grafana-cloud/monitor-infrastructure/integrations/troubleshoot/install-troubleshoot-linux-alloy/#common-errors
```

The content.json `blocks` array should end with:

```json
{
  "type": "markdown",
  "content": "**More to explore (optional)**\n\nAt this point in your journey, you can explore the following paths:\n\n- [Grafana Alloy configuration syntax and examples](/docs/alloy/latest/reference/config-blocks/)"
},
{
  "type": "markdown",
  "content": "**Troubleshooting**\n\nExplore the following troubleshooting topics if you need help:\n\n- [Common errors when executing Alloy installation script](/docs/grafana-cloud/monitor-infrastructure/integrations/troubleshoot/install-troubleshoot-linux-alloy/#common-errors)"
}
```

---

## Scaffolding Process

**For each milestone:**

1. Read `website/content/docs/learning-paths/[slug]/[milestone]/index.md`
2. Parse the YAML frontmatter to extract `side_journeys`, `related_journeys`, and `cta.troubleshooting`
3. Create `interactive-tutorials/[slug]-lj/[milestone]/content.json`
4. Convert the body content using the rules below
5. Append supplementary blocks (More to explore, Related paths, Troubleshooting) at the end

### For Milestones WITH Interactive UI Steps:

- Numbered steps that reference Grafana UI → `interactive` blocks with `action: "highlight"` and empty `reftarget`
- Sequential navigation steps (e.g., "Navigate to X > Y > Z") → `multistep` blocks
- Explanatory text between steps → `markdown` blocks

### For Milestones WITHOUT Interactive UI Steps:

Convert ALL content to `markdown` blocks. Use a single markdown block with the full milestone content.

### For Milestones That Use `pathfinder_data`:

Some milestones already reference a content.json via `pathfinder_data: [slug]-lj/[milestone]` and contain `{{< pathfinder/json >}}` instead of body content. For these:

1. The content.json already exists or is being created
2. You MUST still check the frontmatter for supplementary sections
3. If the existing content.json is missing supplementary blocks that exist in the frontmatter, add them

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
      "content": "[Main body content]"
    },
    {
      "type": "markdown",
      "content": "**More to explore (optional)**\n\n- [Link text](/path)"
    },
    {
      "type": "markdown",
      "content": "**Troubleshooting**\n\n- [Link text](/path)"
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

### Example Complete File (with supplementary content):

```json
{
  "schemaVersion": "1.0.0",
  "id": "mysql-integration-install-alloy",
  "title": "Install Grafana Alloy",
  "blocks": [
    {
      "type": "markdown",
      "content": "In this milestone, you install Grafana Alloy..."
    },
    {
      "type": "section",
      "blocks": [
        {
          "type": "interactive",
          "action": "highlight",
          "reftarget": "button[data-testid='agent-config-button']",
          "requirements": ["exists-reftarget"],
          "content": "In the **Install Alloy** section, click **Run Grafana Alloy**."
        }
      ]
    },
    {
      "type": "markdown",
      "content": "In your next milestone, you'll configure the integration settings."
    },
    {
      "type": "markdown",
      "content": "**More to explore (optional)**\n\nAt this point in your journey, you can explore the following paths:\n\n- [Grafana Alloy configuration syntax and examples](/docs/alloy/latest/reference/config-blocks/)"
    },
    {
      "type": "markdown",
      "content": "**Troubleshooting**\n\nExplore the following troubleshooting topics if you need help:\n\n- [Common errors when executing Alloy installation script](/docs/grafana-cloud/monitor-infrastructure/integrations/troubleshoot/install-troubleshoot-linux-alloy/#common-errors-when-executing-alloy-installation-script)\n- [Alloy is installed, but data doesn't appear in Grafana Cloud](/docs/grafana-cloud/monitor-infrastructure/integrations/troubleshoot/install-troubleshoot-linux-alloy/#alloy-is-installed-but-data-doesnt-appear-in-grafana-cloud)"
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
- [ ] **`side_journeys` from frontmatter** → included as "More to explore" markdown block (if present)
- [ ] **`related_journeys` from frontmatter** → included as "Related paths" markdown block (if present)
- [ ] **`cta.troubleshooting` from frontmatter** → included as "Troubleshooting" markdown block (if present)

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

Supplementary content included:
├── More to explore: [N] milestones
├── Related paths: [N] milestones
└── Troubleshooting: [N] milestones

Verification: All checks passed ✓

⏳ Next: Step 5 - Selector Discovery
   Ready to open the test environment?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
