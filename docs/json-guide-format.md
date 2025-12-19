# JSON Guide Format Reference

This document provides a comprehensive reference for the JSON guide format used to create interactive tutorials.

## Overview

JSON guides are structured documents that combine content blocks (markdown, images, video) with interactive elements (highlight, button clicks, form fills) to create guided learning experiences.

## Root Structure

Every JSON guide has three required fields and one optional field:

```json
{
  "id": "my-guide-id",
  "title": "My Guide Title",
  "blocks": [],
  "match": {
    "urlPrefix": ["/dashboards"],
    "tags": ["beginner", "dashboards"]
  }
}
```

| Field    | Type        | Required | Description                             |
|----------|-------------|----------|-----------------------------------------|
| `id`     | string      | ✅       | Unique identifier for the guide         |
| `title`  | string      | ✅       | Display title shown in the UI           |
| `blocks` | JsonBlock[] | ✅       | Array of content and interactive blocks |
| `match`  | object      | ❌       | Metadata for recommendation matching    |

## Block Types Overview

### Content Blocks

| Block Type | Description | Key Properties |
|------------|-------------|----------------|
| `markdown` | Formatted text with headings, lists, code, tables | `content` |
| `image`    | Embedded images | `src`, `alt`, `width`, `height` |
| `video`    | YouTube or native HTML5 video | `src`, `provider`, `title` |

### Interactive Blocks

| Block Type    | Description | Key Properties |
|---------------|-------------|----------------|
| `interactive` | Single-action step (highlight, button, formfill, navigate, hover) | `action`, `reftarget`, `content` |
| `multistep`   | Automated sequence of actions | `content`, `steps` |
| `guided`      | User-performed sequence with detection | `content`, `steps`, `stepTimeout` |

### Structural Blocks

| Block Type    | Description | Key Properties |
|---------------|-------------|----------------|
| `section`     | Container for grouped steps with "Do Section" | `id`, `title`, `blocks` |
| `conditional` | Shows different content based on conditions | `conditions`, `whenTrue`, `whenFalse` |
| `assistant`   | Wraps blocks with AI customization | `assistantType`, `blocks` |

### Assessment Blocks

| Block Type | Description | Key Properties |
|------------|-------------|----------------|
| `quiz`     | Knowledge check with choices | `question`, `choices`, `multiSelect` |
| `input`    | Collects user responses as variables | `prompt`, `inputType`, `variableName` |

---

## Content Blocks

### Markdown Block

The primary block type for formatted text content.

````json
{
  "type": "markdown",
  "content": "# Heading\n\nParagraph with **bold** and *italic* text.\n\n- List item 1\n- List item 2\n\n```promql\nrate(http_requests_total[5m])\n```"
}
````

**Supported Markdown Features:**
- Headings (`#`, `##`, `###`, etc.)
- Bold (`**text**`) and italic (`*text*`)
- Inline code (`` `code` ``)
- Fenced code blocks with syntax highlighting
- Links (`[text](url)`)
- Unordered lists (`-` or `*`)
- Ordered lists (`1.`, `2.`, etc.)
- Tables

### Image Block

```json
{
  "type": "image",
  "src": "https://example.com/image.png",
  "alt": "Description for accessibility",
  "width": 400,
  "height": 300
}
```

| Field    | Type   | Required | Description                |
|----------|--------|----------|----------------------------|
| `src`    | string | ✅       | Image URL                  |
| `alt`    | string | ❌       | Alt text for accessibility |
| `width`  | number | ❌       | Display width in pixels    |
| `height` | number | ❌       | Display height in pixels   |

### Video Block

```json
{
  "type": "video",
  "src": "https://www.youtube.com/embed/VIDEO_ID",
  "provider": "youtube",
  "title": "Video Title"
}
```

| Field      | Type                      | Required | Description                           |
|------------|---------------------------|----------|---------------------------------------|
| `src`      | string                    | ✅       | Video URL (embed URL for YouTube)     |
| `provider` | `"youtube"` \| `"native"` | ❌       | Video provider (default: `"youtube"`) |
| `title`    | string                    | ❌       | Video title for accessibility         |

---

## Interactive Blocks

### Interactive Block (Single Action)

A single interactive step with "Show me" and "Do it" buttons.

