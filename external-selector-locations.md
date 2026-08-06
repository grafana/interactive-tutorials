# External weak selectors — where data-testids need adding in plugin repos

Generated 2026-08-05. Cross-reference of the 481 `external` rows in
[interactive-tutorials selector-migration-map.json] against the plugin source clones in
`react-detect-plugins/plugins/` (clone HEADs verified fresh, 2026-08-04/05).

296 unique (owner, selector) pairs. Classification:

- **ADD data-testid** — weak anchor (text/aria/placeholder/class) located in plugin source at file:line; add a `data-testid` there.
- **MISSING from source** — the anchor value does not exist anywhere in the current clone (src or dist): the guide anchor is stale or was never shipped; re-record or add the attribute.
- **testid already in source** — the guide already targets a `data-testid`/`data-cy` the plugin emits; no code change strictly needed, but worth registering as a stable contract so it isn't renamed.
- **found in dist only** — attribute present in the built bundle but not in `src/` (generated or dependency-emitted).
- **structural/positional** — no greppable anchor; needs a human/live DOM.

## Summary by plugin

| plugin | rows | ADD testid | missing | testid exists | dist-only | structural |
|---|---|---|---|---|---|---|
| grafana-synthetic-monitoring-app | 48 | 15 | 5 | 25 | 0 | 3 |
| grafana-asserts-app | 57 | 9 | 2 | 43 | 1 | 2 |
| grafana-collector-app | 28 | 3 | 5 | 12 | 8 | 0 |
| grafana-slo-app | 20 | 6 | 1 | 12 | 1 | 0 |
| grafana-easystart-app | 16 | 2 | 3 | 11 | 0 | 0 |
| grafana-adaptive-metrics-app | 6 | 4 | 0 | 2 | 0 | 0 |
| grafana-cube-datasource | 4 | 4 | 0 | 0 | 0 | 0 |
| grafana-github-datasource | 3 | 3 | 0 | 0 | 0 | 0 |
| grafana-irm-app | 29 | 2 | 1 | 26 | 0 | 0 |
| grafana-lokiexplore-app | 12 | 1 | 2 | 9 | 0 | 0 |
| grafana-pathfinder-app | 9 | 2 | 1 | 5 | 0 | 1 |
| grafana-pdc-app | 3 | 3 | 0 | 0 | 0 | 0 |
| k6-app | 4 | 1 | 2 | 1 | 0 | 0 |
| mysql | 3 | 3 | 0 | 0 | 0 | 0 |
| grafana-adaptivelogs-app | 2 | 2 | 0 | 0 | 0 | 0 |
| grafana-app-observability-app | 5 | 2 | 0 | 3 | 0 | 0 |
| grafana-oncall-app | 2 | 2 | 0 | 0 | 0 | 0 |
| plugin-ui | 2 | 2 | 0 | 0 | 0 | 0 |
| grafana-assistant-app | 1 | 1 | 0 | 0 | 0 | 0 |
| grafana-exploretraces-app | 1 | 1 | 0 | 0 | 0 | 0 |
| grafana-metricsdrilldown-app | 4 | 1 | 0 | 2 | 0 | 1 |
| volkovlabs-rss-datasource | 1 | 1 | 0 | 0 | 0 | 0 |
| yesoreyeram-infinity-datasource | 9 | 0 | 1 | 7 | 0 | 1 |
| grafana-demodashboards-app | 1 | 0 | 0 | 1 | 0 | 0 |
| grafana-k8s-app | 1 | 0 | 0 | 0 | 1 | 0 |
| loki | 1 | 0 | 0 | 0 | 1 | 0 |
| tempo | 1 | 0 | 0 | 0 | 0 | 1 |

Not covered: 23 rows with no clone in the registry set (RCA workbench demo app, grafana-enterprise, instance content, @grafana/scenes internals).

## grafana-synthetic-monitoring-app

### ADD data-testid (15)

| selector | action | guides | evidence |
|---|---|---|---|
| `[id='pageContent'] a[href='/a/grafana-synthetic-monitoring-app/home']` | highlight | detect-outages-synthetic-monitoring-lj/navigate-to-synthetic-monitoring, sm-dns-check-tutorial, sm-ping-check-tutorial +2 | `grafana-synthetic-monitoring-app/src/plugin.json:46` |
| `button:contains('Save')` | highlight x3 | how-to-setup-secrets-tutorial | `grafana-synthetic-monitoring-app/src/components/Checkster/components/form/FormRoot.tsx:110` (low confidence, token `Save`) |
| `#secret-name` | formfill x2 | how-to-setup-secrets-tutorial | `grafana-synthetic-monitoring-app/src/page/ConfigPageLayout/tabs/SecretsManagementTab/SecretEditModal.tsx:177`; `grafana-synthetic-monitoring-app/src/page/ConfigPageLayout/tabs/SecretsManagementTab/SecretEditModal.tsx:184` |
| `[aria-label="timeout seconds input"]` | formfill | sm-dns-check-tutorial, sm-tcp-check-tutorial | `grafana-synthetic-monitoring-app/src/page/NewCheck/__tests__/v2/NewCheckV2.journey.test.tsx:244` |
| `input[name='target'][placeholder='grafana.com']` | formfill | detect-outages-synthetic-monitoring-lj/create-ping-check, sm-ping-check-tutorial | `grafana-synthetic-monitoring-app/src/configPage/PluginConfigPage/PluginConfigPage.tsx:110`; `grafana-synthetic-monitoring-app/src/features/tracking/TrackingIdentity.tsx:11` |
| `input[placeholder='name']` | formfill | sm-dns-check-tutorial, sm-tcp-check-tutorial | `grafana-synthetic-monitoring-app/src/services/featureFlags.ts:6`; `grafana-synthetic-monitoring-app/src/services/featureFlags.ts:10` |
| `input[placeholder='value']` | formfill | sm-dns-check-tutorial, sm-tcp-check-tutorial | `grafana-synthetic-monitoring-app/src/services/featureFlags.ts:22`; `grafana-synthetic-monitoring-app/src/services/featureFlags.ts:53` |
| `[aria-label="Query to send 1"]` | formfill | sm-tcp-check-tutorial | `grafana-synthetic-monitoring-app/src/page/NewCheck/__tests__/v2/apiEndpointChecks/tcpCheck/2-defineUptime.payload.test.tsx:38` |
| `[aria-label="Response to expect 1"]` | formfill | sm-tcp-check-tutorial | `grafana-synthetic-monitoring-app/src/page/NewCheck/__tests__/v2/apiEndpointChecks/tcpCheck/2-defineUptime.payload.test.tsx:39` |
| `[name="target"]` | formfill | sm-dns-check-tutorial | `grafana-synthetic-monitoring-app/src/services/featureFlags.ts:44`; `grafana-synthetic-monitoring-app/src/data/useLatency.ts:14` |
| `[name='target']` | formfill | sm-tcp-check-tutorial | `grafana-synthetic-monitoring-app/src/services/featureFlags.ts:44`; `grafana-synthetic-monitoring-app/src/data/useLatency.ts:14` |
| `input[aria-label='Custom labels 1 name']` | formfill | sm-ping-check-tutorial | `grafana-synthetic-monitoring-app/src/page/NewCheck/__tests__/v2/scriptedChecks/scripted/3-labels.payload.test.tsx:32` |
| `input[aria-label='Custom labels 1 value']` | formfill | sm-ping-check-tutorial | `grafana-synthetic-monitoring-app/src/page/NewCheck/__tests__/v2/apiEndpointChecks/CommonFields.payload.test.tsx:73` |
| `label:contains('DNS')` | highlight | sm-dns-check-tutorial | `grafana-synthetic-monitoring-app/src/scenes/Summary/SummaryTableViz.tsx:383`; `grafana-synthetic-monitoring-app/src/components/CheckForm/AlertsPerCheck/AlertsPerCheck.constants.tsx:137` (low confidence, token `DNS`) |
| `label:contains('TCP')` | highlight | sm-tcp-check-tutorial | `grafana-synthetic-monitoring-app/src/scenes/Summary/SummaryTableViz.tsx:392`; `grafana-synthetic-monitoring-app/src/types.ts:60` (low confidence, token `TCP`) |

### MISSING from source (stale anchor?) (5)

| selector | action | guides | evidence |
|---|---|---|---|
| `a[href='/a/grafana-synthetic-monitoring-app/checks/new/api-endpoint']` | highlight | detect-outages-synthetic-monitoring-lj/create-ping-check, sm-dns-check-tutorial, sm-ping-check-tutorial +2 | searched `/a/grafana-synthetic-monitoring-app/checks/new/api` — no hit in src or dist |
| `input[data-testid='checkEditor alerts ProbeFailedExecutionsTooHigh selectedCheckbox']` | highlight | sm-dns-check-tutorial, sm-ping-check-tutorial, sm-setting-up-your-first-check +1 | searched `checkEditor alerts ProbeFailedExecutionsTooHigh se` — no hit in src or dist |
| `div[data-testid='check-group-card-browser'] a:nth-match(1)` | highlight | how-to-setup-secrets-tutorial | searched `check-group-card-browser` — no hit in src or dist |
| `div[data-testid='check-group-card-scripted'] a:nth-match(1)` | highlight | sm-scripted-check-tutorial | searched `check-group-card-scripted` — no hit in src or dist |
| `section[data-testid='config-content'] button:nth-match(2)` | highlight | how-to-setup-secrets-tutorial | searched `config-content` — no hit in src or dist |

### structural/positional — needs human (3)

| selector | action | guides | evidence |
|---|---|---|---|
| `label:contains('1m')` | highlight | detect-outages-synthetic-monitoring-lj/select-probe-locations | searched `—` — no hit in src or dist |
| `label[for^='option-ping-radiogroup-']` | highlight | detect-outages-synthetic-monitoring-lj/create-ping-check | searched `—` — no hit in src or dist |
| `label[title='Check a host for availability and response time.']` | highlight | sm-ping-check-tutorial | searched `—` — no hit in src or dist |

### testid already in source (25)

