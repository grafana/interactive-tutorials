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
  │  │                              + dashboard-guide-rules.md
  │    Output: {guide_dir}/EXTRACTION_REPORT.md
  │
  ├─ Checkpoint: Plan ──────────── orchestrator builds plan, user confirms
  │    Output: {guide_dir}/GUIDE_PLAN.md
  │
  ├─ Phase 3: Generate Guide ──── per-section sub-agents, each loads authoring-guide.mdc
  │    │                            + dashboard-guide-rules.md
  │    │                            + receives panel JSON context for its section
  │    │  3.1 Create guide shell (orchestrator)
  │    │  3.2 For each section → sub-agent generates section JSON
  │    │  3.3 Assemble sections into content.json (orchestrator)
  │    │  3.4 Generate SELECTOR_REPORT.md (orchestrator)
  │    Output: {guide_dir}/content.json + SELECTOR_REPORT.md
  │
  └─ Phase 4: Review & Fix ────── sub-agent loads review-guide-pr.mdc
  │                                 + dashboard-guide-rules.md
       Output: fixed content.json + change report
```

---

## Critical Rules

22 rules govern all generated guides. Sub-agents load them from
`dashboard-guide-rules.md`. Key rules the orchestrator must know:

- Rule 16: no navigation steps (user is already on the dashboard)
- Rule 17: no contextual preamble
- Rule 21: guided steps must include `description`
- Rule 22: no noop-only sections

Full rules, golden examples (A–G), action decision tree, selector patterns,
and the lazy-rendering CRITICAL section are all in `dashboard-guide-rules.md`.

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
- **3–6 panels**: Small dashboard. Expect 8–15 total steps across 1–2 sections. Do not pad to hit higher targets.
- **7–12 panels**: Good scope for one guide with 2–4 sections.
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
3. `.cursor/skills/autogen-guide-dashboard/dashboard-guide-rules.md` -- critical rules, golden examples, action decision tree, selector patterns, lazy rendering

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
- Guide treatment: highlight (above fold only) | guided-lazyRender (below fold, any grade) | guided-hover | noop
- Lazy-render note: (if below fold: "MUST use guided + lazyRender: true — exists-reftarget cannot scroll"; if Red/Yellow + below fold: "nth-match unreliable, prefer noop or guided with lazyRender")

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

### Sections

**Note**: No navigation section is needed. The guide assumes the user is already on the dashboard (rule 16).

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

### Section Viability
For each section, estimate the number of **targeting steps** (steps with a reftarget — `highlight`, `button`, `guided` with `lazyRender`, etc.) vs **noop steps** (informational, no DOM interaction). A section needs **at least 1 targeting step** to justify being standalone. If a section would contain only noop steps (e.g., all below-fold Red-grade panels), **merge its panels into an adjacent section** as a closing "what else is here" block rather than emitting a separate section with no interactivity.

### Notes
- Duplicate panel title handling strategy
- Variable-interpolated panel titles
- Collapsed rows that need expand steps
- Step budget concerns (any sections that may exceed 8 steps)
- Sections flagged as noop-only and which section they were merged into
```

**Present the plan to the user.** Let them adjust section order, add/remove sections, or change emphasis. Confirm the panel groupings before proceeding.

---

## Phase 3: Generate Guide (Per-Section Sub-Agents)

Generate the guide **section by section**. This keeps each sub-agent's context small and focused.

### 3.1 Orchestrator: Create the Guide Shell

Write the initial `{guide_dir}/content.json` with root structure and intro markdown. The intro should be 1–2 sentences max — never mention the dashboard name, instance, or URL (the user already knows where they are). Jump straight to what the guide covers.

```json
{
  "id": "{guide_id}",
  "title": "{guide_title}",
  "blocks": [
    {
      "type": "markdown",
      "content": "{1–2 sentences: what the guide covers and what the user will learn — no dashboard name, no instance name, no preamble}"
    }
  ]
}
```

### 3.2 For Each Section: Launch a Sub-Agent

Iterate through the sections in GUIDE_PLAN.md. For each section, launch a sub-agent that generates just that section's JSON.

**Step budget**: aim for **3–8 interactive steps per section**. A complete dashboard guide should have **8–40 interactive steps** total depending on dashboard size (small dashboards with 3–6 panels are fine at 8–15 steps; do not pad with unnecessary noops to reach a higher count). If a section has more panels than the budget allows, prioritize the most important ones and mention the rest in the intro or summary markdown.

