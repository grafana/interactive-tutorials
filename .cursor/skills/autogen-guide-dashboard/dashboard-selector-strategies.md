# Dashboard Selector Strategies

Selector assessment specific to generating guides from Grafana dashboard JSON. This file covers **only what's unique to the dashboard autogen workflow** -- deriving selectors from panel titles and dashboard structure, grading them for stability, and handling edge cases like duplicate titles and variable interpolation.

For selector priority ordering, fallback patterns, advanced pseudo-selectors (`:contains`, `:has`, `:nth-match`), and known stable Grafana selectors, see:
- [docs/selectors-and-testids.md](../../../docs/selectors-and-testids.md) -- full selector reference
- [selector-library.mdc](../../selector-library.mdc) -- quick-reference catalog of known selectors

---

## Known Dashboard Selectors

These selectors are derived from Grafana's dashboard rendering code and are stable across versions.

### Panel Selectors

| Element | Selector Pattern | Notes |
|---------|-----------------|-------|
| Panel header (wrapper) | `section[data-testid='data-testid Panel header {title}']` | Primary panel selector. `{title}` is the panel's `title` field exactly as written. |
| Panel content area | `section[data-testid='data-testid Panel header {title}'] > div[data-testid='data-testid panel content']` | Targets the visualization inside the panel, not the header chrome. Use `>` child combinator. |
| Panel menu button | `button[data-testid='data-testid Panel menu {title}']` | The three-dot menu on each panel. Rarely needed in guides. |

### Row Selectors

| Element | Selector Pattern | Notes |
|---------|-----------------|-------|
| Row container | `div[data-testid='data-testid Layout container row {row title}']` | Wrapper around all panels in a row. Only present for explicit `type: "row"` panels. |
| Row toggle button | Row title text (use `action: "button"`) | The row title itself is clickable to expand/collapse. Use `action: "button"` with the row title as `reftarget`. |
| Panel within a row | `div[data-testid='data-testid Layout container row {row title}'] section[data-testid='data-testid Panel header {panel title}']` | Row-scoped panel selector for disambiguation. |

### Chart / Visualization Selectors

| Element | Selector Pattern | Notes |
|---------|-----------------|-------|
| uPlot chart canvas | `div[data-testid='uplot-main-div']` | Time series chart area. Use `:nth-match(N)` to target the Nth chart globally. |
| uPlot within a panel | `section[data-testid='data-testid Panel header {title}'] div[data-testid='uplot-main-div']` | Chart within a specific panel. More stable than `:nth-match`. |

### Variable Selectors

Variable selectors are less standardized than panel selectors. These patterns work but may vary across Grafana versions.

| Element | Selector Pattern | Notes |
|---------|-----------------|-------|
| Variable wrapper | `div[data-testid='data-testid template variable']` | Container for all variables. Not very useful alone. |
| Specific variable by label | `label:contains('{variable label}')` | Works when the variable has a `label` set. Falls back to `name` if no label. |
| Variable dropdown button | `button:has(> span:contains('{current value}'))` | Fragile -- depends on current value. Use with caution. |

**Variable selector recommendation**: Use `doIt: false` for all variable steps. Variable selectors are inherently less stable than panel selectors, and the user should choose their own variable values.

### Dashboard Chrome Selectors

| Element | Selector Pattern | Notes |
|---------|-----------------|-------|
| Time picker | `button[data-testid='data-testid TimePicker Open Button']` | Standard Grafana time picker button. |
| Refresh button | `button[data-testid='data-testid RefreshPicker run button']` | Dashboard refresh button. |
| Dashboard settings | `button[data-testid='data-testid Dashboard settings']` | Gear icon for dashboard settings. |
| Share button | `button[data-testid='data-testid share-button']` | Dashboard share button. |

---

## Selector Quality Grading

When extracting panels from dashboard JSON, grade each panel's best available selector. The grade determines guide action confidence.

| Grade | Panel Has | Selector | Confidence |
|-------|----------|----------|------------|
| **Green** | Unique, non-variable title | `section[data-testid='data-testid Panel header {title}']` | High -- `doIt` allowed (though most dashboard panels use `doIt: false` anyway) |
| **Yellow** | Duplicate title (shared by 2+ panels) | `section[data-testid='data-testid Panel header {title}']:nth-match(N)` or row-scoped selector | Medium -- `doIt: false` recommended |
| **Red** | No title, empty title, or variable-interpolated title (`$var` in title) | `:nth-match()` by global position, or `noop` | Low -- `doIt: false` required |

