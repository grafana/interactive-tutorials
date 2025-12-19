# JSON Block Properties Reference

This guide documents all properties for each block type in the JSON guide format.

## Interactive Block Properties

The `interactive` block is used for single-action steps.

```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "selector",
  "content": "Description"
}
```

### Core Properties

| Property        | Type     | Required | Default | Description                                              |
|-----------------|----------|----------|---------|----------------------------------------------------------|
| `type`          | string   | ✅       | —       | Must be `"interactive"`                                  |
| `action`        | string   | ✅       | —       | Action type: `highlight`, `button`, `formfill`, `navigate`, `hover` |
| `reftarget`     | string   | ✅       | —       | Target reference (CSS selector, button text, or URL)     |
| `content`       | string   | ✅       | —       | User-visible description (supports markdown)             |

### Optional Properties

| Property        | Type     | Default | Description                                              |
|-----------------|----------|---------|----------------------------------------------------------|
| `targetvalue`   | string   | —       | Value for `formfill` actions                             |
| `tooltip`       | string   | —       | Tooltip shown when element is highlighted                |
| `requirements`  | string[] | —       | Preconditions that must pass                             |
| `objectives`    | string[] | —       | Conditions that auto-complete the step when met          |
| `hint`          | string   | —       | Hint shown when requirements fail                        |
| `skippable`     | boolean  | `false` | Allow skipping when requirements fail                    |

### Button Control Properties

| Property        | Type     | Default | Description                                              |
|-----------------|----------|---------|----------------------------------------------------------|
| `showMe`        | boolean  | `true`  | Show the "Show me" button                                |
| `doIt`          | boolean  | `true`  | Show the "Do it" button                                  |

### Execution Control Properties

| Property        | Type     | Default | Description                                              |
|-----------------|----------|---------|----------------------------------------------------------|
| `completeEarly` | boolean  | `false` | Mark step complete before action finishes                |
| `verify`        | string   | —       | Post-action verification (e.g., `"on-page:/path"`)       |

### Formfill-Specific Properties

| Property        | Type     | Default | Description                                              |
|-----------------|----------|---------|----------------------------------------------------------|
| `validateInput` | boolean  | `false` | Require input to match `targetvalue` pattern             |
| `formHint`      | string   | —       | Hint shown when form validation fails                    |

**Pattern Matching:**

When `validateInput` is `true`, `targetvalue` is treated as a regex if it starts with `^` or `$`, or is enclosed in `/pattern/` syntax.

| `targetvalue`          | Matches                                   |
|------------------------|-------------------------------------------|
| `prometheus`           | Exact string "prometheus"                 |
| `^https?://`           | Strings starting with http:// or https:// |
| `/^[a-z]+$/`           | Lowercase letters only                    |

---

## Section Block Properties

The `section` block groups steps with "Do Section" functionality.

```json
{
  "type": "section",
  "id": "section-id",
  "title": "Section Title",
  "blocks": []
}
```

| Property        | Type        | Required | Default | Description                                   |
|-----------------|-------------|----------|---------|-----------------------------------------------|
| `type`          | string      | ✅       | —       | Must be `"section"`                           |
| `blocks`        | JsonBlock[] | ✅       | —       | Array of child blocks                         |
| `id`            | string      | ❌       | —       | Unique identifier for section                 |
| `title`         | string      | ❌       | —       | Section heading                               |
| `requirements`  | string[]    | ❌       | —       | Section-level requirements                    |
| `objectives`    | string[]    | ❌       | —       | Auto-complete entire section when met         |

---

## Multistep Block Properties

The `multistep` block executes multiple actions automatically.

```json
{
  "type": "multistep",
  "content": "Description",
  "steps": []
}
```

