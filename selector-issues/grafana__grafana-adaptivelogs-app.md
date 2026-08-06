# Stable selectors for Grafana Pathfinder tutorials (2 anchors, 2 tutorials)

[Pathfinder](https://grafana.com/docs/learning-journeys/) tutorials anchor steps to DOM selectors, and the ones below target UI this plugin renders (audit: grafana/grafana#129672). Weak anchors (text/placeholder/positional) break silently when copy or layout changes.

## Add a `data-testid` (2)

Any value works — we'll retarget the tutorials to whatever you pick.

| element (current weak anchor) | tutorials | where (at 2026-08-04/05) |
|---|---|---|
| `a[href*='adaptive-logs']` | adaptive-logs-lj | `src/pages/Overview/GetStarted/GuidedOnboardingCallout.tsx:12`<br>`src/_test-utils_/utilities.tsx:11` |
| `label[aria-label^='Show early detection patterns']` | adaptive-logs-recommendations | `src/components/RecommendationsTable/RecommendationsTableEmptyState.tsx:160`<br>`src/components/PageHeader/index.tsx:150` |


---
If you've any questions please reach out in the #proj-pathfinder-selectors slack channel.
