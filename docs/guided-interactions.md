# Guided Interactions

Guided interactions highlight elements and display instructions, then **wait for the user to manually perform the action** before proceeding to the next step. They provide a middle ground between fully automated multistep actions and unassisted manual execution.

## When to use guided

- Actions depend on CSS `:hover` states that cannot be programmatically triggered
- You want users to learn by doing rather than watching automation
- UI elements are hidden behind hover states (e.g., RCA Workbench action buttons)
- You need users to experience the actual interaction flow

### Guided vs multistep

| Feature             | Multistep            | Guided                        |
|---------------------|----------------------|-------------------------------|
| Execution           | Fully automated      | User performs manually        |
| Hover support       | Simulated (limited)  | Real hover (works everywhere) |
| CSS `:hover`        | Cannot trigger       | Triggers naturally            |
| Learning            | Watch automation     | Learn by doing                |
| Speed               | Fast                 | User-paced                    |
| Reliability         | Depends on selectors | Depends on user               |
| Section integration | Runs in sequence     | Pauses section                |

## Basic syntax

A guided block contains a `content` description and a `steps` array. Each step specifies an `action` and `reftarget`.

```json
{
  "type": "guided",
  "content": "Inspect the checkout service details",
  "steps": [
    {
      "action": "hover",
      "reftarget": "div[data-cy=\"wb-list-item\"]:contains(\"checkoutservice\")",
      "description": "Hover over the checkout service row to reveal action buttons"
    },
    {
      "action": "button",
      "reftarget": "Dashboard",
      "description": "Click the Dashboard button that appeared"
    }
  ]
}
```

The `description` field on each step appears as a tooltip/instruction when that step is highlighted.

## Supported action types

Guided mode supports these action types within its steps:

### Hover

The system highlights the element and waits for the user to hover over it for 500 ms.

```json
{
  "type": "guided",
  "content": "Hover over the table row to reveal actions",
  "steps": [
    {
      "action": "hover",
      "reftarget": "div.table-row",
      "description": "Hover your mouse over this row to reveal the action buttons"
    }
  ]
}
```

### Button

The system highlights the button and waits for the user to click it.

```json
{
  "type": "guided",
  "content": "Open the settings menu",
  "steps": [
    {
      "action": "button",
      "reftarget": "button[aria-label=\"Settings\"]",
      "description": "Click the Settings button"
    }
  ]
}
```

### Highlight

Same as button -- waits for the user to click the highlighted element.

```json
{
  "type": "guided",
  "content": "Select the dashboard panel",
  "steps": [
    {
      "action": "highlight",
      "reftarget": "#dashboard-panel",
      "description": "Click the panel to select it"
    }
  ]
}
```

## Configuration

### `stepTimeout`

Controls how long to wait for user action before showing a skip/retry option. Default: 30000 ms (30 seconds).

```json
{
  "type": "guided",
  "content": "Complex interaction with longer timeout",
  "stepTimeout": 45000,
  "steps": [{ "action": "hover", "reftarget": "div.service-row" }]
}
```

### `skippable`

Allows users to skip the entire guided interaction if they cannot complete it.

```json
{
  "type": "guided",
  "content": "Optional guided step",
  "skippable": true,
  "steps": [{ "action": "hover", "reftarget": "div.row" }]
}
```

Individual steps can also be marked skippable:

```json
{
  "steps": [
    { "action": "hover", "reftarget": "div.row", "skippable": true },
    { "action": "button", "reftarget": "Edit" }
  ]
}
```

### `completeEarly`

When `true`, the guided block can mark itself complete if the user performs the expected action before the guide formally reaches that step.

```json
{
  "type": "guided",
  "content": "Hover and click the action button",
  "completeEarly": true,
  "steps": [
    { "action": "hover", "reftarget": "tr[data-row-id=\"user-123\"]" },
    { "action": "button", "reftarget": "Edit" }
  ]
}
```

### `requirements` and `objectives`

Guided blocks support the same requirements and objectives system as other interactive blocks.

```json
{
  "type": "guided",
  "content": "Click the button (only enabled when it exists)",
  "requirements": ["exists-reftarget"],
  "objectives": ["on-page:/dashboards/edit"],
  "steps": [{ "action": "button", "reftarget": "button[aria-label=\"Create\"]" }]
}
```

### Per-step requirements

Individual steps can declare their own requirements:

```json
{
  "type": "guided",
  "content": "Multi-step with per-action validation",
  "steps": [
    {
      "action": "hover",
      "reftarget": ".service-row",
      "requirements": ["exists-reftarget"]
    },
    {
      "action": "button",
      "reftarget": "button.action-btn",
      "requirements": ["exists-reftarget"]
    }
  ]
}
```

### Lazy targets and current runtime support

Guided actions scroll an existing target into view before asking the learner to interact. They do not currently discover targets that are absent from the DOM until scrolling. Although the step schema accepts `lazyRender` and `scrollContainer`, the guided parser does not forward them, and the guided handler retries element lookup without progressive scrolling.

For automatic discovery, use a standalone `interactive` block:

```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "[data-testid='collector-status-summary']",
  "requirements": ["exists-reftarget"],
  "lazyRender": true,
  "scrollContainer": "#pageContent",
  "doIt": false,
  "content": "Read the collector status summary."
}
```

The individual **Show me** / **Do it** handlers perform discovery, including when the block is inside a section. `exists-reftarget` does not prevent their buttons from running when lazy discovery is available. Use `doIt: false` for read-only observations; **Show me** highlights and completes the observation without requiring a manual hover.

