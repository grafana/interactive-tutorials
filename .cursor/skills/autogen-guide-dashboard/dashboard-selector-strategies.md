# Dashboard Selector Strategies

Selector assessment specific to generating guides from Grafana dashboard JSON. This file covers **only what's unique to the dashboard autogen workflow** -- deriving selectors from panel titles and dashboard structure, grading them for stability, and handling edge cases like duplicate titles and variable interpolation.

For selector priority ordering, fallback patterns, advanced pseudo-selectors (`:contains`, `:has`, `:nth-match`), and known stable Grafana selectors, see:
- [docs/selectors-and-testids.md](../../../docs/selectors-and-testids.md) -- full selector reference
- [selector-library.mdc](../../selector-library.mdc) -- quick-reference catalog of known selectors
- [symbolic-selector-syntax.md](../convert-guide-selectors/symbolic-selector-syntax.md) -- `grafana:` and `panel:` syntax, and the traps

---

## Known Dashboard Selectors

Emit the **symbolic reference** form. It resolves through `@grafana/e2e-selectors` against the running Grafana version and matches `data-testid` **or** `aria-label`; the literal is a snapshot of one version's value in one attribute.

The "resolves to" column shows the equivalent literal at 13.2.0, given for recognising these selectors when reading a guide. It is shortened: each reference actually emits `:is([data-testid="V"], [aria-label="V"])`, which is what makes it match either attribute. Don't hand-write the shortened form.

Every path listed here resolves at both 12.4.0 and 13.2.0. Re-check with `scripts/validate-paths.ts` from the `convert-guide-selectors` skill before relying on one that isn't listed.

### Panel Selectors

| Element | Reference | Resolves to | Notes |
|---------|-----------|-------------|-------|
| Panel header (wrapper) | `section{grafana:components.Panels.Panel.title:{title}}` | `section[data-testid='data-testid Panel header {title}']` | Primary panel selector. `{title}` is the panel's `title` field exactly as written. |
| Panel content area | `section{grafana:components.Panels.Panel.title:{title}} > {grafana:components.Panels.Panel.content}` | `… > div[data-testid='data-testid panel content']` | Targets the visualization inside the panel, not the header chrome. Use `>` child combinator. |
| Panel menu button | `button{grafana:components.Panels.Panel.menu:{title}}` | `button[data-testid='data-testid Panel menu {title}']` | The three-dot menu on each panel. Rarely needed in guides. |

The embedded `{grafana:…}` form is required here because the reftarget qualifies a tag (`section`, `button`) or combines two selectors. A bare `grafana:<path>` is only for a reftarget that *is* one selector.

