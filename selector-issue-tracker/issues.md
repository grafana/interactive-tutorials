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