Verify the scrolling container for the target layout. Grafana's `#pageContent` has scrolling enabled when its extension sidebar is open. An inner virtualized list may have a different container; scrolling does not switch pagination pages. The current discovery helper scrolls forward from the current position, so it does not guarantee finding an unmounted target above it.

**Do section** follows a separate path: it does not forward lazy-scroll properties or call the standalone discovery wrapper. It also does not preserve `doIt: false` in its step registry, so individual observation behavior must not be described as a guarantee about bulk execution. Guided blocks pause bulk execution for the learner. Keep page/permission prerequisites on the guided block itself; internal guided action requirements are not evaluated by the current handler.

These limitations were checked against [Pathfinder commit 339cd31d](https://github.com/grafana/grafana-pathfinder-app/tree/339cd31d95c636b82b66f27e3496eb1f49aa0fa4) on 22 September 2026:

- `src/docs-retrieval/json-parser.ts`: `convertInteractiveBlock` forwards lazy properties; `convertGuidedBlock` does not.
- `src/components/interactive-tutorial/interactive-step.tsx`: `lazyScrollAvailable` enables individual actions and `executeWithLazyScroll` runs discovery.
- `src/interactive-engine/action-handlers/guided-handler.ts`: target lookup retries, followed by scrolling an existing element into view.
- `src/components/interactive-tutorial/step-type-registry.ts` and `interactive-section.tsx`: bulk execution bypasses the individual action wrapper.

Recheck these paths when the runtime changes. Prefer the supported automatic action over a manual fallback when its target and container are known.

## Integration with sections

Guided blocks integrate seamlessly with sections. When a section's "Do section" execution reaches a guided block:

1. Section **pauses** before the guided step
2. User manually clicks the guided step's "Start guided interaction" button
3. User **performs** each action as highlighted
4. Step **completes** when all actions are done
5. User clicks **Resume** to continue with remaining automated steps

### Mixed automation and guided

```json
{
  "type": "section",
  "title": "RCA Workbench investigation",
  "blocks": [
    {
      "type": "interactive",
      "action": "button",
      "reftarget": "Clear",
      "content": "Clear previous entries"
    },
    {
      "type": "interactive",
      "action": "formfill",
      "reftarget": "input[data-testid=\"search\"]",
      "targetvalue": "adaptive-logs-api",
      "content": "Search for service"
    },
    {
      "type": "guided",
      "content": "Manually inspect service (hover reveals buttons)",
      "steps": [
        {
          "action": "hover",
          "reftarget": "div[data-cy=\"wb-list-item\"]:contains(\"adaptive-logs-api\")",
          "description": "Hover over the service row to reveal action buttons"
        },
        {
          "action": "button",
          "reftarget": "Dashboard",
          "description": "Click the Dashboard button"
        }
      ]
    },
    {
      "type": "interactive",
      "action": "button",
      "reftarget": "Dashboard",
      "content": "Open dashboard view"
    }
  ]
}
```

**Execution flow:**

1. User clicks "Do section (4 steps)"
2. Steps 1-2 execute automatically
3. Section pauses at step 3 (guided)
4. User manually starts the guided interaction
5. User performs hover and click as guided
6. Guided step completes
7. User clicks "Resume (1 step)" to finish step 4

## Timeout behavior

When a step times out (default 30 seconds):

- Progress indicator shows "Timed out"
- Error message: "Step X timed out. Click 'Skip' to continue or 'Retry' to try again."
- **Retry**: restarts the current step
- **Skip**: marks step as complete and moves to next (only when `skippable` is `true`)

## Troubleshooting

### Guided step will not start

The "Start guided interaction" button is disabled.

1. Check that requirements are met
2. Verify target elements exist using browser DevTools
3. Check selector syntax

### Step times out immediately

Element is not visible, selector does not match, or element is in a closed menu.

1. Add `"requirements": ["exists-reftarget"]` to validate target presence
2. Use "Show me" mode first to verify the selector
3. Add navigation requirements if needed (e.g., `"on-page:/dashboards"`)

### Click detection not working

User clicks but the step does not complete.

- Ensure the click is inside the highlighted element boundary
- Check the element is not disabled or covered by `pointer-events: none`
- Verify z-index stacking does not block clicks

### Section does not resume after guided

After completing the guided step, the "Resume" button does not appear.

1. Ensure the guided block is inside a `section` block
2. Verify section's step index advanced past the guided step

## Technical details

### Event detection

- **Hover**: listens for `mouseenter` + 500 ms dwell time (prevents accidental hovers)
- **Click**: listens for `click` event with `capture: true` for reliability
- **Timeout**: configurable per step via `stepTimeout`, defaults to 30000 ms

### No full-page blocking

Unlike automated steps, guided interactions do not block the page. Users can interact with highlighted elements, scroll for context, or cancel (timeout still applies).

### Limitations

- **Navigate actions**: incompatible with guided model (user would leave the page)
- **Popout actions**: not supported in guided mode — single-button action with no user interaction to detect
- **Nested guided**: guided steps inside guided steps are not supported

---

## See Also

- [JSON Guide Reference](json-guide-reference.md) - Block types, properties, and guide structure
- [Interactive Actions](interactive-actions.md) - Action type behavior
- [Requirements Reference](requirements-reference.md) - All supported requirements
- [Selectors Reference](selectors-and-testids.md) - Stable selector patterns
