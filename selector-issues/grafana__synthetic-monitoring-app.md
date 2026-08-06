# Stable selectors for Grafana Pathfinder tutorials (15 anchors, 6 tutorials)

[Pathfinder](https://grafana.com/docs/learning-journeys/) tutorials anchor their steps to DOM selectors. We've identified that the guides mentioned below target UI this plugin renders (audit: grafana/grafana#129672). Weak anchors (text/placeholder/positional) break silently when copy or layout changes in your plugin however data-testids give us a more robust path forwards.

## Add `data-testid`s to the following JSX

Any value works — we'll retarget the tutorials to whatever you pick.

| element (current weak anchor) | tutorials | where (at 2026-08-04/05) |
|---|---|---|
| `button:contains('Save')` | how-to-setup-secrets-tutorial | `src/components/Checkster/components/form/FormRoot.tsx:110`<br>_low confidence (matched `Save`)_ |
| `#secret-name` | how-to-setup-secrets-tutorial | `src/page/ConfigPageLayout/tabs/SecretsManagementTab/SecretEditModal.tsx:177`<br>`src/page/ConfigPageLayout/tabs/SecretsManagementTab/SecretEditModal.tsx:184` |
| `[aria-label="timeout seconds input"]` | sm-dns-check-tutorial, sm-tcp-check-tutorial | _component not located by search — the value only appears in test/fixture files or is built dynamically; you'll know the component_ |
| `input[name='target'][placeholder='grafana.com']` | detect-outages-synthetic-monitoring-lj/create-ping-check, sm-ping-check-tutorial | `src/configPage/PluginConfigPage/PluginConfigPage.tsx:110`<br>`src/features/tracking/TrackingIdentity.tsx:11` |
| `input[placeholder='name']` | sm-dns-check-tutorial, sm-tcp-check-tutorial | `src/services/featureFlags.ts:6`<br>`src/services/featureFlags.ts:10` |
| `input[placeholder='value']` | sm-dns-check-tutorial, sm-tcp-check-tutorial | `src/services/featureFlags.ts:22`<br>`src/services/featureFlags.ts:53` |
| `[aria-label="Query to send 1"]` | sm-tcp-check-tutorial | _component not located by search — the value only appears in test/fixture files or is built dynamically; you'll know the component_ |
| `[aria-label="Response to expect 1"]` | sm-tcp-check-tutorial | _component not located by search — the value only appears in test/fixture files or is built dynamically; you'll know the component_ |
| `[name="target"]` | sm-dns-check-tutorial | `src/services/featureFlags.ts:44`<br>`src/data/useLatency.ts:14` |
| `[name='target']` | sm-tcp-check-tutorial | `src/services/featureFlags.ts:44`<br>`src/data/useLatency.ts:14` |
| `input[aria-label='Custom labels 1 name']` | sm-ping-check-tutorial | _component not located by search — the value only appears in test/fixture files or is built dynamically; you'll know the component_ |
| `input[aria-label='Custom labels 1 value']` | sm-ping-check-tutorial | _component not located by search — the value only appears in test/fixture files or is built dynamically; you'll know the component_ |
| `label:contains('DNS')` | sm-dns-check-tutorial | `src/scenes/Summary/SummaryTableViz.tsx:383`<br>`src/components/CheckForm/AlertsPerCheck/AlertsPerCheck.constants.tsx:137`<br>_low confidence (matched `DNS`)_ |
| `label:contains('TCP')` | sm-tcp-check-tutorial | `src/scenes/Summary/SummaryTableViz.tsx:392`<br>`src/types.ts:60`<br>_low confidence (matched `TCP`)_ |

## Anchor gone — renamed or removed? (1)

Not found in source, bundle, or a live stack (2026-08-06). Tell us the new selector, or we'll re-record the step.

| anchor | tutorials | searched for |
|---|---|---|
| `[data-testid='frequency-component'] [role='radiogroup'] label:contains('1m')` | sm-scripted-check-tutorial | `src/components/CheckEditor/FormComponents/Frequency.constants.ts:10`<br>`src/components/CheckEditor/FormComponents/Frequency.constants.ts:11`<br>_medium confidence (matched `frequency- …(prefix)`)_<br>**❌ absent** 2026-08-06: absent on ping AND scripted check forms — confirm rename/removal with SM team<br>confirmed absent on ping AND scripted check forms, live 2026-08-06 |

### FYI — we'll retarget these ourselves, just don't rename the replacements (4)

- `[id='pageContent'] a[href='/a/grafana-synthetic-monitoring-app/home']` → link is rendered by Grafana core from plugin.json `includes` — tutorials will retarget to the core `Nav menu item` selector
- `div[data-testid='check-group-card-browser'] a:nth-match(1)` → live testid is now `checks group-card-<type>` — we will retarget the tutorials; please keep the new name stable
- `div[data-testid='check-group-card-scripted'] a:nth-match(1)` → live testid is now `checks group-card-<type>` — we will retarget the tutorials; please keep the new name stable
- `section[data-testid='config-content'] button:nth-match(2)` → live testid is now `config content` — we will retarget the tutorials; please keep the new name stable

> [!WARNING]
> 9 tutorials depend on this plugin's existing test ids. Please treat `data-testid`s as part of your public API — do not rename them without pinging the Pathfinder squad first.


---
If you've any questions please reach out in the #proj-pathfinder-selectors slack channel.
