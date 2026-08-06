# Stable selectors for Grafana Pathfinder tutorials (4 anchors, 2 tutorials)

[Pathfinder](https://grafana.com/docs/learning-journeys/) tutorials anchor steps to DOM selectors, and the ones below target UI this plugin renders (audit: grafana/grafana#129672). Weak anchors (text/placeholder/positional) break silently when copy or layout changes.

## Add a `data-testid` (4)

Any value works — we'll retarget the tutorials to whatever you pick.

| element (current weak anchor) | tutorials | where (at 2026-08-04/05) |
|---|---|---|
| `div[aria-label='Generated SQL query']` | semantic-layer-tutorial | `src/components/SQLPreview.tsx:99`<br>`src/components/RawSQL.tsx:26` |
| `#pageContent button:contains('Files')` | semantic-layer-data-model-config | `src/components/DataModelConfigPage.test.tsx:178`<br>_low confidence (matched `Files`)_ |
| `div[aria-label="Generated SQL query"]:contains('payment_method')` | semantic-layer-tutorial | `src/components/SQLPreview.tsx:99`<br>`src/components/RawSQL.tsx:26` |
| `input[aria-label='Dimensions']` | semantic-layer-tutorial | `src/components/JsonQueryViewer.tsx:67`<br>`src/components/JsonQueryViewer.tsx:68` |


---
If you've any questions please reach out in the #proj-pathfinder-selectors slack channel.