| selector | action | guides | evidence |
|---|---|---|---|
| `input[data-testid='checkEditor form job']` | formfill | detect-outages-synthetic-monitoring-lj/create-ping-check, how-to-setup-secrets-tutorial, sm-dns-check-tutorial +4 | `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:63` |
| `a[data-testid='action create check']` | highlight | detect-outages-synthetic-monitoring-lj/create-ping-check, sm-dns-check-tutorial, sm-ping-check-tutorial +3 | `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:6` |
| `button[data-testid='checkEditor form submit']` | highlight | detect-outages-synthetic-monitoring-lj/select-probe-locations, how-to-setup-secrets-tutorial, sm-dns-check-tutorial +3 | `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:61` |
| `button[data-testid='checkEditor navigation execution']` | highlight | detect-outages-synthetic-monitoring-lj/select-probe-locations, how-to-setup-secrets-tutorial, sm-dns-check-tutorial +3 | `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:47`; `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:48` (medium confidence, token `checkEditor navigation …(prefix)`) |
| `button[data-testid='checkEditor feat-adhoc-check testButton']` | highlight | sm-dns-check-tutorial, sm-ping-check-tutorial, sm-setting-up-your-first-check +1 | `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:86` |
| `button[data-testid='checkEditor navigation alerting']` | highlight | sm-dns-check-tutorial, sm-ping-check-tutorial, sm-setting-up-your-first-check +1 | `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:47`; `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:48` (medium confidence, token `checkEditor navigation …(prefix)`) |
| `button[data-testid='checkEditor navigation labels']` | highlight | sm-dns-check-tutorial, sm-ping-check-tutorial, sm-setting-up-your-first-check +1 | `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:47`; `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:48` (medium confidence, token `checkEditor navigation …(prefix)`) |
| `button[data-testid='checkEditor navigation uptime']` | highlight | sm-dns-check-tutorial, sm-ping-check-tutorial, sm-setting-up-your-first-check +1 | `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:47`; `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:48` (medium confidence, token `checkEditor navigation …(prefix)`) |
| `label[data-testid='checkEditor form probeLabel']:first-of-type` | highlight | sm-dns-check-tutorial, sm-ping-check-tutorial, sm-setting-up-your-first-check +1 | `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:69` |
| `[data-testid='checkEditor form'] > div:last-child > div:last-child  button[type='button']` | button x3 | sm-scripted-check-tutorial | `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:56`; `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:60` |
| `[data-testid='checkEditor genericLabelContent']` | highlight | sm-scripted-check-tutorial, sm-setting-up-your-first-check | `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:76` |
| `input[data-testid='checkEditor form instance']` | formfill | how-to-setup-secrets-tutorial, sm-setting-up-your-first-check | `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:64` |
| `[aria-labelledby='form-section-alerting'] [data-testid='checkEditor formTabs content']` | highlight | sm-scripted-check-tutorial | `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:56` |
| `[data-testid='action create check']` | highlight | how-to-setup-secrets-tutorial | `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:6` |
| `[data-testid='checkEditor form'] > div:last-child button[type='button']` | button | sm-scripted-check-tutorial | `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:56`; `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:60` |
| `[data-testid='frequency-component'] [role='radiogroup'] label:contains('1m')` | highlight | sm-scripted-check-tutorial | `grafana-synthetic-monitoring-app/src/components/CheckEditor/FormComponents/Frequency.constants.ts:10`; `grafana-synthetic-monitoring-app/src/components/CheckEditor/FormComponents/Frequency.constants.ts:11` (medium confidence, token `frequency- …(prefix)`) |
| `[data-testid='timepoint-viewer']` | highlight | detect-outages-synthetic-monitoring-lj/view-check-dashboard | `grafana-synthetic-monitoring-app/src/scenes/components/TimepointExplorer/TimepointViewer.tsx:160` |
| `div[data-testid='input-wrapper'] input[data-testid='checkEditor form instance']` | formfill | sm-scripted-check-tutorial | `grafana-synthetic-monitoring-app/src/page/ConfigPageLayout/tabs/SecretsManagementTab/SecretsManagementUI.test.tsx:233` |
| `div[data-testid='timepoint-list']` | highlight | detect-outages-synthetic-monitoring-lj/view-check-dashboard | `grafana-synthetic-monitoring-app/src/scenes/components/TimepointExplorer/TimepointExplorer.constants.ts:10`; `grafana-synthetic-monitoring-app/src/scenes/components/TimepointExplorer/TimepointExplorer.constants.ts:11` |
| `form[data-testid='checkEditor form']` | highlight | sm-ping-check-tutorial | `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:56`; `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:60` |
| `form[data-testid='checkEditor form'] button[data-testid='checkEditor form submit']` | button | sm-scripted-check-tutorial | `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:56`; `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:60` |
| `form[data-testid='checkEditor form'] div[data-testid='timeout']` | highlight | sm-scripted-check-tutorial | `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:56`; `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:60` |
| `form[data-testid='checkEditor form'] label:nth-match(47)` | highlight | sm-scripted-check-tutorial | `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:56`; `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:60` |
| `form[data-testid='checkEditor form'] label:nth-match(5)` | highlight | how-to-setup-secrets-tutorial | `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:56`; `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:60` |
| `input[data-testid='checkEditor form validStatusCodes']` | highlight | sm-setting-up-your-first-check | `grafana-synthetic-monitoring-app/src/test/dataTestIds.ts:67` |

## grafana-asserts-app

### ADD data-testid (9)

| selector | action | guides | evidence |
|---|---|---|---|
| `div.grid.wb-item:has(p[data-original='KubePodCrashLooping'])` | highlight | rca-demo, rca-demo-ops, rca-demo-v2 | `grafana-asserts-app/src/features/Assertions/hooks/useProvideAssistantContext.ts:75` |
| `div.grid.wb-item:has(p:contains('PostgreSQLHighConnections'))` | highlight | rca-demo, rca-demo-ops, rca-demo-v2 | `grafana-asserts-app/src/test/fixtures/k8s_cluster_entity.ts:91` (low confidence, token `PostgreSQLHighConnections`) |
| `div[role="menu"] button[role="menuitem"]:has(span:contains("Time"))` | highlight | rca-demo-ops, rca-demo-v2 | `grafana-asserts-app/src/externalComponents/ObservabilityLanding/ObservabilityLanding.tsx:97`; `grafana-asserts-app/src/features/EntityDetails/components/ServiceEntityOverview/panels/ServiceEntityRelationshipPanel.tsx:151` (low confidence, token `Time`) |
| `div[role='dialog'] div[role='group'] div:contains('Frontend')` | highlight | rca-demo-ops, rca-demo-v2 | `grafana-asserts-app/src/features/PageEditor/AddWidgetPicker.tsx:19`; `grafana-asserts-app/src/features/EntityDetails/hooks/useDrawerTabs.tsx:33` (low confidence, token `Frontend`) |
| `div[role='dialog'] div[role='group'] div:contains('Service')` | highlight | rca-demo-ops, rca-demo-v2 | `grafana-asserts-app/src/services/KgQuality.service.ts:67` (low confidence, token `Service`) |
| `div.text-xs:has(span:contains('Sort By'))` | highlight | rca-demo-ops, rca-demo-v2 | `grafana-asserts-app/src/features/Assertions/components/AssertionsTopMenuButtons/messages.ts:63`; `grafana-asserts-app/src/features/Assertions/components/AssertionsSortBy/messages.ts:22` (low confidence, token `Sort By`) |
| `div[role='dialog'] button[type='button']:has(div:contains('Frontend'))` | hover | rca-demo | `grafana-asserts-app/src/features/ObservabilityHome/widgets/PromoWidget.tsx:39`; `grafana-asserts-app/src/features/ObservabilityHome/registry.tsx:95` (low confidence, token `Frontend`) |
| `div[role='dialog'] button[type='button']:has(div:contains('Service'))` | hover | rca-demo | `grafana-asserts-app/src/services/KgQuality.service.ts:67` (low confidence, token `Service`) |
| `input[placeholder='Search entity']` | highlight | knowledge-graph-guide | `grafana-asserts-app/src/features/Catalog/components/CatalogSearchInput.tsx:34` |

### MISSING from source (stale anchor?) (2)

| selector | action | guides | evidence |
|---|---|---|---|
| `button[aria-label='Workbench AI (Preview)']` | highlight | rca-demo, rca-demo-ops, rca-demo-v2 | searched `Workbench AI (Preview)` — no hit in src or dist |
| `button[data-testid='select-action-asserts:resource:threshold']` | highlight | drilldown-metrics-lj/analyze-data | searched `select-action-asserts:resource:threshold` — no hit in src or dist |

### found in dist only (1)

| selector | action | guides | evidence |
|---|---|---|---|
| `div[data-testid="data-testid panel content"] div[role="button"]:has(span:contains("1"))` | highlight | rca-demo-ops, rca-demo-v2 | `grafana-asserts-app/dist/7805.js:2`; `grafana-asserts-app/dist/6054.js:2` (medium confidence, token `data-testid panel content`) |

### structural/positional — needs human (2)

| selector | action | guides | evidence |
|---|---|---|---|
| `div.h-full.w-full.overflow-y-scroll.block` | highlight | rca-demo, rca-demo-ops, rca-demo-v2 | searched `—` — no hit in src or dist |
| `div[role="grid"] div[role="row"][aria-rowindex="2"] div.cell-link` | highlight | rca-demo-ops, rca-demo-v2 | searched `—` — no hit in src or dist |

### testid already in source (43)