### Green: Unique Panel Title

The most common case. Each panel has a unique `title` that maps directly to a stable `data-testid`.

**Above-fold panels** (`gridPos.y < 8`) can use plain `interactive` blocks:

```json
// Dashboard JSON
{ "title": "CPU Usage", "type": "timeseries", "gridPos": { "y": 0 }, ... }
```
```json
// Guide step -- above fold, safe as interactive
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "section[data-testid='data-testid Panel header CPU Usage']",
  "doIt": false,
  "content": "Review the **CPU Usage** panel.",
  "tooltip": "Shows CPU utilization over time for all selected pods."
}
```

**Below-fold panels** (`gridPos.y >= 8`) **must** use `guided` blocks with `lazyRender: true`. Grafana lazy-renders panels — panels below the viewport do not exist in the DOM until the user scrolls to them. The `exists-reftarget` auto-requirement only waits; it cannot scroll the page. Without `lazyRender: true`, the element will never appear and the step will fail with "Element not found."

```json
// Dashboard JSON
{ "title": "Request Latency", "type": "timeseries", "gridPos": { "y": 16 }, ... }
```
```json
// Guide step -- below fold, MUST use guided + lazyRender
{
  "type": "guided",
  "content": "Review the **Request Latency** panel.\n\nThis panel shows p95 request latency over time.",
  "tooltip": "High latency spikes indicate backend performance degradation.",
  "steps": [
    {
      "action": "highlight",
      "reftarget": "section[data-testid='data-testid Panel header Request Latency']",
      "lazyRender": true
    }
  ]
}
```

### Yellow: Duplicate Panel Title

When multiple panels share the same title (common in dashboards with repeated sections or symmetrical layouts).

**Strategy 1: `:nth-match()` (preferred when panels are not in rows)**

```json
// Dashboard JSON -- two panels titled "Requests/sec"
[
  { "title": "Requests/sec", "type": "timeseries", "gridPos": { "y": 0 } },
  { "title": "Requests/sec", "type": "timeseries", "gridPos": { "y": 8 } }
]
```
```json
// Guide step -- target the first occurrence
{
  "action": "highlight",
  "reftarget": "section[data-testid='data-testid Panel header Requests/sec']:nth-match(1)",
  "doIt": false,
  "content": "The first **Requests/sec** panel shows frontend request throughput.",
  "tooltip": "Rate of incoming HTTP requests per second."
}
```

**Strategy 2: Row-scoped selector (preferred when panels are in different rows)**

```json
// Guide step -- target within a specific row
{
  "action": "highlight",
  "reftarget": "div[data-testid='data-testid Layout container row Frontend'] section[data-testid='data-testid Panel header Requests/sec']",
  "doIt": false,
  "content": "The **Requests/sec** panel in the **Frontend** row shows frontend request throughput.",
  "tooltip": "Rate of incoming HTTP requests per second."
}
```

Row-scoped selectors are more readable and self-documenting than `:nth-match()`.

### Red: No Title or Variable-Interpolated Title

Red-grade panels are the hardest to target reliably. **Prefer describing them in markdown or `noop` blocks rather than attempting fragile selectors.** Only target them with selectors if they are critical to the guide's educational purpose.

#### Why `:nth-match()` is unreliable for untitled panels

Grafana **lazy-renders** panels: only panels visible in the viewport (plus a small buffer) exist in the DOM. Panels below the fold are not rendered until the user scrolls. This means:

- `section[data-testid='data-testid Panel header ']:nth-match(2)` will fail if only the first untitled panel is in the DOM
- The count of matching elements changes as the user scrolls
- `:nth-match(N)` indices are only valid when **all N elements are rendered**, which requires scrolling to the bottom first

**Verified behavior** (play.grafana.org, schema v39): untitled panels render `data-testid="data-testid Panel header "` (with trailing space, empty title). Multiple untitled panels all share this same `data-testid` value.

#### Strategy for untitled panels (in priority order)

