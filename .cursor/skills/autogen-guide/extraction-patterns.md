# Extraction Patterns Reference

Detailed patterns for analyzing React/TypeScript UI components to extract guide-relevant structure. This file is a reference for the [autogen-guide skill](SKILL.md).

---

## Standard Grafana UI Components

These are the primary components from `@grafana/ui` that produce interactive guide targets. When reading source code, search for these component names.

### Component → Guide Action Mapping

| Component | Purpose | Guide Action | Key Props to Extract |
|-----------|---------|-------------|---------------------|
| `Field` | Field wrapper with label | (wrapper -- extract metadata) | `label`, `description`, `tooltip`, `invalid`, `error`, `required` |
| `InlineField` | Horizontal field layout | (wrapper -- extract metadata) | `label`, `labelWidth`, `tooltip` |
| `FieldSet` | Group of fields (section) | Map to `section` block | `label`, `isCollapsible` |
| `Input` | Text input | `formfill` or `highlight` | `id`, `name`, `placeholder`, `value`, `type`, `data-testid` |
| `SecretInput` | Password/token input | `highlight` with `doIt: false` | `isConfigured`, `placeholder`, `data-testid` |
| `Select` | Dropdown | `highlight` with `doIt: false` | `options` (array of {label, value}), `value`, `onChange` |
| `Switch` | Toggle/checkbox | `highlight` with `doIt: false` | `value`, `disabled`, `label` |
| `TextArea` | Multi-line text | `formfill` or `highlight` | `rows`, `placeholder`, `value` |
| `Button` | Action button | `button` | `onClick`, button text (children), `variant` |
| `InlineFieldRow` | Row container | (structural -- not interactive) | -- |
| `Alert` | Warning/info message | `highlight` with `doIt: false` | `severity`, `title` |
| `RadioButtonGroup` | Radio selection | `highlight` or `button` | `options`, `value` |
| `Checkbox` | Checkbox | `highlight` | `label`, `value` |
| `ColorPicker` | Color input | `highlight` with `doIt: false` | `color` |
| `Slider` | Range input | `highlight` with `doIt: false` | `min`, `max`, `value`, `step` |

### Standard DataSource Config Pattern

All Grafana datasource config editors follow this pattern:

```typescript
export const ConfigEditor: React.FC<DataSourcePluginOptionsEditorProps<Options, SecureOptions>> = ({
  options,
  onOptionsChange,
}) => {
  return (
    <>
      <FieldSet label="Connection">
        <Field label="URL">
          <Input value={options.url} onChange={...} />
        </Field>
      </FieldSet>

      <FieldSet label="Authentication">
        {/* Auth fields */}
      </FieldSet>

      <FieldSet label="Additional Settings" isCollapsible>
        {/* Optional fields */}
      </FieldSet>
    </>
  );
};
```

**Extraction rule**: Each `FieldSet` maps to a `section`. Each `Field` containing an interactive component maps to a step within that section.

---

## Props Extraction Guide

### From Field Wrappers

When you see a `<Field>` or `<InlineField>`, extract:

```typescript
<Field
  label="Base URL"                    // → step content & tooltip context
  description="Root URL for requests" // → tooltip or markdown intro
  tooltip="Used as prefix for all queries" // → step tooltip
  required                            // → note in content ("required field")
  invalid={!!errors.url}              // → indicates validation exists
  error={errors.url}                  // → mention validation in tooltip
>
  <Input ... />
</Field>
```

### From Interactive Components

```typescript
<Input
  id="infinity-base-url"             // → reftarget: "#infinity-base-url"
  data-testid="config-url"           // → reftarget: "[data-testid='config-url']"
  name="jsonData.baseUrl"            // → reftarget: "[name='jsonData.baseUrl']"
  aria-label="Base URL"              // → reftarget: "[aria-label='Base URL']"
  placeholder="https://api.example.com" // → use as targetvalue example
  value={options.url}                // → understand what state it maps to
  type="url"                         // → note in content
/>
```

**Selector priority**: `data-testid` > `id` > `name` > `aria-label` > label text

### From Select Components

