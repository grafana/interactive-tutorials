---
name: autogen-guide-dashboard
description: Generate interactive guide content.json files from Grafana dashboard JSON. Analyzes dashboard panels, variables, rows, and data sources to produce a Pathfinder guide that tours or explains a dashboard. Use when the user provides dashboard JSON (file, pasted, or Grafana API URL) and wants to create a guide from it.
---

# AutoGen Guide from Dashboard JSON

Generate an interactive guide `content.json` by analyzing a Grafana dashboard JSON export. This skill orchestrates a multi-phase pipeline where **each phase runs in a sub-agent that loads only the context it needs**. The orchestrator (you) manages the workflow, user interactions, and handoffs.

**Do NOT read external reference files upfront.** Each phase's sub-agent loads its own references. Everything the orchestrator needs is inline below.

---

## Workflow Overview

```
Input (Dashboard JSON)
  │
  ├─ Phase 1: Acquire & Scope ─── orchestrator (no external reads)
  │    Output: dashboard JSON parsed, scope confirmed by user
  │
  ├─ Phase 2: Extract & Assess ── sub-agent loads dashboard-extraction-patterns.md
  │  │                              + dashboard-selector-strategies.md
  │    Output: {guide_dir}/EXTRACTION_REPORT.md
  │
  ├─ Checkpoint: Plan ──────────── orchestrator builds plan, user confirms
  │    Output: {guide_dir}/GUIDE_PLAN.md
  │
  ├─ Phase 3: Generate Guide ──── per-section sub-agents, each loads authoring-guide.mdc
  │    │                            + receives panel JSON context for its section
  │    │  3.1 Create guide shell (orchestrator)
  │    │  3.2 For each section → sub-agent generates section JSON
  │    │  3.3 Assemble sections into content.json (orchestrator)
  │    │  3.4 Generate SELECTOR_REPORT.md (orchestrator)
  │    Output: {guide_dir}/content.json + SELECTOR_REPORT.md
  │
  └─ Phase 4: Review & Fix ────── sub-agent loads review-guide-pr.mdc
       Output: fixed content.json + change report
```

---

## Critical Rules

These rules apply to ALL generated guides. They are passed to sub-agents in their prompts.

1. **No markdown titles** -- the guide `title` renders in the app frame; a leading `## Title` duplicates it
2. **`exists-reftarget` is auto-applied** -- never add it manually to requirements
3. **`navmenu-open`** required for any step targeting navigation menu elements
4. **`on-page:/path`** required for page-specific interactive actions
5. **Tooltips** -- under 250 characters, one sentence, don't name the highlighted element
6. **`verify`** on all state-changing actions (Save, Create, Test)
7. **`doIt: false` for secrets** -- never automate filling passwords/tokens/keys
8. **Section bookends** -- brief "what you'll do" intro markdown, "what you've done" summary markdown
9. **Sections, not markdown headers** -- group steps with `section` blocks, each with a unique kebab-case `id`
10. **Connect sections** -- if section 1's objective creates a resource, section 2 should require it
11. **Action-focused content** -- "Save your configuration" not "The save button can be clicked"
12. **Bold only GUI names** -- "Click **Save & test**" not "Click the **Save & test** button"
13. **`skippable: true`** for conditional fields and permission-gated steps
14. **No multistep singletons** -- a `multistep` with one step must be a plain `interactive` block
15. **No focus-before-formfill** -- `highlight` on an input with `doIt: true` is a no-op; use `formfill` or set `doIt: false`

---

## Golden Examples

These examples show the target output quality for common dashboard guide patterns. Pass the relevant ones to each section's sub-agent.

### Example A: Panel highlight with educational tooltip

The most common pattern for dashboard tours. Highlight a panel and explain what it shows.

```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "section[data-testid='data-testid Panel header CPU throttling']",
  "doIt": false,
  "content": "Review the **CPU throttling** panel.\n\nThis panel shows how much time your container is being artificially slowed down because it's trying to use more CPU than its configured limits allow.",
  "tooltip": "High throttling means your application is running slower than it could."
}
```