| selector | action | guides | evidence |
|---|---|---|---|
| `div[data-cy='wb-list-item']:has(p:contains('frontend'))` | highlight x2, hover/highlight, hover | rca-demo, rca-demo-ops, rca-demo-v2 | `grafana-asserts-app/src/features/RcaWorkbench/components/EntityRow.tsx:154`; `grafana-asserts-app/src/features/Assertions/components/AssertionsListItemWrap/AssertionsListItemWrap.component.tsx:158` |
| `div[data-cy='wb-list-item']:has(p:contains('FeatureFlagStateChange'))` | highlight, hover | rca-demo, rca-demo-ops, rca-demo-v2 | `grafana-asserts-app/src/features/RcaWorkbench/components/EntityRow.tsx:154`; `grafana-asserts-app/src/features/Assertions/components/AssertionsListItemWrap/AssertionsListItemWrap.component.tsx:158` |
| `div[data-cy='wb-list-item']:has(p:contains('failure'))` | highlight x2 | rca-demo, rca-demo-ops, rca-demo-v2 | `grafana-asserts-app/src/features/RcaWorkbench/components/EntityRow.tsx:154`; `grafana-asserts-app/src/features/Assertions/components/AssertionsListItemWrap/AssertionsListItemWrap.component.tsx:158` |
| `div[data-cy='wb-list-item']:has(p:contains('productcatalog-postgres'))` | highlight/highlight x2/highlight, hover | rca-demo, rca-demo-ops, rca-demo-v2 | `grafana-asserts-app/src/features/RcaWorkbench/components/EntityRow.tsx:154`; `grafana-asserts-app/src/features/Assertions/components/AssertionsListItemWrap/AssertionsListItemWrap.component.tsx:158` |
| `div[data-cy='wb-list-item']:has(p:contains('productcatalogservice'))` | highlight/highlight x2/highlight, hover | rca-demo, rca-demo-ops, rca-demo-v2 | `grafana-asserts-app/src/features/RcaWorkbench/components/EntityRow.tsx:154`; `grafana-asserts-app/src/features/Assertions/components/AssertionsListItemWrap/AssertionsListItemWrap.component.tsx:158` |
| `div[data-cy='wb-list-item']:has(p:contains('flagd'))` | highlight/highlight x2 | rca-demo, rca-demo-ops, rca-demo-v2 | `grafana-asserts-app/src/features/RcaWorkbench/components/EntityRow.tsx:154`; `grafana-asserts-app/src/features/Assertions/components/AssertionsListItemWrap/AssertionsListItemWrap.component.tsx:158` |
| `div[data-cy='entity-list-item']:has(p:contains('frontendproxy'))` | highlight/hover | rca-demo, rca-demo-ops, rca-demo-v2 | `grafana-asserts-app/src/features/Entities/components/EntityListItem/EntityListItem.component.tsx:93`; `grafana-asserts-app/src/features/Entities/components/EntityListItem/EntityListItem.component.tsx:95` |
| `div[data-cy='wb-list-item']:has(p:contains('FeatureFlagStateChange')) button:nth-of-typ...` | hover | rca-demo, rca-demo-ops, rca-demo-v2 | `grafana-asserts-app/src/features/RcaWorkbench/components/EntityRow.tsx:154`; `grafana-asserts-app/src/features/Assertions/components/AssertionsListItemWrap/AssertionsListItemWrap.component.tsx:158` |
| `div[data-cy='wb-list-item']:has(p:contains('PostgreSQLHighConnections'))` | highlight | rca-demo, rca-demo-ops, rca-demo-v2 | `grafana-asserts-app/src/features/RcaWorkbench/components/EntityRow.tsx:154`; `grafana-asserts-app/src/features/Assertions/components/AssertionsListItemWrap/AssertionsListItemWrap.component.tsx:158` |
| `div[data-cy='wb-list-item']:has(p:contains('amend'))` | highlight | rca-demo, rca-demo-ops, rca-demo-v2 | `grafana-asserts-app/src/features/Assertions/components/AssertionsListItemWrap/AssertionsListItemWrap.component.tsx:158`; `grafana-asserts-app/src/features/Assertions/components/AssertionsListItemWrap/AssertionsListItemWrap.component.tsx:171` |
| `div[data-cy='wb-list-item']:has(p:contains('anomaly'))` | highlight | rca-demo, rca-demo-ops, rca-demo-v2 | `grafana-asserts-app/src/features/RcaWorkbench/components/EntityRow.tsx:154`; `grafana-asserts-app/src/features/Assertions/components/AssertionsListItemWrap/AssertionsListItemWrap.component.tsx:158` |
| `div[data-cy='wb-list-item']:has(p:contains('frontend')) button:nth-of-type(3)` | highlight/hover | rca-demo, rca-demo-ops, rca-demo-v2 | `grafana-asserts-app/src/features/RcaWorkbench/components/EntityRow.tsx:154`; `grafana-asserts-app/src/features/Assertions/components/AssertionsListItemWrap/AssertionsListItemWrap.component.tsx:158` |
| `div[data-cy='wb-list-item']:has(p[data-original='KubePodCrashLooping'])` | highlight | rca-demo, rca-demo-ops, rca-demo-v2 | `grafana-asserts-app/src/features/RcaWorkbench/components/EntityRow.tsx:154`; `grafana-asserts-app/src/features/Assertions/components/AssertionsListItemWrap/AssertionsListItemWrap.component.tsx:158` |
| `div[data-cy='wb-list-item']:has(p[data-original='outbound - grpc.oteldemo.ProductCatalo...` | highlight | rca-demo, rca-demo-ops, rca-demo-v2 | `grafana-asserts-app/src/features/RcaWorkbench/components/EntityRow.tsx:154`; `grafana-asserts-app/src/features/Assertions/components/AssertionsListItemWrap/AssertionsListItemWrap.component.tsx:158` |
| `div[role='dialog'] div[data-cy='entity-list-item']:has(p:contains('frontend-client'))` | hover | rca-demo, rca-demo-ops, rca-demo-v2 | `grafana-asserts-app/src/features/Entities/components/EntityListItem/EntityListItem.component.tsx:93`; `grafana-asserts-app/src/features/Entities/components/EntityListItem/EntityListItem.component.tsx:95` |
| `div[role='dialog'] div[data-cy='entity-list-item']:has(p:contains('frontend-client')) b...` | highlight/hover | rca-demo, rca-demo-ops, rca-demo-v2 | `grafana-asserts-app/src/features/Entities/components/EntityListItem/EntityListItem.component.tsx:93`; `grafana-asserts-app/src/features/Entities/components/EntityListItem/EntityListItem.component.tsx:95` |
| `div[data-cy='wb-list-item']:has(p:contains('checkoutservice')):nth-match(1)` | hover | rca-demo-ops, rca-demo-v2 | `grafana-asserts-app/src/features/RcaWorkbench/components/EntityRow.tsx:154`; `grafana-asserts-app/src/features/Assertions/components/AssertionsListItemWrap/AssertionsListItemWrap.component.tsx:158` |
| `div[data-cy='wb-list-item']:has(p:contains('checkoutservice')):nth-match(1) button:nth-...` | highlight/hover | rca-demo-ops, rca-demo-v2 | `grafana-asserts-app/src/features/RcaWorkbench/components/EntityRow.tsx:154`; `grafana-asserts-app/src/features/Assertions/components/AssertionsListItemWrap/AssertionsListItemWrap.component.tsx:158` |
| `div[data-cy='wb-list-item']:has(p:contains('frontend')):nth-match(1)` | highlight, hover | knowledge-graph-guide | `grafana-asserts-app/src/features/RcaWorkbench/components/EntityRow.tsx:154`; `grafana-asserts-app/src/features/Assertions/components/AssertionsListItemWrap/AssertionsListItemWrap.component.tsx:158` |
| `div[data-cy='wb-list-item']:has(p:contains('productcatalog-postgres')):nth-match(1)` | hover | rca-demo-ops, rca-demo-v2 | `grafana-asserts-app/src/features/RcaWorkbench/components/EntityRow.tsx:154`; `grafana-asserts-app/src/features/Assertions/components/AssertionsListItemWrap/AssertionsListItemWrap.component.tsx:158` |
| `div[data-cy='wb-list-item']:has(p:contains('productcatalog-postgres')):nth-match(1) but...` | highlight/hover | rca-demo-ops, rca-demo-v2 | `grafana-asserts-app/src/features/RcaWorkbench/components/EntityRow.tsx:154`; `grafana-asserts-app/src/features/Assertions/components/AssertionsListItemWrap/AssertionsListItemWrap.component.tsx:158` |
| `div[data-cy='wb-list-item']:has(p:contains('productcatalogservice')):nth-match(1)` | hover | rca-demo-ops, rca-demo-v2 | `grafana-asserts-app/src/features/RcaWorkbench/components/EntityRow.tsx:154`; `grafana-asserts-app/src/features/Assertions/components/AssertionsListItemWrap/AssertionsListItemWrap.component.tsx:158` |
| `div[data-cy='wb-list-item']:has(p:contains('productcatalogservice')):nth-match(1) butto...` | hover | rca-demo-ops, rca-demo-v2 | `grafana-asserts-app/src/features/RcaWorkbench/components/EntityRow.tsx:154`; `grafana-asserts-app/src/features/Assertions/components/AssertionsListItemWrap/AssertionsListItemWrap.component.tsx:158` |
| `[data-testid='entity-drawer-apps-tab-serviceOverview']` | button, highlight | knowledge-graph-guide | `grafana-asserts-app/src/features/EntityDetails/hooks/useDrawerTabs.tsx:147` (medium confidence, token `entity-drawer-apps-tab- …(prefix)`) |
| `[data-testid='entity-drawer-logs-tab']` | button x2 | knowledge-graph-guide | `grafana-asserts-app/src/testIds.ts:347` |
| `[data-testid='entity-drawer-overview-tab']` | button x2 | knowledge-graph-guide | `grafana-asserts-app/src/testIds.ts:348` |
| `label:has([data-testid='catalog-type-Service-radio'])` | highlight x2 | knowledge-graph-guide | `grafana-asserts-app/src/features/Catalog/components/filters/CatalogTypeFilter.tsx:140`; `grafana-asserts-app/src/testIds.ts:101` (medium confidence, token `catalog-type- …(prefix)`) |
| `[data-testid='entity-drawer-traces-tab']` | button x2 | knowledge-graph-guide | `grafana-asserts-app/src/testIds.ts:354` |
| `div[data-cy='wb-list-item']:has(p:contains('checkoutservice'))` | hover | rca-demo | `grafana-asserts-app/src/features/RcaWorkbench/components/EntityRow.tsx:154`; `grafana-asserts-app/src/features/Assertions/components/AssertionsListItemWrap/AssertionsListItemWrap.component.tsx:158` |
| `div[data-cy='wb-list-item']:has(p:contains('checkoutservice')) button:nth-of-type(4)` | hover | rca-demo | `grafana-asserts-app/src/features/RcaWorkbench/components/EntityRow.tsx:154`; `grafana-asserts-app/src/features/Assertions/components/AssertionsListItemWrap/AssertionsListItemWrap.component.tsx:158` |
| `div[data-cy='wb-list-item']:has(p:contains('productcatalog-postgres')) button:nth-of-ty...` | hover | rca-demo | `grafana-asserts-app/src/features/RcaWorkbench/components/EntityRow.tsx:154`; `grafana-asserts-app/src/features/Assertions/components/AssertionsListItemWrap/AssertionsListItemWrap.component.tsx:158` |
| `div[data-cy='wb-list-item']:has(p:contains('productcatalogservice')) button:nth-of-type(4)` | hover | rca-demo | `grafana-asserts-app/src/features/Assertions/components/AssertionsListItemWrap/AssertionsListItemWrap.component.tsx:158`; `grafana-asserts-app/src/features/Assertions/components/AssertionsListItemWrap/AssertionsListItemWrap.component.tsx:171` |
| `[data-testid='assertions-graph-tab']` | highlight | knowledge-graph-guide | `grafana-asserts-app/src/testIds.ts:28` |
| `[data-testid='assertions-mindmap-tab']` | highlight | knowledge-graph-guide | `grafana-asserts-app/src/testIds.ts:40` |
| `[data-testid='assertions-summary-tab']` | highlight | knowledge-graph-guide | `grafana-asserts-app/src/testIds.ts:51` |
| `[data-testid='catalog-entity-name-btn']:nth-match(1)` | highlight | knowledge-graph-guide | `grafana-asserts-app/src/testIds.ts:95` |
| `[data-testid='empty-assertions-top-services-link']` | highlight | knowledge-graph-guide | `grafana-asserts-app/src/testIds.ts:64` |
| `[data-testid='entity-drawer-kpis-tab']` | button | knowledge-graph-guide | `grafana-asserts-app/src/testIds.ts:346` |
| `button[data-testid='assertions-timeline-tab']` | highlight | knowledge-graph-guide | `grafana-asserts-app/src/testIds.ts:53` |
| `div[data-cy='wb-list-item']:has(p:contains('frontend')):nth-match(1) [data-testid='asse...` | highlight | knowledge-graph-guide | `grafana-asserts-app/src/testIds.ts:21` |
| `label:has([data-testid='catalog-type-Node-radio'])` | highlight | knowledge-graph-guide | `grafana-asserts-app/src/features/Catalog/components/filters/CatalogTypeFilter.tsx:140`; `grafana-asserts-app/src/testIds.ts:101` (medium confidence, token `catalog-type- …(prefix)`) |
| `[data-testid='insight-type-filter']:nth-match(1)` | highlight | knowledge-graph-guide | `grafana-asserts-app/src/testIds.ts:136` |
| `[data-testid='insight-type-filter']:nth-match(6)` | highlight | knowledge-graph-guide | `grafana-asserts-app/src/testIds.ts:136` |

