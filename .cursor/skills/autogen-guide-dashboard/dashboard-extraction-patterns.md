# Dashboard Extraction Patterns Reference

Detailed patterns for analyzing Grafana dashboard JSON exports to extract guide-relevant structure. This file is a reference for the [autogen-guide-dashboard skill](SKILL.md).

---

## Dashboard JSON Top-Level Structure

A Grafana dashboard JSON export has this shape:

```json
{
  "uid": "abc123",
  "title": "My Dashboard",
  "tags": ["production", "sre"],
  "schemaVersion": 39,
  "panels": [],
  "templating": { "list": [] },
  "annotations": { "list": [] },
  "links": [],
  "time": { "from": "now-6h", "to": "now" },
  "timepicker": {},
  "refresh": "30s"
}
```

When fetched via the Grafana API (`/api/dashboards/uid/<uid>`), the dashboard JSON is nested inside a wrapper:

```json
{
  "meta": { "slug": "my-dashboard", "url": "/d/abc123/my-dashboard", ... },
  "dashboard": { /* the actual dashboard JSON */ }
}
```

**Extraction rule**: if the JSON has a `dashboard` key at the top level, unwrap it first.

### Key Fields to Extract

| Field | Purpose in Guide |
|-------|-----------------|
| `uid` | Dashboard URL path: `/d/{uid}/{slug}` |
| `title` | Guide title context |
| `tags[]` | Guide description context |
| `schemaVersion` | Format version (< 16 = legacy row format) |
| `panels[]` | The interactive elements to tour |
| `templating.list[]` | Variable dropdowns to explain |
| `annotations.list[]` | Annotation overlays to mention |
| `links[]` | Dashboard links to other dashboards |
| `time` | Default time range to mention |
| `refresh` | Auto-refresh interval to mention |

---

## Panel Types and Guide Treatment

Each panel `type` maps to a different guide treatment. The `type` field determines what the panel visualizes and how a guide should explain it.

### Panel Type → Guide Treatment Mapping

| Panel Type | Visualization | Guide Treatment | Educational Focus |
|-----------|---------------|-----------------|-------------------|
| `timeseries` | Line/area chart over time | `highlight` panel, explain metric trends | What the metric measures, what trends to look for |
| `stat` | Single big number | `highlight` panel, explain the metric | What the number means, healthy vs concerning ranges |
| `gauge` | Gauge with thresholds | `highlight` panel, explain thresholds | What the ranges mean, when to take action |
| `bargauge` | Horizontal/vertical bars | `highlight` panel, explain comparison | What's being compared, relative sizing |
| `table` | Data table | `highlight` panel content, explain columns | Key columns, how to sort/filter, drill-down links |
| `heatmap` | Heatmap grid | `highlight` panel, explain axes and color | X-axis (time/buckets), Y-axis (values), color intensity |
| `histogram` | Distribution chart | `highlight` panel, explain distribution | What the distribution shows, outliers |
| `logs` | Log lines | `highlight` panel, explain log source | Log labels, filtering, common patterns |
| `piechart` | Pie/donut chart | `highlight` panel, explain proportions | What each slice represents |
| `barchart` | Categorical bar chart | `highlight` panel, explain categories | Category comparison |
| `text` | Markdown/HTML text | Usually skip or `noop` | Only highlight if it contains important instructions |
| `news` | RSS feed | Usually skip | Mention in intro if relevant |
| `row` | Row grouper (collapsible) | `button` to expand | Explain what the row group contains |
| `dashlist` | Dashboard list | `highlight` or skip | Mention linked dashboards |
| `alertlist` | Alert status list | `highlight` panel | Active alerts, alert rules |
| `canvas` | Free-form layout | `highlight` panel, `doIt: false` | Custom visualization explanation |
| `geomap` | Geographic map | `highlight` panel, `doIt: false` | Geographic distribution |
| `nodeGraph` | Node/edge graph | `highlight` panel, `doIt: false` | Relationships, topology |
| `flamegraph` | Flame graph | `highlight` panel, `doIt: false` | CPU/memory profiling |
| `traces` | Trace waterfall | `highlight` panel, `doIt: false` | Span hierarchy, latency breakdown |

### Special Panel Handling

**Repeating panels** (`repeat` field set): These panels duplicate themselves for each value of a template variable. The guide should explain the repeat mechanism rather than highlighting each instance. Use `:nth-match(1)` to target the first instance.

**Panels with no title**: Prefer describing these in `noop` or `markdown` blocks rather than targeting them with fragile `:nth-match()` selectors. Untitled panels produce `data-testid="data-testid Panel header "` (with trailing space), but multiple untitled panels all share this value and can only be disambiguated by `:nth-match(N)`. This is **unreliable for below-fold panels** because Grafana lazy-renders: panels not in the viewport don't exist in the DOM, so `nth-match(N)` counts are wrong until the user scrolls. See `dashboard-selector-strategies.md` for the full decision tree.