Key things: `action: "highlight"` with `doIt: false` (view-only panels), selector uses the panel header `data-testid` pattern, educational content explains what the visualization means, tooltip is concise.

### Example B: Panel content highlight (targeting the visualization area)

When you want to highlight the chart/visualization inside a panel rather than the header.

```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "section[data-testid='data-testid Panel header Alignment: Pod Usage/Requests (%)'] > div[data-testid='data-testid panel content']",
  "doIt": false,
  "content": "Review the **Alignment** graph for Pod CPU usage compared to requests.\n\nDetermine if Pods are running over or too close to their CPU requests.",
  "tooltip": "Ideally usage should be 60-90% of requests."
}
```

Key things: targets panel content `div` inside the header `section`, uses `>` child combinator, content is action-oriented.

### Example C: Variable dropdown interaction

Highlight a template variable dropdown and explain what it filters.

```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "div[data-testid='data-testid template variable'] label:contains('component')",
  "doIt": false,
  "content": "The **component** variable filters all panels to show data for a specific service component.\n\nSelect a value to narrow the dashboard to one service.",
  "tooltip": "Each panel with $component in its query updates when you change this.",
  "skippable": true,
  "hint": "Variable dropdowns appear at the top of the dashboard."
}
```

Key things: `doIt: false` because the user should choose their own value, `skippable: true` because variable interaction is optional, content explains the filtering effect.

### Example D: Row navigation with expand/collapse

Expand a collapsed row to reveal the panels within it.

```json
[
  {
    "type": "interactive",
    "action": "button",
    "reftarget": "Details for $component",
    "content": "Expand the **Details for $component** row to reveal detailed panels.",
    "tooltip": "Rows group related panels; click to expand or collapse."
  },
  {
    "type": "interactive",
    "action": "highlight",
    "reftarget": "div[data-testid='data-testid Layout container row Details for $component'] section:nth-match(1)",
    "doIt": false,
    "content": "The first panel in this row shows the error rate for the selected component.",
    "tooltip": "Errors are calculated as non-2xx responses divided by total requests."
  }
]
```

Key things: row expand uses `action: "button"` with the row title text, subsequent panel highlights are scoped inside the row's `Layout container` div, `:nth-match()` disambiguates panels within the row.

### Example E: Guided hover interaction for panel drill-down

Use a `guided` block when the user needs to hover to reveal a data link or tooltip.

```json
{
  "type": "guided",
  "content": "Hover over the **Frontend Response Latency** panel to see detailed data points.",
  "steps": [
    {
      "action": "hover",
      "reftarget": "section[data-testid='data-testid Panel header Frontend Response Latency'] div:nth-match(7)"
    }
  ]
}
```

Key things: `guided` (not `multistep`) for user-performed actions, hover reveals tooltip data in time-series panels, uses `:nth-match()` to target the correct inner div.

### Example F: Navigate to a specific dashboard

When the guide needs to direct the user to a specific dashboard URL.

```json
{
  "type": "interactive",
  "action": "navigate",
  "reftarget": "/d/abc123/my-dashboard",
  "content": "Navigate to the **My Dashboard** dashboard to begin the tour."
}
```

Key things: `action: "navigate"` with the dashboard path, no `doIt` needed for navigation.

### Example G: noop for dashboard concepts

When no single element can be targeted but the user needs context about the dashboard structure.

```json
{
  "type": "interactive",
  "action": "noop",
  "content": "This dashboard uses **Prometheus** as its data source and queries metrics with PromQL. All panels share the same time range, which you can adjust using the time picker in the top-right corner.",
  "skippable": true
}
```

Key things: `noop` when there's no sensible element to highlight. Use for explaining dashboard-wide concepts (shared data source, time range, refresh interval).

---

## Phase 1: Acquire and Scope (Orchestrator)

You handle this phase directly. No sub-agent needed.

### 1.1 Parse the Input

