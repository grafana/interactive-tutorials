# Selectors and Test IDs Reference

This guide covers stable selectors and patterns for targeting Grafana UI elements, including advanced pseudo-selectors.

## Selector Best Practices

### Stability Priority

1. **`data-testid` attributes** - Most stable, maintained by Grafana
2. **Semantic attributes** - `href`, `aria-*`, `id`, `role`
3. **Element + attribute combos** - `button[type="submit"]`
4. **Avoid** - Auto-generated CSS classes like `.css-8mjxyo`

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
| Query mode toggle (Code)    | `div[data-testid="QueryEditorModeToggle"] label[for^="option-code"]`    |
| Visualization picker toggle | `button[data-testid="data-testid toggle-viz-picker"]`                   |
| Panel title input           | `input[data-testid="data-testid Panel editor option pane field input Title"]` |

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

| Selector             | Meaning                                             |
|----------------------|-----------------------------------------------------|
| `div:nth-child(3)`   | Element that is the 3rd child of its parent         |
| `div:nth-match(3)`   | The 3rd div matching this selector in the document  |

`:nth-child()` fails when matching elements are in different parents.

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

Some UI elements only appear on hover. Use with `hover` action or `guided` blocks.

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

## Browser Compatibility

### Native Support

- **`:has()`**: Chrome 105+, Safari 17.2+, Firefox 140+
- **`:contains()`**: Not native (jQuery extension)
- **`:nth-match()`**: Custom implementation

### Automatic Fallback

The selector engine automatically provides JavaScript fallbacks for older browsers.

---

## Troubleshooting

### "No elements found"

1. **Test the base selector** in browser DevTools:
   ```javascript
   document.querySelectorAll('div[data-testid="uplot-main-div"]').length
   ```

2. **Check element count** for `:nth-match()`:
   - `:nth-match(3)` needs at least 3 elements

3. **Check timing** - elements may not be loaded yet:
   - Add requirements like `on-page:/dashboards`

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