1. **Prefer `noop` or `markdown`**: describe what the panel shows without targeting it. This is the safest option and still provides educational value.

2. **If the panel is above the fold** (roughly `gridPos.y < 8`): `:nth-match(1)` may work for the first untitled panel since it will be in the DOM at page load. Always use `doIt: false`.

3. **If the panel is below the fold** and you must target it: use a `guided` block with `lazyRender: true`. This tells the guide system to scroll the element into view and wait for it to render before attempting the selector.

```json
// Untitled panel below the fold -- guided with lazyRender
{
  "type": "guided",
  "content": "Scroll down to review the vertical gradient bar gauge.\n\nThis panel shows 16 series using gradient mode in vertical orientation.",
  "steps": [
    {
      "action": "highlight",
      "reftarget": "section[data-testid='data-testid Panel header ']:nth-match(2)",
      "lazyRender": true
    }
  ]
}
```

4. **If there are many untitled panels**: strongly prefer `noop` for all but the first. The `:nth-match` indices become increasingly fragile as N grows, and each depends on all prior untitled panels being rendered.

#### Variable-interpolated title

```json
// Dashboard JSON
{ "title": "Details for $component", "type": "table", ... }
```

The rendered title depends on the current variable value (e.g., "Details for quickpizza-api"). The `data-testid` will contain the interpolated value, not the template.

```json
// Guide step -- explain the variable dependency, use row scoping if possible
{
  "action": "highlight",
  "reftarget": "div[data-testid='data-testid Layout container row Details for $component'] section:nth-match(1)",
  "doIt": false,
  "content": "This panel shows details for the currently selected **$component**.",
  "tooltip": "The panel title and content change based on the component variable."
}
```

**Important**: When the row title also contains `$variable`, the row `data-testid` will likewise contain the interpolated value. Use the guide intro to specify which variable value the guide expects, or use `:nth-match()` as a last resort.

---

## Selector Derivation Algorithm

Given a panel from the dashboard JSON, derive its best selector:

```
1. Read panel.title
2. If title is empty, null, or missing:
     → Grade: Red
     → Estimate fold position: gridPos.y < 8 ≈ above fold, ≥ 8 ≈ below fold
     → If above fold AND this is the 1st untitled panel (by gridPos order):
         → Selector: section[data-testid='data-testid Panel header ']:nth-match(1)
         → Use: interactive block with doIt: false
     → If below fold OR 2nd+ untitled panel:
         → Preferred: use noop or markdown to describe the panel (no selector needed)
         → If selector is essential: use guided block with lazyRender: true
           and section[data-testid='data-testid Panel header ']:nth-match(N)
         → N = this panel's position among untitled panels (sorted by gridPos.y, then x)
     → Record: fold position and recommended treatment in extraction report
3. If title contains `$` (variable interpolation):
     → Grade: Red
     → Selector: row-scoped or `:nth-match()` if possible
     → Note: selector depends on current variable value
     → If below fold: same lazyRender guidance as untitled panels
4. Count how many panels share this exact title:
     If count == 1:
       → Grade: Green
       → Selector: `section[data-testid='data-testid Panel header {title}']`
       → If above fold: use plain interactive block (exists-reftarget auto-waits)
       → If below fold: MUST use guided block with lazyRender: true
         (exists-reftarget only waits — it cannot scroll; without lazyRender
         Grafana never renders the panel and the selector times out)
     If count > 1:
       → Grade: Yellow
       → If panels are in different rows:
           → Selector: row-scoped `div[...row...] section[...panel...]`
       → Else:
           → Selector: `section[...panel...]:nth-match(N)`
           → N = this panel's position among same-titled panels (sorted by gridPos.y, then x)
       → If below fold: same nth-match + lazy-render caution applies
5. Record the grade, fold position, and selector in the extraction report
```

**Fold estimation heuristic**: Grafana's default grid has ~8 vertical units visible without scrolling on a standard viewport (1080px). Panels with `gridPos.y >= 8` are likely below the fold. This is approximate -- actual visibility depends on browser height, panel heights of preceding panels, and whether rows are collapsed.

---

## Selector Quality Report Template

Include this report alongside every generated guide as `SELECTOR_REPORT.md` in the guide directory.