The user provides dashboard JSON via one of:
- **File path**: local path to a `.json` file
- **Pasted JSON**: raw JSON in the conversation
- **Grafana API URL**: `https://<instance>/api/dashboards/uid/<uid>`
- **Dashboard URL**: `https://<instance>/d/<uid>/<slug>?...` (derive API URL from this)

If given a dashboard URL, extract the UID (the path segment immediately after `/d/`) and strip any query parameters or trailing slug:

```
Dashboard URL: https://play.grafana.org/d/vmie2cmWz/bar-gauge?orgId=1&from=now-6h&to=now
                                          ^^^^^^^^^^
                                          UID
API URL:       https://play.grafana.org/api/dashboards/uid/vmie2cmWz
```

### 1.2 Load the Dashboard JSON

- **File path**: read the file directly.
- **Pasted JSON**: save to `{guide_dir}/dashboard-source.json` for reference.
- **Dashboard URL or API URL**: fetch via curl as shown below.

#### Fetching from a URL

Extract the UID from the dashboard URL and run:

```bash
curl -sf "https://<instance>/api/dashboards/uid/<uid>" | jq '.dashboard' > {guide_dir}/dashboard-source.json
```

The Grafana REST API wraps the dashboard model inside `{"dashboard": {...}, "meta": {...}}`. The `jq '.dashboard'` step unwraps it so the file contains the raw dashboard JSON with `panels`, `title`, `uid`, etc. at the top level.

If `jq` is not available, fetch without piping and manually read the `.dashboard` key from the response.

**Authentication limitation**: This curl approach only works for **unauthenticated / anonymous-access Grafana instances** (e.g., play.grafana.org). If the instance is protected by password auth, Okta, SAML, OAuth, or any other login mechanism, the curl will fail with a 401/403 or return an HTML login page instead of JSON. **Do not attempt to resolve authentication issues.** Instead, tell the user:

> "This Grafana instance requires authentication, so I can't fetch the dashboard JSON directly. Please export the dashboard JSON yourself:
> 1. Open the dashboard in your browser
> 2. Click the **Share** icon (or go to Dashboard settings → JSON Model)
> 3. Copy the JSON and paste it here, or save it to a file and give me the path."

After fetching or receiving the JSON, validate it has the expected top-level keys: `panels` (or `rows` for legacy format), `templating`, `title`, `uid`. If you see HTML or an `{"error": ...}` response instead, the fetch failed — fall back to asking the user to provide the JSON manually as described above.

### 1.3 Assess Scope

Count the dashboard elements and present to the user:

> "This dashboard contains 8 panels across 2 rows, with 3 template variables and 1 data source. This will produce a guide with approximately 3 sections and 12-16 steps. Should I proceed?"

Scope guidelines by panel count:
- **< 3 panels**: Too small for a guide. Suggest combining with another dashboard or expanding scope.
- **3–12 panels**: Good scope for one guide.
- **12–25 panels**: Large. Consider splitting by row or logical grouping.
- **> 25 panels**: Must split. Suggest one guide per row group or logical theme.

### 1.4 Identify Dashboard Metadata

Extract from the JSON:
- `uid` and `title` -- for guide ID and title
- `schemaVersion` -- for format compatibility
- URL path: `/d/<uid>/<slug>` -- for `on-page:` requirements
- `tags[]` -- context for guide description

### 1.5 Create the Guide Directory

Create `{guide-id}/` in the workspace root. The `guide-id` should be kebab-case, derived from the dashboard title (e.g., `performance-stats-tour`, `k8s-cpu-dashboard`).

Proceed to Phase 2 after the user confirms scope.

---

## Phase 2: Extract & Assess (Sub-Agent)

Launch a sub-agent using the Task tool. This sub-agent loads the dashboard-specific extraction and selector references, analyzes the JSON, and writes a structured report.

### Sub-agent prompt template

Fill in `{placeholders}` and pass as the Task prompt:

