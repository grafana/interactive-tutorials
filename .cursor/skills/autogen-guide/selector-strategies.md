# Selector Strategies for AutoGen

Selector assessment specific to generating guides from source code. This file covers **only what's unique to the autogen workflow** -- grading selectors found in source, mapping grades to guide actions, and producing a quality report.

For selector priority ordering, fallback patterns, advanced pseudo-selectors (`:contains`, `:has`, `:nth-match`), and known stable Grafana selectors, see:
- [docs/selectors-and-testids.md](../../../docs/selectors-and-testids.md) -- full selector reference
- [selector-library.mdc](../../selector-library.mdc) -- quick-reference catalog of known selectors

---

## Selector Quality Grading

When extracting interactive elements from source code, grade each element's best available selector and use that grade to decide the guide action.

| Grade | Source Code Has | Guide Action | Confidence |
|-------|----------------|-------------|------------|
| **Green** | `data-testid` or `id` attribute | Full interactive step, `doIt` allowed | High |
| **Yellow** | `aria-label`, `name`, or stable button/link text | Interactive step; prefer `action: "button"` for buttons, `aria-label` or `:contains()` for inputs | Medium |
| **Red** | No stable attributes; only structural position | `doIt: false` with educational tooltip | Low |

### Green Example

```typescript
// Source
<Input data-testid="config-base-url" value={...} />
```
```json
// Guide step
{ "action": "formfill", "reftarget": "[data-testid='config-base-url']", "targetvalue": "https://api.example.com" }
```

### Yellow Example

```typescript
// Source
<Button onClick={onSave}>Save & test</Button>
```
```json
// Guide step -- button text matching is native to the guide system
{ "action": "button", "reftarget": "Save & test" }
```

### Red Example

```typescript
// Source -- no testid, no id, no aria-label
<Field label="Timeout">
  <Input value={options.jsonData?.timeout} onChange={...} />
</Field>
```
```json
// Guide step -- show-only, never automate
{ "action": "highlight", "reftarget": "label:contains('Timeout') + div input", "doIt": false,
  "tooltip": "Set the HTTP request timeout in seconds." }
```

---

## When the Source Code Lies

This is unique to autogen: you're reading source code to infer selectors, but source code doesn't always reflect what reaches the rendered DOM.

Watch for:
- **HOC wrapping** -- a higher-order component may strip or rename props before passing them to the native element
- **Wrapper mismatch** -- `data-testid` may be on a containing `<div>`, not on the `<input>` itself
- **Library components that don't forward** -- a `@grafana/ui` or third-party component may accept `data-testid` in its props but not apply it to the underlying DOM element

When you see `data-testid` in source, note these risks in the extraction report. The grade stays Green (it's the best signal available) but add a caveat that live testing should confirm the selector works. The guide system's `exists-reftarget` auto-check will catch mismatches at runtime.

---

## Selector Quality Report Template

Include this report alongside every generated guide as `SELECTOR_REPORT.md` in the guide directory.

```markdown
## Selector Quality Report

**Generated from**: `<owner>/<repo>@<sha>`
**Date**: <date>
**Guide**: `<guide-id>/content.json`

### Summary
- **Total interactive elements**: <N>
- **Green (stable)**: <n> (<percent>%)
- **Yellow (usable)**: <n> (<percent>%)
- **Red (fragile)**: <n> (<percent>%)

### Fragile Selectors

| Step | Selector Used | Source Location | Suggested Fix |
|------|--------------|-----------------|---------------|
| "Set timeout" | `label:contains('Timeout') + div input` | `Config.tsx:85` | Add `data-testid="config-timeout"` to the Input |
| "Upload CA cert" | `div.tls-section input[type='file']` | `TLS.tsx:42` | Add `data-testid="tls-ca-cert"` to the file input |

### Suggestions for Source Code Authors

To improve guide reliability, add `data-testid` attributes to these elements:

1. `Config.tsx:85` -- timeout input → `data-testid="config-timeout"`
2. `TLS.tsx:42` -- CA cert file input → `data-testid="tls-ca-cert"`
3. `Auth.tsx:142` -- Add Header button → `data-testid="add-custom-header"`
```