## grafana-collector-app

### ADD data-testid (3)

| selector | action | guides | evidence |
|---|---|---|---|
| `button:text('Next')` | highlight x2 | otel-fleet-management | `grafana-collector-app/src/feature/remote-configuration/components/edit/ConfigurationWizard.test.tsx:125` (low confidence, token `Next`) |
| `#collector-status-filter` | highlight | fleet-mgt-monitor-health-lj/check-health-status, fleet-mgt-monitor-health-lj/determine-config | `grafana-collector-app/src/feature/collector-list/components/CollectorListStatusFilter.tsx:50`; `grafana-collector-app/src/feature/collector-list/components/CollectorListStatusFilter.tsx:55` |
| `[aria-label="Search collectors"]` | highlight | fleet-mgt-monitor-health-lj/determine-config | `grafana-collector-app/src/feature/collector-list/components/CollectorListBar/SearchInput.tsx:114`; `grafana-collector-app/src/feature/remote-configuration/components/drawer/MatchedCollectorsTab.tsx:173` |

### MISSING from source (stale anchor?) (5)

| selector | action | guides | evidence |
|---|---|---|---|
| `[data-testid="tab-fleet-inventory"]` | highlight | fleet-mgt-monitor-health-lj/determine-config, fleet-mgt-monitor-health-lj/register-collector | searched `tab-fleet-inventory` — no hit in src or dist |
| `[data-testid="tab-api-access"]` | highlight | fleet-mgt-monitor-health-lj/register-collector | searched `tab-api-access` — no hit in src or dist |
| `[data-testid='tab-fleet-inventory']` | highlight | categorize-collector-fleet-lj/navigate-to-fleet | searched `tab-fleet-inventory` — no hit in src or dist |
| `button[data-testid='tab-fleet-inventory']` | highlight | fleet-management-onboarding | searched `tab-fleet-inventory` — no hit in src or dist |
| `div[data-testid='alloy-advanced-integrations-block']+button` | highlight | mongodb-integration-lj/configure-alloy | searched `alloy-advanced-integrations-block` — no hit in src or dist |

### found in dist only (8)

| selector | action | guides | evidence |
|---|---|---|---|
| `div[data-testid='collector-arch-selection'] input` | highlight | haproxy-load-balancer-lj/select-platform, linux-server-integration-lj/select-platform, macos-integration-lj/select-architecture +1 | `grafana-collector-app/dist/4155.js:407` (medium confidence, token `collector-arch-selection`) |
| `div[data-testid='collector-os-selection'] input` | highlight | haproxy-load-balancer-lj/select-platform, linux-server-integration-lj/select-platform, mysql-integration-lj/select-platform | `grafana-collector-app/dist/4155.js:407` (medium confidence, token `collector-os-selection`) |
| `button[data-testid='generate-token-submit-button']` | highlight | fleet-management-onboarding | `grafana-collector-app/dist/4155.js:11` (medium confidence, token `generate-token-submit-button`) |
| `div[data-testid='collector-os-selection']` | highlight | postgresql-integration-lj/select-platform | `grafana-collector-app/dist/4155.js:407` (medium confidence, token `collector-os-selection`) |
| `input[data-testid='generate-token-name-input']` | formfill | fleet-management-onboarding | `grafana-collector-app/dist/4155.js:11` (medium confidence, token `generate-token-name-input`) |
| `div[data-testid='collector-arch-selection']` | highlight | postgresql-integration-lj/select-platform | `grafana-collector-app/dist/4155.js:407` (medium confidence, token `collector-arch-selection`) |
| `div[data-testid='collector-installation-method'] input` | highlight | macos-integration-lj/select-architecture | `grafana-collector-app/dist/4155.js:407` (medium confidence, token `collector-installation-method`) |
| `button:contains("Copy to clipboard"):nth-match(2)` | highlight | fleet-management-onboarding | `grafana-collector-app/dist/4155.js:1`; `grafana-collector-app/dist/4155.js:397` (medium confidence, token `Copy to clipboard`) |

### testid already in source (12)

| selector | action | guides | evidence |
|---|---|---|---|
| `[data-testid="api-access-page"] > h3 + br + br + p + div` | highlight | fleet-mgt-monitor-health-lj/register-collector | `grafana-collector-app/src/feature/common/e2eSelectors/pages.ts:44` |
| `[data-testid="api-access-page"] > h3 + br + p + div` | highlight | fleet-mgt-monitor-health-lj/register-collector | `grafana-collector-app/src/feature/common/e2eSelectors/pages.ts:44` |
| `[data-testid="fleet-inventory-filter-button"]` | highlight | fleet-mgt-monitor-health-lj/determine-config | `grafana-collector-app/src/feature/common/e2eSelectors/pages.ts:17` |
| `[data-testid='home-install-alloy-button']` | highlight | send-logs-alloy-loki-lj/install-alloy | `grafana-collector-app/src/feature/common/e2eSelectors/pages.ts:3` |
| `button[data-testid='remote-config-delete-pipeline-application_o11y_linux'] svg[data-tes...` | highlight | otel-fleet-management | `grafana-collector-app/src/feature/common/e2eSelectors/pages.ts:35` (medium confidence, token `remote-config-delete-pipeline- …(prefix)`) |
| `div[data-testid='fleet-management-page'] button[data-testid='tab-remote-configuration']` | highlight | otel-fleet-management | `grafana-collector-app/src/feature/common/e2eSelectors/pages.ts:6` |
| `div[data-testid='remote-configuration-page'] button[data-testid='remote-configuration-c...` | highlight | otel-fleet-management | `grafana-collector-app/src/feature/common/e2eSelectors/pages.ts:23` |
| `div[data-testid='remote-configuration-page'] span:nth-match(3)` | highlight | otel-fleet-management | `grafana-collector-app/src/feature/common/e2eSelectors/pages.ts:23` |
| `button[data-testid='fleet-inventory-add-collector-button']` | highlight | fleet-management-onboarding | `grafana-collector-app/src/feature/common/e2eSelectors/pages.ts:15` |
| `div[data-testid^="collector-row-"]:nth-match(1)` | highlight | fleet-management-onboarding | `grafana-collector-app/src/feature/collector-list/components/CollectorListTable/CellWrapper.tsx:38`; `grafana-collector-app/src/feature/collector-list/components/CollectorListTable/CellWrapper.tsx:40` |
| `tr:has([data-testid^="collector-row-"]) td:nth-child(2) [data-testid^="collector-row-"]...` | highlight | fleet-mgt-monitor-health-lj/view-health-dashboards | `grafana-collector-app/src/feature/collector-list/components/CollectorListTable/CollectorListTable.tsx:174`; `grafana-collector-app/src/feature/collector-list/components/CollectorListTable/CellWrapper.tsx:38` |
| `tr:has([data-testid^="collector-row-"]) td:nth-child(3) [aria-label="Healthy"], tr:has(...` | hover | fleet-mgt-monitor-health-lj/check-health-status | `grafana-collector-app/src/feature/collector-list/components/CollectorListTable/CellWrapper.tsx:38`; `grafana-collector-app/src/feature/collector-list/components/CollectorListTable/CellWrapper.tsx:40` |