```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "a[data-testid='data-testid Nav menu item'][href='/dashboards']",
  "content": "Click on **Dashboards** to view your dashboards.",
  "tooltip": "The Dashboards section shows all your visualization panels.",
  "requirements": ["navmenu-open"],
  "objectives": ["visited-dashboards"],
  "skippable": true,
  "hint": "Open the navigation menu first"
}
```

| Field           | Type     | Required | Default | Description                                              |
|-----------------|----------|----------|---------|----------------------------------------------------------|
| `action`        | string   | ✅       | —       | Action type (see below)                                  |
| `reftarget`     | string   | ✅       | —       | CSS selector or button text                              |
| `content`       | string   | ✅       | —       | Markdown description shown to user                       |
| `targetvalue`   | string   | ❌       | —       | Value for `formfill` actions                             |
| `tooltip`       | string   | ❌       | —       | Tooltip shown on highlight (supports markdown)           |
| `requirements`  | string[] | ❌       | —       | Conditions that must be met                              |
| `objectives`    | string[] | ❌       | —       | Objectives marked complete after this step               |
| `skippable`     | boolean  | ❌       | `false` | Allow skipping if requirements fail                      |
| `hint`          | string   | ❌       | —       | Hint shown when step cannot be completed                 |
| `formHint`      | string   | ❌       | —       | Hint shown when form validation fails                    |
| `validateInput` | boolean  | ❌       | `false` | Require input to match `targetvalue` pattern             |
| `showMe`        | boolean  | ❌       | `true`  | Show the "Show me" button                                |
| `doIt`          | boolean  | ❌       | `true`  | Show the "Do it" button                                  |
| `completeEarly` | boolean  | ❌       | `false` | Mark step complete BEFORE action executes                |
| `verify`        | string   | ❌       | —       | Post-action verification (e.g., `"on-page:/path"`)       |

**Action Types:**

| Action      | Description          | `reftarget`             | `targetvalue` |
|-------------|----------------------|-------------------------|---------------|
| `highlight` | Highlight and click  | CSS selector            | —             |
| `button`    | Click a button       | Button text             | —             |
| `formfill`  | Enter text in input  | CSS selector            | Text to enter |
| `navigate`  | Navigate to URL      | URL path                | —             |
| `hover`     | Hover over element   | CSS selector            | —             |

### Section Block

Groups related interactive steps into a sequence with "Do Section" functionality.

```json
{
  "type": "section",
  "id": "explore-tour",
  "title": "Explore the Interface",
  "requirements": ["is-logged-in"],
  "objectives": ["completed-tour"],
  "blocks": [
    {
      "type": "interactive",
      "action": "highlight",
      "reftarget": "...",
      "content": "First step..."
    },
    {
      "type": "interactive",
      "action": "highlight",
      "reftarget": "...",
      "content": "Second step..."
    }
  ]
}
```

| Field          | Type        | Required | Description                         |
|----------------|-------------|----------|-------------------------------------|
| `id`           | string      | ❌       | Unique section identifier           |
| `title`        | string      | ❌       | Section heading                     |
| `blocks`       | JsonBlock[] | ✅       | Nested blocks (usually interactive) |
| `requirements` | string[]    | ❌       | Section-level requirements          |
| `objectives`   | string[]    | ❌       | Objectives for the entire section   |

### Multistep Block

Executes multiple actions **automatically** when user clicks "Do it".

```json
{
  "type": "multistep",
  "content": "This will automatically navigate to Explore and open the query editor.",
  "requirements": ["navmenu-open"],
  "skippable": true,
  "steps": [
    {
      "action": "button",
      "reftarget": "a[href='/explore']",
      "tooltip": "Navigating to Explore..."
    },
    {
      "action": "highlight",
      "reftarget": "[data-testid='query-editor']",
      "tooltip": "This is the query editor!"
    }
  ]
}
```

| Field          | Type       | Required | Description                       |
|----------------|------------|----------|-----------------------------------|
| `content`      | string     | ✅       | Description shown to user         |
| `steps`        | JsonStep[] | ✅       | Sequence of steps to execute      |
| `requirements` | string[]   | ❌       | Requirements for the entire block |
| `objectives`   | string[]   | ❌       | Objectives tracked                |
| `skippable`    | boolean    | ❌       | Allow skipping                    |

