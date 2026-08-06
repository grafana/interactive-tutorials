# Stable selectors for Grafana Pathfinder tutorials (9 anchors, 5 tutorials)

[Pathfinder](https://grafana.com/docs/learning-journeys/) tutorials anchor their steps to DOM selectors. We've identified that the guides mentioned below target UI this plugin renders (audit: grafana/grafana#129672). Weak anchors (text/placeholder/positional) break silently when copy or layout changes in your plugin however data-testids give us a more robust path forwards.

## Add `data-testid`s to the following JSX

Any value works — we'll retarget the tutorials to whatever you pick.

| element (current weak anchor) | tutorials | where (at 2026-08-04/05) |
|---|---|---|
| `div[role="menu"] button[role="menuitem"]:has(span:contains("Time"))` | rca-demo-ops, rca-demo-v2 | `src/externalComponents/ObservabilityLanding/ObservabilityLanding.tsx:97`<br>`src/features/EntityDetails/components/ServiceEntityOverview/panels/ServiceEntityRelationshipPanel.tsx:151`<br>_low confidence (matched `Time`)_ |
| `div[role='dialog'] div[role='group'] div:contains('Frontend')` | rca-demo-ops, rca-demo-v2 | `src/features/PageEditor/AddWidgetPicker.tsx:19`<br>`src/features/EntityDetails/hooks/useDrawerTabs.tsx:33`<br>_low confidence (matched `Frontend`)_ |
| `div[role='dialog'] div[role='group'] div:contains('Service')` | rca-demo-ops, rca-demo-v2 | `src/services/KgQuality.service.ts:67`<br>_low confidence (matched `Service`)_ |
| `div.text-xs:has(span:contains('Sort By'))` | rca-demo-ops, rca-demo-v2 | `src/features/Assertions/components/AssertionsTopMenuButtons/messages.ts:63`<br>`src/features/Assertions/components/AssertionsSortBy/messages.ts:22`<br>_low confidence (matched `Sort By`)_ |
| `div[role='dialog'] button[type='button']:has(div:contains('Frontend'))` | rca-demo | `src/features/ObservabilityHome/widgets/PromoWidget.tsx:39`<br>`src/features/ObservabilityHome/registry.tsx:95`<br>_low confidence (matched `Frontend`)_ |
| `div[role='dialog'] button[type='button']:has(div:contains('Service'))` | rca-demo | `src/services/KgQuality.service.ts:67`<br>_low confidence (matched `Service`)_ |
| `input[placeholder='Search entity']` | knowledge-graph-guide | `src/features/Catalog/components/CatalogSearchInput.tsx:34` |

## Anchor gone — renamed or removed? (2)

Not found in source, bundle, or a live stack (2026-08-06). Tell us the new selector, or we'll re-record the step.

| anchor | tutorials | searched for |
|---|---|---|
| `button[aria-label='Workbench AI (Preview)']` | rca-demo, rca-demo-ops +1 | `Workbench AI (Preview)` |
| `button[data-testid='select-action-asserts:resource:threshold']` | drilldown-metrics-lj/analyze-data | `select-action-asserts:resource:threshold` |

### FYI — we'll retarget these ourselves, just don't rename the replacements (2)

- `div.grid.wb-item:has(p[data-original='KubePodCrashLooping'])` → existing parameterized test id `wb-list-item-${name}` — src/testIds.ts:77, emitted by src/features/RcaWorkbench/components/EntityRow.tsx:154
- `div.grid.wb-item:has(p:contains('PostgreSQLHighConnections'))` → existing parameterized test id `wb-list-item-${name}` — src/testIds.ts:77, emitted by src/features/RcaWorkbench/components/EntityRow.tsx:154

> [!WARNING]
> 4 tutorials depend on this plugin's existing test ids. Please treat `data-testid`s as part of your public API — do not rename them without pinging the Pathfinder squad first.


---
If you've any questions please reach out in the #proj-pathfinder-selectors slack channel.
