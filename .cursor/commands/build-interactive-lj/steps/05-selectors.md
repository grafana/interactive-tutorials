# Step 5: Selector Discovery

Use browser automation to find CSS selectors for each interactive element.

---

## Before Starting

> 📖 **CRITICAL:** Re-read `reference/selector-patterns.md` before discovering selectors.
> You MUST try selectors in this order: data-testid → aria-label → href → id → class

---

## Authentication Setup (REQUIRED)

Selector discovery happens by walking through the actual Grafana UI at: `https://learn.grafana.net/`

> ⚠️ **Important:** This is different from testing in Pathfinder (Step 6), which uses 
> `https://learn.grafana.net/?pathfinder-dev=true`

Playwright opens a **fresh browser with no session**. Before discovering selectors:

1. **Navigate to the test environment** using Playwright: `https://learn.grafana.net/`
2. **User must manually log in** through the Playwright browser window (Okta SAML)
3. **Wait for user confirmation** that they are logged in
4. **Walk through the UI flow** — navigate to pages where the learning path actions happen and inspect the DOM

> ⚠️ **The AI cannot log the user in** — authentication requires manual user action 
> in the Playwright-controlled browser window.

**Display:**
```
I'll open the Grafana UI to discover selectors by walking through the actual pages.

Opening: https://learn.grafana.net/

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

Walk through the actual Grafana UI at `https://learn.grafana.net/` to find selectors:

1. Navigate to the starting page for the learning path (e.g., Dashboards page for dashboard creation flows)
2. For each interactive block with empty `reftarget`:
   - Navigate to the relevant page in Grafana
   - Query the DOM for the element (see Playwright usage below)
   - Find the element and extract the best available selector
   - Update the content.json with the discovered selector
3. Continue through the entire UI flow, capturing selectors as you go

### Efficient Playwright Usage

Full-page snapshots are expensive and consume significant context. Prefer targeted queries:

| Goal | Preferred approach | Avoid |
|------|--------------------|-------|
| Find a button's selector | `browser_evaluate`: `document.querySelector('button')?.getAttribute('data-testid')` | Full-page snapshot |
| Check if element exists | `browser_evaluate`: `!!document.querySelector('[data-testid="..."]')` | Full-page snapshot |
| List all data-testids on page | `browser_evaluate`: `[...document.querySelectorAll('[data-testid]')].map(e => e.getAttribute('data-testid'))` | Full-page snapshot |
| Find elements near a label | `browser_evaluate`: query by label text, then inspect siblings | Full-page snapshot |

**When a snapshot IS useful:**
- When you have no idea what selectors exist in a region
- When the element structure is complex (nested menus, modals)
- Limit to one snapshot per page, then switch to targeted queries

**Batch discoveries per page.** Group interactive blocks by the page they appear on. Navigate once, discover all selectors for that page, then move on. This avoids redundant navigation and repeated snapshots.

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

## Verification Checklist (REQUIRED)

Before proceeding to Step 6, verify:

- [ ] All resolvable interactive blocks have real selectors (no placeholders)
- [ ] No `"[selector]"` strings remain (only `"TODO:manual-review"` for unresolved blocks)
- [ ] Selectors follow priority order (data-testid preferred)
- [ ] Each selector attempt per block did not exceed 3 tries

---

## Completion

Display a summary showing: selectors found per milestone, confidence level (high/medium/unresolved), and any unresolved blocks with their failed attempts and suggestions. If there are unresolved selectors, list them before the summary so the user sees them first.

Ask the user if they're ready to proceed to Step 6 (Test in Pathfinder).
