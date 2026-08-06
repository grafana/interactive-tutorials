# Stable selectors for Grafana Pathfinder tutorials (4 anchors, 3 tutorials)

[Pathfinder](https://grafana.com/docs/learning-journeys/) tutorials anchor their steps to DOM selectors. We've identified that the guides mentioned below target UI this plugin renders (audit: grafana/grafana#129672). Weak anchors (text/placeholder/positional) break silently when copy or layout changes in your plugin however data-testids give us a more robust path forwards.

## Add `data-testid`s to the following JSX

Any value works — we'll retarget the tutorials to whatever you pick.

| element (current weak anchor) | tutorials | where (at 2026-08-04/05) |
|---|---|---|
| `a[href*='adaptive-metrics']` | adaptive-metrics-recommendations | `src/pages/NoAccess/index.tsx:7`<br>`src/_test-utils_/utilities.tsx:19` |
| `button:contains("Apply all recommendations")` | adaptive-logs-recommendations | `src/components/PageHeader/RuleManagement/BatchApply.tsx:133`<br>`src/hooks/context-hooks.ts:299`<br>_low confidence (matched `Apply all recommendations`)_ |
| `input[placeholder="Metric name"]` | adaptive-metrics-lj/review-apply | `src/components/PageHeader/Filters/SearchFilter/index.tsx:62`<br>`src/components/Customizations/CustomizationDrawer/useCustomizationDrawerState.ts:25` |
| `select, div:has(label:contains('Segment'))` | adaptive-metrics-recommendations | `src/pages/App/PageDefinitions.tsx:51`<br>`src/components/Configuration/Segments/header.tsx:22`<br>_low confidence (matched `Segment`)_ |

> [!WARNING]
> 1 tutorial depend on this plugin's existing test ids. Please treat `data-testid`s as part of your public API — do not rename them without pinging the Pathfinder squad first.


---
If you've any questions please reach out in the #proj-pathfinder-selectors slack channel.