## grafana-slo-app

### ADD data-testid (6)

| selector | action | guides | evidence |
|---|---|---|---|
| `#generate-alerts` | highlight | slo-quickstart | `grafana-slo-app/src/components/Wizard/Alerts.tsx:35`; `grafana-slo-app/src/components/Wizard/Alerts.tsx:46` |
| `a[href="/a/grafana-slo-app/wizard/review"]` | highlight | create-availability-slo-lj/configure-targets | `grafana-slo-app/src/utils/grafanaExtensions.tsx:73`; `grafana-slo-app/src/utils/grafanaExtensions.tsx:125` |
| `input[name="name"]` | highlight | create-availability-slo-lj/configure-targets | `grafana-slo-app/src/pages/SloReports/Report.tsx:23`; `grafana-slo-app/src/pages/SloReports/Report.tsx:27` |
| `input[name="objective"]` | highlight | create-availability-slo-lj/configure-targets | `grafana-slo-app/src/pages/ManageSlos.tsx:25`; `grafana-slo-app/src/pages/SloPerformance.tsx:36` |
| `input[name="timeWindow"]` | formfill | create-availability-slo-lj/create-availability-slo | `grafana-slo-app/src/components/ErrorBudgetPanel/BigTentErrorBudgetPanel.tsx:21`; `grafana-slo-app/src/components/ErrorBudgetPanel/BigTentErrorBudgetPanel.tsx:22` |
| `textarea[name="description"]` | highlight | create-availability-slo-lj/configure-targets | `grafana-slo-app/src/pages/SloReports/Report.tsx:24`; `grafana-slo-app/src/pages/SloReports/Report.tsx:27` |

### MISSING from source (stale anchor?) (1)

| selector | action | guides | evidence |
|---|---|---|---|
| `a[href="/a/grafana-slo-app/wizard/alerts"]` | highlight | create-availability-slo-lj/configure-targets | searched `/a/grafana-slo-app/wizard/alerts` — no hit in src or dist |

### found in dist only (1)

| selector | action | guides | evidence |
|---|---|---|---|
| `a[href="/a/grafana-slo-app/wizard/new"]` | highlight | create-availability-slo-lj/create-availability-slo | `grafana-slo-app/dist/plugin.json:65` (medium confidence, token `/a/grafana-slo-app/wizard/new`) |

### testid already in source (12)

| selector | action | guides | evidence |
|---|---|---|---|
| `[data-testid='walk-next-button']` | highlight x4 | slo-quickstart | `grafana-slo-app/src/components/Wizard/NextButton.tsx:43` |
| `[data-testid='query-type-ratio']` | highlight | slo-quickstart | `grafana-slo-app/src/components/Wizard/Indicator/QueryType.tsx:24` (medium confidence, token `query-type- …(prefix)`) |
| `[data-testid='run-queries-btn']` | highlight | slo-quickstart | `grafana-slo-app/src/components/Wizard/Indicator/RatioQueryEditor.tsx:153` |
| `[data-testid='success-metric-field'] textarea.inputarea.monaco-mouse-cursor-text` | formfill | slo-quickstart | `grafana-slo-app/src/components/Wizard/Indicator/RatioQueryEditor.tsx:97` |
| `[data-testid='total-metric-field'] textarea.inputarea.monaco-mouse-cursor-text` | formfill | slo-quickstart | `grafana-slo-app/src/components/Wizard/Indicator/RatioQueryEditor.tsx:118` |
| `[data-testid='walk-save-button']` | highlight | slo-quickstart | `grafana-slo-app/src/components/Wizard/SubmitButton.tsx:76` |
| `a[data-testid='walk-next-button']` | highlight | create-availability-slo-lj/create-availability-slo | `grafana-slo-app/src/components/Wizard/NextButton.tsx:43` |
| `button[data-testid='run-queries-btn']` | highlight | create-availability-slo-lj/create-availability-slo | `grafana-slo-app/src/components/Wizard/Indicator/RatioQueryEditor.tsx:153` |
| `input[data-testid='slo-name-input']` | formfill | slo-quickstart | `grafana-slo-app/src/components/Wizard/Information/Information.tsx:44` |
| `input[data-testid='time-window-input']` | highlight | slo-quickstart | `grafana-slo-app/src/components/Wizard/Indicator/Indicator.tsx:91` |
| `textarea[data-testid='slo-description-input']` | formfill | slo-quickstart | `grafana-slo-app/src/components/Wizard/Information/Information.tsx:60` |
| `input[data-testid='target-input']` | formfill | slo-quickstart | `grafana-slo-app/src/components/Wizard/Objective.tsx:54` |

## grafana-easystart-app

### ADD data-testid (2)

| selector | action | guides | evidence |
|---|---|---|---|
| `[aria-label='Search connections by name']` | formfill | haproxy-load-balancer-lj/install-dashboards, iis-web-server-lj/select-integration | `grafana-easystart-app/src/features/catalog/Search/SemanticSearch.tsx:167` |
| `[aria-label="Search connections by name"]` | formfill | windows-integration/select-platform | `grafana-easystart-app/src/features/catalog/Search/SemanticSearch.tsx:167` |

### MISSING from source (stale anchor?) (3)

| selector | action | guides | evidence |
|---|---|---|---|
| `input[data-testid='search-input-input']` | formfill | connect-prometheus-metrics, grafana-cloud-tour-lj/explore-connect-data, grafana-cloud-tour-lj/explore-send-data +6 | searched `search-input-input` — no hit in src or dist |
| `[role='button']:has([data-testid='icon-plus-circle'])` | highlight | grafana-cloud-tour-lj/explore-connect-data, grafana-cloud-tour-lj/explore-send-data | searched `icon-plus-circle` — no hit in src or dist |
| `[data-testid='search-input-input']` | formfill | kafka-monitoring-lj/install-grafana-alloy | searched `search-input-input` — no hit in src or dist |

### testid already in source (11)

| selector | action | guides | evidence |
|---|---|---|---|
| `button[data-testid='agent-config-button']` | highlight | haproxy-load-balancer-lj/install-alloy, linux-server-integration-lj/install-alloy, macos-integration-lj/install-alloy +3 | `grafana-easystart-app/src/e2eSelectors/pages.ts:26` |
| `a[data-testid='view-dashboards-button']` | highlight | haproxy-load-balancer-lj/install-dashboards, iis-web-server-lj/install-dashboards, linux-server-integration-lj/install-dashboards-alerts +3 | `grafana-easystart-app/src/e2eSelectors/pages.ts:47` |
| `[data-testid='install-button']` | button/highlight | haproxy-load-balancer-lj/install-dashboards, iis-web-server-lj/install-dashboards, kafka-monitoring-lj/install-dashboards +1 | `grafana-easystart-app/src/e2eSelectors/pages.ts:20`; `grafana-easystart-app/src/e2eSelectors/pages.ts:46` |
| `button[data-testid='test-connection-button']` | highlight | linux-server-integration-lj/restart-test-connection, macos-integration-lj/test-connection, mongodb-integration-lj/test-connection +1 | `grafana-easystart-app/src/e2eSelectors/pages.ts:33`; `grafana-easystart-app/src/e2eSelectors/pages.ts:65` |
| `button[data-testid='install-button']` | highlight | linux-server-integration-lj/install-dashboards-alerts, macos-integration-lj/install-dashboards-alerts, mysql-integration-lj/install-dashboards-alerts | `grafana-easystart-app/src/e2eSelectors/pages.ts:20`; `grafana-easystart-app/src/e2eSelectors/pages.ts:46` |
| `div[data-testid='alloy-simple-block']+button` | highlight | linux-server-integration-lj/configure-alloy, macos-integration-lj/configure-alloy, postgresql-integration-lj/configure-alloy | `grafana-easystart-app/src/e2eSelectors/pages.ts:40` |
| `[data-testid='agent-config-button']` | highlight | iis-web-server-lj/install-alloy, kafka-monitoring-lj/install-grafana-alloy | `grafana-easystart-app/src/e2eSelectors/pages.ts:26` |
| `[data-testid='test-connection-button']` | button/highlight | iis-web-server-lj/verify-metrics, postgresql-integration-lj/test-connection | `grafana-easystart-app/src/e2eSelectors/pages.ts:33`; `grafana-easystart-app/src/e2eSelectors/pages.ts:65` |
| `[data-testid='view-dashboards-button']` | highlight | kafka-monitoring-lj/install-dashboards, postgresql-integration-lj/install-dashboards-alerts | `grafana-easystart-app/src/e2eSelectors/pages.ts:47` |
| `[data-testid="agent-config-button"]` | highlight | windows-integration/install-alloy | `grafana-easystart-app/src/e2eSelectors/pages.ts:26` |
| `a:has([data-testid='datasource-mysql-card'])` | highlight | grafana-cloud-tour-lj/explore-connect-data | `grafana-easystart-app/src/features/catalog/CardContent/PermissionMissingModalContent/PermissionMissingModalContent.tsx:52`; `grafana-easystart-app/src/features/catalog/CardContent/FeaturedConnectionsModalContent/MySQLRouterModalContent.tsx:24` (medium confidence, token `datasource- …(prefix)`) |

## grafana-adaptive-metrics-app

### ADD data-testid (4)

| selector | action | guides | evidence |
|---|---|---|---|
| `a[href*='adaptive-metrics']` | highlight | adaptive-metrics-recommendations | `grafana-adaptive-metrics-app/src/pages/NoAccess/index.tsx:7`; `grafana-adaptive-metrics-app/src/_test-utils_/utilities.tsx:19` |
| `button:contains("Apply all recommendations")` | highlight | adaptive-logs-recommendations | `grafana-adaptive-metrics-app/src/components/PageHeader/RuleManagement/BatchApply.tsx:133`; `grafana-adaptive-metrics-app/src/hooks/context-hooks.ts:299` (low confidence, token `Apply all recommendations`) |
| `input[placeholder="Metric name"]` | formfill | adaptive-metrics-lj/review-apply | `grafana-adaptive-metrics-app/src/components/PageHeader/Filters/SearchFilter/index.tsx:62`; `grafana-adaptive-metrics-app/src/components/Customizations/CustomizationDrawer/useCustomizationDrawerState.ts:25` |
| `select, div:has(label:contains('Segment'))` | highlight | adaptive-metrics-recommendations | `grafana-adaptive-metrics-app/src/pages/App/PageDefinitions.tsx:51`; `grafana-adaptive-metrics-app/src/components/Configuration/Segments/header.tsx:22` (low confidence, token `Segment`) |