```
You are analyzing a Grafana dashboard JSON export to extract interactive elements for a Pathfinder guide.

**Read these reference files first:**
1. `.cursor/skills/autogen-guide-dashboard/dashboard-extraction-patterns.md` -- panel types, row detection, variable extraction, data source mapping
2. `.cursor/skills/autogen-guide-dashboard/dashboard-selector-strategies.md` -- selector patterns for panels, rows, variables; grading model

**Dashboard JSON to analyze** (read this file):
{path_to_dashboard_json}

**Your task:**
1. Parse the top-level dashboard structure: title, uid, schemaVersion, tags
2. Extract all panels: title, type, gridPos, targets (query expressions), datasource, repeat config
3. Detect row groupings: explicit `type: "row"` panels, or gridPos.y clustering
4. Extract template variables from `templating.list[]`: name, type, query, current value, datasource
5. Map variable-to-panel bindings: scan targets[].expr, panel titles, and repeat config for $varName references
6. Extract data sources: from panels[].datasource and templating.list[].datasource
7. Grade each panel's selector stability (Green/Yellow/Red based on title uniqueness)
8. Note any transformations or overrides that affect panel behavior

**Write your results** to `{guide_dir}/EXTRACTION_REPORT.md` using this structure:

## Extraction Report

**Dashboard**: {title} (uid: {uid})
**Schema version**: {schemaVersion}
**URL path**: /d/{uid}/{slug}
**Panels**: N
**Variables**: N
**Data sources**: N
**Rows/groups**: N

### Selector Quality
- N/N Green (unique panel title → unique data-testid)
- N/N Yellow (duplicate title, needs nth-match or row scoping)
- N/N Red (no title, or variable-interpolated title)

### Row/Section Groups

For each row or logical group:
#### {Row/Group Name}
- Panels: (table with columns: Title, Type, Selector, Grade, Variables Referenced, Data Source)
- Row selector: `div[data-testid='data-testid Layout container row {title}']` (if explicit row)

### Template Variables

For each variable:
- Name: $varName
- Type: query | custom | datasource | interval | textbox
- Current value: {current.value}
- Referenced by panels: (list panel titles)
- Datasource: {datasource name/uid}

### Data Sources
- (table: Name/UID, Type, Referenced by N panels)

### Panel Details

For each panel:
#### {Panel Title}
- Type: {timeseries | stat | gauge | table | heatmap | logs | ...}
- Position: row {y-group}, col {x}, size {w}x{h}
- Fold: above | below (gridPos.y < 8 ≈ above, ≥ 8 ≈ below)
- Query: {abbreviated target expression}
- Variables used: $var1, $var2
- Transformations: {count} ({types})
- Overrides: {count}
- Repeat: {variable name} (if repeating panel)
- Best selector: `section[data-testid='data-testid Panel header {title}']`
- Grade: Green | Yellow | Red
- Guide treatment: highlight | guided-hover | guided-lazyRender | noop
- Lazy-render note: (if Red/Yellow + below fold: "nth-match unreliable, prefer noop or guided with lazyRender")

### Concerns
- (list any issues: duplicate titles, missing titles, very large panel count, etc.)

**Return** a brief summary: row/section count, panel count, variable count, selector quality breakdown, and any concerns.
```

After the sub-agent completes, present the extraction report summary to the user.

---

## Checkpoint: Build the Guide Plan (Orchestrator)

After the user sees the extraction report, build a structural plan. Read `{guide_dir}/EXTRACTION_REPORT.md` and produce `{guide_dir}/GUIDE_PLAN.md`:

