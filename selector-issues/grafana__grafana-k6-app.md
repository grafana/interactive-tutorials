# Stable selectors for Grafana Pathfinder tutorials (1 anchor, 1 tutorial)

[Pathfinder](https://grafana.com/docs/learning-journeys/) tutorials anchor their steps to DOM selectors. We've identified that the guides mentioned below target UI this plugin renders (audit: grafana/grafana#129672). Weak anchors (text/placeholder/positional) break silently when copy or layout changes in your plugin however data-testids give us a more robust path forwards.

## Add `data-testid`s to the following JSX

Any value works — we'll retarget the tutorials to whatever you pick.

| element (current weak anchor) | tutorials | where (at 2026-08-04/05) |
|---|---|---|
| `#secret-description` | how-to-setup-secrets-tutorial | `src/pages/SettingsPage/tabs/SecretsManagementTab/SecretEditModal.tsx:274`<br>`src/pages/SettingsPage/tabs/SecretsManagementTab/SecretEditModal.tsx:281` |

> [!WARNING]
> 1 tutorial depend on this plugin's existing test ids. Please treat `data-testid`s as part of your public API — do not rename them without pinging the Pathfinder squad first.


---
If you've any questions please reach out in the #proj-pathfinder-selectors slack channel.
