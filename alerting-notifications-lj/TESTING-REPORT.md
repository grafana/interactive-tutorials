# Testing Report: Configure notification policies with mute timings

**Tester:** Bonny Welsford  
**Date:** February 18–19, 2026  
**Test environment:** learn.grafana-ops.net (Pathfinder dev mode, Block Editor)  
**Selector discovery environment:** bonnystack.grafana.net (Cursor embedded browser)  
**Source LJ:** grafana/website PR #28825 ("Configure notification policies with mute timings")

---

## How testing was performed

Interactive guide JSON was authored and tested using the `/build-interactive-lj` workflow. The process for each milestone was:

1. **Scaffold JSON** -- The AI generated a `content.json` file from the source markdown, populating selectors and interactive actions.
2. **Open Block Editor** -- In Chrome, navigate to `learn.grafana-ops.net`, open the Pathfinder sidebar (Help button **?** → Debug icon → **Block Editor**). Dev mode must be enabled first (one-time setup).
3. **Paste JSON** -- Copy the full `content.json` content and paste it into the Block Editor's JSON input field, then click **Load**.
4. **Step through the guide** -- Click **Show me** (highlights the target element) and **Do it** (performs the action) for each interactive step to verify selectors work and actions behave correctly.
5. **Report issues** -- When a step fails (element not found, wrong element highlighted, action doesn't work), report the issue back. The AI updates the JSON and you re-paste and re-test.
6. **Iterate** -- Repeat steps 3–5 until all steps in the milestone pass.

For full setup instructions (dev mode, Block Editor access, Playwright MCP, repo configuration), see [`.cursor/commands/build-interactive-lj/SETUP.md`](../.cursor/commands/build-interactive-lj/SETUP.md).

---

## Environment Differences (Critical)

The ops stack (`learn.grafana-ops.net`) differs from personal stacks in several important ways:

| Feature | Personal stack (bonnystack) | Ops stack (learn.grafana-ops) |
|---------|---------------------------|-------------------------------|
| Nav item name | Notification policies | **Notification configuration** |
| Nav href | `/alerting/routes` | **`/alerting/notifications`** |
| Default landing tab | Notification policies | **Contact points** |
| Create policy button | New child policy | **New notification policy** |
| Multiple routing trees | Unknown | **Not supported** (feature toggle `alertingMultiplePolicies` disabled) |
| Create policy form | Has Matching labels | **Has Name, Default contact point, Group by, Timing options** |
| Mute timings in policy form | Unknown | **Not present** (Timing options only has Group wait / Group interval) |

**Recommendation:** The writer should verify which Grafana version end-users will run these guides on, and ensure selectors/text match that version. The ops stack appears to be running a newer version with a reorganized Notification configuration page.

---

## Milestone 1: Create time intervals for common scenarios

**Status: PASS (with fixes applied during testing)**

### Selectors tested

| Element | Selector | Result |
|---------|----------|--------|
| Alerts & IRM nav | `a[data-testid='data-testid Nav menu item'][href='/alerts-and-incidents']` | PASS |
| Alerting nav | `a[data-testid='data-testid Nav menu item'][href='/alerting']` | PASS |
| Notification configuration nav | `a[data-testid='data-testid Nav menu item'][href='/alerting/notifications']` | PASS |
| Time intervals tab | `[data-testid='data-testid Tab Time intervals']` | PASS |
| Add time interval link | `a[href*='mute-timing/new']` | PASS |
| Name field | `[data-testid='mute-timing-name']` | PASS |
| Start time field | `[data-testid='mute-timing-starts-at']` | PASS |
| End time field | `[data-testid='mute-timing-ends-at']` | PASS |
| Sunday button | `button` action with text "Sun" | PASS |
| Saturday button | `button` action with text "Sat" | PASS |
| Save time interval | `button` action with text "Save time interval" | PASS |
| Add another time range | `button` action with text "Add another time range" | PASS |
| Add another time interval item | `button` action with text "Add another time interval item" | PASS |

### Issues found and fixed during testing

1. **Nav href mismatch:** Original selector used `/alerting/routes` but ops stack uses `/alerting/notifications`. Fixed.
2. **Standalone nav step failed:** "Notification policies" as a separate interactive step couldn't find the nav item when menu was collapsed. Fixed by merging into 3-step multistep.
3. **"Add time interval" is a link, not a button:** `action: "button"` couldn't find it. Fixed by changing to `action: "highlight"` with `a[href*='mute-timing/new']`.
4. **Midnight-crossing time range validation error:** Setting Start 18:00 / End 08:00 triggers "Start time must be before end time". Fixed by splitting into two ranges: 18:00–23:59 and 00:00–08:00 (second range via markdown instruction).
5. **Sticky validation errors:** After correcting invalid time values, Grafana UI sometimes shows stale validation error messages. Known UI quirk.
6. **Sunday/Saturday buttons:** Originally markdown instructions -- converted to interactive `button` actions for better UX.
7. **Location field:** Shows blank by default, not "UTC" as originally described. Text updated.

---

## Milestone 2: Create a notification policy

**Status: PARTIAL PASS (interactive elements work; content needs writer review)**

### Selectors tested

| Element | Selector | Result |
|---------|----------|--------|
| Navigation multistep (3 steps) | Same as M1 | PASS |
| Notification policies tab | `[data-testid='data-testid Tab Notification policies']` | PASS |
| New notification policy button | `button` action with text "New notification policy" | PASS |

### Issues for writer

1. **Feature toggle blocker:** Ops stack returns error "Multiple routes are not supported, see feature toggle alertingMultiplePolicies". Cannot create additional notification policies.
2. **Form doesn't match source LJ:** The "New notification policy" dialog has Name, Default contact point, Group by, and Timing options -- NOT Matching labels as the source LJ describes. The source LJ assumed a "child policy" flow that doesn't exist on this version.
3. **Modal buttons unreachable:** Pathfinder's `button` action cannot find buttons inside the modal dialog (Create, Cancel). The Create step was converted to markdown.
4. **No mute timings in creation form:** The Timing options section only contains Group wait and Group interval, not mute timings.

---

## Milestone 3: Add mute timings to notification policy

**Status: PARTIAL PASS (navigation works; content needs writer review)**

### Selectors tested

| Element | Selector | Result |
|---------|----------|--------|
| Navigation multistep (3 steps) | Same as M1 | PASS |
| Notification policies tab | `[data-testid='data-testid Tab Notification policies']` | PASS |

### Issues for writer

1. **Edit dialog for Default Policy:** The user could not locate a "Mute timings" section when editing the Default Policy. The writer needs to verify where mute timings are configured in this Grafana version.
2. **Steps are mostly markdown:** Due to modal interactions that Pathfinder can't automate, most steps in this milestone are markdown instructions.

---

## Milestone 4: Create a silence for scheduled suppression

**Status: PASS (with one fix applied during testing)**

### Selectors tested

| Element | Selector | Result |
|---------|----------|--------|
| Silences nav | `a[data-testid='data-testid Nav menu item'][href='/alerting/silences']` | PASS |
| Create silence link | `a[href*='silence/new']` | PASS |
| Duration field | `#duration` | PASS |
| Comment field | `textarea[name='comment']` | PASS |
| Save silence button | `button` action with text "Save silence" | PASS |

### Issues found and fixed during testing

1. **"Create silence" is a link, not a button:** Same pattern as "Add time interval". Fixed by changing to `action: "highlight"` with `a[href*='silence/new']`.
2. **Section name mismatch:** Source LJ said "Preview affected alert instances" but actual UI says "Affected alert instances". Text updated.
3. **Source LJ said "Submit" button:** Actual button text is "Save silence". Already corrected during scaffolding.

---

## Milestone 5: Verify notification behavior

**Status: PASS (navigation works; verification is manual review)**

### Selectors tested

| Element | Selector | Result |
|---------|----------|--------|
| Navigation multistep (3 steps) | Same as M1 | PASS |
| Notification policies tab | `[data-testid='data-testid Tab Notification policies']` | PASS |
| Time intervals tab | `[data-testid='data-testid Tab Time intervals']` | PASS |
| Alert rules nav | `a[data-testid='data-testid Nav menu item'][href='/alerting/list']` | PASS |

### Notes

1. **"Fix this" needed for Time intervals tab:** The `on-page:/alerting/notifications` requirement sometimes fails to recognize the current page (possibly due to query parameters in the URL). The "Fix this" button resolves it.
2. **No mute timings visible on policies:** Expected, since M2/M3 couldn't successfully configure them due to ops stack limitations.

---

## Summary

| Milestone | Navigation | Selectors | Content accuracy | Overall |
|-----------|-----------|-----------|-----------------|---------|
| 1. Create time intervals | PASS | PASS | PASS | **PASS** |
| 2. Create notification policy | PASS | PASS | NEEDS REVIEW | **PARTIAL** |
| 3. Add mute timings to policy | PASS | PASS | NEEDS REVIEW | **PARTIAL** |
| 4. Create a silence | PASS | PASS | PASS | **PASS** |
| 5. Verify notification behavior | PASS | PASS | PASS | **PASS** |

### Key patterns learned

- **Links vs buttons:** Several Grafana UI elements that look like buttons are actually `<a>` links. Use `action: "highlight"` with `href`-based selectors for these, not `action: "button"`.
- **Modal dialogs:** Pathfinder's `button` action cannot find elements inside modals. Use markdown instructions for modal interactions.
- **Version differences:** The ops stack nav uses `/alerting/notifications` with "Notification configuration" while personal stacks use `/alerting/routes` with "Notification policies". Selectors using `data-testid` + `href` are version-dependent.
- **Time range validation:** Grafana does not accept time ranges crossing midnight. Split overnight ranges into two (e.g., 18:00–23:59 + 00:00–08:00).

### Changes from original learning journey

The source markdown (PR #28825) required these adjustments to work as interactive guides. The writer should review these and decide which reflect genuine corrections vs. environment-specific differences.

| Milestone | Original LJ said | Changed to | Reason |
|-----------|-----------------|------------|--------|
| All | Navigate to "Notification policies" at `/alerting/routes` | Navigate to "Notification configuration" at `/alerting/notifications` | Ops stack uses different nav label and URL path |
| All | 2-step nav (Alerts & IRM > Alerting) | 3-step nav (Alerts & IRM > Alerting > Notification configuration) | Need to explicitly expand to the third level for Pathfinder to find the target |
| All | Assumed landing on Notification policies tab | Added explicit tab-click step | Default landing tab is Contact points, not Notification policies |
| M1 | Click "Add time interval" (button) | Highlight `a[href*='mute-timing/new']` (link) | UI element is an `<a>` link, not a `<button>` |
| M1 | Non-business hours: 18:00 to 08:00 as one range | Split into 18:00–23:59 + 00:00–08:00 (two ranges) | Grafana validates start < end; overnight ranges must be split |
| M1 | "Leave the Location set to UTC" | "Leave the Location blank" | Field is blank by default, not pre-filled with UTC |
| M1 | Sunday/Saturday selection as prose | Converted to interactive `button` actions ("Sun", "Sat") | Better UX with Show me / Do it |
| M2 | "New child policy" button | "New notification policy" button | Different button text on ops stack |
| M2 | Form with "Matching labels" section | Form with Name, Default contact point, Group by, Timing options | Ops stack creates routing trees, not child policies with label matchers |
| M2 | Click "Save policy" | Click "Create" (as markdown step) | Different button text; modal buttons unreachable by Pathfinder |
| M3 | Edit policy to add mute timings | Mostly markdown instructions | Could not locate Mute timings section in the Default Policy edit dialog |
| M4 | Click "Create silence" (button) | Highlight `a[href*='silence/new']` (link) | Same link-vs-button pattern as M1 |
| M4 | "Preview affected alert instances" section | "Affected alert instances" section | Different section name in UI |
| M4 | Click "Submit" | Click "Save silence" | Different button text in UI |

### Recommendations for writer

1. **Verify target Grafana version** -- The notification policy creation/editing flow differs significantly between versions. Confirm which version users will have.
2. **Milestone 2 rework needed** -- The "Matching labels" / child policy flow doesn't exist on the ops stack. The form creates a routing tree instead.
3. **Milestone 3 rework needed** -- Determine where mute timings are actually configured (Edit dialog, or a different UI path).
4. **Consider combining M2 and M3** -- If mute timings can be set during policy creation on newer versions, these milestones could merge.
5. **Test on target user stack** -- Several issues stemmed from version differences between environments. Testing on the actual target environment is essential.