### testid already in source (2)

| selector | action | guides | evidence |
|---|---|---|---|
| `div[data-testid='filter-field'] div:nth-match(5)` | highlight | adaptive-metrics-recommendations | `grafana-adaptive-metrics-app/src/components/PageHeader/Filters/SearchFilter/index.tsx:59` |
| `div[data-testid='recommendation-type']` | highlight | adaptive-metrics-recommendations | `grafana-adaptive-metrics-app/src/components/PageHeader/Filters/RecommendationTypeFilter/index.tsx:21` |

## grafana-cube-datasource

### ADD data-testid (4)

| selector | action | guides | evidence |
|---|---|---|---|
| `div[aria-label='Generated SQL query']` | highlight x4 | semantic-layer-tutorial | `grafana-cube-datasource/src/components/SQLPreview.tsx:99`; `grafana-cube-datasource/src/components/RawSQL.tsx:26` |
| `#pageContent button:contains('Files')` | highlight | semantic-layer-data-model-config | `grafana-cube-datasource/src/components/DataModelConfigPage.test.tsx:178` (low confidence, token `Files`) |
| `div[aria-label="Generated SQL query"]:contains('payment_method')` | highlight | semantic-layer-tutorial | `grafana-cube-datasource/src/components/SQLPreview.tsx:99`; `grafana-cube-datasource/src/components/RawSQL.tsx:26` |
| `input[aria-label='Dimensions']` | highlight | semantic-layer-tutorial | `grafana-cube-datasource/src/components/JsonQueryViewer.tsx:67`; `grafana-cube-datasource/src/components/JsonQueryViewer.tsx:68` |

## grafana-github-datasource

### ADD data-testid (3)

| selector | action | guides | evidence |
|---|---|---|---|
| `[aria-label='Query editor owner']` | highlight | github-visualize-lj/build-issues-panel, github-visualize-lj/build-pr-panel, github-visualize-lj/build-repository-panel | `grafana-github-datasource/src/components/selectors.ts:12` |
| `[aria-label='Query editor repository']` | highlight | github-visualize-lj/build-issues-panel, github-visualize-lj/build-pr-panel, github-visualize-lj/build-repository-panel | `grafana-github-datasource/src/components/selectors.ts:15` |
| `input[placeholder='Personal Access Token']` | formfill | github-data-source-lj/config-github-datasource | `grafana-github-datasource/src/views/ConfigEditor.tsx:37`; `grafana-github-datasource/src/views/ConfigEditor.tsx:127` |

## grafana-irm-app

### ADD data-testid (2)

| selector | action | guides | evidence |
|---|---|---|---|
| `td.title a[href="/a/grafana-irm-app/incidents/1"]:contains("Day in the Life Demo")` | highlight | rca-demo-ops, rca-demo-v2 | `irm/packages/@plugins/grafana-incident-datasource/pkg/datasource/testdata/activities.annotations.golden.jsonc:11` |
| `button:text("Acknowledge")` | highlight | grafana-irm-configuration-lj/run-end-to-end-test | `irm/packages/@plugins/grafana-irm-app/src/pages/Integrations/Apps/OnCallSlackAdditionalFields.tsx:18`; `irm/packages/@plugins/grafana-oncall-app/src/pages/incidents/Incidents.tsx:376` (low confidence, token `Acknowledge`) |

### MISSING from source (stale anchor?) (1)

| selector | action | guides | evidence |
|---|---|---|---|
| `div:text("Wait")` | highlight | grafana-irm-configuration-lj/create-escalation-chain, irm-configuration | searched `Wait` — no hit in src or dist |

### testid already in source (26)

| selector | action | guides | evidence |
|---|---|---|---|
| `[data-pathfinder="new-schedule-button"]` | button | grafana-irm-configuration-lj/create-on-call-schedule, irm-configuration | `irm/packages/@plugins/grafana-oncall-app/src/pages/schedules/Schedules.tsx:100` |
| `[data-pathfinder="add-integration-button"]` | button | grafana-irm-configuration-lj/connect-grafana-alerting, irm-configuration | `irm/packages/@plugins/grafana-irm-app/src/pages/Integrations/IntegrationsContent.tsx:331` |
| `[data-pathfinder="escalation-chain-name-input"]` | formfill | grafana-irm-configuration-lj/create-escalation-chain, irm-configuration | `irm/packages/@plugins/grafana-irm-app/src/pages/EscalationChains/EscalationChainModals.tsx:274` |
| `[data-pathfinder="escalation-chain-option-0"]` | highlight | grafana-irm-configuration-lj/connect-grafana-alerting, irm-configuration | `irm/packages/@grafana-irm/features/src/integrations/components/RouteDisplay/ExpandedIntegrationRouteDisplay.tsx:684` (medium confidence, token `escalation-chain-option- …(prefix)`) |
| `[data-pathfinder="new-escalation-chain-button"]` | button | grafana-irm-configuration-lj/create-escalation-chain, irm-configuration | `irm/packages/@plugins/grafana-irm-app/src/pages/EscalationChains/EscalationChains.tsx:78` |
| `[data-pathfinder="save-escalation-chain-button"]` | button | grafana-irm-configuration-lj/create-escalation-chain, irm-configuration | `irm/packages/@plugins/grafana-irm-app/src/pages/EscalationChains/EscalationChainModals.tsx:307` |
| `[data-pathfinder="save-integration-button"]` | button | grafana-irm-configuration-lj/connect-grafana-alerting, irm-configuration | `irm/packages/@grafana-irm/features/src/integrations/components/IntegrationForm/IntegrationForm.tsx:449` |
| `[data-pathfinder="save-rotation-button"]` | button | grafana-irm-configuration-lj/create-on-call-schedule, irm-configuration | `irm/packages/@plugins/grafana-oncall-app/src/containers/RotationForm/RotationForm.tsx:915`; `irm/packages/@plugins/grafana-oncall-app/src/containers/RotationForm/RotationForm.tsx:930` |
| `[data-pathfinder="save-schedule-button"]` | button | grafana-irm-configuration-lj/create-on-call-schedule, irm-configuration | `irm/packages/@plugins/grafana-oncall-app/src/containers/ScheduleForm/ScheduleForm.tsx:88` |
| `[data-pathfinder="submit-send-alert-button"]` | button | grafana-irm-configuration-lj/run-end-to-end-test, irm-configuration | `irm/packages/@grafana-irm/features/src/integrations/components/IntegrationSendDemoAlertModal.tsx:120` |
| `[data-pathfinder="timeline-item-1"]` | highlight | grafana-irm-configuration-lj/create-escalation-chain, irm-configuration | `irm/packages/@grafana-irm/components/src/components/Timeline/TimelineItem.tsx:44` (medium confidence, token `timeline-item- …(prefix)`) |
| `div[data-testid="input-wrapper"] input[placeholder="Select Schedule"]` | highlight | grafana-irm-configuration-lj/create-escalation-chain, irm-configuration | `irm/packages/@grafana-irm/features/src/incidentLabels/components/IncidentLabelsDialog.tsx:271` |
| `div[data-testid="schedule-rotations"] button:first-of-type` | highlight | grafana-irm-configuration-lj/create-on-call-schedule, irm-configuration | `irm/packages/@plugins/grafana-oncall-app/src/containers/Rotations/Rotations.tsx:157`; `irm/packages/@grafana-irm/core/src/core/dom.ts:36` |
| `[data-pathfinder="add-user-select"]` | highlight | grafana-irm-configuration-lj/create-on-call-schedule, irm-configuration | `irm/packages/@plugins/grafana-oncall-app/src/components/UserGroups/UserGroups.tsx:183` |
| `[data-pathfinder="create-web-schedule-button"]` | button | grafana-irm-configuration-lj/create-on-call-schedule, irm-configuration | `irm/packages/@plugins/grafana-oncall-app/src/components/NewScheduleSelector/NewScheduleSelector.tsx:50` |
| `[data-pathfinder="integration-grafanaalerting"]` | highlight | grafana-irm-configuration-lj/connect-grafana-alerting, irm-configuration | `irm/packages/@grafana-irm/features/src/insights/oncall/components/Tutorial/Tutorial.tsx:15`; `irm/packages/@grafana-irm/features/src/insights/oncall/components/Tutorial/Tutorial.tsx:50` (medium confidence, token `integration- …(prefix)`) |
| `[data-pathfinder="integration-name-input"]` | formfill | grafana-irm-configuration-lj/connect-grafana-alerting, irm-configuration | `irm/packages/@grafana-irm/features/src/integrations/components/IntegrationForm/IntegrationForm.tsx:210` |
| `[data-pathfinder="new-contact-point-input"]` | formfill | grafana-irm-configuration-lj/connect-grafana-alerting, irm-configuration | `irm/packages/@grafana-irm/features/src/integrations/components/IntegrationForm/IntegrationForm.tsx:679` |
| `[data-pathfinder="route-heading-0"]` | highlight | grafana-irm-configuration-lj/connect-grafana-alerting, irm-configuration | `irm/packages/@grafana-irm/features/src/integrations/components/RouteDisplay/RouteHeading.tsx:32` (medium confidence, token `route-heading- …(prefix)`) |
| `[data-pathfinder="schedule-name"]` | formfill | grafana-irm-configuration-lj/create-on-call-schedule, irm-configuration | `irm/packages/@plugins/grafana-oncall-app/src/containers/ScheduleForm/ScheduleForm.tsx:205` |
| `[data-pathfinder="send-demo-alert-button"]` | button | grafana-irm-configuration-lj/run-end-to-end-test, irm-configuration | `irm/packages/@plugins/grafana-oncall-app/src/pages/integration/IntegrationActions.tsx:170` |
| `[data-pathfinder="timeline-item-2"]` | highlight | grafana-irm-configuration-lj/create-escalation-chain, irm-configuration | `irm/packages/@grafana-irm/components/src/components/Timeline/TimelineItem.tsx:44` (medium confidence, token `timeline-item- …(prefix)`) |
| `[data-pathfinder="timeline-item-3"]` | highlight | grafana-irm-configuration-lj/create-escalation-chain, irm-configuration | `irm/packages/@grafana-irm/components/src/components/Timeline/TimelineItem.tsx:44` (medium confidence, token `timeline-item- …(prefix)`) |
| `[data-testid="escalation-chain-select"]` | highlight | grafana-irm-configuration-lj/connect-grafana-alerting | `irm/packages/@grafana-irm/features/src/integrations/components/RouteDisplay/ExpandedIntegrationRouteDisplay.tsx:345`; `irm/packages/@grafana-irm/features/src/integrations/components/RouteDisplay/ExpandedIntegrationRouteDisplay.tsx:671` |
| `[data-testid="integration-url"]:nth-match(1) a` | highlight | grafana-irm-configuration-lj/run-end-to-end-test | `irm/packages/@plugins/grafana-oncall-app/src/pages/incidents/Incidents.tsx:777` |
| `div[data-testid='escalation-chain-select']` | highlight | irm-configuration | `irm/packages/@grafana-irm/features/src/integrations/components/RouteDisplay/ExpandedIntegrationRouteDisplay.tsx:345`; `irm/packages/@grafana-irm/features/src/integrations/components/RouteDisplay/ExpandedIntegrationRouteDisplay.tsx:671` |

