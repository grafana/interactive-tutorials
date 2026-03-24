# JSON Guide Reference

Complete reference for the JSON guide format — root structure, all block types, properties, and examples.

## Root Structure

Every JSON guide has three required fields:

```json
{
  "id": "my-guide-id",
  "title": "My Guide Title",
  "blocks": []
}
```

| Field    | Type        | Required | Description                             |
|----------|-------------|----------|-----------------------------------------|
| `id`     | string      | ✅       | Unique identifier for the guide         |
| `title`  | string      | ✅       | Display title shown in the UI           |
| `blocks` | JsonBlock[] | ✅       | Array of content and interactive blocks |

---

## Block Quick Reference

| Block Type | Category | Purpose | When to Use |
|------------|----------|---------|-------------|
| `markdown` | Content | Formatted text | Explanations, instructions, section bookends |
| `html` | Content | Raw HTML (use sparingly) | Legacy content, custom rich HTML |
| `image` | Content | Embedded image | Screenshots, diagrams |
| `video` | Content | YouTube or native video | Tutorials, demos |
| `interactive` | Interactive | Single action | Click, fill, navigate, highlight, hover, noop |
| `multistep` | Interactive | Automated multi-action sequence | Bundle micro-steps (automated) |
| `guided` | Interactive | User-performed with detection | User learns by doing, CSS :hover required |
| `section` | Structural | Grouped steps with "Do Section" | Organize related steps |
| `conditional` | Structural | Runtime condition branching | Different content by user state |
| `assistant` | Structural | Wraps blocks with AI customization | Adaptive content via Grafana Assistant |
| `quiz` | Assessment | Knowledge check with choices | Test understanding |
| `input` | Assessment | Collect user response as variable | Dynamic guides |
| `code-block` | Interactive | Insert code into Monaco editor | Queries, configs for code editors |
| `terminal` | Interactive | Shell command with Copy/Exec | Coda terminal commands |
| `terminal-connect` | Interactive | Connect to Coda terminal | Establish terminal session |

---

## Action Types

Actions are used in `interactive`, `multistep`, and `guided` blocks. See [Interactive Actions](interactive-actions.md) for detailed Show vs Do behavior.

| Action | Description | `reftarget` | `targetvalue` |
|--------|-------------|-------------|---------------|
| `highlight` | Highlight and click an element | CSS selector | — |
| `button` | Click a button by text | Button text or selector | — |
| `formfill` | Enter text in input | CSS selector | Text to enter |
| `navigate` | Navigate to URL | URL path | — |
| `hover` | Hover over element | CSS selector | — |
| `noop` | Informational step (no action) | Optional | — |

---

## Content Blocks

### Markdown Block

Formatted text content with headings, bold, italic, code blocks, lists, tables, and links.

````json
{
  "type": "markdown",
  "content": "# Heading\n\nParagraph with **bold** and *italic* text.\n\n```promql\nrate(http_requests_total[5m])\n```"
}
````

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `type` | string | ✅ | Must be `"markdown"` |
| `content` | string | ✅ | Markdown content |

**AI Customization Properties** (also available on `interactive` blocks):

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `assistantEnabled` | boolean | `false` | Enable AI customization button |
| `assistantId` | string | — | Unique ID for persistence |
| `assistantType` | `"query"` \| `"config"` \| `"code"` \| `"text"` | — | Type of content for AI prompts |

### HTML Block

Raw HTML content. Use sparingly — prefer markdown for new content. HTML is sanitized before rendering.

```json
{
  "type": "html",
  "content": "<div class='custom-box'><p>Custom HTML content</p></div>"
}
```

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `type` | string | ✅ | Must be `"html"` |
| `content` | string | ✅ | Raw HTML content (sanitized before rendering) |

### Image Block

Embed images with optional dimensions.

```json
{
  "type": "image",
  "src": "https://example.com/image.png",
  "alt": "Description for accessibility",
  "width": 400,
  "height": 300
}
```

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `type` | string | ✅ | Must be `"image"` |
| `src` | string | ✅ | Image URL |
| `alt` | string | ❌ | Alt text for accessibility |
| `width` | number | ❌ | Display width in pixels |
| `height` | number | ❌ | Display height in pixels |