### Guided Block

Highlights elements and **waits for user** to perform actions.

```json
{
  "type": "guided",
  "content": "Follow along by clicking each highlighted element.",
  "stepTimeout": 30000,
  "completeEarly": true,
  "requirements": ["navmenu-open"],
  "steps": [
    {
      "action": "highlight",
      "reftarget": "a[href='/dashboards']",
      "tooltip": "Click Dashboards to continue..."
    },
    {
      "action": "highlight",
      "reftarget": "button[aria-label='New dashboard']",
      "tooltip": "Now click New to create a dashboard"
    }
  ]
}
```

| Field           | Type       | Required | Description                              |
|-----------------|------------|----------|------------------------------------------|
| `content`       | string     | ✅       | Description shown to user                |
| `steps`         | JsonStep[] | ✅       | Sequence of steps for user to perform    |
| `stepTimeout`   | number     | ❌       | Timeout per step in ms (default: 30000)  |
| `completeEarly` | boolean    | ❌       | Complete when user performs action early |
| `requirements`  | string[]   | ❌       | Requirements for the block               |
| `objectives`    | string[]   | ❌       | Objectives tracked                       |
| `skippable`     | boolean    | ❌       | Allow skipping                           |

**Key differences from multistep:**
- **Multistep**: System performs all actions automatically
- **Guided**: System highlights and waits for user to perform actions manually
- **Hover support**: Real hover (triggers CSS `:hover` states), not simulated

### Conditional Block

Shows different content based on runtime condition evaluation.

```json
{
  "type": "conditional",
  "conditions": ["has-datasource:prometheus"],
  "description": "Show Prometheus-specific content or fallback",
  "whenTrue": [
    {
      "type": "markdown",
      "content": "Great! You have Prometheus configured. Let's write some PromQL queries."
    }
  ],
  "whenFalse": [
    {
      "type": "markdown",
      "content": "You'll need to set up a Prometheus data source first."
    },
    {
      "type": "interactive",
      "action": "navigate",
      "reftarget": "/connections/datasources/new",
      "content": "Click here to add a data source."
    }
  ]
}
```

| Field                    | Type                      | Required | Default    | Description                                      |
|--------------------------|---------------------------|----------|------------|--------------------------------------------------|
| `conditions`             | string[]                  | ✅       | —          | Conditions to evaluate (uses requirement syntax) |
| `whenTrue`               | JsonBlock[]               | ✅       | —          | Blocks shown when ALL conditions pass            |
| `whenFalse`              | JsonBlock[]               | ✅       | —          | Blocks shown when ANY condition fails            |
| `description`            | string                    | ❌       | —          | Author note (not shown to users)                 |
| `display`                | `"inline"` \| `"section"` | ❌       | `"inline"` | Display mode for the branch content              |

---

## Assessment Blocks

### Quiz Block

Knowledge assessment with single or multiple choice questions.

```json
{
  "type": "quiz",
  "question": "Which query language does Prometheus use?",
  "completionMode": "correct-only",
  "choices": [
    { "id": "a", "text": "SQL", "hint": "SQL is used by traditional databases." },
    { "id": "b", "text": "PromQL", "correct": true },
    { "id": "c", "text": "GraphQL", "hint": "GraphQL is an API query language." },
    { "id": "d", "text": "LogQL", "hint": "LogQL is for Loki logs." }
  ]
}
```

| Field            | Type         | Required | Default          | Description                                     |
|------------------|--------------|----------|------------------|-------------------------------------------------|
| `question`       | string       | ✅       | —                | Question text (supports markdown)               |
| `choices`        | QuizChoice[] | ✅       | —                | Answer choices                                  |
| `multiSelect`    | boolean      | ❌       | `false`          | Allow multiple answers                          |
| `completionMode` | string       | ❌       | `"correct-only"` | `"correct-only"` or `"max-attempts"`            |
| `maxAttempts`    | number       | ❌       | `3`              | Attempts before revealing answer                |
| `requirements`   | string[]     | ❌       | —                | Requirements for this quiz                      |
| `skippable`      | boolean      | ❌       | `false`          | Allow skipping                                  |

### Input Block

Collects user responses that can be stored as variables.