**Targeting vs noop steps**: The step budget counts all interactive steps, but distinguish between **targeting steps** (those with a `reftarget` — highlights, buttons, guided steps) and **noop steps** (informational, no DOM targeting). A section must have **at least 1 targeting step**. If a planned section would contain only noop steps (e.g., all panels are below-fold Red-grade), do not emit it as a standalone section — instead merge its noop blocks into the preceding section's tail (after that section's summary markdown but before the section closing).

#### Per-section sub-agent prompt template

Fill in `{placeholders}` and launch via the Task tool:

```
You are generating ONE section of a Pathfinder interactive guide for a Grafana dashboard as a JSON object.

**Read these reference files first:**
1. `.cursor/authoring-guide.mdc` -- block types, action types, requirements, best practices
2. `.cursor/skills/autogen-guide-dashboard/dashboard-guide-rules.md` -- critical rules, golden examples, action decision tree, selector patterns, lazy rendering

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

**Golden examples to follow:** {list the matching example letters, e.g. "A, G" or "C, D, G"}

**Step budget:** Generate 3–8 interactive steps for this section, with **at least 1 targeting step** (a step with a reftarget — highlight, button, or guided). If ALL panels in the section would be noop (e.g., all below-fold Red-grade), report this in your summary so the orchestrator can merge this section into an adjacent one. If the section has more panels than the budget allows, prioritize the most important ones and mention the rest in the intro or summary markdown.

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
| Above-fold panels to highlight | Example A + B |
| Below-fold panels to highlight | **Example G** (required for ANY below-fold panel) |
| Mix of above + below fold panels | Example A + **Example G** |
| Variable dropdowns to explore | Example C |
| Collapsed row to expand + panels | Example D |
| Hover to reveal tooltips/data links | Example E |
| Dashboard-wide concept explanation | Example F |
| Mix of patterns | Pass Example G + the most relevant other |

### 3.3 Orchestrator: Assemble the Guide

After all section sub-agents complete:

1. **Read each returned section JSON** and validate it parses correctly
2. **Check for noop-only sections** — if a section has zero targeting steps (every interactive step is `noop`), merge its blocks into the preceding section rather than appending it as standalone. Move the noop blocks to the end of the preceding section (after the summary markdown), and replace the preceding section's summary with the merged section's summary. If the noop-only section is the *first* section (no preceding section to merge into), merge it into the *following* section's intro instead.
3. **Append each viable section** to `{guide_dir}/content.json`'s `blocks` array, in plan order
4. **Add the closing summary markdown** as the final block — ultra-short, 1–2 sentences max. Never recap every section or panel. A single forward-looking sentence is ideal.
   ```json
   {
     "type": "markdown",
     "content": "{1–2 sentences: one takeaway or next step — not a recap}"
   }
   ```
5. **Write the assembled file** to `{guide_dir}/content.json`
6. **Spot-check**: read the first and last 30 lines to verify structure and bookends

### 3.4 Orchestrator: Generate Selector Report

After assembly, write `{guide_dir}/SELECTOR_REPORT.md` by collating sub-agent feedback. Use the template from `dashboard-selector-strategies.md` (section "Selector Quality Report Template").

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

**Read these reference files first:**
1. `.cursor/review-guide-pr.mdc` -- complete review protocol (sections 1-4 are blocking checks)
2. `.cursor/skills/autogen-guide-dashboard/dashboard-guide-rules.md` -- rules, golden examples, and the "Review Checklist (Always Include)" section

**Then read the guide:**
3. `{guide_dir}/content.json`

**Apply every check from sections 1-4** of the review protocol against the guide JSON.
**Apply every item** from the "Review Checklist (Always Include)" in dashboard-guide-rules.md.

**Additionally check for these dashboard-specific issues:**
{tailored_items_conditional_only}

For each issue found, **fix it directly** in `{guide_dir}/content.json`.

After fixing all issues, **return a report**:
- List of issues found and how each was fixed
- Any issues that couldn't be auto-fixed (need human decision)
- Confirmation that the guide JSON is valid/parseable
- Confirmation that all section IDs are unique
- Confirmation that the requirements chain is logical
- Step count per section: total interactive steps, targeting steps (with reftarget), and noop steps — flag any section with 0 targeting steps (noop-only) or >10 total steps
```

### Building the tailored review checklist

Before launching the review sub-agent, build `{tailored_items_conditional_only}` from the Phase 2 extraction report. Only include the sections that apply to this dashboard — the "always include" items are now in `dashboard-guide-rules.md` and the sub-agent reads them directly.

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