### Video Block

Embed YouTube or native HTML5 video.

```json
{
  "type": "video",
  "src": "https://www.youtube.com/embed/VIDEO_ID",
  "provider": "youtube",
  "title": "Getting Started with Grafana",
  "start": 10,
  "end": 120
}
```

| Property | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `type` | string | ✅ | — | Must be `"video"` |
| `src` | string | ✅ | — | Video URL (embed URL for YouTube) |
| `provider` | `"youtube"` \| `"native"` | ❌ | `"youtube"` | Video provider |
| `title` | string | ❌ | — | Video title for accessibility |
| `start` | number | ❌ | — | Start time in seconds |
| `end` | number | ❌ | — | End time in seconds |

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

**Core Properties:**

| Property | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `type` | string | ✅ | — | Must be `"interactive"` |
| `action` | string | ✅ | — | Action type: `highlight`, `button`, `formfill`, `navigate`, `hover`, `noop` |
| `reftarget` | string | ✅\* | — | Target reference (\*optional for `noop`) |
| `content` | string | ✅ | — | Markdown description shown to user |
| `targetvalue` | string | ❌ | — | Value for `formfill` actions |
| `tooltip` | string | ❌ | — | Tooltip shown when element is highlighted |
| `requirements` | string[] | ❌ | — | Preconditions that must pass |
| `objectives` | string[] | ❌ | — | Conditions that auto-complete the step when met |
| `hint` | string | ❌ | — | Hint shown when requirements fail |
| `skippable` | boolean | ❌ | `false` | Allow skipping when requirements fail |

**Button Control:**

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `showMe` | boolean | `true` | Show the "Show me" button |
| `doIt` | boolean | `true` | Show the "Do it" button |

| Setting | "Show me" | "Do it" | Use Case |
|---------|-----------|---------|----------|
| Default (both `true`) | ✅ | ✅ | Normal interactive step |
| `doIt: false` | ✅ | ❌ | Educational highlight only |
| `showMe: false` | ❌ | ✅ | Direct action without preview |

**Execution Control:**

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `completeEarly` | boolean | `false` | Mark step complete before action finishes |
| `verify` | string | — | Post-action verification (e.g., `"on-page:/path"`) |

**Formfill-Specific:**

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `validateInput` | boolean | `false` | Require input to match `targetvalue` pattern |
| `formHint` | string | — | Hint shown when form validation fails |

When `validateInput` is `true`, `targetvalue` is treated as a regex if it starts with `^` or `$`, or is enclosed in `/pattern/` syntax.

| `targetvalue` | Matches |
|---------------|---------|
| `prometheus` | Exact string "prometheus" |
| `^https?://` | Strings starting with http:// or https:// |
| `/^[a-z]+$/` | Lowercase letters only |

