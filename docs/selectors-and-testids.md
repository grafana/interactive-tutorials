### Selectors and test IDs mapped to Grafana components

This file lists common, stable selectors and patterns already used across tutorials. Prefer these over brittle CSS class selectors.

## Navigation and core areas

| Component/Area          | Preferred selector                                                | Notes                                                                                                          |
| ----------------------- | ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Nav menu item (by href) | `a[data-testid='data-testid Nav menu item'][href='/connections']` | Used for Connections, Dashboards, Explore, Alerting, Admin, Home. Replace href accordingly.                    |
| Navigation container    | `div[data-testid="data-testid navigation mega-menu"]`             | Used to detect open nav. Fallbacks include `ul[aria-label='Navigation']` and `div[data-testid*='navigation']`. |

## Editor and panel building

| Component/Area              | Preferred selector                                                              | Notes                                |
| --------------------------- | ------------------------------------------------------------------------------- | ------------------------------------ |
| Query mode toggle (Code)    | `div[data-testid="QueryEditorModeToggle"] label[for^="option-code-radiogroup"]` | Switch to Code mode for raw queries. |
| Visualization picker toggle | `button[data-testid="data-testid toggle-viz-picker"]`                           | Opens visualization picker.          |
| Panel title input           | `input[data-testid="data-testid Panel editor option pane field input Title"]`   | Edit panel title.                    |

## Drilldowns (example)

| Component/Area        | Preferred selector                                                                             | Notes                    |
| --------------------- | ---------------------------------------------------------------------------------------------- | ------------------------ |
| Metrics drilldown app | `a[data-testid='data-testid Nav menu item'][href='/a/grafana-metricsdrilldown-app/drilldown']` | Opens app entrypoint.    |
| Select metric action  | `button[data-testid="select-action_<metric_name>"]`                                            | Replace `<metric_name>`. |
| Related metrics tab   | `button[data-testid="data-testid Tab Related metrics"]`                                        | Tab toggle.              |
| Related logs tab      | `button[data-testid="data-testid Tab Related logs"]`                                           | Tab toggle.              |

## Buttons by text

For generic buttons, prefer the `button` action with `data-reftarget` as the button’s visible text. The system finds buttons by text reliably and avoids brittle CSS.

Examples:

```html
<li class="interactive" data-targetaction="button" data-reftarget="Add new data source"></li>
<li class="interactive" data-targetaction="button" data-reftarget="Save & test"></li>
<li class="interactive" data-targetaction="button" data-reftarget="Save"></li>
<li class="interactive" data-targetaction="button" data-reftarget="New"></li>
```

## Inputs and fields

- Prefer attribute-stable selectors like `input[id='basic-settings-name']`, `input[placeholder='https://feed']`, `textarea.inputarea` (Monaco), or ARIA roles (e.g., `role='combobox'`).
- ARIA comboboxes: the system detects `role='combobox'` and stages tokens with Enter presses.

## Notes on stability

- `data-testid` values under Grafana core are more stable than CSS classes. Favor them whenever available.
- Avoid selecting by auto-generated class names or deep DOM nesting; use attributes (`data-testid`, `href`, `aria-*`, `id`) instead.

## Unsupported selectors

Some CSS pseudo-classes are **not supported** in our selector engine. Avoid these:

| Unsupported Selector | Use Instead        | Example                                                                     |
| -------------------- | ------------------ | --------------------------------------------------------------------------- |
| `:first`             | `:nth-match(1)`    | `div[data-cy="item"]:nth-match(1)` instead of `div[data-cy="item"]:first`  |
| `:last`              | `:nth-match(-1)`   | `div[data-cy="item"]:nth-match(-1)` instead of `div[data-cy="item"]:last`  |

**Why `:nth-match()`?**
- `:nth-match(1)` selects the first element matching the entire selector
- `:first` is ambiguous in complex selectors and not widely supported
- Use `:nth-match(1)` for the first match, `:nth-match(-1)` for the last

**Note on auto-generated CSS classes:**
- Avoid classes like `.css-8mjxyo`, `.css-1fg2lur` - these are auto-generated and change between builds
- Use semantic attributes (`data-cy`, `data-testid`, `aria-label`) or stable structural selectors instead

## Contributing more mappings

When you find a reliable selector, contribute it here with a short note so authors can reuse stable patterns.