**Community / plugin panels** (`type` not in the table above): Panels from community plugins
(e.g., `innius-video-panel`, `marcusolsson-json-datasource`) may use custom rendering that
doesn't follow Grafana's `data-testid` conventions. Treat as `noop` in the guide unless
the panel has a recognizable standard panel header. Note the plugin type in the extraction report.

**Panels with very long titles**: The selector still works, but the step content should use a shortened name. E.g., `section[data-testid='data-testid Panel header Very Long Panel Title That Describes Everything']` is valid but the step should say "Review the **Very Long Panel Title** panel."

---

## Row Detection

Dashboards group panels into rows. There are two row formats:

### Modern Format: Explicit Row Panels (schemaVersion ≥ 16)

Rows appear as panel objects with `type: "row"` in the flat `panels[]` array:

```json
{
  "type": "row",
  "title": "Resource Usage",
  "collapsed": false,
  "gridPos": { "h": 1, "w": 24, "x": 0, "y": 8 },
  "panels": []
}
```

**When `collapsed: true`**: the row's child panels are nested inside `panels[]` on the row object itself (not in the top-level `panels[]` array). The guide needs an expand step before highlighting child panels.

**When `collapsed: false`**: child panels follow the row in the top-level `panels[]` array. They have `gridPos.y` values greater than the row's `gridPos.y` and less than the next row's `gridPos.y`.

### Row-to-Section Mapping

1. Collect all `type: "row"` panels, sorted by `gridPos.y`
2. For each row, collect its child panels:
   - If `collapsed: true`: panels are in `row.panels[]`
   - If `collapsed: false`: panels are in the top-level `panels[]` array with `gridPos.y` between this row's y and the next row's y
3. Panels before the first row (if any) form a "top-level" section
4. Each row becomes a guide section

### Legacy Format: rows[] Array (schemaVersion < 16)

Older dashboards use a `rows[]` array instead of flat panels:

```json
{
  "rows": [
    {
      "title": "Resource Usage",
      "collapse": false,
      "panels": [
        { "title": "CPU", "type": "graph", ... }
      ]
    }
  ]
}
```

**Extraction rule**: flatten to modern format. Each `rows[i]` becomes a section. Each `rows[i].panels[j]` becomes a panel with `gridPos` derived from the row index.

### No Explicit Rows: gridPos.y Clustering

Some dashboards don't use row panels at all. Group panels by `gridPos.y` proximity:

1. Sort panels by `gridPos.y`
2. Panels sharing the same `gridPos.y` are on the same visual row
3. Group adjacent visual rows into sections when there's a large y-gap (≥ 4 grid units) or when panel types change significantly
4. Name these synthetic sections based on the dominant panel type or the first panel's title

---

## Template Variable Extraction

Template variables live in `templating.list[]`. Each variable produces a dropdown (or other input) at the top of the dashboard.

### Variable Properties

```json
{
  "name": "component",
  "type": "query",
  "label": "Component",
  "datasource": { "type": "prometheus", "uid": "grafanacloud-prom" },
  "query": "label_values(up{job=\"quickpizza\"}, service_name)",
  "current": { "text": "All", "value": "$__all" },
  "options": [...],
  "multi": false,
  "includeAll": true,
  "allValue": ".*",
  "refresh": 1,
  "hide": 0
}
```

### Variable Types

| Type | Purpose | Guide Treatment |
|------|---------|-----------------|
| `query` | Values from a data source query | Explain what it filters, mention the data source |
| `custom` | Static list of values | Explain the options and when to use each |
| `datasource` | Data source picker | Explain data source selection |
| `interval` | Time interval selector | Explain how interval affects granularity |
| `textbox` | Free-text input | Explain what value to enter |
| `constant` | Hidden constant | Usually skip (not interactive) |
| `adhoc` | Ad-hoc filter builder | Explain the label/value filtering concept |

### Variable Visibility

