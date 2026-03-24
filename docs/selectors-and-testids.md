# Selectors and Test IDs Reference

This guide covers stable selectors and patterns for targeting Grafana UI elements, including advanced pseudo-selectors.

## Selector Best Practices

### Selector Priority

Follow this priority order when choosing selectors:

1. **`data-testid` attributes** -- most stable, maintained by Grafana core
2. **Semantic attributes** -- `href`, `aria-*`, `id`, `role`
3. **`:contains()` text matching** -- reliable for buttons and labels
4. **`:has()` structural matching** -- when you need to match by descendants
5. **CSS class selectors** -- least stable; avoid auto-generated class names

> Avoid selecting by auto-generated class names or deep DOM nesting. Use attributes (`data-testid`, `href`, `aria-*`, `id`) instead.

### Example

```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "a[data-testid='data-testid Nav menu item'][href='/dashboards']",
  "requirements": ["navmenu-open", "exists-reftarget"],
  "content": "Click Dashboards"
}
```

---

## Common Stable Selectors

### Navigation Elements

| Component               | Selector                                                          |
|-------------------------|-------------------------------------------------------------------|
| Home                    | `a[data-testid='data-testid Nav menu item'][href='/']`            |
| Dashboards              | `a[data-testid='data-testid Nav menu item'][href='/dashboards']`  |
| Explore                 | `a[data-testid='data-testid Nav menu item'][href='/explore']`     |
| Alerting                | `a[data-testid='data-testid Nav menu item'][href='/alerting']`    |
| Connections             | `a[data-testid='data-testid Nav menu item'][href='/connections']` |
| Admin                   | `a[data-testid='data-testid Nav menu item'][href='/admin']`       |
| Navigation container    | `div[data-testid="data-testid navigation mega-menu"]`             |

### Editor and Panel Building

| Component                   | Selector                                                                |
|-----------------------------|-------------------------------------------------------------------------|
| Query mode toggle (Code)    | `div[data-testid="QueryEditorModeToggle"] label[for^="option-code-radiogroup"]` |
| Visualization picker toggle | `button[data-testid="data-testid toggle-viz-picker"]`                           |
| Panel title input           | `input[data-testid="data-testid Panel editor option pane field input Title"]`   |

### Drilldowns

| Component             | Selector                                                                                       | Notes                   |
|-----------------------|------------------------------------------------------------------------------------------------|-------------------------|
| Metrics drilldown app | `a[data-testid='data-testid Nav menu item'][href='/a/grafana-metricsdrilldown-app/drilldown']` | Opens app entrypoint    |
| Select metric action  | `button[data-testid="select-action_<metric_name>"]`                                            | Replace `<metric_name>` |
| Related metrics tab   | `button[data-testid="data-testid Tab Related metrics"]`                                        | Tab toggle              |
| Related logs tab      | `button[data-testid="data-testid Tab Related logs"]`                                           | Tab toggle              |

### Data Source Elements

| Component        | Selector                                             |
|------------------|------------------------------------------------------|
| Name input       | `input[id='basic-settings-name']`                    |
| Connection URL   | `input[id='connection-url']`                         |
| Prometheus type  | `a[href='/connections/datasources/prometheus']`      |

---

## Button Action vs CSS Selector

For buttons with stable text, prefer the `button` action:

```json
{
  "type": "interactive",
  "action": "button",
  "reftarget": "Save & test",
  "content": "Save the data source"
}
```

Common button texts:
- `"Add new data source"`
- `"Save & test"`
- `"Save"`
- `"New"`
- `"Add visualization"`

---

## Advanced Selectors

The selector engine supports complex CSS selectors with automatic browser fallbacks.

### `:nth-match()` Pseudo-Selector

Finds the Nth occurrence of an element matching the selector **globally** (not within parent).

```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "div[data-testid='uplot-main-div']:nth-match(3)",
  "content": "Highlight the third chart on the page"
}
```

**Why use `:nth-match()` instead of `:nth-child()`?**

`:nth-child(3)` means "match this element only if it is the 3rd child of its parent." When charts live in separate parent containers, `:nth-child()` fails because each chart is the 1st child of its own parent.

```html
<!-- Each chart is the 1st child of its own parent -- :nth-child(3) matches nothing -->
<div class="parent1">
  <div data-testid="uplot-main-div">First chart</div>
</div>
<div class="parent2">
  <div data-testid="uplot-main-div">Second chart</div>
</div>
<div class="parent3">
  <div data-testid="uplot-main-div">Third chart</div>
</div>
```

**Quick reference:**

| Selector             | Meaning                                                     | Use when                                       |
|----------------------|-------------------------------------------------------------|------------------------------------------------|
| `div:nth-child(3)`   | Element that is the 3rd child of its parent                 | You know the element's position in its parent  |
| `div:nth-of-type(3)` | Element that is the 3rd `div` child of its parent           | You know the position among same-type siblings |
| `div:nth-match(3)`   | The 3rd `div` matching this selector in the entire document | You want the Nth global occurrence             |

### `:contains()` Pseudo-Selector

Finds elements containing specific text content (jQuery-style).

```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "div:contains('checkoutservice')",
  "content": "Highlight service containers"
}
```

### `:has()` Pseudo-Selector

Finds elements that contain specific descendant elements.

```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "div[data-cy='service-card']:has(p)",
  "content": "Highlight service cards with descriptions"
}
```

