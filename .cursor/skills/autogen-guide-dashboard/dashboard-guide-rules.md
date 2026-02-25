# Dashboard Guide Rules

Consolidated rules, patterns, and golden examples for generating interactive guides from Grafana dashboard JSON. Sub-agents load this file directly; every rule here is blocking.

---

## Critical Rules

These rules apply to ALL generated guides. Violations are blocking.

1. **No markdown titles** -- the guide `title` renders in the app frame; a leading `## Title` duplicates it
2. **`exists-reftarget` is auto-applied** -- never add it manually to requirements
3. **`navmenu-open`** required for any step targeting navigation menu elements
4. **`on-page:/path`** required for page-specific interactive actions
5. **Tooltips** -- under 250 characters, one sentence, don't name the highlighted element
6. **`verify`** on all state-changing actions (Save, Create, Test)
7. **`doIt: false` for secrets** -- never automate filling passwords/tokens/keys
8. **Section bookends** -- 1-sentence "what you'll do" intro markdown, 1-sentence "what you learned" summary markdown
9. **Sections, not markdown headers** -- group steps with `section` blocks, each with a unique kebab-case `id`
10. **Connect sections** -- if section 1's objective creates a resource, section 2 should require it
11. **Action-focused content** -- "Save your configuration" not "The save button can be clicked"
12. **Bold only GUI names** -- "Click **Save & test**" not "Click the **Save & test** button"
13. **`skippable: true`** for conditional fields and permission-gated steps
14. **No multistep singletons** -- a `multistep` with one step must be a plain `interactive` block
15. **No focus-before-formfill** -- `highlight` on an input with `doIt: true` is a no-op; use `formfill` or set `doIt: false`
16. **No navigation steps** -- assume the user is already on the correct dashboard page; never emit a "navigate to the XYZ dashboard" step. (For rare cross-dashboard links, `action: "navigate"` with the target path is valid but not part of this skill's scope.)
17. **No contextual preamble** -- never write "this is a guide to the XYZ dashboard" or mention the Grafana instance; the user already knows where they are
18. **Minimal text** -- the guide renders in a narrow sidebar; use short declarative sentences, not paragraphs; every word must earn its place
19. **Link to Grafana docs** -- when introducing a visualization type, query concept, or Grafana feature, include a `[docs](https://grafana.com/docs/...)` link so users can learn more
20. **Ultra-short closings** -- final summary blocks should be 1–2 sentences max; never recap every section
21. **Guided step descriptions** -- every `guided` step MUST include a `description` field; use `"Click inside the highlighted area"` for highlight/button actions and `"Hover over the highlighted area"` for hover actions; never rely on the default "Click this element" which is too vague
22. **No noop-only sections** -- a section where every interactive step is `noop` (zero targeting steps) provides no guided interactivity and feels hollow; merge its blocks into an adjacent section instead of emitting it as standalone

---

## Golden Examples

These examples show the target output quality for common dashboard guide patterns. Pass the relevant ones to each section's sub-agent.

### Example A: Panel highlight with educational tooltip

The most common pattern for dashboard tours. Highlight a panel and explain what it shows. Keep content short and declarative — the guide renders in a narrow sidebar.

```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "section[data-testid='data-testid Panel header CPU throttling']",
  "doIt": false,
  "content": "**CPU throttling** shows how often containers are slowed by exceeding CPU limits. [docs](https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/time-series/)",
  "tooltip": "High throttling means your app is running slower than it could."
}
```

Key things: `action: "highlight"` with `doIt: false` (view-only panels), selector uses the panel header `data-testid` pattern, content is short and punchy (no paragraphs), includes a docs link for the visualization type, tooltip is concise. **This `interactive` pattern is only valid for above-fold panels** (`gridPos.y < 8`). For below-fold panels, use Example G instead.

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

Key things: targets panel content `div` inside the header `section`, uses `>` child combinator, content is action-oriented. **This `interactive` pattern is only valid for above-fold panels.** For below-fold panels, wrap in a `guided` block with `lazyRender: true` (see Example G).

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
      "reftarget": "section[data-testid='data-testid Panel header Frontend Response Latency'] div:nth-match(7)",
      "description": "Hover over the highlighted area"
    }
  ]
}
```

Key things: `guided` (not `multistep`) for user-performed actions, hover reveals tooltip data in time-series panels, uses `:nth-match()` to target the correct inner div, `description` provides clear user-facing instruction (never omit it).

### Example F: noop for dashboard concepts

When no single element can be targeted but the user needs context about the dashboard structure. Keep it brief.

```json
{
  "type": "interactive",
  "action": "noop",
  "content": "All panels query **Prometheus** via [PromQL](https://grafana.com/docs/grafana/latest/datasources/prometheus/). The time picker (top-right) controls the shared time range.",
  "skippable": true
}
```

Key things: `noop` when there's no sensible element to highlight. Use for dashboard-wide concepts (shared data source, time range, refresh interval). Keep text to 1–2 sentences. Include a docs link when referencing a Grafana feature or query language.

### Example G: Below-fold panel highlight (guided + lazyRender)

**CRITICAL**: Any panel below the fold (`gridPos.y >= 8`) must use a `guided` block with `lazyRender: true`, even if it has a unique title (Green-grade selector). Grafana lazy-renders panels — below-fold panels do not exist in the DOM until the user scrolls. A plain `interactive` block will fail with "Element not found" because `exists-reftarget` waits but cannot scroll.

```json
{
  "type": "guided",
  "content": "**State timeline strings** plots discrete states (LOW, NORMAL, HIGH, CRITICAL) as colored bands over time. [docs](https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/state-timeline/)",
  "tooltip": "Band width shows how long each state lasted.",
  "steps": [
    {
      "action": "highlight",
      "reftarget": "section[data-testid='data-testid Panel header State timeline strings']",
      "lazyRender": true,
      "description": "Click inside the highlighted area"
    }
  ]
}
```

Key things: `guided` (not `interactive`) with `lazyRender: true` on the step, educational `content` and `tooltip` live on the outer `guided` block, `description` provides the user-facing instruction (always include it — the default "Click this element" is too vague), the selector is Green-grade (unique title) but `lazyRender` is still required because the panel is below the fold. **This pattern applies to ALL below-fold panels regardless of selector grade.**

---

## Action Decision Tree

| Dashboard Element | Guide Action |
| --------------------- | ------------------------------------------------------ |
| Panel (above fold, view mode) | `interactive` `highlight` with `doIt: false`, explain what it shows |
| Panel (below fold, view mode) | **`guided`** with `highlight` step + `lazyRender: true` (see Lazy Rendering section) |
| Panel content (above fold) | `interactive` `highlight` targeting panel content div, `doIt: false` |
| Panel content (below fold) | **`guided`** with `highlight` step targeting content div + `lazyRender: true` |
| Panel with hover data | `guided` with `hover` step, then highlight |
| Variable dropdown | `highlight` with `doIt: false`, explain filter options |
| Time picker | `highlight` or `button`, explain time range |
| Row expand/collapse | `button` on row title text |
| Dashboard link | `button` or `navigate` |
| Panel drill-down link | `guided` with hover + button |
| Untitled panel (above fold) | `highlight` with `doIt: false` using nth-match(1) — only for the 1st untitled panel |
| Untitled panel (below fold) | `noop` describing the panel, OR `guided` with `lazyRender: true` |
| Text panel (`type: "text"`) | Skip -- informational content, not an interactive target |
| Plugin panel (unrecognized type) | `noop` describing the panel -- plugin panels may not follow standard `data-testid` conventions |

---

## Selector Patterns

- Panel header: `section[data-testid='data-testid Panel header {title}']`
- Panel content: `section[data-testid='data-testid Panel header {title}'] > div[data-testid='data-testid panel content']`
- Row container: `div[data-testid='data-testid Layout container row {row title}']`
- Panel within row: `div[data-testid='data-testid Layout container row {row title}'] section[data-testid='data-testid Panel header {panel title}']`
- Nth chart (when title is not unique): `section[data-testid='data-testid Panel header {title}']:nth-match(N)`

---

## Lazy Rendering (CRITICAL)

Grafana lazy-renders panels. Only panels in or near the viewport exist in the DOM. Panels below the fold (`gridPos.y >= 8`) do NOT exist in the DOM at page load. `exists-reftarget` only waits — **it cannot scroll the page**. Rules:

- **ALL panels below the fold** (any selector grade): MUST use `guided` with `lazyRender: true` — a plain `interactive` block WILL fail with "Element not found"
- Green selectors (unique title) above the fold: safe in plain `interactive` blocks
- Yellow/Red selectors using `nth-match(N)` where N > 1: **unreliable even with lazyRender** for below-fold panels — prefer `noop`/`markdown`
- Below-fold panel example:

```json
{"type":"guided","content":"Review the **Request Latency** panel.","tooltip":"High latency indicates degraded performance.","steps":[{"action":"highlight","reftarget":"section[data-testid='data-testid Panel header Request Latency']","lazyRender":true,"description":"Click inside the highlighted area"}]}
```

---

## Review Checklist (Always Include)

These items apply to every dashboard guide review. The Phase 4 review sub-agent checks all of them.

**Data source requirements**:
- Dashboard uses these data sources: {list types}
- Verify on-page requirement includes the dashboard path
- Consider whether has-datasource requirements are needed

**Section chaining**:
- Verify section-completed is NOT used between independent dashboard sections
- Dashboard tour sections should use on-page:/d/{uid}/{slug} instead
- Every section should have on-page:/d/{uid}/{slug}

**Lazy rendering** (the #1 source of dashboard guide bugs):
- ANY below-fold panel (gridPos.y >= 8) in a plain `interactive` block is a bug — even Green-grade selectors
- Grafana lazy-renders panels: below-fold panels do not exist in the DOM until scrolled into view
- `exists-reftarget` only waits — it CANNOT scroll the page — so the element never appears
- For EVERY interactive step that targets a below-fold panel: verify it uses a `guided` block with `lazyRender: true`
- Fix plain `interactive` blocks targeting below-fold panels by converting to `guided` with `lazyRender: true`:
  Before: `{"type":"interactive","action":"highlight","reftarget":"...","doIt":false,"content":"...","tooltip":"..."}`
  After:  `{"type":"guided","content":"...","tooltip":"...","steps":[{"action":"highlight","reftarget":"...","lazyRender":true,"description":"Click inside the highlighted area"}]}`
- nth-match(1) on an above-fold untitled panel is acceptable in an `interactive` block
- nth-match(N) where N > 1 in a plain `interactive` block is ALWAYS a bug — it will fail due to lazy rendering
- Fix nth-match issues by converting to `guided` with `lazyRender: true`, or replacing with `noop`

**Step budget and section viability**:
- Verify each section has 3–8 interactive steps
- Distinguish **targeting steps** (with reftarget: highlight, button, guided) from **noop steps** (informational, no DOM interaction)
- A section must have **at least 1 targeting step** — if every interactive step is `noop`, the section provides no guided interactivity
- Fix noop-only sections by merging their blocks into the preceding section (move noops after the preceding section's summary, replace that summary with the merged section's summary)
- Flag sections with 0 or 1 total interactive steps (too thin)
- Flag sections with >10 interactive steps (should be split)

**No navigation steps**:
- The guide assumes the user is already on the dashboard
- Remove any `action: "navigate"` steps that go to the dashboard itself
- Remove any "Navigate to..." intro text

**No contextual preamble**:
- Remove any text like "this is a guide to the XYZ dashboard" or "on the Grafana Play instance"
- The user knows where they are; don't tell them

**Text brevity**:
- Flag any `content` field longer than 2 sentences (likely too verbose for sidebar rendering)
- Replace paragraphs with short declarative statements
- Verify section intro/summary markdown is 1 sentence each

**Grafana docs links**:
- Verify that visualization types and Grafana features have a `[docs](https://grafana.com/docs/...)` link
- Links should appear naturally in the step content, not as separate blocks

**Closing brevity**:
- The final markdown block should be 1–2 sentences max
- Never recap every section or panel in the closing