## grafana-lokiexplore-app

### ADD data-testid (1)

| selector | action | guides | evidence |
|---|---|---|---|
| `button:contains('Include')` | highlight | drilldown-logs-lj/labels-and-fields | `grafana-lokiexplore-app/src/Components/FilterButton.tsx:40`; `grafana-lokiexplore-app/src/Components/IndexScene/PatternControls.tsx:45` (low confidence, token `Include`) |

### MISSING from source (stale anchor?) (2)

| selector | action | guides | evidence |
|---|---|---|---|
| `[data-testid='stream-selector-input']` | formfill | adaptive-logs-lj | searched `stream-selector-input` — no hit in src or dist |
| `a[aria-label='Select detected_level']` | highlight | drilldown-logs-lj/labels-and-fields | searched `Select detected_level` — no hit in src or dist |

### testid already in source (9)

| selector | action | guides | evidence |
|---|---|---|---|
| `a[data-testid='data-testid tab-logs']` | highlight | drilldown-logs-lj/labels-and-fields, drilldown-logs-lj/log-patterns | `grafana-lokiexplore-app/src/services/testIds.ts:48` |
| `a[data-testid="data-testid tab-fields"]` | highlight | explore-drilldowns-101 | `grafana-lokiexplore-app/src/services/testIds.ts:46` |
| `a[data-testid="data-testid tab-labels"]` | highlight | explore-drilldowns-101 | `grafana-lokiexplore-app/src/services/testIds.ts:47` |
| `a[data-testid="data-testid tab-patterns"]` | highlight | explore-drilldowns-101 | `grafana-lokiexplore-app/src/services/testIds.ts:49` |
| `a[data-testid='data-testid tab-fields']` | highlight | drilldown-logs-lj/labels-and-fields | `grafana-lokiexplore-app/src/services/testIds.ts:46` |
| `a[data-testid='data-testid tab-labels']` | highlight | drilldown-logs-lj/labels-and-fields | `grafana-lokiexplore-app/src/services/testIds.ts:47` |
| `a[data-testid='data-testid tab-patterns']` | highlight | drilldown-logs-lj/log-patterns | `grafana-lokiexplore-app/src/services/testIds.ts:49` |
| `div[data-testid='input-wrapper'] input:nth-match(1)` | highlight | drilldown-logs-lj/search-logs | `grafana-lokiexplore-app/src/Components/IndexScene/LineFilter/LineFilterEditor.tsx:142`; `grafana-lokiexplore-app/src/Components/IndexScene/LineFilter/LineFilterEditor.tsx:146` |
| `input[data-testid='pattern-filter']` | highlight | adaptive-logs-recommendations | `grafana-lokiexplore-app/src/services/extensions/links.test.ts:416` |

## grafana-pathfinder-app

### ADD data-testid (2)

| selector | action | guides | evidence |
|---|---|---|---|
| `#dev-mode` | highlight | enable-block-editor, enable-coda | `grafana-pathfinder-app/src/integrations/assistant-integration/AssistantCustomizable.tsx:12`; `grafana-pathfinder-app/src/integrations/assistant-integration/AssistantCustomizable.tsx:13` |
| `button[aria-label='Expand terminal']` | highlight | fleet-management-onboarding | `grafana-pathfinder-app/src/integrations/coda/TerminalPanel.tsx:430`; `grafana-pathfinder-app/src/integrations/coda/TerminalPanel.tsx:449` |

### MISSING from source (stale anchor?) (1)

| selector | action | guides | evidence |
|---|---|---|---|
| `[role='button']:contains('TerminalDisconnected')` | highlight | enable-coda | searched `TerminalDisconnected` — no hit in src or dist |

### structural/positional — needs human (1)

| selector | action | guides | evidence |
|---|---|---|---|
| `label[for='enable-coda-terminal']` | highlight | enable-coda | searched `—` — no hit in src or dist |

### testid already in source (5)

| selector | action | guides | evidence |
|---|---|---|---|
| `button[data-testid='config-submit']` | highlight | enable-coda | `grafana-pathfinder-app/src/constants/testIds.ts:180` |
| `button[data-testid='docs-panel-tab-devtools']` | highlight | enable-block-editor | `grafana-pathfinder-app/src/components/docs-panel/docs-panel.contract.test.tsx:80` |
| `div[data-testid='input-wrapper']:nth-match(5)` | highlight | enable-coda | `grafana-pathfinder-app/src/bundled-interactives/first-dashboard-cloud/content.json:222`; `grafana-pathfinder-app/src/bundled-interactives/block-editor-tutorial/content.json:39` |
| `div[data-testid='input-wrapper']:nth-match(6)` | highlight | enable-coda | `grafana-pathfinder-app/src/lib/dom/dom-utils.ts:384`; `grafana-pathfinder-app/src/lib/dom/dom-utils.ts:390` |
| `div[data-testid='input-wrapper']:nth-match(7)` | highlight | enable-coda | `grafana-pathfinder-app/src/bundled-interactives/first-dashboard-cloud/content.json:222`; `grafana-pathfinder-app/src/bundled-interactives/block-editor-tutorial/content.json:39` |

## grafana-pdc-app

### ADD data-testid (3)

| selector | action | guides | evidence |
|---|---|---|---|
| `[aria-label="Private data source connect"]` | highlight | prometheus-lj/select-private-connection | `grafana-pdc-app/src/module.tsx:73`; `grafana-pdc-app/src/feature/datasource-config/components/DataSourceExtensionFieldAgent.tsx:87` |
| `[aria-label='Private data source connect']` | highlight | infinity-csv-lj/select-private-connection | `grafana-pdc-app/src/module.tsx:73`; `grafana-pdc-app/src/feature/datasource-config/components/DataSourceExtensionFieldAgent.tsx:87` |
| `input[aria-label='Private data source connect']` | highlight | mysql-data-source-lj/test-connection | `grafana-pdc-app/src/module.tsx:73`; `grafana-pdc-app/src/feature/datasource-config/components/DataSourceExtensionFieldAgent.tsx:87` |

## k6-app

### ADD data-testid (1)

| selector | action | guides | evidence |
|---|---|---|---|
| `#secret-description` | formfill x2 | how-to-setup-secrets-tutorial | `k6-app/src/pages/SettingsPage/tabs/SecretsManagementTab/SecretEditModal.tsx:274`; `k6-app/src/pages/SettingsPage/tabs/SecretsManagementTab/SecretEditModal.tsx:281` |

### MISSING from source (stale anchor?) (2)

| selector | action | guides | evidence |
|---|---|---|---|
| `button[aria-label='Delete quickpizza-password']` | highlight | how-to-setup-secrets-tutorial | searched `Delete quickpizza-password` — no hit in src or dist |
| `button[aria-label='Delete quickpizza-username']` | highlight | how-to-setup-secrets-tutorial | searched `Delete quickpizza-username` — no hit in src or dist |

### testid already in source (1)

| selector | action | guides | evidence |
|---|---|---|---|
| `[data-testid="project-listing-layout-table"] a:nth-match(1)` | highlight | k6-extensions-grafana-cloud | `k6-app/src/types/dataTestIds.ts:70` |

## mysql

### ADD data-testid (3)

| selector | action | guides | evidence |
|---|---|---|---|
| `input[name='host']` | formfill | mysql-data-source-lj/configure-datasource | `mysql/src/configuration/ConfigurationEditor.tsx:77`; `mysql/src/configuration/ConfigurationEditor.tsx:80` |
| `input[placeholder='Password']` | formfill | mysql-data-source-lj/configure-datasource | `mysql/src/configuration/ConfigurationEditor.tsx:36`; `mysql/src/configuration/ConfigurationEditor.tsx:113` |
| `input[placeholder='Username']` | formfill | mysql-data-source-lj/configure-datasource | `mysql/src/configuration/ConfigurationEditor.tsx:104`; `mysql/src/configuration/ConfigurationEditor.tsx:108` |

## grafana-adaptivelogs-app

### ADD data-testid (2)

| selector | action | guides | evidence |
|---|---|---|---|
| `a[href*='adaptive-logs']` | highlight | adaptive-logs-lj | `grafana-adaptivelogs-app/src/pages/Overview/GetStarted/GuidedOnboardingCallout.tsx:12`; `grafana-adaptivelogs-app/src/pages/Overview/index.tsx:15` |
| `label[aria-label^='Show early detection patterns']` | highlight | adaptive-logs-recommendations | `grafana-adaptivelogs-app/src/components/PageHeader/index.tsx:150`; `grafana-adaptivelogs-app/src/components/PageHeader/index.tsx:152` |