**Rendering Properties:**

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `lazyRender` | boolean | `false` | Enable progressive scroll discovery for virtualized containers |
| `scrollContainer` | string | `".scrollbar-view"` | CSS selector for the scroll container when `lazyRender` is enabled |

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
    { "type": "interactive", "action": "highlight", "reftarget": "...", "content": "First step..." },
    { "type": "interactive", "action": "highlight", "reftarget": "...", "content": "Second step..." }
  ]
}
```

| Property | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `type` | string | ✅ | — | Must be `"section"` |
| `blocks` | JsonBlock[] | ✅ | — | Array of child blocks |
| `id` | string | ❌ | — | Unique identifier for section |
| `title` | string | ❌ | — | Section heading |
| `requirements` | string[] | ❌ | — | Section-level requirements |
| `objectives` | string[] | ❌ | — | Auto-complete entire section when met |
| `autoCollapse` | boolean | ❌ | `true` | Collapse section when completed |

### Conditional Block

Shows different content based on runtime condition evaluation. Conditions use requirement syntax; when ALL pass, `whenTrue` is shown; otherwise `whenFalse`.

```json
{
  "type": "conditional",
  "conditions": ["has-datasource:prometheus"],
  "description": "Show Prometheus-specific content or fallback",
  "display": "section",
  "whenTrueSectionConfig": { "title": "Query your data", "objectives": ["queried-data"] },
  "whenTrue": [{ "type": "markdown", "content": "Great! You have Prometheus configured." }],
  "whenFalse": [{ "type": "markdown", "content": "You'll need to set up a Prometheus data source first." }]
}
```

| Property | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `type` | string | ✅ | — | Must be `"conditional"` |
| `conditions` | string[] | ✅ | — | Conditions to evaluate (requirement syntax) |
| `whenTrue` | JsonBlock[] | ✅ | — | Blocks shown when ALL conditions pass |
| `whenFalse` | JsonBlock[] | ✅ | — | Blocks shown when ANY condition fails |
| `description` | string | ❌ | — | Author note (not shown to users) |
| `reftarget` | string | ❌ | — | CSS selector for `exists-reftarget` auto-check |
| `display` | `"inline"` \| `"section"` | ❌ | `"inline"` | Display mode for branch content |
| `whenTrueSectionConfig` | object | ❌ | — | Section config for pass branch (when display is section) |
| `whenFalseSectionConfig` | object | ❌ | — | Section config for fail branch (when display is section) |

**ConditionalSectionConfig:** `{ title?: string, requirements?: string[], objectives?: string[] }`

### Multistep Block

Executes multiple actions **automatically** when user clicks "Do it".

```json
{
  "type": "multistep",
  "content": "Navigate to Explore and open the query editor.",
  "requirements": ["navmenu-open"],
  "steps": [
    { "action": "button", "reftarget": "a[href='/explore']", "tooltip": "Navigating to Explore..." },
    { "action": "highlight", "reftarget": "[data-testid='query-editor']", "tooltip": "This is the query editor!" }
  ]
}
```

| Property | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `type` | string | ✅ | — | Must be `"multistep"` |
| `content` | string | ✅ | — | Description shown to user |
| `steps` | JsonStep[] | ✅ | — | Sequence of steps to execute |
| `requirements` | string[] | ❌ | — | Requirements for the entire block |
| `objectives` | string[] | ❌ | — | Objectives tracked |
| `skippable` | boolean | ❌ | `false` | Allow skipping |

### Guided Block

Highlights elements and **waits for user** to perform actions. See [Guided Interactions](guided-interactions.md) for detailed documentation.

```json
{
  "type": "guided",
  "content": "Explore Prometheus configuration settings and save your data source.",
  "stepTimeout": 45000,
  "skippable": true,
  "steps": [
    { "action": "hover", "reftarget": ".gf-form:has([data-testid='prometheus-type']) label > svg", "tooltip": "The **Performance** section contains advanced settings." },
    { "action": "button", "reftarget": "Save & test", "tooltip": "Click **Save & test** to create your data source." }
  ]
}
```

| Property | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `type` | string | ✅ | — | Must be `"guided"` |
| `content` | string | ✅ | — | Description shown to user |
| `steps` | JsonStep[] | ✅ | — | Steps for user to perform |
| `stepTimeout` | number | ❌ | `30000` | Timeout per step in milliseconds |
| `completeEarly` | boolean | ❌ | `false` | Complete when user performs action early |
| `requirements` | string[] | ❌ | — | Requirements for the block |
| `objectives` | string[] | ❌ | — | Objectives tracked |
| `skippable` | boolean | ❌ | `false` | Allow skipping |

**Supported guided actions:** `hover`, `button`, `highlight` (formfill and navigate not supported).

**Key differences from multistep:**
- **Multistep**: System performs all actions automatically
- **Guided**: System highlights and waits for user to perform actions manually
- **Hover support**: Real hover (triggers CSS `:hover` states), not simulated

### Assistant Block

Wraps child blocks with AI-powered customization. Each child block gets a "Customize" button via Grafana Assistant.

````json
{
  "type": "assistant",
  "assistantId": "prom-queries",
  "assistantType": "query",
  "blocks": [
    { "type": "markdown", "content": "Sample query:\n\n```promql\nrate(http_requests_total[5m])\n```" },
    { "type": "interactive", "action": "formfill", "reftarget": "textarea[data-testid='query-editor']", "targetvalue": "rate(http_requests_total[5m])", "content": "Enter this query." }
  ]
}
````

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `type` | string | ✅ | Must be `"assistant"` |
| `blocks` | JsonBlock[] | ✅ | Child blocks to wrap |
| `assistantId` | string | ❌ | Unique ID prefix (auto-generated if omitted) |
| `assistantType` | `"query"` \| `"config"` \| `"code"` \| `"text"` | ❌ | Type of content for AI behavior |

Instead of a wrapper block, you can enable AI customization directly on `markdown` and `interactive` blocks using the `assistantEnabled`, `assistantId`, and `assistantType` properties (see [Markdown Block](#markdown-block)).

---

## Code and Terminal Blocks

### Code Block

Inserts syntax-highlighted code into a Monaco editor. "Show me" highlights the target editor; "Insert" clears and inserts the code.

```json
{
  "type": "code-block",
  "reftarget": "textarea[data-testid='query-editor']",
  "code": "rate(http_requests_total[5m])",
  "language": "promql",
  "content": "Insert this PromQL query to calculate the per-second rate of HTTP requests."
}
```

| Property | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `type` | string | ✅ | — | Must be `"code-block"` |
| `reftarget` | string | ✅ | — | CSS selector for the target Monaco editor container |
| `code` | string | ✅ | — | The code to display and insert |
| `language` | string | ❌ | — | Language for syntax highlighting (e.g., `"promql"`, `"yaml"`) |
| `content` | string | ❌ | — | Markdown description shown above the code block |
| `requirements` | string[] | ❌ | — | Requirements that must be met |
| `objectives` | string[] | ❌ | — | Objectives tracked for this step |
| `skippable` | boolean | ❌ | `false` | Allow skipping when requirements fail |
| `hint` | string | ❌ | — | Hint shown when step cannot be completed |

**When to use code-block vs formfill:** Use `code-block` for Monaco editors — it clears existing content, inserts code properly, and shows a syntax-highlighted preview. Use `formfill` for standard input/textarea fields.

### Terminal Block

Displays a shell command with Copy and Exec buttons. Requires a connected Coda terminal session.

```json
{
  "type": "terminal",
  "command": "curl -s http://localhost:9090/api/v1/status/config | jq .",
  "content": "Check that Prometheus is running and inspect its configuration.",
  "requirements": ["is-terminal-active"]
}
```

| Property | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `type` | string | ✅ | — | Must be `"terminal"` |
| `command` | string | ✅ | — | Shell command to display and execute |
| `content` | string | ✅ | — | Markdown description shown to the user |
| `requirements` | string[] | ❌ | — | Requirements that must be met |
| `objectives` | string[] | ❌ | — | Objectives tracked for this step |
| `skippable` | boolean | ❌ | `false` | Allow skipping when requirements fail |
| `hint` | string | ❌ | — | Hint shown when step cannot be completed |

### Terminal Connect Block

Renders a button that opens and connects to a Coda terminal session. Place before `terminal` blocks so the user has a connected session.

```json
{
  "type": "terminal-connect",
  "content": "Start a terminal session to follow along with the commands in this guide.",
  "buttonText": "Open terminal",
  "vmTemplate": "vm-aws"
}
```

| Property | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `type` | string | ✅ | — | Must be `"terminal-connect"` |
| `content` | string | ✅ | — | Markdown description shown above the button |
| `buttonText` | string | ❌ | `"Try in terminal"` | Custom button text |
| `vmTemplate` | string | ❌ | `"vm-aws"` | VM template: `"vm-aws"`, `"vm-aws-sample-app"`, or `"vm-aws-alloy-scenario"` |
| `vmApp` | string | ❌ | — | App name for sample-app template (e.g., `"nginx"`, `"mysql"`) |
| `vmScenario` | string | ❌ | — | Scenario name for alloy-scenario template |

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
    { "id": "a", "text": "SQL", "hint": "SQL is for traditional databases." },
    { "id": "b", "text": "PromQL", "correct": true },
    { "id": "c", "text": "GraphQL", "hint": "GraphQL is an API query language." }
  ]
}
```

