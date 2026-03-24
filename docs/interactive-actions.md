# Interactive Actions Reference

How each action type behaves at runtime — Show vs Do modes, target semantics, and when to use each.

## Concepts

- **Show vs Do**: Every action runs in two modes. Show highlights the target without changing state; Do performs the action (click, fill, navigate) and marks the step completed.
- **Targets**: Depending on the action, `reftarget` is either a CSS selector, button text, a URL/path, or a section container selector.

---

## highlight

- **Purpose**: Focus and (on Do) click a specific element by CSS selector.
- **reftarget**: CSS selector.
- **Show**: Ensures visibility and highlights.
- **Do**: Ensures visibility then clicks.
- **Use when**: The target element is reliably selectable via a CSS selector (often `data-testid`-based).

```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "a[data-testid='data-testid Nav menu item'][href='/dashboards']",
  "requirements": ["navmenu-open"],
  "content": "Open Dashboards"
}
```

## button

- **Purpose**: Interact with buttons by their visible text.
- **reftarget**: Button text (exact match preferred; partial supported but less stable).
- **Show**: Highlights matching buttons.
- **Do**: Clicks matching buttons.
- **Use when**: The button text is stable; avoids brittle CSS.

```json
{
  "type": "interactive",
  "action": "button",
  "reftarget": "Save & test",
  "content": "Save the data source"
}
```

## formfill

- **Purpose**: Fill inputs, textareas (including Monaco), selects, and ARIA comboboxes.
- **reftarget**: CSS selector for the input element.
- **targetvalue**: String to set (required).
- **Show**: Highlights the field.
- **Do**: Sets the value and fires the right events; ARIA comboboxes are handled token-by-token; Monaco editors use enhanced events.
- **Use when**: Setting values in fields or editors.

```json
{
  "type": "interactive",
  "action": "formfill",
  "reftarget": "input[id='connection-url']",
  "targetvalue": "http://prometheus:9090",
  "content": "Set URL"
}
```

**Formfill Validation:**

Use `validateInput: true` to require the input to match a pattern:

```json
{
  "type": "interactive",
  "action": "formfill",
  "reftarget": "input[data-testid='prometheus-url']",
  "targetvalue": "^https?://",
  "validateInput": true,
  "formHint": "URL must start with http:// or https://",
  "content": "Enter your Prometheus server URL."
}
```

## navigate

- **Purpose**: Navigate to a Grafana route or external URL.
- **reftarget**: Internal path (e.g. `/dashboard/new`) or absolute URL.
- **Show**: Indicates the intent to navigate.
- **Do**: Uses Grafana `locationService.push` for internal paths; opens new tab for external URLs.
- **Use when**: The interaction is pure navigation.

```json
{
  "type": "interactive",
  "action": "navigate",
  "reftarget": "/dashboard/new",
  "verify": "on-page:/dashboard/new",
  "content": "Create dashboard"
}
```

## hover

- **Purpose**: Trigger hover states on elements to reveal UI that appears only on hover.
- **reftarget**: CSS selector for element to hover over.
- **Show**: Highlights the element without triggering hover.
- **Do**: Dispatches mouse events (`mouseenter`, `mouseover`, `mousemove`) and maintains hover state.
- **Use when**: UI elements are hidden until hover, or CSS hover states need to be triggered.

```json
{
  "type": "interactive",
  "action": "hover",
  "reftarget": "div[data-testid='table-row']",
  "content": "Hover over the row to reveal action buttons"
}
```

## noop

- **Purpose**: Informational step with no DOM action.
- **reftarget**: Optional. If provided, highlights the element for context.
- **Show**: Highlights the element (if reftarget provided), otherwise no visual effect.
- **Do**: No action performed. Step completes immediately.
- **Use when**: You need an informational pause between actions, or a step that only explains without interacting.

```json
{
  "type": "interactive",
  "action": "noop",
  "content": "Now that you've saved your data source, let's create a dashboard to visualize the data."
}
```

**With optional highlight:**

```json
{
  "type": "interactive",
  "action": "noop",
  "reftarget": "div[data-testid='alert-banner']",
  "content": "Notice the success banner confirming your data source is connected.",
  "tooltip": "This confirms the connection test passed."
}
```

---

## Show-Only Mode

Use `doIt: false` to create educational steps that only highlight elements without requiring user action:

```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "div[data-testid='dashboard-panel']",
  "content": "Notice the **metrics panel** displaying your data.",
  "tooltip": "This panel shows real-time metrics from your Prometheus data source.",
  "doIt": false
}
```

When `doIt` is false:
- Only the "Show me" button appears (no "Do it" button)
- Step completes automatically after showing the element
- No state changes occur in the application

---

## See Also

- [JSON Guide Reference](json-guide-reference.md) - Block types and property tables
- [Guided Interactions](guided-interactions.md) - Detailed guided block documentation
- [Requirements Reference](requirements-reference.md) - All supported requirements
- [Selectors Reference](selectors-and-testids.md) - Stable selector patterns
