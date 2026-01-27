# Selector Issues

This file tracks CSS selectors that need engineering attention (e.g., missing `data-testid` attributes, tiny highlight areas).

---

## Drilldown Metrics LJ

### Data source selector dropdown - Tiny highlight area

**Learning Journey:** drilldown-metrics  
**Milestone:** search-metrics  
**Step:** Select the data source you want to query

**Current selector:**
```css
input[data-testid='data-testid Dashboard template variables Variable Value DropDown value link text grafanacloud-prom-input']
```

**Problem:** Highlight area is tiny (only highlights the input element, not the full dropdown)

**Suggested fix:** Add `data-testid` to the parent dropdown container element

**Workaround:** Mark as "Show me" only (`doIt: false`)

**Priority:** Medium

---

### Panel menu - Dynamic metric name in selector

**Learning Journey:** drilldown-metrics  
**Milestone:** open-metrics-explore  
**Step:** Click the Menu icon on a metric visualization

**Current selector:**
```css
button[data-testid='data-testid Panel menu asserts:resource:threshold']
```

**Problem:** Selector contains specific metric name `asserts:resource:threshold` which varies by user/environment

**Suggested fix:** Add a stable `data-testid` to panel menu buttons that doesn't include the metric name, OR use wildcard pattern `button[data-testid*='Panel menu']:not([data-testid*='item'])`

**Workaround:** Works for testing but will fail for users with different metrics

**Priority:** High

---

### Explore Add button - Position-based selector

**Learning Journey:** drilldown-metrics  
**Milestone:** add-metric-dashboard  
**Step:** Click Add > Add to dashboard

**Current selector:**
```css
div[data-testid='data-testid Explore'] button:nth-match(4)
```

**Problem:** Position-based selector (4th button) is fragile and will break if toolbar buttons are added/removed/reordered

**Suggested fix:** Add `data-testid` to the Add button in Explore toolbar (e.g., `data-testid="explore-add-button"`)

**Workaround:** None - selector may break with UI changes

**Priority:** High

---

### Add to dashboard menu item - Non-standard CSS selector

**Learning Journey:** drilldown-metrics  
**Milestone:** add-metric-dashboard  
**Step:** Click "Add to dashboard" menu option

**Current selector:**
```css
[role='menuitem']:contains('Add to dashboard')
```

**Problem:** `:contains()` is a jQuery selector, not standard CSS. May not work in all browser/Pathfinder contexts.

**Suggested fix:** Add `data-testid` to menu items (e.g., `data-testid="menu-item-add-to-dashboard"`)

**Workaround:** Test thoroughly - works in some contexts but not guaranteed

**Priority:** Medium

---

## Drilldown Logs LJ

### Service dropdown - Tiny highlight area

**Learning Journey:** drilldown-logs  
**Milestone:** view-logs  
**Step:** Select the service you want to view

**Current selector:**
```css
input[data-testid='data-testid search-services-input']
```

**Problem:** Highlight area is tiny (only highlights the inner input element, not the full dropdown container)

**Suggested fix:** Add `data-testid` to the dropdown container element

**Workaround:** Mark as "Show me" only (`doIt: false`)

**Priority:** Medium

---

### Include button - No data-testid for i18n support

**Learning Journey:** drilldown-logs  
**Milestone:** labels-and-fields, log-patterns  
**Step:** Click Include to filter by value/pattern

**Current selector:**
```css
button:contains('Include')
```

**Problem:** `:contains()` relies on English button text. When Grafana UI is translated to other languages, this selector will break.

**Suggested fix:** Add `data-testid` to Include buttons:
- Labels tab Include button
- Fields tab Include button
- Patterns tab Include button

**Workaround:** Only works for English UI

**Priority:** Medium

---

### Panel menu Log volume - Dynamic log count

**Learning Journey:** drilldown-logs  
**Milestone:** open-logs-explore  
**Step:** Click Menu icon on Log volume panel

**Current selector:**
```css
button[data-testid*='Panel menu Log volume']
```

**Problem:** The full testid includes dynamic log count (e.g., `Panel menu Log volume (3K)`), which changes based on actual data.

**Suggested fix:** Remove dynamic content from `data-testid` attributes

**Workaround:** Using wildcard `*=` selector works across environments ✅

**Priority:** Low (workaround works)

---