```json
{
  "type": "input",
  "prompt": "What is the name of your Prometheus data source?",
  "inputType": "text",
  "variableName": "prometheusName",
  "placeholder": "e.g., prometheus-main",
  "required": true,
  "pattern": "^[a-zA-Z][a-zA-Z0-9-]*$",
  "validationMessage": "Name must start with a letter"
}
```

| Field               | Type                    | Required | Default | Description                                    |
|---------------------|-------------------------|----------|---------|------------------------------------------------|
| `prompt`            | string                  | ✅       | —       | Question shown to user (supports markdown)     |
| `inputType`         | `"text"` \| `"boolean"` | ✅       | —       | Input type: text field or checkbox             |
| `variableName`      | string                  | ✅       | —       | Identifier for storing the response            |
| `placeholder`       | string                  | ❌       | —       | Placeholder text for text input                |
| `checkboxLabel`     | string                  | ❌       | —       | Label for boolean checkbox                     |
| `defaultValue`      | string \| boolean       | ❌       | —       | Default value for the input                    |
| `required`          | boolean                 | ❌       | `false` | Whether a response is required                 |
| `pattern`           | string                  | ❌       | —       | Regex pattern for text validation              |
| `validationMessage` | string                  | ❌       | —       | Message shown when validation fails            |

---

## Variable Substitution

Variables collected by Input blocks can be used throughout the guide:

### In Content

Use `{{variableName}}` syntax:

```json
{
  "type": "markdown",
  "content": "Your data source **{{datasourceName}}** is configured."
}
```

### In Requirements

Use the `var-` prefix:

```json
{
  "type": "section",
  "title": "Advanced configuration",
  "requirements": ["var-termsAccepted:true"],
  "blocks": []
}
```

---

## Step Structure

Steps used in `multistep` and `guided` blocks share this structure:

```json
{
  "action": "highlight",
  "reftarget": "selector",
  "targetvalue": "value for formfill",
  "requirements": ["step-requirement"],
  "tooltip": "Tooltip shown during execution",
  "skippable": true,
  "formHint": "Hint for formfill validation",
  "validateInput": false
}
```

| Field           | Type     | Required | Default | Description                                     |
|-----------------|----------|----------|---------|-------------------------------------------------|
| `action`        | string   | ✅       | —       | Action type: `highlight`, `button`, `formfill`, `navigate`, `hover` |
| `reftarget`     | string   | ✅       | —       | CSS selector or button text                     |
| `targetvalue`   | string   | ❌       | —       | Value for `formfill` actions                    |
| `requirements`  | string[] | ❌       | —       | Requirements for this specific step             |
| `tooltip`       | string   | ❌       | —       | Tooltip shown during execution                  |
| `skippable`     | boolean  | ❌       | `false` | Whether this step can be skipped                |

---

## Complete Example

```json
{
  "id": "dashboard-basics",
  "title": "Dashboard Basics",
  "blocks": [
    {
      "type": "markdown",
      "content": "# Getting Started with Dashboards\n\nIn this guide, you'll learn how to navigate to the dashboards section."
    },
    {
      "type": "section",
      "id": "navigation",
      "title": "Navigate to Dashboards",
      "blocks": [
        {
          "type": "interactive",
          "action": "highlight",
          "reftarget": "a[data-testid='data-testid Nav menu item'][href='/dashboards']",
          "requirements": ["navmenu-open"],
          "content": "First, let's find the **Dashboards** section.",
          "tooltip": "Dashboards contain your visualizations and panels."
        },
        {
          "type": "interactive",
          "action": "button",
          "reftarget": "New",
          "requirements": ["on-page:/dashboards", "exists-reftarget"],
          "skippable": true,
          "content": "Click **New** to start creating a dashboard."
        }
      ]
    },
    {
      "type": "markdown",
      "content": "## Congratulations!\n\nYou've learned the basics of dashboard navigation."
    }
  ]
}
```

---

## See Also

- [Interactive Types Reference](interactive-types.md) - Detailed documentation of all interactive actions
- [JSON Block Properties](json-block-properties.md) - Complete property reference
- [Requirements Reference](requirements-reference.md) - All supported requirements
- [Selectors Reference](selectors-and-testids.md) - Stable selector patterns

