### Interactive types

This guide explains the supported interactive types, when to use each, what `data-reftarget` expects, and how Show vs Do behaves.

## Concepts

- **Show vs Do**: Every action runs in two modes. Show highlights the target without changing state; Do performs the action (click, fill, navigate) and marks the step completed.
- **Targets**: Depending on the action, `data-reftarget` is either a CSS selector, button text, a URL/path, or a section container selector.

## Types

### highlight

- **Purpose**: Focus and (on Do) click a specific element by CSS selector.
- **reftarget**: CSS selector.
- **Show**: Ensures visibility and highlights.
- **Do**: Ensures visibility then clicks.
- **Use when**: The target element is reliably selectable via a CSS selector (often `data-testid`-based).

```html
<li
  class="interactive"
  data-targetaction="highlight"
  data-reftarget="a[data-testid='data-testid Nav menu item'][href='/dashboards']"
>
  Open Dashboards
</li>
```

### button

- **Purpose**: Interact with buttons by their visible text.
- **reftarget**: Button text (exact match preferred; partial supported but less stable).
- **Show**: Highlights matching buttons.
- **Do**: Clicks matching buttons.
- **Use when**: The button text is stable; avoids brittle CSS.

```html
<li class="interactive" data-targetaction="button" data-reftarget="Save & test">Save the data source</li>
```

### formfill

- **Purpose**: Fill inputs, textareas (including Monaco), selects, and ARIA comboboxes.
- **reftarget**: CSS selector for the input element.
- **targetvalue**: String to set.
- **Show**: Highlights the field.
- **Do**: Sets the value and fires the right events; ARIA comboboxes are handled token-by-token; Monaco editors use enhanced events.
- **Use when**: Setting values in fields or editors.

```html
<li
  class="interactive"
  data-targetaction="formfill"
  data-reftarget="input[id='connection-url']"
  data-targetvalue="http://prometheus:9090"
>
  Set URL
</li>
```

### navigate

- **Purpose**: Navigate to a Grafana route or external URL.
- **reftarget**: Internal path (e.g. `/dashboard/new`) or absolute URL.
- **Show**: Indicates the intent to navigate.
- **Do**: Uses Grafana `locationService.push` for internal paths; opens new tab for external URLs.
- **Use when**: The interaction is pure navigation.

```html
<li class="interactive" data-targetaction="navigate" data-reftarget="/dashboard/new">Create dashboard</li>
```

### sequence

- **Purpose**: Group and run a list of steps inside a container.
- **reftarget**: Container selector (typically the section `<span>` with an `id`).
- **Behavior**: Show highlights each step; Do performs each step with timing and completion management.
- **Use when**: Teaching a linear set of steps as a single section with “Do Section”.

```html
<span id="setup-datasource" class="interactive" data-targetaction="sequence" data-reftarget="span#setup-datasource">
  <ul>
    <li class="interactive" data-targetaction="highlight" data-reftarget="a[href='/connections']">Open Connections</li>
    <li
      class="interactive"
      data-targetaction="formfill"
      data-reftarget="input[id='basic-settings-name']"
      data-targetvalue="prometheus-datasource"
    >
      Name it
    </li>
  </ul>
</span>
```

### multistep

- **Purpose**: A single "step" that internally performs multiple actions in order.
- **Definition**: A `<li class="interactive" data-targetaction="multistep">` with internal `<span class="interactive" ...>` actions.
- **Behavior**: Handles its own Show/Do timing and requirement checks per internal action.
- **Use when**: A user-facing instruction bundles multiple micro-actions that should run as one.

```html
<li class="interactive" data-targetaction="multistep">
  <span class="interactive" data-targetaction="button" data-reftarget="Add visualization"></span>
  <span class="interactive" data-targetaction="button" data-reftarget="prometheus-datasource"></span>
  Click Add visualization, then pick the data source.
</li>
```

### guided

- **Purpose**: A middle ground between automated "Do it" actions and manual user execution. The system highlights elements and displays instructions, then **waits for the user to manually perform the action** before proceeding.
- **Definition**: A `<li class="interactive" data-targetaction="guided">` with internal `<span class="interactive" ...>` actions that define the sequence.
- **Behavior**: Highlights each action step and waits for user to complete it manually (hover for 500ms, or click). Each internal action can have an `<span class="interactive-comment">` child that appears as a tooltip.
- **Supported actions**: `hover`, `button`, `highlight` (formfill and navigate not supported)
- **Use when**: Actions depend on CSS `:hover` states that can't be programmatically triggered, or you want users to learn by doing rather than watching automation.
- **Options**:
  - `data-step-timeout`: How long to wait for user action before showing skip option (default: 30000ms)
  - `data-skippable`: Whether users can skip the guided interaction (default: false)

```html
<li class="interactive"
    data-targetaction="guided"
    data-step-timeout="45000"
    data-skippable="true">
  <span class="interactive" 
        data-targetaction="hover"
        data-reftarget='.gf-form:has([data-testid="data-testid prometheus type"]) label > svg[tabindex="0"]'
        data-requirements="exists-reftarget">
    <span class="interactive-comment">
      The <strong>Performance</strong> section contains advanced settings. Hovering over the information icon reveals detailed explanations.
    </span>
  </span>
  <span class="interactive"
        data-targetaction="highlight"
        data-reftarget='[data-testid="data-testid prometheus type"]'>
    <span class="interactive-comment">
      The <strong>Prometheus type</strong> dropdown lets you specify whether you're connecting to a standard Prometheus server or a compatible service.
    </span>
  </span>
  <span class="interactive"
        data-targetaction="button"
        data-reftarget="Save & test">
    <span class="interactive-comment">
      Click <strong>Save & test</strong> to create your data source and verify the connection is working.
    </span>
  </span>
  
  Explore Prometheus configuration settings and save your data source.
</li>
```

**Key differences from multistep**:
- **Multistep**: System performs all actions automatically
- **Guided**: System highlights and waits for user to perform actions manually
- **Hover support**: Real hover (triggers CSS `:hover` states), not simulated
- **Learning**: Users learn by doing rather than watching automation

## Choosing the right type

- **Click by CSS selector**: highlight
- **Click by button text**: button
- **Enter text/select values**: formfill
- **Route change**: navigate
- **Teach a linear section**: sequence
- **Bundle micro-steps into one**: multistep
- **User manual interaction with highlights**: guided
