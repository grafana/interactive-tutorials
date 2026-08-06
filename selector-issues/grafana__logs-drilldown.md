# Stable selectors for Grafana Pathfinder tutorials (3 anchors, 2 tutorials)

[Pathfinder](https://grafana.com/docs/learning-journeys/) tutorials anchor their steps to DOM selectors. We've identified that the guides mentioned below target UI this plugin renders (audit: grafana/grafana#129672). Weak anchors (text/placeholder/positional) break silently when copy or layout changes in your plugin however data-testids give us a more robust path forwards.

## Add `data-testid`s to the following JSX

Any value works — we'll retarget the tutorials to whatever you pick.

| element (current weak anchor) | tutorials | where (at 2026-08-04/05) |
|---|---|---|
| `button:contains('Include')` | drilldown-logs-lj/labels-and-fields | `src/Components/FilterButton.tsx:40`<br>`src/Components/IndexScene/PatternControls.tsx:45`<br>_low confidence (matched `Include`)_ |

## Anchor gone — renamed or removed? (2)

Not found in source, bundle, or a live stack (2026-08-06). Tell us the new selector, or we'll re-record the step.

| anchor | tutorials | searched for |
|---|---|---|
| `[data-testid='stream-selector-input']` | adaptive-logs-lj | `stream-selector-input`<br>**❌ absent** 2026-08-06: absent on Logs Drilldown landing — stale, re-record<br>confirmed absent on Logs Drilldown landing, live 2026-08-06 |
| `a[aria-label='Select detected_level']` | drilldown-logs-lj/labels-and-fields | `Select detected_level`<br>**❌ absent** 2026-08-06: no `Select *` aria-labels on Drilldown landing — needs re-record deeper in flow<br>confirmed absent on Logs Drilldown landing, live 2026-08-06 |

> [!WARNING]
> 5 tutorials depend on this plugin's existing test ids. Please treat `data-testid`s as part of your public API — do not rename them without pinging the Pathfinder squad first.


---
If you've any questions please reach out in the #proj-pathfinder-selectors slack channel.
