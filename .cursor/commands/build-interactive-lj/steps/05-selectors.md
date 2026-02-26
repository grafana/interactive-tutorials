# Step 5: Selector Discovery

Use browser automation to find CSS selectors for each interactive element.

---

## Before Starting

> 📖 **CRITICAL:** Re-read `reference/selector-patterns.md` before discovering selectors.
> You MUST try selectors in this order: data-testid → aria-label → href → id → class

---

## Authentication Setup (REQUIRED)

Selector discovery happens by walking through the actual Grafana UI at: `https://learn.grafana-ops.net/`

> ⚠️ **Important:** This is different from testing in Pathfinder (Step 6), which uses 
> `https://learn.grafana-ops.net/?pathfinder-dev=true`

Playwright opens a **fresh browser with no session**. Before discovering selectors:

1. **Navigate to the test environment** using Playwright: `https://learn.grafana-ops.net/`
2. **User must manually log in** through the Playwright browser window (Okta SAML)
3. **Wait for user confirmation** that they are logged in
4. **Walk through the UI flow** — navigate to pages where the learning path actions happen and inspect the DOM

> ⚠️ **The AI cannot log the user in** — authentication requires manual user action 
> in the Playwright-controlled browser window.

**Display:**
```
I'll open the Grafana UI to discover selectors by walking through the actual pages.

Opening: https://learn.grafana-ops.net/

Please log in when the browser window appears. Let me know when you're logged in. (Y/N)
```

---

## Tutorial Mode Introduction

```
**Step 5: Selector Discovery**

I'll use browser automation to find selectors for each interactive element:
- Navigate to the relevant Grafana pages
- Inspect the DOM to find stable selectors
- Update the content.json files with discovered selectors

Selector priority: data-testid > aria-label > id > placeholder > href

Ready to proceed? (Y/N)
```

Wait for confirmation, then discover.

---

## Expert Mode

Discover immediately without introduction.

---

## Discovery Process

Walk through the actual Grafana UI at `https://learn.grafana-ops.net/` to find selectors:

1. Navigate to the starting page for the learning path (e.g., Dashboards page for dashboard creation flows)
2. For each interactive block with empty `reftarget`:
   - Navigate to the relevant page in Grafana
   - Use Playwright snapshot to inspect the DOM
   - Find the element and extract the best available selector
   - Update the content.json with the discovered selector
3. Continue through the entire UI flow, capturing selectors as you go

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

## Stability Check (REQUIRED)

After selecting a selector, verify it's stable:

| Check | If Yes... |
|-------|-----------|
| Does the selector contain a data value (metric name, service name, label)? | Use `^=` starts-with pattern |
| Does the selector use position (`:first-of-type`, `:nth-child`)? | Find a `data-testid` or `aria-label` instead |
| Does the selector use `:contains()` or `:nth-match()`? | Convert to standard CSS with `data-testid` |
| Does the `id` or `for` attribute have random characters? | Use `^=` starts-with pattern |

> ⚠️ **Why this matters:** Selectors that work for you may fail for colleagues with different data. Always prefer patterns that work regardless of the specific data displayed.

---

## Display Progress

Use this exact format:

```
Discovering selectors for [milestone-name]...
├── [element description] → [selector] 🟢
├── [element description] → [selector] 🟡
└── [element description] → FAILED ❌
    Attempt 1: [selector tried] - [why it failed]
    Attempt 2: [selector tried] - [why it failed]
```

---

## Verification Checklist (REQUIRED)

Before proceeding to Step 6, verify:

- [ ] All interactive blocks have real selectors (no placeholders)
- [ ] No `"[selector]"` or `"TODO"` strings remain
- [ ] Selectors follow priority order (data-testid preferred)
- [ ] Failed selectors are noted for user decision

---

## Display

Use this exact format:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Step 5 complete: Selector Discovery

Results by milestone:
├── [milestone-1]: [N] selectors found
├── [milestone-2]: [N] selectors found
└── ...

Selector quality:
├── 🟢 High confidence: [N]
├── 🟡 Medium confidence: [N]
└── 🔴 Failed/needs review: [N]

⏳ Next: Step 6 - Test in Pathfinder
   Ready to test? (Y/N)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