```markdown
## Guide Plan

**Guide ID**: {guide-id}
**Title**: {Guide Title}
**Guide type**: Dashboard Tour | Observability Guide | Monitoring Deep-Dive | SRE Walkthrough
**Dashboard URL path**: /d/{uid}/{slug}
**Data sources**: {list data source types}

### Navigation Sequence
How the user reaches the dashboard (e.g., Main menu → Dashboards → folder → dashboard link)

### Sections

#### 0. Navigation (if needed)
- Section ID: navigate-to-dashboard
- Steps: navigate action to dashboard URL, or guided menu navigation
- Requirements: [navmenu-open] (if using menu navigation)

#### 1. {Section Name} (maps to row or logical group)
- Section ID: {kebab-case-id}
- Row/group: {row title or "top-level"}
- Panels: {count} ({list panel titles})
- Variables relevant: $var1, $var2 (if any)
- Key panels to highlight: {list the most important 3-5}
- Row expand needed: yes/no (if collapsed row)
- Requirements: [on-page:/d/{uid}/{slug}]
- Objectives: [] (if any)
- Chains from: independent | section-completed:{previous-id} (only if dependent)

#### 2. {Section Name}
...

### Variable Exploration Section (if variables exist)
- Section ID: explore-variables
- Variables: {list variable names and types}
- Placement: first section after navigation (helps user understand filtering before panel tour)

### Section Chaining
Only chain when section N creates something section N+1 depends on.
Dashboard tours are typically independent sections -- use `on-page:/d/{uid}/{slug}` instead.

### Notes
- Duplicate panel title handling strategy
- Variable-interpolated panel titles
- Collapsed rows that need expand steps
- Step budget concerns (any sections that may exceed 8 steps)
```

**Present the plan to the user.** Let them adjust section order, add/remove sections, or change emphasis. Confirm the panel groupings before proceeding.

---

## Phase 3: Generate Guide (Per-Section Sub-Agents)

Generate the guide **section by section**. This keeps each sub-agent's context small and focused.

### 3.1 Orchestrator: Create the Guide Shell

Write the initial `{guide_dir}/content.json` with root structure and intro markdown:

```json
{
  "id": "{guide_id}",
  "title": "{guide_title}",
  "blocks": [
    {
      "type": "markdown",
      "content": "{brief intro — what the dashboard monitors, what the guide covers, no markdown title}"
    }
  ]
}
```

### 3.2 For Each Section: Launch a Sub-Agent

Iterate through the sections in GUIDE_PLAN.md. For each section, launch a sub-agent that generates just that section's JSON.

**Step budget**: aim for **3–8 interactive steps per section**. If a section has more panels than that, prioritize the most important ones and mention the rest in the intro or summary markdown. A complete dashboard guide should have **15–40 interactive steps** total (lower than the 25–50 range for source-code guides, because dashboard panels are view-only highlights rather than interactive form fills).

#### Per-section sub-agent prompt template

Fill in `{placeholders}` and launch via the Task tool:

```
You are generating ONE section of a Pathfinder interactive guide for a Grafana dashboard as a JSON object.

**Read this reference file first:**
1. `.cursor/authoring-guide.mdc` -- block types, action types, requirements, best practices

**Section to generate:**
- Section ID: {section_id}
- Section title: {section_title}
- Requirements: {section_requirements_array}
- Objectives: {section_objectives_array_or_none}
- Row expand needed: {yes_no}
- Variables relevant to this section: {variable_list_or_none}

**Panel JSON context** (the panels in this section):
```json
{panel_json_array_for_this_section}
```

**Variable definitions** (template variables referenced by these panels):
```json
{variable_definitions_json}
```

**Critical rules** (violations are blocking):
1. No markdown titles -- the section `title` is rendered by the app
2. `exists-reftarget` is auto-applied -- never add it manually
3. `navmenu-open` required for navigation menu element interactions
4. `on-page:/path` required for page-specific actions
5. Tooltips under 250 characters, one sentence, don't name the highlighted element
6. `verify` on state-changing actions (Save, Create, Test)
7. `doIt: false` for secrets -- never automate passwords/tokens/keys
8. Start with a brief intro markdown, end with a brief summary markdown
9. `skippable: true` + `hint` for optional steps (variable interaction, collapsed rows)
10. Action-focused language -- "Review the CPU usage panel" not "The CPU usage panel shows data"
11. Bold only GUI names -- "Expand the **Details** row" not "Expand the **Details** row panel"
12. No multistep singletons -- single-step multistep → plain interactive block
13. No focus-before-formfill -- highlight on input with doIt:true → use formfill or doIt:false

**Dashboard action decision tree:**

| Dashboard Element     | Guide Action                                           |
| --------------------- | ------------------------------------------------------ |
| Panel (view mode)     | `highlight` with `doIt: false`, explain what it shows  |
| Panel content area    | `highlight` targeting panel content div, `doIt: false`  |
| Panel with hover data | `guided` with `hover` step, then highlight              |
| Variable dropdown     | `highlight` with `doIt: false`, explain filter options  |
| Time picker           | `highlight` or `button`, explain time range             |
| Row expand/collapse   | `button` on row title text                              |
| Dashboard link        | `button` or `navigate`                                  |
| Panel drill-down link | `guided` with hover + button                            |
| Navigate to dashboard | `navigate` with dashboard path                          |
| Untitled panel (above fold) | `highlight` with `doIt: false` using nth-match(1) — only for the 1st untitled panel |
| Untitled panel (below fold) | `noop` describing the panel, OR `guided` with `lazyRender: true` (see below) |

**Selector patterns for dashboard elements:**
- Panel header: `section[data-testid='data-testid Panel header {title}']`
- Panel content: `section[data-testid='data-testid Panel header {title}'] > div[data-testid='data-testid panel content']`
- Row container: `div[data-testid='data-testid Layout container row {row title}']`
- Panel within row: `div[data-testid='data-testid Layout container row {row title}'] section[data-testid='data-testid Panel header {panel title}']`
- Nth chart (when title is not unique): `section[data-testid='data-testid Panel header {title}']:nth-match(N)`

**CRITICAL — Lazy rendering and nth-match:**
Grafana lazy-renders panels. Only panels in or near the viewport exist in the DOM. `nth-match(N)` fails if the Nth matching element hasn't rendered yet (the user hasn't scrolled to it). Rules:
- Green selectors (unique title): safe — `exists-reftarget` auto-waits
- Yellow/Red selectors using `nth-match(N)` where N > 1: **unreliable for below-fold panels**
- For untitled below-fold panels, prefer `noop`/`markdown` or use a `guided` block with `lazyRender: true`:
```json
{"type":"guided","content":"Scroll down to review the gradient bar gauge.","steps":[{"action":"highlight","reftarget":"section[data-testid='data-testid Panel header ']:nth-match(2)","lazyRender":true}]}
```

**Step budget:** Generate 3–8 interactive steps for this section. If the section has more panels than that, prioritize the most important ones and mention the rest in the intro or summary markdown.

**Golden examples:**
{paste the matching golden examples from SKILL.md — choose examples that best match this section's patterns}

**Your task:**
1. Return a single JSON object: `{"type": "section", "id": "{section_id}", ...}`
2. First block: brief intro markdown (what the user will explore in this section)
3. If a row needs expanding, that's the first interactive step
4. Generate steps for each key panel per the action decision tree
5. Last block: brief summary markdown (what the user learned)
6. Return ONLY the section JSON object — no wrapper, no root structure

**Also return** a brief text summary: step count, any selectors you're uncertain about, any panels you omitted and why.
```

#### Building the panel JSON context

For each section, include the **relevant panel objects** from the dashboard JSON:

1. Find the panels belonging to this section (by row grouping or gridPos)
2. Include the full panel JSON objects (title, type, targets, fieldConfig, options)
3. Include the variable definitions referenced by those panels
4. Trim large `targets[].expr` queries to the first 200 characters if very long

This gives the sub-agent direct access to query expressions, thresholds, legends, and other educational context.

#### Choosing which golden example to pass

Match the section's patterns to the golden examples:

| Section pattern | Golden examples |
|----------------|----------------|
| Panels to highlight and explain | Example A + B |
| Variable dropdowns to explore | Example C |
| Collapsed row to expand + panels | Example D |
| Hover to reveal tooltips/data links | Example E |
| Navigate to a dashboard first | Example F |
| Dashboard-wide concept explanation | Example G |
| Mix of patterns | Pass Examples A + the most relevant other |

### 3.3 Orchestrator: Assemble the Guide

After all section sub-agents complete:

