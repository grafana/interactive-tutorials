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

### 3-Attempt Limit Per Block

You have a **maximum of 3 attempts** to find a working selector for each interactive block. On each attempt, try a different strategy from the Selector Decision Tree.

- **Attempt 1:** Try the highest-priority selector available (data-testid, aria-label, etc.)
- **Attempt 2:** Try the next selector strategy down the priority list, or adjust the page state (scroll, expand menus, wait for lazy-loaded elements)
- **Attempt 3:** Try a broader DOM inspection or alternative navigation path to the element

If all 3 attempts fail:
1. **Do NOT keep retrying.** Move on to the next block.
2. Leave the `reftarget` as `"TODO:manual-review"` in content.json.
3. Record the block details and all 3 failed attempts in the **Unresolved Selectors** report (see below).

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
└── [element description] → UNRESOLVED (3/3 attempts failed) ❌
    Attempt 1: [selector tried] - [why it failed]
    Attempt 2: [selector tried] - [why it failed]
    Attempt 3: [selector tried] - [why it failed]
```

---

## Verification Checklist (REQUIRED)

Before proceeding to Step 6, verify:

- [ ] All resolvable interactive blocks have real selectors (no placeholders)
- [ ] No `"[selector]"` strings remain (only `"TODO:manual-review"` for unresolved blocks)
- [ ] Selectors follow priority order (data-testid preferred)
- [ ] Each selector attempt per block did not exceed 3 tries
- [ ] All unresolved selectors are listed in the Unresolved Selectors report below

---

## Unresolved Selectors Report

If any blocks remain unresolved after 3 attempts, display this section **before** the final summary:

```
⚠️  UNRESOLVED SELECTORS — Needs manual review
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[milestone-name] / [block description]
  File: [path/to/content.json], block index [N]
  Page: [URL where the element should appear]
  Attempt 1: [selector] — [reason it failed]
  Attempt 2: [selector] — [reason it failed]
  Attempt 3: [selector] — [reason it failed]
  Suggestion: [any hints — e.g. "element may be behind a feature flag",
               "rendered inside an iframe", "only visible after specific user action"]

[repeat for each unresolved block]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

> The user must resolve these manually before Step 6 testing can fully pass.

---

## Display

Use this exact format:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Step 5 complete: Selector Discovery

Results by milestone:
├── [milestone-1]: [N] selectors found, [M] unresolved
├── [milestone-2]: [N] selectors found, [M] unresolved
└── ...

Selector quality:
├── 🟢 High confidence: [N]
├── 🟡 Medium confidence: [N]
└── 🔴 Unresolved/needs manual review: [N]

⏳ Next: Step 6 - Test in Pathfinder
   Ready to test? (Y/N)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

> If there are unresolved selectors, display the Unresolved Selectors Report 
> immediately above this summary so the user sees it first.