| Property | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `type` | string | ✅ | — | Must be `"quiz"` |
| `question` | string | ✅ | — | Question text (supports markdown) |
| `choices` | QuizChoice[] | ✅ | — | Answer choices |
| `multiSelect` | boolean | ❌ | `false` | Allow multiple answers (checkboxes) |
| `completionMode` | string | ❌ | `"correct-only"` | `"correct-only"` or `"max-attempts"` |
| `maxAttempts` | number | ❌ | `3` | Attempts before revealing (max-attempts mode) |
| `requirements` | string[] | ❌ | — | Requirements for this quiz |
| `skippable` | boolean | ❌ | `false` | Allow skipping |

**Choice Properties:** `id` (string, required), `text` (string, required), `correct` (boolean), `hint` (string — shown when this wrong choice is selected).

### Input Block

Collects user responses stored as variables. Variables can be referenced with `{{variableName}}` in content or `var-name:value` in requirements.

```json
{
  "type": "input",
  "prompt": "What is the name of your Prometheus data source?",
  "inputType": "text",
  "variableName": "prometheusName",
  "placeholder": "e.g., prometheus-main",
  "required": true,
  "pattern": "^[a-zA-Z][a-zA-Z0-9-]*$",
  "validationMessage": "Name must start with a letter and contain only letters, numbers, and dashes"
}
```