1. **Read each returned section JSON** and validate it parses correctly
2. **Append each section** to `{guide_dir}/content.json`'s `blocks` array, in plan order
3. **Add the closing summary markdown** as the final block:
   ```json
   {
     "type": "markdown",
     "content": "{summary of what the user explored, list the key sections, suggest next steps}"
   }
   ```
4. **Write the assembled file** to `{guide_dir}/content.json`
5. **Spot-check**: read the first and last 30 lines to verify structure and bookends

### 3.4 Orchestrator: Generate Selector Report

After assembly, write `{guide_dir}/SELECTOR_REPORT.md` by collating sub-agent feedback:

```markdown
## Selector Quality Report

**Generated from**: dashboard `{uid}` -- "{title}"
**Date**: {date}
**Guide**: `{guide_id}/content.json`

### Summary
- **Total interactive steps**: N
- **Green (unique panel title)**: n (percent%)
- **Yellow (duplicate title, nth-match used)**: n (percent%)
- **Red (no title or variable-interpolated)**: n (percent%)

### Uncertain Selectors
(list selectors that sub-agents flagged as uncertain)

### Variable-Interpolated Titles
(list panels whose titles contain $variable references -- these selectors
depend on the current variable value and may break)

### Suggestions
(list improvements: panels that would benefit from unique titles, rows
that should be named, etc.)
```

### Section chaining guidance

Dashboard tour sections are almost always independent. Use chaining only in rare cases:

| Relationship | Use `section-completed`? |
|-------------|------------------------|
| Section 1 navigates to the dashboard, section 2 explores panels | No -- use `on-page:/d/{uid}/{slug}` |
| Section 1 explains variables, section 2 depends on a variable value | Rarely -- only if section 2 literally requires a specific value |
| Sections map to different rows on the same dashboard | No -- use `on-page:/d/{uid}/{slug}` |
| Section 1 installs prerequisites (data source, demo data) | Yes -- section 2 requires the prerequisite |

---

## Phase 4: Review & Fix (Sub-Agent)

Launch a sub-agent to review and fix the assembled guide.

### Sub-agent prompt template

```
You are reviewing an auto-generated Pathfinder guide for a Grafana dashboard tour.

**Read this reference file first:**
1. `.cursor/review-guide-pr.mdc` -- complete review protocol (sections 1-4 are blocking checks)

**Then read the guide:**
2. `{guide_dir}/content.json`

**Apply every check from sections 1-4** of the review protocol against the guide JSON.

**Additionally check for these dashboard-guide-specific issues:**
{tailored_items}

For each issue found, **fix it directly** in `{guide_dir}/content.json`.

After fixing all issues, **return a report**:
- List of issues found and how each was fixed
- Any issues that couldn't be auto-fixed (need human decision)
- Confirmation that the guide JSON is valid/parseable
- Confirmation that all section IDs are unique
- Confirmation that the requirements chain is logical
- Step count per section (flag any section with 0 interactive steps or >10)
```

### Building the tailored review checklist

Before launching the review sub-agent, build `{tailored_items}` systematically from the Phase 2 extraction report:

```
**Panel title uniqueness** (include if duplicate titles were found):
- These panels have duplicate titles: {list titles and how they're disambiguated}
- Verify nth-match indices are correct
- Verify row-scoped selectors target the right panel

**Variable-interpolated titles** (include if any panel title contains $variable):
- These panels have variable-interpolated titles: {list}
- Verify the selector accounts for the current variable value
- Consider using nth-match or row scoping instead of the interpolated title

**Variable interactions** (include if guide has variable exploration steps):
- These variables are referenced: {list names and types}
- Verify variable highlight steps use doIt: false
- Verify tooltip explains what the variable filters

**Row expand steps** (include if guide has collapsed rows):
- These rows need expanding: {list row titles}
- Verify expand step uses action: "button" with row title text
- Verify subsequent panel highlights in the row use row-scoped selectors

**Data source requirements** (include always):
- Dashboard uses these data sources: {list types}
- Verify on-page requirement includes the dashboard path
- Consider whether has-datasource requirements are needed

**Section chaining** (include always):
- Verify section-completed is NOT used between independent dashboard sections
- Dashboard tour sections should use on-page:/d/{uid}/{slug} instead
- Every section should have on-page:/d/{uid}/{slug}

**Lazy rendering + nth-match** (include if any Yellow/Red selectors exist):
- These steps use nth-match selectors: {list steps with nth-match and their gridPos.y}
- For below-fold panels (gridPos.y >= 8): verify the step uses a `guided` block with `lazyRender: true`, OR is a `noop`/`markdown` instead
- nth-match(1) on an above-fold untitled panel is acceptable in an `interactive` block
- nth-match(N) where N > 1 in a plain `interactive` block is ALWAYS a bug — it will fail due to lazy rendering
- Fix by converting to `guided` with `lazyRender: true`, or replacing with `noop`

**Step budget** (include always):
- Verify each section has 3–8 interactive steps
- Flag sections with 0 or 1 interactive steps (too thin)
- Flag sections with >10 interactive steps (should be split)
```

