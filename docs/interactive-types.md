# Interactive Types Reference

This guide explains the supported interactive types, when to use each, what `reftarget` expects, and how Show vs Do behaves.

## Concepts

- **Show vs Do**: Every action runs in two modes. Show highlights the target without changing state; Do performs the action (click, fill, navigate) and marks the step completed.
- **Targets**: Depending on the action, `reftarget` is either a CSS selector, button text, a URL/path, or a section container selector.

---

## Interactive Action Types

### highlight

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

### button

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

### formfill

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

### navigate

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

### hover

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

### noop

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

## Structural Block Types

### section

- **Purpose**: Group multiple steps with coordinated execution.
- **Structure**: JSON object with `type: "section"` and `blocks` array.
- **Features**: Progress tracking, resumable execution, state persistence.
- **Button**: Single "Do Section" button executes all child steps.

```json
{
  "type": "section",
  "id": "setup-datasource",
  "title": "Set up data source",
  "objectives": ["has-datasource:prometheus"],
  "blocks": [
    {
      "type": "interactive",
      "action": "highlight",
      "reftarget": "a[href='/connections']",
      "content": "Open Connections"
    },
    {
      "type": "interactive",
      "action": "formfill",
      "reftarget": "input[id='basic-settings-name']",
      "targetvalue": "prometheus-datasource",
      "content": "Name it"
    }
  ]
}
```

### multistep

- **Purpose**: Execute multiple actions as single atomic step.
- **Structure**: JSON object with `type: "multistep"` and `steps` array.
- **Execution**: Shows each action, then executes in sequence.
- **Button**: Single "Do it" button executes all steps automatically.

```json
{
  "type": "multistep",
  "content": "Click Add visualization, then pick the data source.",
  "requirements": ["on-page:/dashboard/new"],
  "steps": [
    { "action": "button", "reftarget": "Add visualization" },
    { "action": "button", "reftarget": "prometheus-datasource" }
  ]
}
```

### guided

- **Purpose**: Highlights elements and waits for the user to perform actions manually.
- **Structure**: JSON object with `type: "guided"` and `steps` array.
- **Behavior**: System highlights each step and waits for user interaction before proceeding.
- **Supported actions**: `hover`, `button`, `highlight` (formfill and navigate not yet supported).
- **Use when**: Actions depend on CSS `:hover` states or you want users to learn by doing.
- **Detailed docs**: See [Guided Interactions](guided-interactions.md) for configuration, section integration, timeout behavior, and troubleshooting.

```json
{
  "type": "guided",
  "content": "Explore Prometheus configuration settings and save your data source.",
  "stepTimeout": 45000,
  "skippable": true,
  "steps": [
    {
      "action": "hover",
      "reftarget": ".gf-form:has([data-testid='prometheus-type']) label > svg",
      "tooltip": "The **Performance** section contains advanced settings."
    },
    {
      "action": "highlight",
      "reftarget": "[data-testid='prometheus-type']",
      "tooltip": "The **Prometheus type** dropdown specifies your connection type."
    },
    {
      "action": "button",
      "reftarget": "Save & test",
      "tooltip": "Click **Save & test** to create your data source."
    }
  ]
}
```

**Key differences from multistep:**
- **Multistep**: System performs all actions automatically
- **Guided**: System highlights and waits for user to perform actions manually
- **Hover support**: Real hover (triggers CSS `:hover` states), not simulated

### conditional

- **Purpose**: Shows different content based on runtime condition evaluation.
- **Conditions**: Use requirement syntax (e.g., `has-datasource:prometheus`, `is-admin`).
- **Behavior**: When ALL conditions pass, shows `whenTrue`; otherwise shows `whenFalse`.

```json
{
  "type": "conditional",
  "conditions": ["has-datasource:prometheus"],
  "description": "Show Prometheus-specific content or fallback",
  "whenTrue": [
    {
      "type": "markdown",
      "content": "Great! You have Prometheus configured."
    }
  ],
  "whenFalse": [
    {
      "type": "markdown",
      "content": "You'll need to set up a Prometheus data source first."
    }
  ]
}
```

---

## Content Block Types

### markdown

- **Purpose**: Formatted text content.
- **Features**: Headings, bold, italic, code blocks, lists, tables, links.

```json
{
  "type": "markdown",
  "content": "## Getting Started\n\nWelcome to **Grafana**!\n\n- Feature one\n- Feature two"
}
```

### image

- **Purpose**: Embed images with optional dimensions.

```json
{
  "type": "image",
  "src": "https://example.com/screenshot.png",
  "alt": "Dashboard screenshot",
  "width": 400
}
```

### video

- **Purpose**: Embed YouTube or native HTML5 video.

```json
{
  "type": "video",
  "src": "https://www.youtube.com/embed/VIDEO_ID",
  "provider": "youtube",
  "title": "Getting Started with Grafana"
}
```

---

## Assessment Block Types

### quiz

- **Purpose**: Knowledge assessment with single or multiple choice questions.

```json
{
  "type": "quiz",
  "question": "Which query language does Prometheus use?",
  "completionMode": "correct-only",
  "choices": [
    { "id": "a", "text": "SQL", "hint": "SQL is for traditional databases." },
    { "id": "b", "text": "PromQL", "correct": true },
    { "id": "c", "text": "GraphQL", "hint": "GraphQL is an API query language." }
  ]
}
```

### input

- **Purpose**: Collects user responses that can be stored as variables.
- **Variable usage**: Reference with `{{variableName}}` in content or `var-name:value` in requirements.

```json
{
  "type": "input",
  "prompt": "What is the name of your Prometheus data source?",
  "inputType": "text",
  "variableName": "prometheusName",
  "placeholder": "e.g., prometheus-main",
  "required": true
}
```

---

## Show-Only Mode

Use `doIt: false` to create educational steps that only highlight elements without requiring user action.

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
- Focus is on education rather than interaction

**Button Visibility Control:**

| Setting               | "Show me" Button | "Do it" Button | Use Case                      |
|-----------------------|------------------|----------------|-------------------------------|
| Default (both `true`) | ✅               | ✅             | Normal interactive step       |
| `doIt: false`         | ✅               | ❌             | Educational highlight only    |
| `showMe: false`       | ❌               | ✅             | Direct action without preview |

---

## Choosing the Right Type

| Need                                    | Block Type / Action              |
|-----------------------------------------|----------------------------------|
| Click by CSS selector                   | `interactive` + `highlight`      |
| Click by button text                    | `interactive` + `button`         |
| Enter text/select values                | `interactive` + `formfill`       |
| Route change                            | `interactive` + `navigate`       |
| Hover to reveal hidden UI               | `interactive` + `hover`          |
| Informational pause (no DOM action)     | `interactive` + `noop`           |
| Teach a linear section                  | `section`                        |
| Bundle micro-steps into one (automated) | `multistep`                      |
| User performs steps manually            | `guided`                         |
| Show different content by condition     | `conditional`                    |
| Test user knowledge                     | `quiz`                           |
| Collect user input for variables        | `input`                          |
| Just explanation (no action)            | `interactive` with `doIt: false` |

---

## See Also

- [JSON Guide Format](json-guide-format.md) - Root structure and block overview
- [JSON Block Properties](json-block-properties.md) - Complete property reference
- [Guided Interactions](guided-interactions.md) - Detailed guided block documentation
- [Requirements Reference](requirements-reference.md) - All supported requirements
- [Selectors Reference](selectors-and-testids.md) - Stable selector patterns