| Property | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `type` | string | ✅ | — | Must be `"input"` |
| `prompt` | string | ✅ | — | Question/instruction (supports markdown) |
| `inputType` | `"text"` \| `"boolean"` \| `"datasource"` | ✅ | — | Input type |
| `variableName` | string | ✅ | — | Identifier for storing response |
| `placeholder` | string | ❌ | — | Placeholder text (text input only) |
| `checkboxLabel` | string | ❌ | — | Label for checkbox (boolean only) |
| `defaultValue` | string \| boolean | ❌ | — | Default value |
| `required` | boolean | ❌ | `false` | Require response to proceed |
| `pattern` | string | ❌ | — | Regex pattern for validation |
| `validationMessage` | string | ❌ | — | Message when validation fails |
| `datasourceFilter` | string | ❌ | — | Filter datasources by type (e.g., `"prometheus"`). Only for `"datasource"` inputType |
| `requirements` | string[] | ❌ | — | Requirements for this input |
| `skippable` | boolean | ❌ | `false` | Allow skipping |

---

## Step Structure

Steps used in `multistep` and `guided` blocks:

```json
{
  "action": "highlight",
  "reftarget": "selector",
  "targetvalue": "value for formfill",
  "tooltip": "Tooltip during multistep execution",
  "description": "Description in guided steps panel"
}
```

| Property | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `action` | string | ✅ | — | Action type: `highlight`, `button`, `formfill`, `navigate`, `hover`, `noop` |
| `reftarget` | string | ✅\* | — | Target reference (\*optional for `noop`) |
| `targetvalue` | string | ❌ | — | Value for `formfill` actions (supports regex patterns) |
| `requirements` | string[] | ❌ | — | Requirements for this specific step |
| `tooltip` | string | ❌ | — | Tooltip shown during multistep execution |
| `description` | string | ❌ | — | Description shown in guided steps panel |
| `skippable` | boolean | ❌ | `false` | Whether this step can be skipped (guided only) |
| `formHint` | string | ❌ | — | Hint shown when form validation fails |
| `validateInput` | boolean | ❌ | `false` | Require input to match `targetvalue` pattern |
| `lazyRender` | boolean | ❌ | `false` | Enable progressive scroll discovery |
| `scrollContainer` | string | ❌ | `".scrollbar-view"` | CSS selector for the scroll container |