## grafana-app-observability-app

### ADD data-testid (2)

| selector | action | guides | evidence |
|---|---|---|---|
| `button:has(span:contains('productcatalogservice'))` | highlight | rca-demo, rca-demo-ops, rca-demo-v2 | `grafana-app-observability-app/plugin/cypress/support/fixtures/serviceMap/data/1.json:382` (low confidence, token `productcatalogservice`) |
| `a[href*="a/grafana-app-observability-app"]` | highlight | welcome-to-play/main-page | `grafana-app-observability-app/plugin/src/links.ts:86`; `grafana-app-observability-app/plugin/src/plugin.json:199` |

### testid already in source (3)

| selector | action | guides | evidence |
|---|---|---|---|
| `a[data-testid="data-testid button-select-service"]:first-of-type` | highlight | explore-drilldowns-101 | `grafana-app-observability-app/plugin/src/components/FilterBy/AdHocFilterRenderer.tsx:111`; `grafana-app-observability-app/plugin/src/components/FilterBy/AdHocFilterRenderer.tsx:133` (medium confidence, token `data-testid …(prefix)`) |
| `a[data-testid='data-testid button-select-service']:first-of-type` | highlight | drilldown-logs-lj/view-logs | `grafana-app-observability-app/plugin/src/components/FilterBy/AdHocFilterRenderer.tsx:111`; `grafana-app-observability-app/plugin/src/components/FilterBy/AdHocFilterRenderer.tsx:133` (medium confidence, token `data-testid …(prefix)`) |
| `input[data-testid='data-testid search-services-input']` | highlight | drilldown-logs-lj/view-logs | `grafana-app-observability-app/plugin/src/components/FilterBy/AdHocFilterRenderer.tsx:111`; `grafana-app-observability-app/plugin/src/components/FilterBy/AdHocFilterRenderer.tsx:133` (medium confidence, token `data-testid …(prefix)`) |

## grafana-oncall-app

### ADD data-testid (2)

| selector | action | guides | evidence |
|---|---|---|---|
| `div:text("Notify users from on-call schedule")` | highlight | grafana-irm-configuration-lj/create-escalation-chain, irm-configuration | `irm/packages/@plugins/grafana-oncall-app/e2e-tests/utils/escalationChain.ts:7` (low confidence, token `Notify users from on-call schedule`) |
| `div:text("Notify users")` | highlight | grafana-irm-configuration-lj/create-escalation-chain, irm-configuration | `irm/packages/@plugins/grafana-irm-app/e2e-tests/utils/escalationChain.ts:7` (low confidence, token `Notify users`) |

## plugin-ui

### ADD data-testid (2)

| selector | action | guides | evidence |
|---|---|---|---|
| `#auth-method-select` | highlight | prometheus-lj/config-authentication | `plugin-ui/src/components/ConfigEditor/Auth/auth-method/AuthMethodSettings.tsx:147` |
| `#connection-url` | formfill | prometheus-lj/add-data-source-url | `plugin-ui/src/components/ConfigEditor/Connection/ConnectionSettings.tsx:40`; `plugin-ui/src/components/ConfigEditor/Connection/ConnectionSettings.tsx:60` |

## grafana-assistant-app

### ADD data-testid (1)

| selector | action | guides | evidence |
|---|---|---|---|
| `div[class*='connectionBanner']` | highlight | assistant-self-hosted | `grafana-assistant-app/apps/plugin/src/components/config/OSSSettings.tsx:305`; `grafana-assistant-app/apps/plugin/src/components/config/OSSSettings.tsx:306` |

## grafana-exploretraces-app

### ADD data-testid (1)

| selector | action | guides | evidence |
|---|---|---|---|
| `label:contains('All spans')` | highlight | drilldown-traces-lj/view-distribution | `grafana-exploretraces-app/src/pages/Explore/primary-signals.ts:13` (low confidence, token `All spans`) |

## grafana-metricsdrilldown-app

### ADD data-testid (1)

| selector | action | guides | evidence |
|---|---|---|---|
| `a[href="/a/grafana-metricsdrilldown-app/drilldown"]` | highlight | prom-remote-write-lj/verify-metrics-query-works, prometheus-lj/verify-ds-connection | `grafana-metricsdrilldown-app/src/App/Onboarding.tsx:52`; `grafana-metricsdrilldown-app/src/App/assistant/questions.ts:7` |

### structural/positional — needs human (1)

| selector | action | guides | evidence |
|---|---|---|---|
| `div[id="ds"]` | highlight | explore-drilldowns-101 | searched `—` — no hit in src or dist |

### testid already in source (2)

| selector | action | guides | evidence |
|---|---|---|---|
| `div[data-testid="metrics-list"] div[data-testid="with-usage-data-preview-panel"]:first-...` | highlight | explore-drilldowns-101 | `grafana-metricsdrilldown-app/src/MetricsReducer/MetricsList/MetricsList.tsx:41`; `grafana-metricsdrilldown-app/src/MetricsReducer/MetricsList/MetricsList.tsx:67` |
| `div[data-testid="metrics-list"] div[data-testid="with-usage-data-preview-panel"]:first-...` | highlight | explore-drilldowns-101 | `grafana-metricsdrilldown-app/src/MetricsReducer/MetricsList/MetricsList.tsx:41`; `grafana-metricsdrilldown-app/src/MetricsReducer/MetricsList/MetricsList.tsx:67` |

## volkovlabs-rss-datasource

### ADD data-testid (1)

| selector | action | guides | evidence |
|---|---|---|---|
| `input[placeholder='https://feed']` | formfill | first-dashboard | `volkovlabs-rss-datasource/src/components/ConfigEditor/ConfigEditor.tsx:51` |

## yesoreyeram-infinity-datasource

### MISSING from source (stale anchor?) (1)

| selector | action | guides | evidence |
|---|---|---|---|
| `button[aria-label='Toggle Parsing options & Result fields']` | highlight | infinity-csv-lj/build-dashboard | searched `Toggle Parsing options & Result fields` — no hit in src or dist |

### structural/positional — needs human (1)

| selector | action | guides | evidence |
|---|---|---|---|
| `input[placeholder=',']` | formfill | infinity-csv-lj/build-dashboard | searched `—` — no hit in src or dist |

### testid already in source (7)

| selector | action | guides | evidence |
|---|---|---|---|
| `div[data-testid='infinity-query-row-wrapper-query-options']` | highlight | play-5k-run-results, play-gb-railway-usage, play-nz-geonet-tour | `yesoreyeram-infinity-datasource/src/editors/query/query.filters.test.tsx:12` (medium confidence, token `infinity-query-row- …(prefix)`) |
| `div[data-testid='infinity-query-field-wrapper-rows/root'] textarea` | highlight | play-carbon-intensity, play-nz-geonet-tour | `yesoreyeram-infinity-datasource/src/editors/query.editor.test.tsx:50` (medium confidence, token `infinity-query-field-wrapper- …(prefix)`) |
| `[data-testid='infinity-query-field-label-method']` | highlight | infinity-csv-lj/build-dashboard | `yesoreyeram-infinity-datasource/src/editors/query.editor.test.tsx:50` (medium confidence, token `infinity-query-field- …(prefix)`) |
| `[data-testid='infinity-query-field-label-type']` | highlight | infinity-csv-lj/build-dashboard | `yesoreyeram-infinity-datasource/src/editors/query/infinityQuery.test.tsx:52` (medium confidence, token `infinity-query-field- …(prefix)`) |
| `[data-testid='infinity-query-url-input']` | formfill | infinity-csv-lj/build-dashboard | `yesoreyeram-infinity-datasource/src/editors/query/query.url.tsx:132` |
| `button[data-testid='infinity-query-row-collapse-show-parsing-options-&-result-fields']` | highlight | play-nz-geonet-tour | `yesoreyeram-infinity-datasource/src/editors/query/query.filters.test.tsx:12` (medium confidence, token `infinity-query-row-collapse-show- …(prefix)`) |
| `button[data-testid='infinity-query-row-collapse-show-parsing-options-&-result-fields'] svg` | highlight | play-carbon-intensity | `yesoreyeram-infinity-datasource/src/editors/query/query.filters.test.tsx:12` (medium confidence, token `infinity-query-row-collapse-show- …(prefix)`) |

## grafana-demodashboards-app

### testid already in source (1)

| selector | action | guides | evidence |
|---|---|---|---|
| `button[data-testid='install-quickpizza']` | highlight | understanding-the-four-golden-signals-of-observability | `grafana-demodashboards-app/src/components/DashboardCard.tsx:158` (medium confidence, token `install- …(prefix)`) |

## grafana-k8s-app

### found in dist only (1)

| selector | action | guides | evidence |
|---|---|---|---|
| `a[href*="a/grafana-k8s-app"]` | highlight | welcome-to-play/main-page | `grafana-k8s-app/dist/1123.js:1`; `grafana-k8s-app/dist/plugin.json:117` (medium confidence, token `a/grafana-k8s-app`) |

## loki

### found in dist only (1)

| selector | action | guides | evidence |
|---|---|---|---|
| `[data-testid="label-browser-button"]` | highlight | visualization-logs/write-query | `loki/dist/module.js:9` (medium confidence, token `label-browser-button`) |

## tempo

### structural/positional — needs human (1)

| selector | action | guides | evidence |
|---|---|---|---|
| `label[for*='traceqlSearch']` | highlight | visualization-traces-lj/add-traces-table | searched `—` — no hit in src or dist |

## No clone available

- RCA demo node-graph panel plugin (not grafana/grafana): 10 selectors
- external (owner not recorded in analysis): 5 selectors
- instance-content (provisioned dashboard/demo data): 4 selectors
- @grafana/scenes AdHocFiltersVariable (rendered by the Drilldown apps): 2 selectors
- grafana-enterprise (Query Library): 2 selectors