---

## Final Delivery (Orchestrator)

After Phase 4 completes:

1. **Read the review report** -- check if any issues couldn't be auto-fixed
2. **Validate JSON** -- ensure `{guide_dir}/content.json` parses correctly
3. **Spot-check** -- read the first and last sections to verify bookends and structure
4. **Present to the user** -- summarize what was generated:
   - Guide location: `{guide_dir}/content.json`
   - Sections: N (list names)
   - Total interactive steps: N (average per section)
   - Selector quality: N Green, N Yellow, N Red
   - Any compromises, omitted panels, or known issues
   - Review fixes applied
5. **Note the index.json entry** -- remind the user that an `index.json` entry is needed for the guide to appear in recommendations
6. **Note selector improvements** -- point the user to `SELECTOR_REPORT.md` for any fragile selectors

---

## Optional Inputs

The user may provide additional context. Use it when available:

| Input | How to Use |
|-------|-----------|
| **Guide type hint** | "dashboard tour", "SRE guide" → influences plan structure and tone |
| **Dashboard URL path** | `/d/abc123/my-dashboard` → use in `on-page:` requirements |
| **Audience** | "beginners", "SREs", "platform engineers" → adjust depth and terminology |
| **Focus panels** | "focus on the latency panels" → prioritize those panels, mention others briefly |
| **Data source type** | "Prometheus", "Loki" → tailor query explanations |

---

## Error Handling

### Dashboard JSON is not valid Grafana format
Report immediately. Validate the presence of `panels` (or legacy `rows`), `title`, and `uid`. If missing, ask the user to provide a valid Grafana dashboard JSON export.

### Legacy row format (schemaVersion < 16)
Older dashboards use `rows[].panels[]` instead of flat `panels[]`. Detect via `schemaVersion` or the presence of `rows` array. Flatten to the modern format for extraction: each row becomes a section, each row's panels become top-level panels with gridPos derived from their row position.

### No panel titles
Generate the guide anyway, but **do not rely on `:nth-match()` for below-fold untitled panels**. Grafana lazy-renders panels, so `nth-match(N)` only works when all N matching elements are in the DOM (i.e., the user has scrolled past them). Instead:
- Use `noop` or `markdown` to describe untitled panels (safest)
- For the first untitled above-fold panel, `nth-match(1)` in an `interactive` block with `doIt: false` is acceptable
- For below-fold untitled panels, use `guided` blocks with `lazyRender: true` if you must target them
- Include a prominent note in the extraction report about the fragile selectors

### Variable-interpolated titles
Panels with titles like `Details for $component` produce selectors that depend on the current variable value. Flag these in the extraction report. Use row-scoped selectors or `:nth-match()` as fallback. The guide may need to specify a default variable value in its intro.

### Very large dashboard (> 25 panels)
Stop at the first natural boundary (e.g., after the first 3 row groups). Report what was covered and what was omitted. Suggest the user split into multiple guides or narrow the focus.

### Sub-agent failures
If a sub-agent returns an error or incomplete result, read its output, diagnose the issue, and either retry with adjusted parameters or handle the phase manually as a fallback.
