# Selector Patterns and Stability Rules

This document defines how to discover, validate, and ensure stability of CSS selectors for interactive guides.

---

## Selector Priority (Most to Least Stable)

When discovering selectors, try in this order:

| Priority | Selector Type | Example | Confidence |
|----------|---------------|---------|------------|
| 1 | `data-testid` | `[data-testid="agent-config-button"]` | 🟢 High |
| 2 | `aria-label` | `[aria-label="Search connections by name"]` | 🟢 High |
| 3 | `href` (for links) | `a[href="/connections/add-new-connection"]` | 🟢 High |
| 4 | `id` | `#my-element` | 🟡 Medium |
| 5 | Stable class | `.specific-component-class` | 🟡 Medium |

**Avoid:** Generic classes (`.btn`, `.input`), positional selectors (`:nth-child`), text content

---

## Selector Decision Tree

When you find an element, choose selector in this order:

1. Has `data-testid`? → Use `[data-testid="..."]` 🟢
2. Has `aria-label`? → Use `[aria-label="..."]` 🟢
3. Is a link with href? → Use `a[href="..."]` 🟢
4. Is a button with stable text? → Use `action: "button"` 🟡
5. Has unique id? → Use `#id` 🟡
6. None of above? → Try class-based, then ask user 🔴

---

## Stability Anti-Patterns

These patterns cause selectors to work for one user but fail for another—even in the same environment:

| Anti-Pattern | Example | Why It Fails | Fix |
|--------------|---------|--------------|-----|
| **Position-based** | `:first-of-type`, `:nth-child(4)` | Order depends on data; different users see different lists | Use `data-testid` or `aria-label` |
| **Data-dependent values** | `[data-testid='select-action-asserts:resource:threshold']` | Only works with specific metrics/services/labels | Use `^=` starts-with: `[data-testid^='select-action-']` |
| **Hardcoded dynamic IDs** | `label[for='option-traceql-xyz123']` | IDs may include random suffixes | Use `^=` starts-with: `label[for^='option-traceql-']` |
| **Non-standard CSS** | `:contains()`, `:nth-match()`, `:has-text()` | Playwright/jQuery-only, not standard CSS | Find `data-testid` or `aria-label` instead |
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

3. **Is it Playwright/jQuery-specific syntax?**
   - ❌ `button:contains('Include')` or `input:nth-match(1)`
   - ✅ `button[data-testid='data-testid button-filter-include']`

4. **Does the ID have a random suffix?**
   - ❌ `label[for='option-traceql-abc123']`
   - ✅ `label[for^='option-traceql-']`

> 💡 **Pro tip:** When you find multiple valid selectors for an element, always prefer:
> `data-testid` (exact) > `data-testid` (starts-with) > `aria-label` > `href` > other attributes

---

## Selector Syntax Limitations

> ⚠️ **Pathfinder uses standard CSS selectors, NOT Playwright-style selectors.**

### These DON'T work in Pathfinder:

| ❌ Doesn't Work | ✅ Use Instead |
|-----------------|----------------|
| `label:has-text('Service')` | `label[for="service-option"]` or find a stable attribute |
| `button:has-text('Submit')` | `action: "button"` with `reftarget: "Submit"` |
| `div:has(> span.icon)` | Find a direct selector with `data-testid` or `aria-label` |
| `text=Click here` | Not supported; use element selectors |

### These DO work:

| ✅ Works | Example |
|----------|---------|
| Attribute selectors | `[data-testid="my-button"]` |
| Attribute contains | `[aria-label*='section: Alerts']` |
| Attribute starts with | `[data-testid^="select-"]` |
| Combinators | `div > button`, `ul li a` |
| Standard pseudo-classes | `:first-child`, `:last-child` |

**Key rule:** If you discover a selector using Playwright's `getByText()`, `getByRole()`, or `:has-text()`, you MUST convert it to a standard CSS selector before using it in content.json.

---

## Common Selector Patterns

### Don't Use vs Use Instead

| Don't Use | Use Instead | Why |
|-----------|-------------|-----|
| `input[placeholder="..."]` | `[aria-label="..."]` | Placeholder text may change; aria-label is more stable |
| Generic classes (`.btn`) | `[data-testid="..."]` | Classes change frequently; test IDs are intentional |
| `:nth-child()` selectors | Specific attributes | Position-based selectors break when UI reorders |
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