**Untitled panels are the exception -- they stay literal.** An empty argument is inexpressible: `grafana:components.Panels.Panel.title:` has nothing after the colon, so the resolver reads the trailing colon as part of the path and throws. See [Red: No Title](#red-no-title-or-variable-interpolated-title).

### Row Selectors

| Element | Reference | Resolves to | Notes |
|---------|-----------|-------------|-------|
| Row container | `div{grafana:components.LayoutContainer:row {row title}}` | `div[data-testid='data-testid Layout container row {row title}']` | Wrapper around all panels in a row. Only present for explicit `type: "row"` panels. The argument includes the `row ` prefix -- the path is parameterized on the whole identifier. |
| Row toggle button | Row title text (use `action: "button"`) | -- | The row title itself is clickable to expand/collapse. Text match, so it breaks under translation -- but a row title is dashboard content, not UI copy, so it isn't translated. |
| Panel within a row | `div{grafana:components.LayoutContainer:row {row title}} section{grafana:components.Panels.Panel.title:{panel title}}` | Row-scoped literal pair | Row-scoped panel selector for disambiguation. |

`components.LayoutContainer` is only defined from **12.4.0**, and the row container attribute doesn't exist in the DOM before then -- so on an older instance neither the reference nor a literal matches anything. Don't target a row container below 12.4.0; disambiguate with `:nth-match()` instead.

`validate-paths.ts` flags this as `WARN … (defined only from 12.4.0)` and lists it under **BELOW FLOOR**, because the resolver's below-floor fallback would otherwise resolve it cleanly to a value 12.3.0 never carried. See [trap 7](../convert-guide-selectors/symbolic-selector-syntax.md#7-a-path-below-its-floor-resolves-to-the-newest-value).

### Chart / Visualization Selectors

| Element | Reference | Resolves to | Notes |
|---------|-----------|-------------|-------|
| uPlot chart canvas | `grafana:components.UPlotChart.container` | `[data-testid='uplot-main-div']` | Time series chart area. Matches **every** chart on the page -- scope it, don't index it (see below). |
| uPlot within a panel | `section{grafana:components.Panels.Panel.title:{title}} {grafana:components.UPlotChart.container}` | `section[data-testid='data-testid Panel header {title}'] [data-testid='uplot-main-div']` | The stable way to target one panel's chart, and the form to emit. |
| …via the `panel:` shorthand | `panel:{title} > div[data-testid='uplot-main-div']` | `[data-viz-panel-key]:has([data-testid*="Panel header {title}"]) div[data-testid='uplot-main-div']` | Equivalent scoping, but the tail must be **plain CSS** -- see the warning below. |

**Scope the chart, don't index it.** Either row above pins the chart to one panel. `:nth-match(N)` for "the Nth chart globally" is a last resort: the index counts what is *currently rendered*, and Grafana lazy-renders panels -- so `N` is only meaningful once all N charts are in the DOM, and it shifts as the user scrolls. The same caution that applies to untitled panels applies here; see [Why `:nth-match()` is unreliable](#why-nth-match-is-unreliable-for-untitled-panels).

> ⚠️ **`panel:` and `{grafana:}` cannot be combined.** `resolveSelectorForVersion` dispatches on `{grafana:` **first** and returns immediately, so a reftarget containing both never reaches the `panel:` branch. `panel:CPU > {grafana:components.UPlotChart.container}` resolves the token but leaves the literal text `panel:CPU > ` in front of it:
>
> ```
> panel:CPU > :is([data-testid='uplot-main-div'], [aria-label='uplot-main-div'])
> ```
>
> That is not a valid selector and matches nothing, with no error beyond an `onError` callback. Use the fully symbolic form (row 2) or keep the `panel:` tail literal (row 3) -- never both.

`panel:<title> > <rest>` has two further syntax details that read wrong:

- The separator must be exactly `" > "`, spaces included. Without it the whole remainder is taken as the **panel title**, so `panel:CPU uplot-main-div` looks for a panel titled `CPU uplot-main-div`.
- Despite the `>`, `<rest>` joins with a **descendant** combinator, not a child one.

### Variable Selectors

Variable selectors are less standardized than panel selectors. These patterns work but may vary across Grafana versions.

| Element | Reference | Resolves to | Notes |
|---------|-----------|-------------|-------|
| Variable wrapper | `{grafana:pages.Dashboard.SubMenu.submenuItem}` | `div[data-testid='data-testid template variable']` | Container for all variables. Not very useful alone. |
| Specific variable by label | `label:contains('{variable label}')` | -- | No package selector. Works when the variable has a `label` set; falls back to `name` if no label. |
| Variable dropdown button | `button:has(> span:contains('{current value}'))` | -- | Fragile -- depends on current value. Use with caution. |

The two `:contains()` rows match on visible copy. A variable *label* is dashboard content and isn't translated, but a current *value* rendered by Grafana may be -- another reason to prefer `doIt: false` here.

**Variable selector recommendation**: Use `doIt: false` for all variable steps. Variable selectors are inherently less stable than panel selectors, and the user should choose their own variable values.

### Dashboard Chrome Selectors

These are whole-reftarget selectors, so they take the bare `grafana:` form.

| Element | Reference | Resolves to |
|---------|-----------|-------------|
| Time picker | `grafana:components.TimePicker.openButton` | `data-testid TimePicker Open Button` |
| Refresh button | `grafana:components.RefreshPicker.runButtonV2` | `data-testid RefreshPicker run button` |
| Dashboard settings | `grafana:components.NavToolbar.editDashboard.settingsButton` | `data-testid Dashboard settings` |
| Share button | `grafana:pages.Dashboard.DashNav.shareButton` | `data-testid share-button` |

---

## Selector Quality Grading

When extracting panels from dashboard JSON, grade each panel's best available selector. The grade determines guide action confidence.

| Grade | Panel Has | Selector | Confidence |
|-------|----------|----------|------------|
| **Green** | Unique, non-variable title | `section{grafana:components.Panels.Panel.title:{title}}` | High -- `doIt` allowed (though most dashboard panels use `doIt: false` anyway) |
| **Yellow** | Duplicate title (shared by 2+ panels) | Row-scoped reference, or `section{grafana:…title:{title}}:nth-match(N)` | Medium -- `doIt: false` recommended |
| **Red** | No title, empty title, or variable-interpolated title (`$var` in title) | Literal `data-testid` (the reference form can't express an empty title), or `noop` | Low -- `doIt: false` required |

### Green: Unique Panel Title

The most common case. Each panel has a unique `title` that the selector package parameterizes directly.

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
  "reftarget": "section{grafana:components.Panels.Panel.title:CPU Usage}",
  "doIt": false,
  "content": "Review the **CPU Usage** panel.",
  "tooltip": "Shows CPU utilization over time for all selected pods."
}
```

**Below-fold panels** (`gridPos.y >= 8`) **must** use `guided` blocks with `lazyRender: true`. Grafana lazy-renders panels — panels below the viewport do not exist in the DOM until the user scrolls to them. The `exists-reftarget` requirement only waits; it cannot scroll the page. Without `lazyRender: true`, the element will never appear and the step will fail with "Element not found."

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
      "reftarget": "section{grafana:components.Panels.Panel.title:Request Latency}",
      "lazyRender": true,
      "description": "Click inside the highlighted area"
    }
  ]
}
```

### Yellow: Duplicate Panel Title

When multiple panels share the same title (common in dashboards with repeated sections or symmetrical layouts).

**Strategy 1: Row-scoped selector (preferred whenever the panels are in different rows)**

```json
// Guide step -- target within a specific row
{
  "action": "highlight",
  "reftarget": "div{grafana:components.LayoutContainer:row Frontend} section{grafana:components.Panels.Panel.title:Requests/sec}",
  "doIt": false,
  "content": "The **Requests/sec** panel in the **Frontend** row shows frontend request throughput.",
  "tooltip": "Rate of incoming HTTP requests per second."
}
```

Row-scoped selectors are readable, self-documenting, and index-independent.

**Strategy 2: `:nth-match()` (last resort -- only when the panels share a row or the dashboard has none)**

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
  "reftarget": "section{grafana:components.Panels.Panel.title:Requests/sec}:nth-match(1)",
  "doIt": false,
  "content": "The first **Requests/sec** panel shows frontend request throughput.",
  "tooltip": "Rate of incoming HTTP requests per second."
}
```

`:nth-match(1)` is the only index that is reliably safe, because the first match is in the DOM at page load. Anything above 1 depends on every earlier match being rendered -- see [Why `:nth-match()` is unreliable](#why-nth-match-is-unreliable-for-untitled-panels), which applies to titled duplicates just as much as to untitled panels.

### Red: No Title or Variable-Interpolated Title

Red-grade panels are the hardest to target reliably. **Prefer describing them in markdown or `noop` blocks rather than attempting fragile selectors.** Only target them with selectors if they are critical to the guide's educational purpose.

**These stay literal.** The reference form is parameterized on the title, and an empty argument is inexpressible: `splitGrafanaPathParam` only treats a colon as a parameter separator when something follows it, so `grafana:components.Panels.Panel.title:` reads the trailing colon as part of the path and throws `Selector not found`. Write `section[data-testid='data-testid Panel header ']` -- with the trailing space -- and note it in the extraction report as one of the few places a literal is correct.

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
      "lazyRender": true,
      "description": "Click inside the highlighted area"
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

The rendered title depends on the current variable value (e.g., "Details for quickpizza-api"). The resolved value will contain the interpolated value, not the template -- so whichever form you use, you are writing one variable value into the guide.

```json
// Guide step -- explain the variable dependency, use row scoping if possible
{
  "action": "highlight",
  "reftarget": "div{grafana:components.LayoutContainer:row Details for quickpizza-api} section:nth-match(1)",
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
     → Selector: row-scoped reference with the interpolated value, or `:nth-match()`
     → Note: selector depends on current variable value
     → If below fold: same lazyRender guidance as untitled panels
4. Count how many panels share this exact title:
     If count == 1:
       → Grade: Green
       → Selector: `section{grafana:components.Panels.Panel.title:{title}}`
       → If above fold: use plain interactive block (exists-reftarget waits for the element)
       → If below fold: MUST use guided block with lazyRender: true
         (exists-reftarget only waits — it cannot scroll; without lazyRender
         Grafana never renders the panel and the selector times out)
     If count > 1:
       → Grade: Yellow
       → If panels are in different rows:
           → Selector: `div{grafana:components.LayoutContainer:row {row title}}
                        section{grafana:components.Panels.Panel.title:{title}}`
       → Else:
           → Selector: `section{grafana:components.Panels.Panel.title:{title}}:nth-match(N)`
           → N = this panel's position among same-titled panels (sorted by gridPos.y, then x)
       → If below fold: same nth-match + lazy-render caution applies
5. Record the grade, fold position, and selector in the extraction report
6. Validate every `grafana:` path the guide emits before shipping:
     GRAFANA_REPO=~/Repos/grafana npx tsx \
       ../convert-guide-selectors/scripts/validate-paths.ts '[...]' "<min>,<current>"
     One unresolvable token voids the entire reftarget, so validate all of them, not a sample.
```

**Untitled panels are the one case that stays literal** (step 2 above). Everything else emits the reference form: it resolves per running Grafana version and matches `data-testid` or `aria-label`, where a literal pins one version's value in one attribute.

**Fold estimation heuristic**: Estimate fold position by summing the `gridPos.h` values of all panels whose `gridPos.y` is less than this panel's `gridPos.y`. A cumulative height >= 8 grid units suggests the panel is below the fold on a standard 1080px viewport. The `gridPos.y >= 8` shortcut is a rough approximation; summing actual panel heights is more accurate when large panels (h >= 8) appear early in the layout.

---

## Selector Quality Report Template

Include this report alongside every generated guide as `assets/selector-report.md` in the guide directory. Start the file with the standard frontmatter disclaimer (see SKILL.md "Generated Files" section).

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

Untitled panels are the one grade that stays on a literal `data-testid` -- the reference form can't express an empty title.

| Position (gridPos) | Panel Type | Selector |
|-------------------|------------|----------|
| y:0, x:12 | stat | nth-match(3) |

### Path Validation

| Grafana version | Paths checked | Failures | Below floor |
|-----------------|---------------|----------|-------------|
| {min supported} | {n} | 0 | 0 |
| {current} | {n} | 0 | 0 |

Produced by `convert-guide-selectors/scripts/validate-paths.ts`. A non-zero **failure** count means the guide ships a reftarget that resolves to nothing. A non-zero **below floor** count means a path resolves but its selector didn't exist at that version -- so it matches nothing there even though validation "passed".

### Suggestions
- Panels with duplicate titles would benefit from unique titles for selector stability
- Variable-interpolated titles create fragile selectors; consider static titles with variable in subtitle
```

---

## Dashboard-Specific Selector Caveats

For lazy rendering guidance — why below-fold panels require `guided` blocks with `lazyRender: true`, and why `nth-match(N)` is unreliable for panels not yet in the DOM — see the **Lazy Rendering (CRITICAL)** section in `dashboard-guide-rules.md`.

### Repeated Panels

Panels with `"repeat": "varName"` create copies for each variable value. The copies share the same base title but may have the variable value appended. When the value is known, name it in the reference -- `section{grafana:components.Panels.Panel.title:{title} {value}}` -- which is stable in a way an index isn't. Otherwise use `:nth-match(1)` for the first instance, or explain the repeat pattern in a `noop` step.

### Embedded Links in Panels

Table panels and stat panels often contain data links that navigate to other dashboards or drill-down views. These links appear on hover or click. Use `guided` blocks with `hover` steps to reveal them before targeting.

### Dashboard Annotations

Annotation overlays (vertical lines on time-series panels) are not directly targetable with selectors. Mention annotations in `noop` or `markdown` blocks to explain their presence.