```typescript
<Select
  options={[
    { label: 'No Auth', value: 'none' },
    { label: 'Basic Auth', value: 'basic' },
    { label: 'Bearer Token', value: 'bearer' },
  ]}
  value={currentAuthType}
  onChange={onAuthTypeChange}
/>
```

**Extract**: The `options` array is critical. Each option represents a choice the user can make. Document all options in the step's tooltip or a preceding markdown block.

---

## Conditional Rendering Detection

### Pattern 1: Logical AND

```typescript
{authType === 'bearer' && (
  <Field label="Bearer Token">
    <SecretInput ... />
  </Field>
)}
```

**Extract**: Field "Bearer Token" is conditional on `authType === 'bearer'`.

### Pattern 2: Ternary

```typescript
{isAdvanced ? <AdvancedConfig /> : <BasicConfig />}
```

**Extract**: Two mutually exclusive components. Generate steps for both, with appropriate skippable annotations.

### Pattern 3: Switch/Case (in JSX or render function)

```typescript
const renderAuthFields = () => {
  switch (authType) {
    case 'basic': return <BasicAuthFields />;
    case 'bearer': return <BearerFields />;
    case 'oauth2': return <OAuthFields />;
    default: return null;
  }
};
```

**Extract**: Multiple conditional branches. Each branch becomes a group of steps. Use `skippable: true` since the user will only need one branch.

### Pattern 4: Map/Array Rendering

```typescript
{customHeaders.map((header, index) => (
  <InlineFieldRow key={index}>
    <InlineField label="Name"><Input ... /></InlineField>
    <InlineField label="Value"><Input ... /></InlineField>
    <Button onClick={() => remove(index)}>Remove</Button>
  </InlineFieldRow>
))}
<Button onClick={addHeader}>Add Header</Button>
```

**Extract**: This is a repeatable field array. Generate a guide step that explains the pattern (add/remove) rather than trying to interact with dynamic array items. Use `doIt: false` highlight on the "Add" button with an explanatory tooltip.

---

## State and Type Analysis

### Finding Configuration Types

Look for TypeScript interfaces that define the configuration shape. Common locations:
- `types.ts`, `config.types.ts`, `datasource.types.ts`
- Inline in the component file
- Imported from `@grafana/data` (`DataSourceSettings<T, S>`)

```typescript
interface MyPluginOptions {
  auth?: {
    type: 'none' | 'basic' | 'bearer';
  };
  timeout?: number;
  enableCaching?: boolean;
}
```

**Extract**: Field names, types, and optionality from the interface. Union types (`'none' | 'basic'`) indicate select/dropdown options. Optional fields (`?`) are candidates for `skippable: true` steps.

### Finding Default Values

Look for:
- `defaultProps` or default parameter values
- Initial state in `useState()` or `useReducer()`
- Default values in type definitions
- Fallback values in `value={options.field ?? defaultValue}`

Defaults are useful as `targetvalue` in `formfill` actions, and as context in tooltips ("Defaults to 30 seconds").

---

## Component Tree Traversal Strategy

### Step 1: Read the Entry Point

Read the main component file (e.g., `ConfigEditor.tsx`). Identify:
- All local imports (`import { AuthConfig } from './Auth'`)
- Package imports (skip these -- just note them)
- The JSX return structure

### Step 2: Follow Local Imports (One Level Deep)

For each locally imported component:
1. Read its file
2. Extract its props and JSX structure
3. Do NOT follow its local imports further (prevents context explosion)

### Step 3: Read Type Files

If the entry point imports types from a separate file, read that file. Type files are typically small and high-value.

### Step 4: Check Plugin Metadata

If `plugin.json` exists, read it for:
- Plugin ID (for `plugin-enabled:` requirement)
- Plugin name (for guide title context)
- Supported features / `includes` array

### Boundaries

- **Stop at 15 files** total. Report what you couldn't analyze.
- **Stop at 3000 lines** cumulative. Report the cutoff.
- **Skip test files** (`*.test.tsx`, `*.spec.ts`, `__tests__/`).
- **Skip story files** (`*.stories.tsx`).
- **Skip build artifacts** (`dist/`, `build/`, `node_modules/`).