---

## Variable Substitution

Variables collected by [Input blocks](#input-block) can be used throughout the guide:

**In content** — `{{variableName}}` syntax:

```json
{
  "type": "markdown",
  "content": "Your data source **{{datasourceName}}** is configured at `{{datasourceUrl}}`."
}
```

If the variable is not set, `[not set]` is displayed as a fallback.

**In requirements** — `var-` prefix:

```json
{
  "type": "section",
  "title": "Advanced configuration",
  "requirements": ["var-termsAccepted:true"],
  "blocks": []
}
```

**Syntax:** `var-{variableName}:{expectedValue}`

---

## Common Property Patterns

### Requirements Array

Requirements are specified as string arrays. All must pass for the element to be enabled:

```json
{
  "requirements": ["navmenu-open", "on-page:/dashboards"]
}
```

### Objectives Array

Objectives use the same syntax but auto-complete when met:

```json
{
  "objectives": ["has-datasource:prometheus"]
}
```

If objectives are met, the step is automatically marked complete regardless of requirements.

---

## TypeScript Types

All types are exported from the Pathfinder app's `src/types/json-guide.types.ts`:

```typescript
import {
  // Root structure
  JsonGuide, JsonMatchMetadata,
  // Block union
  JsonBlock,
  // Content blocks
  JsonMarkdownBlock, JsonHtmlBlock, JsonImageBlock, JsonVideoBlock,
  // Structural blocks
  JsonSectionBlock, JsonConditionalBlock, ConditionalDisplayMode,
  ConditionalSectionConfig, JsonAssistantBlock, AssistantProps,
  // Interactive blocks
  JsonInteractiveBlock, JsonMultistepBlock, JsonGuidedBlock,
  JsonInteractiveAction, JsonStep,
  // Assessment blocks
  JsonQuizBlock, JsonQuizChoice, JsonInputBlock,
  // Code and terminal blocks
  JsonCodeBlockBlock, JsonTerminalBlock, JsonTerminalConnectBlock,
} from '../types/json-guide.types';
```

Type guards: `isMarkdownBlock`, `isHtmlBlock`, `isImageBlock`, `isVideoBlock`, `isSectionBlock`, `isConditionalBlock`, `isAssistantBlock`, `isInteractiveBlock`, `isMultistepBlock`, `isGuidedBlock`, `isQuizBlock`, `isInputBlock`, `isCodeBlockBlock`, `isTerminalBlock`, `isTerminalConnectBlock`, `hasAssistantEnabled`.

Zod schemas: `JsonGuideSchema`, `JsonGuideSchemaStrict`, `JsonBlockSchema`, `CURRENT_SCHEMA_VERSION` from `src/types/json-guide.schema.ts`.

---

## Complete Example

```json
{
  "id": "dashboard-basics",
  "title": "Dashboard Basics",
  "blocks": [
    {
      "type": "markdown",
      "content": "In this guide, you'll learn how to navigate to the dashboards section and create your first dashboard."
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
          "content": "Find the **Dashboards** section in the navigation menu.",
          "tooltip": "Dashboards contain your visualizations and panels."
        },
        {
          "type": "interactive",
          "action": "button",
          "reftarget": "New",
          "requirements": ["on-page:/dashboards"],
          "skippable": true,
          "content": "Click **New** to start creating a dashboard."
        }
      ]
    },
    {
      "type": "markdown",
      "content": "You've learned the basics of dashboard navigation. Next, try adding panels to your dashboard."
    }
  ]
}
```

---

## See Also

- [Interactive Actions](interactive-actions.md) - Show vs Do behavior for each action type
- [Requirements Reference](requirements-reference.md) - All supported requirements
- [Selectors Reference](selectors-and-testids.md) - Stable selector patterns
- [Guided Interactions](guided-interactions.md) - Detailed guided block documentation
- [Manifest Reference](manifest-reference.md) - Package metadata