### Combined Complex Selectors

The most powerful feature: combining `:has()` and `:contains()`.

```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "div[data-cy='wb-list-item']:has(p:contains('checkoutservice'))",
  "content": "Highlight the checkout service item"
}
```

**More examples:**

```json
{
  "type": "interactive",
  "action": "button",
  "reftarget": "div[data-cy='service-item']:has(h3:contains('Auth Service')) button[data-action='configure']",
  "content": "Configure the authentication service"
}
```

---

## Hover-Dependent Selectors

Some UI elements only appear when hovering over their parent containers (e.g., Tailwind's `group-hover:` or CSS `:hover` states). Use the `hover` action to reveal elements before interacting with them.

### How Hover Actions Work

**Show mode** (Show me): highlights the element that will be hovered; does not trigger hover events.

**Do mode** (Do it): dispatches `mouseenter`, `mouseover`, `mousemove` events, triggering CSS `:hover` and Tailwind `group-hover:` classes. Maintains hover state for 2 seconds (configurable via `INTERACTIVE_CONFIG.delays.perceptual.hover`). Subsequent actions can then interact with revealed elements.

### Multistep with Hover

```json
{
  "type": "multistep",
  "content": "Hover over service row and click Dashboard button",
  "steps": [
    {
      "action": "hover",
      "reftarget": "div[data-cy='wb-list-item']:has(p:contains('checkoutservice'))"
    },
    {
      "action": "button",
      "reftarget": "Dashboard"
    }
  ]
}
```

### Guided with Hover

```json
{
  "type": "guided",
  "content": "Manually hover and click",
  "steps": [
    {
      "action": "hover",
      "reftarget": "tr[data-row-id='user-123']",
      "tooltip": "Hover over the row to reveal action buttons"
    },
    {
      "action": "button",
      "reftarget": "Edit",
      "tooltip": "Click the Edit button"
    }
  ]
}
```

---

## Inputs and Form Fields

### Text Inputs

Use attribute-stable selectors:

```json
{
  "type": "interactive",
  "action": "formfill",
  "reftarget": "input[id='basic-settings-name']",
  "targetvalue": "my-datasource",
  "content": "Enter data source name"
}
```

### Monaco Editor

```json
{
  "type": "interactive",
  "action": "formfill",
  "reftarget": "textarea.inputarea.monaco-mouse-cursor-text",
  "targetvalue": "rate(http_requests_total[5m])",
  "content": "Enter the PromQL query"
}
```

### ARIA Comboboxes

The system detects `role='combobox'` and handles token entry automatically:

```json
{
  "type": "interactive",
  "action": "formfill",
  "reftarget": "input[role='combobox'][aria-autocomplete='list']",
  "targetvalue": "container = 'alloy'",
  "content": "Enter container label"
}
```

---

## Unsupported Selectors

Some pseudo-classes are **not supported**. Use alternatives:

| Unsupported | Use Instead       | Example                                |
|-------------|-------------------|----------------------------------------|
| `:first`    | `:nth-match(1)`   | `div[data-cy="item"]:nth-match(1)`     |
| `:last`     | `:nth-match(-1)`  | `div[data-cy="item"]:nth-match(-1)`    |

---

## Performance Best Practices

1. **Native first** -- the engine always tries the browser's native `querySelector()` before falling back to JavaScript parsing
2. **Specific base selectors** -- narrow the search scope (e.g., `div[data-testid="panel"]:has(...)` rather than `div:has(...)`)
3. **Prefer `data-testid`** -- fastest and most stable
4. **Test in target browsers** -- especially when using `:has()` on older Firefox

---

## Browser Compatibility

| Selector                         | Native support                            | Fallback                           |
|----------------------------------|-------------------------------------------|------------------------------------|
| `:has()`                         | Chrome 105+, Safari 17.2+, Firefox 140+   | Automatic JS fallback              |
| `:contains()`                    | Not natively supported (jQuery extension) | Automatic JS fallback              |
| `:nth-match()`                   | Custom implementation                     | Uses `querySelectorAll` internally |
| `:nth-child()`, `:nth-of-type()` | All browsers                              | Standard CSS                       |

The selector engine automatically detects browser capabilities and provides JavaScript-based fallbacks when native support is missing.

---

## Troubleshooting

### "No elements found" with `:nth-match()`

1. Verify the base selector finds elements: `document.querySelectorAll('div[data-testid="uplot-main-div"]').length` in the browser console
2. Confirm enough matches exist (`:nth-match(3)` needs at least 3 elements)
3. Ensure elements are loaded -- add `requirements: ["exists-reftarget"]` or `requirements: ["on-page:/dashboards"]`

### General Selector Issues

- **Invalid syntax** -- the engine handles malformed selectors gracefully and returns empty arrays
- **Missing elements** -- check requirements to ensure the page state is correct before the step runs
- **Browser compatibility** -- automatic fallback handles most cases; check the browser console for detailed logging

### Avoiding Brittle Selectors

❌ **Avoid**:
```
.css-8mjxyo
div > div > div > button
[class*='partial-match']
```

✅ **Prefer**:
```
button[data-testid='save-button']
a[href='/dashboards']
input[id='connection-url']
```

---

## See Also

- [Interactive Types](interactive-types.md) - When to use each action type
- [JSON Block Properties](json-block-properties.md) - Complete property reference
- [Requirements Reference](requirements-reference.md) - Requirement conditions
