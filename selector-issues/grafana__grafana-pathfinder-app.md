# Stable selectors for Grafana Pathfinder tutorials (2 anchors, 3 tutorials)

[Pathfinder](https://grafana.com/docs/learning-journeys/) tutorials anchor their steps to DOM selectors. We've identified that the guides mentioned below target UI this plugin renders (audit: grafana/grafana#129672). Weak anchors (text/placeholder/positional) break silently when copy or layout changes in your plugin however data-testids give us a more robust path forwards.

## Add `data-testid`s to the following JSX

Any value works — we'll retarget the tutorials to whatever you pick.

| element (current weak anchor) | tutorials | where (at 2026-08-04/05) |
|---|---|---|
| `#dev-mode` | enable-block-editor, enable-coda | `src/integrations/assistant-integration/AssistantCustomizable.tsx:12`<br>`src/integrations/assistant-integration/AssistantCustomizable.tsx:13` |
| `button[aria-label='Expand terminal']` | fleet-management-onboarding | `src/integrations/coda/TerminalPanel.tsx:430`<br>`src/integrations/coda/TerminalPanel.tsx:449` |

> [!WARNING]
> 2 tutorials depend on this plugin's existing test ids. Please treat `data-testid`s as part of your public API — do not rename them without pinging the Pathfinder squad first.


---
If you've any questions please reach out in the #proj-pathfinder-selectors slack channel.
