# Selector Patterns and Stability Rules

This document defines how to discover, validate, and ensure stability of CSS selectors for interactive guides.

---

## Selector Priority (Most to Least Stable)

When discovering selectors, try in this order:

| Priority | Selector Type | Example | Confidence |
|----------|---------------|---------|------------|
| 1 | `grafana:` symbolic reference | `grafana:components.TimePicker.openButton` | 🟢 High |
| 2 | `data-testid` | `[data-testid="agent-config-button"]` | 🟢 High |
| 3 | `aria-label` | `[aria-label="Search connections by name"]` | 🟢 High |
| 4 | `href` (for links) | `a[href="/connections/add-new-connection"]` | 🟢 High |
| 5 | `id` | `#my-element` | 🟡 Medium |
| 6 | Stable class | `.specific-component-class` | 🟡 Medium |

A `grafana:` reference resolves through `@grafana/e2e-selectors` against the *running* Grafana
version and matches `data-testid` **or** `aria-label`; a literal `data-testid` is a snapshot of one
version's value. See [docs/selectors-and-testids.md](../../../../docs/selectors-and-testids.md#symbolic-selector-references).

**Avoid:** Generic classes (`.btn`, `.input`), positional selectors (`:nth-child`), text content

---

## Selector Decision Tree

When you find an element, choose selector in this order:

1. Does `@grafana/e2e-selectors` define it? → Use `grafana:<path>` 🟢
2. Has `data-testid`? → Use `[data-testid="..."]` 🟢
3. Has `aria-label`? → Use `[aria-label="..."]` 🟢
4. Is a link with href? → Use `a[href="..."]` 🟢
5. Is a button with stable text? → Use `action: "button"` 🟡 — but see [Text and translation](#text-and-translation)
6. Has unique id? → Use `#id` 🟡
7. None of above? → Try class-based, then ask user 🔴

**Exception:** nav menu items stay literal —
`a[data-testid='data-testid Nav menu item'][href='/explore']`. Pathfinder regex-matches that exact
shape to auto-expand a collapsed section, and a resolved reference defeats the fix.

---

## Stability Anti-Patterns

These patterns cause selectors to work for one user but fail for another—even in the same environment:

| Anti-Pattern | Example | Why It Fails | Fix |
|--------------|---------|--------------|-----|
| **Position-based** | `:first-of-type`, `:nth-child(4)` | Order depends on data; different users see different lists | Use `data-testid` or `aria-label` |
| **Data-dependent values** | `[data-testid='select-action-asserts:resource:threshold']` | Only works with specific metrics/services/labels | Use `^=` starts-with: `[data-testid^='select-action-']` |
| **Hardcoded dynamic IDs** | `label[for='option-traceql-xyz123']` | IDs may include random suffixes | Use `^=` starts-with: `label[for^='option-traceql-']` |
| **Text matching** | `:contains()`, `:has-text()` | Compares against translated copy; breaks in any non-English UI | Use a `grafana:` reference, or `data-testid` |
| **Position-dependent matching** | `:nth-match()` | Supported by Pathfinder, but index depends on what is rendered — and Grafana lazy-renders | Scope to a container instead; see [dashboard-selector-strategies.md](../../../skills/autogen-guide-dashboard/dashboard-selector-strategies.md) |
| **Exact label matches** | `a[aria-label='Select detected_level']` | Label text includes data-specific values | Use `^=` starts-with: `a[aria-label^='Select ']` |

---

## Stability Verification Checklist

**Before committing a selector, ask:**

1. **Does it contain a data value?** (metric name, service name, label value)
   - ❌ `button[data-testid='select-action-asserts:resource:threshold']`
   - ✅ `button[data-testid^='select-action-']`

2. **Does it assume position in a list?** (`:first-of-type`, `:nth-child()`)
   - ❌ `a[data-testid='button-select-service']:first-of-type`
   - ✅ `a[data-testid^='data-testid button-select-service']`

3. **Does it depend on translated text?**
   - ❌ `button:contains('Include')` — breaks in every non-English UI
   - ✅ `button[data-testid='data-testid button-filter-include']`

4. **Does the ID have a random suffix?**
   - ❌ `label[for='option-traceql-abc123']`
   - ✅ `label[for^='option-traceql-']`

5. **Is there a `grafana:` reference for it?**
   - ❌ `button[data-testid='data-testid TimePicker Open Button']` — pins one version's value
   - ✅ `grafana:components.TimePicker.openButton`

> 💡 **Pro tip:** When you find multiple valid selectors for an element, always prefer:
> `grafana:` reference > `data-testid` (exact) > `data-testid` (starts-with) > `aria-label` > `href` > other attributes
>
> See [docs/selectors-and-testids.md](../../../../docs/selectors-and-testids.md) for the `grafana:`
> forms, and the `convert-guide-selectors` skill to convert an existing guide.

---

## Selector Syntax Limitations

> ⚠️ **Pathfinder uses standard CSS selectors plus a small set of its own extensions.** It is not a
> Playwright selector engine, but it is not plain `querySelector` either.

The extensions, in full:

| Extension | Form | Reference |
|-----------|------|-----------|
| Symbolic selector references | `grafana:<path>`, `grafana:<path>:<arg>`, `{grafana:<path>}` | [docs/selectors-and-testids.md](../../../../docs/selectors-and-testids.md#symbolic-selector-references) |
| Panel scoping | `panel:<title>`, `panel:<title> > <rest>` | [symbolic-selector-syntax.md](../../../skills/convert-guide-selectors/symbolic-selector-syntax.md) |
| Text matching (subtree) | `:contains('…')` | [docs/selectors-and-testids.md](../../../../docs/selectors-and-testids.md) |
| Text matching (direct nodes) | `:text('…')` | [docs/selectors-and-testids.md](../../../../docs/selectors-and-testids.md) |
| Global Nth occurrence | `:nth-match(N)`, `:nth-match(-1)` | [docs/selectors-and-testids.md](../../../../docs/selectors-and-testids.md) |

`:has()` needs no extension — it is standard CSS, and the engine adds a JS fallback for older
browsers. Everything not listed above must be standard CSS.

### These DON'T work in Pathfinder:

| ❌ Doesn't Work | ✅ Use Instead |
|-----------------|----------------|
| `label:has-text('Service')` | `label[for="service-option"]` or find a stable attribute |
| `button:has-text('Submit')` | `:text('Submit')`, or `action: "button"` with `reftarget: "Submit"` |
| `text=Click here` | Not supported; use element selectors |
| `getByRole()`, `getByText()` | Playwright APIs, not selectors; convert to CSS |

### These DO work:

| ✅ Works | Example |
|----------|---------|
| Symbolic selector reference | `grafana:components.TimePicker.openButton` |
| …parameterized | `grafana:components.Panels.Panel.title:Graph` |
| …embedded in CSS | `{grafana:components.VizLegend.legend} button` |
| Attribute selectors | `[data-testid="my-button"]` |
| Attribute contains | `[aria-label*='section: Alerts']` |
| Attribute starts with | `[data-testid^="select-"]` |
| Combinators | `div > button`, `ul li a` |
| Standard pseudo-classes | `:first-child`, `:last-child` |
| `:has()` structural matching | `div[data-testid="panel"]:has(p)` |
| Text matching | `div:contains('svc')`, `button:text('Save')` |
| Global Nth occurrence | `div[data-testid='uplot-main-div']:nth-match(3)` |
| Panel scoping | `panel:CPU > .legend` |

**Key rule:** If you discover a selector using Playwright's `getByText()`, `getByRole()`, or `:has-text()`, you MUST convert it to a standard CSS selector before using it in content.json.

---

## Text and Translation

Anything that matches on visible copy — `:contains()`, `:text()`, and `action: "button"` with a text
`reftarget` — compares against **translated** UI strings. It works in English and silently matches
nothing in every other locale.

This applies to `action: "button"` just as much as to `:contains()`; the action is convenient, not
i18n-safe. Where a `grafana:` reference or a `data-testid` exists, use it. Where none does, that is a
gap to fix in grafana/grafana rather than paper over in the guide.

A `data-testid` is not automatically safe either — if its value derives from a `t()`-wrapped string
it changes with the UI language. See
[symbolic-selector-syntax.md](../../../skills/convert-guide-selectors/symbolic-selector-syntax.md)
trap 4.

---

## Common Selector Patterns

### Don't Use vs Use Instead

| Don't Use | Use Instead | Why |
|-----------|-------------|-----|
| `input[placeholder="..."]` | `[aria-label="..."]` | Placeholder text may change; aria-label is more stable |
| Generic classes (`.btn`) | `[data-testid="..."]` | Classes change frequently; test IDs are intentional |
| `:nth-child()` selectors | Specific attributes | Position-based selectors break when UI reorders |
| Literal `data-testid` when a path exists | `grafana:<path>` | A literal pins one Grafana version's value and one attribute spelling |
| `button[aria-label*='section:']` for nav | `a[data-testid='data-testid Nav menu item'][href='/path']` | Nav links work whether sections are expanded/collapsed |

---

## When Markdown Beats Interactive

Some UI patterns are better documented as markdown instructions rather than automated:

- **Conditional dialogs** - Buttons that only appear after user completes a real-world action (e.g., "Test connection" after installing software)
- **Multi-path flows** - When user must choose between options (create new vs use existing)
- **External actions** - Steps performed outside the browser (run CLI commands, install software)

---

## Lessons Learned

### Integration-Specific Notes

For **integration setup learning paths** (Linux, Windows, macOS, MySQL, etc.):
- The "Run Grafana Alloy" expand button works: `[data-testid="agent-config-button"]`
- Token creation and "Test connection" buttons are conditional — use markdown
- "Install" button for dashboards/alerts works: `action: "button"` with `reftarget: "Install"`