```markdown
## Selector Quality Report

**Generated from**: dashboard `{uid}` -- "{title}"
**Date**: {date}
**Guide**: `{guide-id}/content.json`

### Summary
- **Total interactive steps**: {N}
- **Green (unique title)**: {n} ({percent}%)
- **Yellow (duplicate title)**: {n} ({percent}%)
- **Red (no title / variable title)**: {n} ({percent}%)

### Duplicate Titles

| Title | Occurrences | Disambiguation Strategy |
|-------|-------------|------------------------|
| "Requests/sec" | 3 | Row-scoped: Frontend, Backend, Database rows |
| "Usage" | 2 | nth-match(1), nth-match(2) |

### Variable-Interpolated Titles

| Panel Title (template) | Variable | Rendered Example | Selector Strategy |
|------------------------|----------|------------------|-------------------|
| "Details for $component" | component | "Details for quickpizza-api" | Row-scoped nth-match |

### Panels Without Titles

| Position (gridPos) | Panel Type | Selector |
|-------------------|------------|----------|
| y:0, x:12 | stat | nth-match(3) |

### Suggestions
- Panels with duplicate titles would benefit from unique titles for selector stability
- Variable-interpolated titles create fragile selectors; consider static titles with variable in subtitle
```

---

## Dashboard-Specific Selector Caveats

### Lazy-Loaded Panels and nth-match

Grafana lazy-renders dashboard panels: only panels in or near the viewport exist in the DOM. Panels below the fold are **not in the DOM at all** until the user scrolls down. This has critical implications for selectors:

**ALL below-fold panels are affected by lazy rendering, regardless of selector grade.** Grafana does not render panels into the DOM until the user scrolls them into (or near) the viewport. The `exists-reftarget` auto-requirement only waits for an element to appear — **it cannot scroll the page**. If the panel hasn't been rendered, the wait times out and the step fails with "Element not found."

**For Green-grade selectors (unique title)**:
- **Above fold**: safe in a plain `interactive` block — the element is already in the DOM at page load.
- **Below fold**: **must use `guided` with `lazyRender: true`**. The `lazyRender` flag tells the guide system to scroll the element into view and wait for Grafana to render it before matching the selector. A plain `interactive` block will fail because `exists-reftarget` cannot trigger scrolling.

Verified on play.grafana.org (schema v41): a dashboard with 5 uniquely-titled visualization panels at `gridPos.y >= 8` — none existed in the DOM at page load. Plain `interactive` blocks with `exists-reftarget` timed out with "Element not found" for all of them.

**For Yellow/Red-grade selectors using `:nth-match(N)`**: **doubly broken by lazy rendering.** Not only is the element not in the DOM, but `nth-match(N)` counts are wrong when earlier matching elements haven't rendered. This was verified on play.grafana.org — a dashboard with 3 untitled panels only had 1 in the DOM at initial page load; `nth-match(2)` failed.

**Mitigations for below-fold panels** (in priority order):
1. **Use `guided` blocks with `lazyRender: true`** — this is required for ALL below-fold panels, including Green-grade:
   ```json
   {
     "type": "guided",
     "content": "Review the **Request Latency** panel.\n\nThis panel shows p95 latency.",
     "tooltip": "Spikes above 500ms indicate degraded performance.",
     "steps": [{
       "action": "highlight",
       "reftarget": "section[data-testid='data-testid Panel header Request Latency']",
       "lazyRender": true
     }]
   }
   ```
2. **For untitled/duplicate-title below-fold panels**: prefer `noop` or `markdown` to avoid fragile `nth-match` + lazy rendering issues
3. **Restructure the guide** so that earlier steps naturally scroll the user past the needed panels, causing them to render before subsequent steps run

### Repeated Panels

Panels with `"repeat": "varName"` create copies for each variable value. The copies share the same base title but may have the variable value appended. Use `:nth-match(1)` to target the first instance, or explain the repeat pattern in a `noop` step.

### Embedded Links in Panels

Table panels and stat panels often contain data links that navigate to other dashboards or drill-down views. These links appear on hover or click. Use `guided` blocks with `hover` steps to reveal them before targeting.

### Dashboard Annotations

Annotation overlays (vertical lines on time-series panels) are not directly targetable with selectors. Mention annotations in `noop` or `markdown` blocks to explain their presence.