| Property        | Type       | Required | Default | Description                                   |
|-----------------|------------|----------|---------|-----------------------------------------------|
| `type`          | string     | ✅       | —       | Must be `"multistep"`                         |
| `content`       | string     | ✅       | —       | User-visible description                      |
| `steps`         | JsonStep[] | ✅       | —       | Array of steps to execute                     |
| `requirements`  | string[]   | ❌       | —       | Requirements for the entire block             |
| `objectives`    | string[]   | ❌       | —       | Objectives tracked                            |
| `skippable`     | boolean    | ❌       | `false` | Allow skipping                                |
| `reftarget`     | string     | ❌       | —       | For `exists-reftarget` requirement (use first step's target) |

---

## Guided Block Properties

The `guided` block waits for user to perform actions manually.

```json
{
  "type": "guided",
  "content": "Description",
  "steps": []
}
```

| Property        | Type       | Required | Default | Description                                   |
|-----------------|------------|----------|---------|-----------------------------------------------|
| `type`          | string     | ✅       | —       | Must be `"guided"`                            |
| `content`       | string     | ✅       | —       | User-visible description                      |
| `steps`         | JsonStep[] | ✅       | —       | Steps for user to perform                     |
| `stepTimeout`   | number     | ❌       | `30000` | Timeout per step in milliseconds              |
| `completeEarly` | boolean    | ❌       | `false` | Complete when user performs action early      |
| `requirements`  | string[]   | ❌       | —       | Requirements for the block                    |
| `objectives`    | string[]   | ❌       | —       | Objectives tracked                            |
| `skippable`     | boolean    | ❌       | `false` | Allow skipping                                |

---

## Step Properties (for multistep/guided)

Steps used within `multistep` and `guided` blocks:

```json
{
  "action": "highlight",
  "reftarget": "selector"
}
```

| Property        | Type     | Required | Default | Description                                   |
|-----------------|----------|----------|---------|-----------------------------------------------|
| `action`        | string   | ✅       | —       | Action type                                   |
| `reftarget`     | string   | ✅       | —       | Target reference                              |
| `targetvalue`   | string   | ❌       | —       | Value for formfill                            |
| `requirements`  | string[] | ❌       | —       | Step-specific requirements                    |
| `tooltip`       | string   | ❌       | —       | Tooltip during execution                      |
| `skippable`     | boolean  | ❌       | `false` | Allow skipping (guided only)                  |
| `validateInput` | boolean  | ❌       | `false` | Validate formfill input                       |
| `formHint`      | string   | ❌       | —       | Hint for formfill validation                  |

---

## Conditional Block Properties

The `conditional` block shows different content based on conditions.

```json
{
  "type": "conditional",
  "conditions": ["requirement"],
  "whenTrue": [],
  "whenFalse": []
}
```

| Property                 | Type                      | Required | Default    | Description                                   |
|--------------------------|---------------------------|----------|------------|-----------------------------------------------|
| `type`                   | string                    | ✅       | —          | Must be `"conditional"`                       |
| `conditions`             | string[]                  | ✅       | —          | Conditions to evaluate (requirement syntax)   |
| `whenTrue`               | JsonBlock[]               | ✅       | —          | Blocks shown when ALL conditions pass         |
| `whenFalse`              | JsonBlock[]               | ✅       | —          | Blocks shown when ANY condition fails         |
| `description`            | string                    | ❌       | —          | Author note (not shown to users)              |
| `display`                | `"inline"` \| `"section"` | ❌       | `"inline"` | Display mode for branch content               |
| `whenTrueSectionConfig`  | object                    | ❌       | —          | Section config when display is "section"      |
| `whenFalseSectionConfig` | object                    | ❌       | —          | Section config when display is "section"      |

**Section Config Properties:**

| Property        | Type     | Description                                   |
|-----------------|----------|-----------------------------------------------|
| `title`         | string   | Section title for this branch                 |
| `requirements`  | string[] | Requirements that must be met                 |
| `objectives`    | string[] | Objectives tracked for completion             |

---

## Quiz Block Properties

The `quiz` block tests user knowledge.

```json
{
  "type": "quiz",
  "question": "Question text",
  "choices": []
}
```

| Property         | Type         | Required | Default          | Description                                   |
|------------------|--------------|----------|------------------|-----------------------------------------------|
| `type`           | string       | ✅       | —                | Must be `"quiz"`                              |
| `question`       | string       | ✅       | —                | Question text (supports markdown)             |
| `choices`        | QuizChoice[] | ✅       | —                | Answer choices                                |
| `multiSelect`    | boolean      | ❌       | `false`          | Allow multiple answers (checkboxes)           |
| `completionMode` | string       | ❌       | `"correct-only"` | `"correct-only"` or `"max-attempts"`          |
| `maxAttempts`    | number       | ❌       | `3`              | Attempts before revealing (max-attempts mode) |
| `requirements`   | string[]     | ❌       | —                | Requirements for this quiz                    |
| `skippable`      | boolean      | ❌       | `false`          | Allow skipping                                |

**Choice Properties:**

| Property  | Type    | Required | Description                                   |
|-----------|---------|----------|-----------------------------------------------|
| `id`      | string  | ✅       | Choice identifier (e.g., "a", "b")            |
| `text`    | string  | ✅       | Choice text (supports markdown)               |
| `correct` | boolean | ❌       | Is this a correct answer?                     |
| `hint`    | string  | ❌       | Hint shown when this wrong choice is selected |

---

## Input Block Properties

The `input` block collects user responses as variables.

```json
{
  "type": "input",
  "prompt": "Question",
  "inputType": "text",
  "variableName": "varName"
}
```

| Property            | Type                    | Required | Default | Description                                   |
|---------------------|-------------------------|----------|---------|-----------------------------------------------|
| `type`              | string                  | ✅       | —       | Must be `"input"`                             |
| `prompt`            | string                  | ✅       | —       | Question/instruction (supports markdown)      |
| `inputType`         | `"text"` \| `"boolean"` | ✅       | —       | Input type: text field or checkbox            |
| `variableName`      | string                  | ✅       | —       | Identifier for storing response               |
| `placeholder`       | string                  | ❌       | —       | Placeholder text (text input only)            |
| `checkboxLabel`     | string                  | ❌       | —       | Label for checkbox (boolean only)             |
| `defaultValue`      | string \| boolean       | ❌       | —       | Default value                                 |
| `required`          | boolean                 | ❌       | `false` | Require response to proceed                   |
| `pattern`           | string                  | ❌       | —       | Regex pattern for validation                  |
| `validationMessage` | string                  | ❌       | —       | Message when validation fails                 |
| `requirements`      | string[]                | ❌       | —       | Requirements for this input                   |
| `skippable`         | boolean                 | ❌       | `false` | Allow skipping                                |

---

## Markdown Block Properties

```json
{
  "type": "markdown",
  "content": "# Heading\n\nParagraph text."
}
```

| Property | Type   | Required | Description                                   |
|----------|--------|----------|-----------------------------------------------|
| `type`   | string | ✅       | Must be `"markdown"`                          |
| `content`| string | ✅       | Markdown content                              |

**AI Customization Properties:**

| Property           | Type                                            | Default | Description                                   |
|--------------------|-------------------------------------------------|---------|-----------------------------------------------|
| `assistantEnabled` | boolean                                         | `false` | Enable AI customization button                |
| `assistantId`      | string                                          | —       | Unique ID for persistence                     |
| `assistantType`    | `"query"` \| `"config"` \| `"code"` \| `"text"` | —       | Type of content for AI prompts                |

---

## Image Block Properties

```json
{
  "type": "image",
  "src": "https://example.com/image.png"
}
```

| Property | Type   | Required | Description                                   |
|----------|--------|----------|-----------------------------------------------|
| `type`   | string | ✅       | Must be `"image"`                             |
| `src`    | string | ✅       | Image URL                                     |
| `alt`    | string | ❌       | Alt text for accessibility                    |
| `width`  | number | ❌       | Display width in pixels                       |
| `height` | number | ❌       | Display height in pixels                      |

---

## Video Block Properties

```json
{
  "type": "video",
  "src": "https://www.youtube.com/embed/VIDEO_ID"
}
```

| Property   | Type                      | Required | Default     | Description                                   |
|------------|---------------------------|----------|-------------|-----------------------------------------------|
| `type`     | string                    | ✅       | —           | Must be `"video"`                             |
| `src`      | string                    | ✅       | —           | Video URL (embed URL for YouTube)             |
| `provider` | `"youtube"` \| `"native"` | ❌       | `"youtube"` | Video provider                                |
| `title`    | string                    | ❌       | —           | Video title for accessibility                 |

---

## Assistant Block Properties

The `assistant` block wraps child blocks with AI customization.

```json
{
  "type": "assistant",
  "assistantType": "query",
  "blocks": []
}
```

| Property        | Type                                            | Required | Description                                   |
|-----------------|-------------------------------------------------|----------|-----------------------------------------------|
| `type`          | string                                          | ✅       | Must be `"assistant"`                         |
| `blocks`        | JsonBlock[]                                     | ✅       | Child blocks to wrap                          |
| `assistantId`   | string                                          | ❌       | Unique ID prefix (auto-generated if omitted)  |
| `assistantType` | `"query"` \| `"config"` \| `"code"` \| `"text"` | ❌       | Type of content for AI behavior               |

---

## Common Property Patterns

### Requirements Array

Requirements are specified as string arrays:

```json
{
  "requirements": ["navmenu-open", "exists-reftarget", "on-page:/dashboards"]
}
```

All requirements must pass for the element to be enabled.

### Objectives Array

Objectives use the same syntax as requirements but auto-complete when met:

```json
{
  "objectives": ["has-datasource:prometheus"]
}
```

If objectives are met, the step is automatically marked complete.

### Variable Substitution

Variables from `input` blocks can be referenced:

- **In content**: `"content": "Your data source **{{datasourceName}}** is configured."`
- **In requirements**: `"requirements": ["var-termsAccepted:true"]`

---

## See Also

- [JSON Guide Format](json-guide-format.md) - Root structure overview
- [Interactive Types](interactive-types.md) - When to use each type
- [Requirements Reference](requirements-reference.md) - All requirement types

