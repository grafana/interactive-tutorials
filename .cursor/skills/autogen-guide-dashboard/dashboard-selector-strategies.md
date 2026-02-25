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

```json
// Dashboard JSON
{ "title": "CPU Usage", "type": "timeseries", ... }
```
```json
// Guide step
{
  "action": "highlight",
  "reftarget": "section[data-testid='data-testid Panel header CPU Usage']",
  "doIt": false,
  "content": "Review the **CPU Usage** panel.",
  "tooltip": "Shows CPU utilization over time for all selected pods."
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

**No title:**

```json
// Dashboard JSON -- panel with empty title
{ "title": "", "type": "stat", "gridPos": { "y": 0, "x": 0 } }
```
```json
// Guide step -- fallback to nth-match
{
  "action": "highlight",
  "reftarget": "section[data-testid='data-testid Panel header ']:nth-match(1)",
  "doIt": false,
  "content": "This stat panel shows the current value of the primary metric.",
  "tooltip": "The exact metric depends on your data source configuration."
}
```

**Variable-interpolated title:**

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
2. If title is empty or null:
     → Grade: Red
     → Selector: `:nth-match()` by global panel position
3. If title contains `$` (variable interpolation):
     → Grade: Red
     → Selector: row-scoped or `:nth-match()` if possible
     → Note: selector depends on current variable value
4. Count how many panels share this exact title:
     If count == 1:
       → Grade: Green
       → Selector: `section[data-testid='data-testid Panel header {title}']`
     If count > 1:
       → Grade: Yellow
       → If panels are in different rows:
           → Selector: row-scoped `div[...row...] section[...panel...]`
       → Else:
           → Selector: `section[...panel...]:nth-match(N)`
           → N = this panel's position among same-titled panels (sorted by gridPos.y, then gridPos.x)
5. Record the grade and selector in the extraction report
```

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

### Lazy-Loaded Panels

Panels below the fold may not render until the user scrolls. When targeting these panels:
- The `exists-reftarget` auto-requirement will wait for the element
- Add `"lazyRender": true` to `guided` steps if the element needs scrolling to appear

### Repeated Panels

Panels with `"repeat": "varName"` create copies for each variable value. The copies share the same base title but may have the variable value appended. Use `:nth-match(1)` to target the first instance, or explain the repeat pattern in a `noop` step.

### Embedded Links in Panels

Table panels and stat panels often contain data links that navigate to other dashboards or drill-down views. These links appear on hover or click. Use `guided` blocks with `hover` steps to reveal them before targeting.

### Dashboard Annotations

Annotation overlays (vertical lines on time-series panels) are not directly targetable with selectors. Mention annotations in `noop` or `markdown` blocks to explain their presence.