The `hide` field controls visibility:
- `0` -- visible (include in guide)
- `1` -- label hidden (include in guide, note the label isn't shown)
- `2` -- completely hidden (skip in guide -- not interactive)

---

## Variable-to-Panel Binding

Panels reference variables in multiple ways. Scan for `$varName` or `${varName}` patterns.

### Where Variables Appear

| Location | Example | How to Detect |
|----------|---------|---------------|
| Query expressions | `rate(http_requests{service="$component"}[5m])` | Scan `targets[].expr` |
| Panel title | `Details for $component` | Scan `panels[].title` |
| Repeat config | `"repeat": "component"` | Check `panels[].repeat` |
| Legend format | `{{instance}} - $component` | Scan `targets[].legendFormat` |
| Transformations | Field rename with `$varName` | Scan `panels[].transformations[]` |
| Thresholds | Rarely, but possible | Scan `panels[].fieldConfig.defaults.thresholds` |
| Link URLs | `/d/other-dash?var-component=$component` | Scan `panels[].links[]` and `links[]` |

### Binding Analysis

For each variable, build a binding map:

```
$component:
  - Panel "Request Volume" (in target expr)
  - Panel "Error Rate" (in target expr)
  - Panel "Details for $component" (in title AND target expr)
  - Row "Details for $component" (in title, repeat)
```

This binding map tells the guide which panels change when a variable is adjusted, which is the key educational content for variable exploration sections.

---

## Data Source Extraction

Data sources appear in two locations:

### Panel Data Sources

```json
{
  "datasource": {
    "type": "prometheus",
    "uid": "grafanacloud-prom"
  }
}
```

Or as a string in older formats: `"datasource": "Prometheus"`.

### Variable Data Sources

Template variables of type `query` reference a data source for their value lookup:

```json
{
  "datasource": {
    "type": "prometheus",
    "uid": "grafanacloud-prom"
  }
}
```

### Data Source Summary

Collect all unique data sources from panels and variables. For each:
- **Type**: prometheus, loki, elasticsearch, influxdb, etc.
- **UID**: the unique identifier
- **Name**: if available in the JSON
- **Used by**: count of panels + variables referencing it

This information may be needed for guide requirements (e.g., `has-datasource:<name>`) and for educational content about the query language (PromQL, LogQL, etc.).

---

## Transformation and Override Detection

### Transformations

Panels may have `transformations[]` that modify data before rendering:

```json
{
  "transformations": [
    { "id": "organize", "options": { "excludeByName": { "Time": true } } },
    { "id": "sortBy", "options": { "sort": [{ "field": "Value", "desc": true }] } }
  ]
}
```

**Guide relevance**: mention significant transformations in the panel's educational tooltip. Common transformations worth noting:
- `organize` -- column reordering/hiding (table panels)
- `sortBy` -- data sorting
- `calculateField` -- computed columns
- `filterByValue` -- data filtering
- `groupBy` -- aggregation
- `joinByField` -- multi-query joins

### Field Overrides

Panels may have `fieldConfig.overrides[]` that customize specific fields:

```json
{
  "fieldConfig": {
    "overrides": [
      {
        "matcher": { "id": "byName", "options": "errors" },
        "properties": [
          { "id": "color", "value": { "fixedColor": "red", "mode": "fixed" } }
        ]
      }
    ]
  }
}
```

**Guide relevance**: overrides indicate intentional visual emphasis. If a field is colored red, the guide should explain why (e.g., "errors are highlighted in red to draw attention to failure rates").

### Thresholds

Panels with thresholds in `fieldConfig.defaults.thresholds` have visual breakpoints:

```json
{
  "thresholds": {
    "mode": "absolute",
    "steps": [
      { "color": "green", "value": null },
      { "color": "yellow", "value": 70 },
      { "color": "red", "value": 90 }
    ]
  }
}
```

**Guide relevance**: thresholds are prime educational content. Explain what each threshold means ("Green below 70%, yellow at 70-90%, red above 90% indicates critical resource saturation").

---

## Panel Option Extraction

Panel options contain visualization-specific settings worth mentioning in guides.

### Common Options

| Option Path | Panel Types | Guide Relevance |
|------------|-------------|-----------------|
| `options.legend.displayMode` | timeseries, barchart | Whether legend is visible, helps user read the chart |
| `options.tooltip.mode` | timeseries | "single" vs "all" -- affects hover behavior |
| `fieldConfig.defaults.unit` | all | Units (bytes, percent, seconds) -- mention in educational content |
| `fieldConfig.defaults.min/max` | gauge, bargauge | Expected range -- use in threshold explanation |
| `options.reduceOptions.calcs` | stat, gauge | Which calculation (last, mean, max) -- explain what the number represents |
| `options.orientation` | bargauge | Horizontal vs vertical -- helps describe the visual |

### Query Expression Summarization

For educational tooltips, summarize what the query does in plain language: what metric it measures, what the function computes (rate, percentile, sum, etc.), and what high or low values indicate. Reference [Grafana docs](https://grafana.com/docs/) for query language specifics.

---

## Extraction Report Template

When writing `assets/extraction-report.md`, use the standard frontmatter from the skill-memory convention (with added `dashboard`, `dashboardTitle`, and `dashboardSha256` fields), then this structure:

```markdown
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
- Fold: above | below (sum gridPos.h of all panels above this one; cumulative >= 8 ≈ below fold)
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
```

---

## Guide Plan Template

When writing `assets/guide-plan.md`, use the standard frontmatter from the skill-memory convention (with dashboard-specific fields), then this structure:

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
For each section, estimate **targeting steps** (steps with a reftarget) vs **noop steps** (informational, no DOM interaction). A section needs **at least 1 targeting step** to justify being standalone. If a section would contain only noop steps, **merge its panels into an adjacent section**.

### Notes
- Duplicate panel title handling strategy
- Variable-interpolated panel titles
- Collapsed rows that need expand steps
- Step budget concerns (any sections that may exceed 8 steps)
- Sections flagged as noop-only and which section they were merged into
```
