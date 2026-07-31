# Pathfinder weak-selector migration map — what was, and what will be

Programme: grafana/grafana#129672 — every weak reftarget in the interactive-tutorials guides was traced to its
owning code and, where that code is grafana/grafana, given a versioned `@grafana/e2e-selectors` entry.
**All 15 core PRs are merged to main** (#129669, #129698, #129704, #129723, #129725, #129749, #129753, #129768, #129769, #129770, #129807, #129809, #129814, #129818, #129821); origin/main @ a881f219680 is the source of truth for
every selector value below (mapping docs were re-verified against it).

**Totals** (738 guide-level rows / 516 unique weak anchors across 152 guides):

| status | meaning | rows | unique anchors |
|---|---|---|---|
| `ready` | new/upgraded selector merged on main — retarget the guide | 139 | 125 |
| `no-change` | anchor resolves to a pre-existing selector (adopt it; no core change was needed) | 66 | 54 |
| `stale` | old element is gone from main — guide-side re-record/retarget only | 11 | 7 |
| `not-fixable` | instance data, positional picks, Monaco internals, or grafana-ui API gaps | 41 | 35 |
| `external` | element is owned by another repo/plugin (named per row) — file the fix there | 481 | 296 |

**grafana-ui API gaps (follow-up candidates, tracked as not-fixable rows):** `LogListControlsSelectOption`
(no test-id prop on its button), the `Alert` action button (`buttonContent` has no test-id), and
`RadioButtonList`/`RadioButtonDot` (forward no test id — `RadioButton.option` does not apply).

**Rollout gating:** selectors rendered by decoupled plugin bundles ship with the plugin asset, not with core —
the 7 rows marked `gate: plugin rollout` (grafana-testdata-datasource `seriesCount`, InfluxDB
`configPage.*`) only match the DOM once the NEW plugin bundle is what the cloud stack loads. Plugin assets
deploy at their own cadence, so gate those guide retargets on plugin rollout, not on the PR merge.

**Version note:** all new selector values carry the `'13.2.0'` version key, i.e. they resolve at Grafana >= 13.2.0.
`grafana:` **token** consumers resolve per stack version automatically (Pathfinder resolves the token against the
running Grafana's version, falling back to older keys below 13.2), while **CSS** consumers match the literal DOM
value and therefore only work on >= 13.2 stacks. Token syntax observed in guides: whole-reftarget
`grafana:<path>` (parameter appended as `:<param>`), embedded `{grafana:<path>}` inside a larger CSS selector;
tokens resolve to `:is([data-testid="…"], [aria-label="…"])`.

Rows whose **parameter could not be derived** from the old anchor are flagged in the notes (`<...>` placeholders
or "verify" callouts) — see the `paramsNeedingHumanInput` list in the JSON. "Leftover triage" rows (weak anchors
outside the group mapping docs, classified against origin/main during map generation) are marked in notes where
relevant.


## adaptive-logs-lj

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[data-testid='stream-selector-input']` | formfill | external | — | — | owner: grafana-lokiexplore-app. Not fixable in grafana/grafana — owned by grafana-lokiexplore-app. Loki stream-selector terminology; not in core or bundles — most likely Logs Drilldown, confirm via live DOM. |
| `a[href*='adaptive-logs']` | highlight | external | — | — | owner: grafana-adaptivelogs-app. Not fixable in grafana/grafana — owned by grafana-adaptivelogs-app. No core hit; href fragment points at the Adaptive Logs app. |

## adaptive-logs-recommendations

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `button:contains("Apply all recommendations")` | highlight | external | — | — | owner: grafana-adaptive-metrics-app. Not fixable in grafana/grafana — owned by grafana-adaptive-metrics-app. Adaptive Metrics recommendations page action. |
| `input[data-testid='pattern-filter']` | highlight | external | — | — | owner: grafana-lokiexplore-app. Not fixable in grafana/grafana — owned by grafana-lokiexplore-app. Log patterns filter input; not in core — most likely Logs Drilldown patterns tab. |
| `label[aria-label^='Show early detection patterns']` | highlight | external | — | — | owner: grafana-adaptivelogs-app. Not fixable in grafana/grafana — owned by grafana-adaptivelogs-app. Toggle on the Adaptive Logs Patterns tab at /a/grafana-adaptivelogs-app (guide navigates there explicitly). |

## adaptive-metrics-lj/review-apply

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[aria-label="Expand section: Adaptive Telemetry"]` | highlight | ready | `[data-testid="data-testid navigation mega-menu section toggle /adaptive-telemetry"]` | `grafana:components.NavMenu.sectionToggleButton:/adaptive-telemetry` | Param assumed "/adaptive-telemetry" (matching the guide's nav-item hrefs) — verify on a Cloud stack. GD-5 compound: keep the href half; a section rendered in both the pinned box and the main nav can double-match — scope with components.NavMenu.Menu ([data-testid="data-testid navigation mega-menu"]) when needed. |
| `a[href="/a/grafana-adaptive-metrics-app/overview"]` | highlight | no-change | `a[data-testid="data-testid Nav menu item"][href='/a/grafana-adaptive-metrics-app/overview']` | `a{grafana:components.NavMenu.item}[href='/a/grafana-adaptive-metrics-app/overview']` | Markup is core mega-menu even though the href comes from plugin nav registration. GD-5 compound: keep the href half; a section rendered in both the pinned box and the main nav can double-match — scope with components.NavMenu.Menu ([data-testid="data-testid navigation mega-menu"]) when needed. |
| `a[href="/a/grafana-adaptive-metrics-app/rule-management"]` | highlight | no-change | `a[data-testid="data-testid Nav menu item"][href='/a/grafana-adaptive-metrics-app/rule-management']` | `a{grafana:components.NavMenu.item}[href='/a/grafana-adaptive-metrics-app/rule-management']` | Markup is core mega-menu even though the href comes from plugin nav registration. GD-5 compound: keep the href half; a section rendered in both the pinned box and the main nav can double-match — scope with components.NavMenu.Menu ([data-testid="data-testid navigation mega-menu"]) when needed. |
| `input[placeholder="Metric name"]` | formfill | external | — | — | owner: grafana-adaptive-metrics-app. No core match for the placeholder. |

## adaptive-metrics-recommendations

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[href*='adaptive-metrics']` | highlight | external | — | — | owner: grafana-adaptive-metrics-app. Adaptive Metrics app UI (the slice's gauge-panel "core" match for the Segment selector was a false positive). |
| `div[data-testid='filter-field'] div:nth-match(5)` | highlight | external | — | — | owner: grafana-adaptive-metrics-app. Adaptive Metrics app UI (the slice's gauge-panel "core" match for the Segment selector was a false positive). |
| `div[data-testid='recommendation-type']` | highlight | external | — | — | owner: grafana-adaptive-metrics-app. Adaptive Metrics app UI (the slice's gauge-panel "core" match for the Segment selector was a false positive). |
| `select, div:has(label:contains('Segment'))` | highlight | external | — | — | owner: grafana-adaptive-metrics-app. Adaptive Metrics app UI (the slice's gauge-panel "core" match for the Segment selector was a false positive). |

## alert-activity

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[role='dialog'] [role='radiogroup']` | hover | ready | `[data-testid="data-testid triage history-filter"]` | `grafana:pages.Alerting.Triage.historyFilterRadioGroup` | Individual options via components.RadioButton.option('all'\|'states'\|'notifications') (PR #129669). |
| `[role='dialog'] button[aria-label='Toggle notification details']:nth-match(1)` | highlight | ready | `[data-testid="data-testid Drawer"] [data-testid="data-testid triage notification-toggle-button"]:nth-match(1)` | `{grafana:components.Drawer.General.title:<drawer title>} — scope via Drawer; see notes` | Repeated element — keep :nth-match; scope with the Drawer instead of [role=dialog]. Base selector: [data-testid="data-testid triage notification-toggle-button"]. |
| `button:contains('Clear filters')` | highlight | ready | `[data-testid="data-testid triage clear-filters-button"]` | `grafana:pages.Alerting.Triage.clearFiltersButton` | — |
| `button:has(span:contains('Critical'))` | highlight | ready | `[data-testid="data-testid triage severity-filter critical"]` | `grafana:pages.Alerting.Triage.severityFilterButton:critical` | Param = severity level key (lowercase, from SEVERITY_DEFINITIONS). |
| `button:has(span:contains('Firing'))` | highlight | ready | `[data-testid="data-testid triage state-filter firing"]` | `grafana:pages.Alerting.Triage.stateFilterButton:firing` | — |
| `button:has(span:contains('Pending'))` | highlight | ready | `[data-testid="data-testid triage state-filter pending"]` | `grafana:pages.Alerting.Triage.stateFilterButton:pending` | — |
| `button[aria-label='Collapse sidebar'], button[aria-label='Expand sidebar']` | highlight | ready | `[data-testid="data-testid triage sidebar-toggle-button"]` | `grafana:pages.Alerting.Triage.sidebarToggleButton` | — |
| `button[aria-label='Open in sidebar']:contains('Instance details')` | highlight | ready | `[data-testid="data-testid triage open-drawer-button"]` | `grafana:pages.Alerting.Triage.openDrawerButton` | Static testid repeated per instance row — keep :nth-match scoping. |
| `div:contains('ServiceHealth') > button[aria-label='Toggle group']` | highlight | ready | `[data-testid="data-testid triage group-row ServiceHealth"] button[aria-label='Toggle group']` | `{grafana:pages.Alerting.Triage.groupRow:ServiceHealth} button[aria-label='Toggle group']` | Param = formatted label value (instance data). Toggle button is a DESCENDANT of the row wrapper, not a direct child. |
| `div[data-testid='groups-container']` | highlight | ready | `[data-testid="data-testid triage groups-container"]` | `grafana:pages.Alerting.Triage.groupsContainer` | Literal promoted from bare groups-container (MIN preserved). |
| `[role='dialog'] section[data-testid*='Panel header']:nth-match(1)` | hover | no-change | `section[data-testid="data-testid Panel header <panel title>"]` | `grafana:components.Panels.Panel.title:<panel title>` | Pre-existing selector; scope with components.Drawer.General instead of [role=dialog]. Panel title is instance data. |

## alerting-101

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[aria-label='add contact point']` | highlight | ready | `[data-testid="data-testid contact-points add-contact-point-link"]` | `grafana:pages.Alerting.ContactPoints.addContactPointLink` | — |
| `a[href='alerting/new/alerting']` | highlight | ready | `[data-testid="data-testid rule-list empty-state-new-rule-link"]` | `grafana:pages.Alerting.RuleList.emptyStateNewRuleLink` | Empty-state CTA (NoRulesCTA). Distinct from the toolbar link, see newAlertRuleLink. |
| `button[type='submit']` | highlight | ready | `[data-testid="data-testid contact-point-form save-button"]` | `grafana:pages.Alerting.ContactPointForm.saveButton` | Mapped for the contact-point form flow (alerting-101). If another guide uses a bare button[type=submit] on a different page this mapping does not apply there. |
| `div[data-testid='contact-point-picker'] div[data-testid='input-wrapper']` | formfill | ready | `[data-testid="data-testid alert-rule contact-point-input"]` | `grafana:components.AlertRules.contactPointInput` | New selector on the Field wrapper; the Combobox input itself is components.AlertRules.contactPointPicker. |
| `input[id='contact-point-type-items.0.']` | formfill | ready | `[data-testid="data-testid contact-point-form integration-type items.0."]` | `grafana:pages.Alerting.ContactPointForm.integrationTypeField:items.0.` | Literal promoted: old DOM value was the bare rhf path (items.0.type); param = react-hook-form pathPrefix. |
| `input[id='eval-for-input']` | formfill | ready | `[data-testid="data-testid alert-rule pending-period-input"]` | `grafana:components.AlertRules.pendingPeriodInput` | — |
| `input[id='name']` | formfill x2 | ready | `[data-testid="data-testid contact-point-form name-input"]` | `grafana:pages.Alerting.ContactPointForm.nameInput` | — |
| `input[type='number']` | formfill | ready | `[data-testid="data-testid alert-rule threshold-input"]` | `grafana:components.AlertRules.thresholdInput` | Single-value threshold Input (SimpleCondition); range-variant inputs left untagged. |
| `textarea[id='items.0.settings.addresses']` | formfill | ready | `[data-testid="data-testid contact-point-form settings-field items.0.settings.addresses"]` | `grafana:pages.Alerting.ContactPointForm.settingsField:items.0.settings.addresses` | Param = full form path from the old id. |
| `a[href='/alerting/notifications']` | highlight | no-change | `a[data-testid="data-testid Nav menu item"][href='/alerting/notifications']` | `a{grafana:components.NavMenu.item}[href='/alerting/notifications']` | GD-5 compound: keep the href half; a section rendered in both the pinned box and the main nav can double-match — scope with components.NavMenu.Menu ([data-testid="data-testid navigation mega-menu"]) when needed. |
| `textarea.inputarea` | formfill | not-fixable | — | — | Monaco editor internal — not taggable in grafana/grafana. Scope the surrounding CodeEditor container (data-testid Code editor container) and drive input via keyboard instead. |

## assistant-self-hosted

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `div[data-testid='input-wrapper'] input[placeholder='Search Grafana plugins']` | formfill | ready | `[data-testid="data-testid Search field input"]` | `grafana:components.SearchField.searchInput` | 13.2.0 selector on the catalog SearchField. Never anchor on input-wrapper (grafana-ui Input internal). |
| `div[data-testid='plugin-list'] a[href='/plugins/grafana-assistant-app']` | highlight | ready | `[data-testid="data-testid Plugins list item grafana-assistant-app"]` | `grafana:pages.PluginsList.listItem:grafana-assistant-app` | Parameterized listItem makes the plugin-list outer scope unnecessary. NOTE: the list DOM testid changed plugin-list -> "data-testid Plugins list" (pages.PluginsList.list) at 13.2. |
| `div[class*='connectionBanner']` | highlight | external | — | — | owner: grafana-assistant-app. Emotion class in the assistant app. |

## billing-usage-lj/create-billing-alert

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `#eval-for-input` | highlight | ready | `[data-testid="data-testid alert-rule pending-period-input"]` | `grafana:components.AlertRules.pendingPeriodInput` | — |
| `[data-testid='add-labels-button']` | highlight | ready | `[data-testid="data-testid alert-rule add-labels-button"]` | `grafana:components.AlertRules.addLabelsButton` | Literal promoted from add-labels-button; wired in both form versions. |
| `[data-testid='contact-point-picker']` | highlight | ready | `[data-testid="data-testid alert-rule contact-point-picker"]` | `grafana:components.AlertRules.contactPointPicker` | Literal promoted: bare contact-point-picker is the MIN resolution; at >=13.2 the DOM value is the prefixed string. |
| `[data-testid='data-testid alert-rule step-2'] input[type='number']` | highlight | ready | `[data-testid="data-testid alert-rule step-2"] [data-testid="data-testid alert-rule threshold-input"]` | `{grafana:components.AlertRules.step:2} {grafana:components.AlertRules.thresholdInput}` | Keep the pre-existing AlertRules.step("2") scope around the new thresholdInput. |
| `[data-testid='folder-picker']` | highlight | ready | `[data-testid="data-testid alert-rule folder-picker"]` | `grafana:components.AlertRules.folderPicker` | Literal promoted from folder-picker. Distinct from components.FolderPicker.input (folder-picker-input) — different element. |
| `[data-testid='group-picker']` | highlight | ready | `[data-testid="data-testid alert-rule group-picker"]` | `grafana:components.AlertRules.groupPicker` | Literal promoted from group-picker; all 4 emitters wired. |
| `[data-testid='save-rule']` | highlight | ready | `[data-testid="data-testid alert-rule save-rule-button"]` | `grafana:components.AlertRules.saveRuleButton` | Literal promoted from save-rule (MIN preserved). |

## billing-usage-lj/navigate-to-billing-dashboard

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `button[aria-label='Expand folder GrafanaCloud'] ~ div a` | highlight | no-change | `[data-testid="data-testid browse dashboards row GrafanaCloud"] a` | `{grafana:pages.BrowseDashboards.table.row:GrafanaCloud} a` | Pre-existing parameterized row selector (10.2.0); folder title is instance data the guide already hardcodes. |
| `a[href*='billingusage']` | highlight | not-fixable | — | — | Cloud-provisioned billing dashboard UID — instance data. |

## categorize-collector-fleet-lj/navigate-to-fleet

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[data-testid='tab-fleet-inventory']` | highlight | external | — | — | owner: grafana-collector-app. Not fixable in grafana/grafana — owned by grafana-collector-app. Fleet Management inventory tab. |

## connect-prometheus-metrics

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[href='/connections/add-new-connection/hmInstancePromId']` | highlight | no-change | `[data-testid="data-testid Connections plugin card Prometheus"] a` | `{grafana:pages.Connections.AddNewConnection.pluginCard:Prometheus} a` | Group 6 — zero core code: card already carries the pre-existing pluginCard(name) testid (CardGrid.tsx). PARAM = Cloud catalog display name, derived best-effort from the href slug "hmInstancePromId" — verify the exact display name in the Cloud connections catalog. Testid sits on the Card wrapper; append " a" to click the anchor. |
| `input[data-testid='search-input-input']` | formfill | external | — | — | owner: grafana-easystart-app (Grafana Cloud Connections console). Not fixable in grafana/grafana — owned by grafana-easystart-app (Grafana Cloud Connections console). Search box on the Cloud /connections/add-new-connection catalog and integration setup (select-platform) pages, which the Cloud connections/onboarding app renders; OSS core uses SearchField with id, not this testid. |

## create-availability-slo-lj/configure-targets

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[href="/a/grafana-slo-app/wizard/alerts"]` | highlight | external | — | — | owner: grafana-slo-app. wizard link — SLO app UI, not grafana/grafana. |
| `a[href="/a/grafana-slo-app/wizard/review"]` | highlight | external | — | — | owner: grafana-slo-app. wizard link — SLO app UI, not grafana/grafana. |
| `input[name="name"]` | highlight | external | — | — | owner: grafana-slo-app. SLO wizard name input — SLO app UI, not grafana/grafana. |
| `input[name="objective"]` | highlight | external | — | — | owner: grafana-slo-app. SLO objective input — SLO app UI, not grafana/grafana. |
| `textarea[name="description"]` | highlight | external | — | — | owner: grafana-slo-app. SLO description — SLO app UI, not grafana/grafana. |

## create-availability-slo-lj/create-availability-slo

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `input[aria-label="Select a data source"]` | highlight | no-change | `[data-testid="data-testid Select a data source"]` | `grafana:components.DataSourcePicker.inputV2` | Core DataSourcePicker rendered inside the SLO app — pre-existing selector applies. |
| `a[data-testid='walk-next-button']` | highlight | external | — | — | owner: grafana-slo-app. wizard stepper — SLO app UI, not grafana/grafana. |
| `a[href="/a/grafana-slo-app/wizard/new"]` | highlight | external | — | — | owner: grafana-slo-app. wizard CTA — SLO app UI, not grafana/grafana. |
| `button[data-testid='run-queries-btn']` | highlight | external | — | — | owner: grafana-slo-app. run queries — SLO app UI, not grafana/grafana. |
| `input[name="timeWindow"]` | formfill | external | — | — | owner: grafana-slo-app. time window input — SLO app UI, not grafana/grafana. |

## detect-outages-synthetic-monitoring-lj/create-ping-check

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[data-testid='action create check']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check-creation action button |
| `a[href='/a/grafana-synthetic-monitoring-app/checks/new/api-endpoint']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. |
| `input[data-testid='checkEditor form job']` | formfill | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor job name input |
| `input[name='target'][placeholder='grafana.com']` | formfill | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. No core hit; matches the react-hook-form 'target' field in the Synthetic Monitoring check editor (uncertain). |
| `label[for^='option-ping-radiogroup-']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Check-type radio (ping) in Synthetic Monitoring; the id itself came from grafana-ui RadioButton's old `option-${value}-radiogroup-N` scheme, replaced by useId() in PR #124384 — anchor is stale against current grafana-ui. |

## detect-outages-synthetic-monitoring-lj/initialize-plugin

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `button[data-testid='app-init init-button']` | highlight | external | — | — | owner: external (owner not recorded in analysis). Not fixable in grafana/grafana — owned by external (owner not recorded in analysis). Not in core source or bundles; looks like an app plugin's initialization button — owning plugin not identifiable from this repo. |

## detect-outages-synthetic-monitoring-lj/navigate-to-synthetic-monitoring

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[id='pageContent'] a[href='/a/grafana-synthetic-monitoring-app/home']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. #pageContent is core; the SM home link is rendered by the SM app. |

## detect-outages-synthetic-monitoring-lj/select-probe-locations

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `button[data-testid='checkEditor form submit']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor submit button |
| `button[data-testid='checkEditor navigation execution']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor section navigation |
| `label:contains('1m')` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Pairs with frequency-component radiogroup (1m option) in the SM check editor |

## detect-outages-synthetic-monitoring-lj/view-check-dashboard

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[data-testid='timepoint-viewer']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Timepoint explorer view in Synthetic Monitoring |
| `div[data-testid='timepoint-list']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Not in core source/bundles; 'timepoint' matches the Synthetic Monitoring check timeline UI (attribution uncertain). |

## dpm-explore-up-metric

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `div[data-testid="data-source-card"]:has(small:contains("Prometheus")) button:nth-match(1)` | highlight | ready | `[data-testid="data-testid data source card Prometheus"]` | `grafana:components.DataSourcePicker.dataSourceCard:Prometheus` | Legacy data-source-card literal preserved as the MIN_GRAFANA_VERSION resolution. |
| `div[data-testid='QueryEditorModeToggle'] label:contains('Code')` | highlight | ready | `[data-testid="data-testid QueryEditorModeToggle"] [data-testid="data-testid radio-button-option code"]` | `{grafana:components.DataSource.Prometheus.queryEditor.editorToggle} {grafana:components.RadioButton.option:code}` | Scope with components.DataSource.Prometheus.queryEditor.editorToggle (pre-existing wrapper). RadioButton.option is unique within a group, not across a page — scope to the owning group container. |
| `fieldset[data-testid='data-testid prometheus type'] label:contains('Instant')` | highlight | ready | `[data-testid="data-testid prometheus type"] [data-testid="data-testid radio-button-option instant"]` | `{grafana:components.DataSource.Prometheus.queryEditor.type} {grafana:components.RadioButton.option:instant}` | Scope with the pre-existing prometheus type wrapper. RadioButton.option is unique within a group, not across a page — scope to the owning group container. |
| `textarea.inputarea` | formfill x2 | not-fixable | — | — | Monaco editor internal — not taggable in grafana/grafana. Scope the surrounding CodeEditor container (data-testid Code editor container) and drive input via keyboard instead. |

## drilldown-logs-lj/add-log-dashboard

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[role='menuitem']:contains('Add to dashboard')` | highlight | no-change | `[data-testid="data-testid explore-toolbar-add-button Add to dashboard"]` | `grafana:pages.Explore.toolbar.add:Add to dashboard` | Pre-existing parameterized selector (12.4.0); param = extension title. |
| `div[data-testid='data-testid Explore'] button:nth-match(4)` | highlight | no-change | `[data-testid="data-testid explore-toolbar-add-dropdown-button"]` | `grafana:pages.Explore.toolbar.addTo` | Pre-existing selector (12.4.0), already wired on the Explore toolbar add dropdown. |

## drilldown-logs-lj/labels-and-fields

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[aria-label='Select detected_level']` | highlight | external | — | — | owner: grafana-lokiexplore-app. Not fixable in grafana/grafana — owned by grafana-lokiexplore-app. Logs Drilldown label-selection link ('Select <label>'). |
| `a[data-testid='data-testid tab-fields']` | highlight | external | — | — | owner: grafana-lokiexplore-app. Not fixable in grafana/grafana — owned by grafana-lokiexplore-app. Logs Drilldown 'Fields' tab; not selectors.pages.AddDashboard.itemButton despite matching prefix. |
| `a[data-testid='data-testid tab-labels']` | highlight | external | — | — | owner: grafana-lokiexplore-app. Not fixable in grafana/grafana — owned by grafana-lokiexplore-app. Labels tab (with sibling tab-fields/tab-logs/tab-patterns) in the Logs Drilldown app service view at /a/grafana-lokiexplore-app/explore. |
| `a[data-testid='data-testid tab-logs']` | highlight | external | — | — | owner: grafana-lokiexplore-app. Not fixable in grafana/grafana — owned by grafana-lokiexplore-app. Logs Drilldown app builds `data-testid tab-${name}` testids; the workfile's pages.AddDashboard.itemButton e2ePath is a spurious match |
| `button:contains('Include')` | highlight | external | — | — | owner: grafana-lokiexplore-app. Not fixable in grafana/grafana — owned by grafana-lokiexplore-app. Include button on a label-value breakdown card in the Logs Drilldown Labels tab (step directly follows tab-labels/Select detected_level). |

## drilldown-logs-lj/log-patterns

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[data-testid='data-testid tab-logs']` | highlight | external | — | — | owner: grafana-lokiexplore-app. Not fixable in grafana/grafana — owned by grafana-lokiexplore-app. Logs Drilldown app builds `data-testid tab-${name}` testids; the workfile's pages.AddDashboard.itemButton e2ePath is a spurious match |
| `a[data-testid='data-testid tab-patterns']` | highlight | external | — | — | owner: grafana-lokiexplore-app. Not fixable in grafana/grafana — owned by grafana-lokiexplore-app. Patterns tab of Logs Drilldown; workfile e2ePath was a spurious match |

## drilldown-logs-lj/open-logs-explore

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `button[data-testid*='Panel menu Log volume']` | highlight | no-change | `[data-testid="data-testid Panel menu Log volume"]` | `grafana:components.Panels.Panel.menu:Log volume` | Already the strongest available anchor; panel title is supplied by the Drilldown app. |

## drilldown-logs-lj/search-logs

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `div[data-testid='input-wrapper'] input:nth-match(1)` | highlight | external | — | — | owner: grafana-lokiexplore-app. Drilldown search form; input-wrapper is a generic grafana-ui Input internal (never anchor on it). |

## drilldown-logs-lj/view-logs

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `label[data-testid*='Data source']` | highlight | no-change | `label[data-testid="data-testid Dashboard template variables submenu Label Data source"]` | `grafana:pages.Dashboard.SubMenu.submenuItemLabels:Data source` | Rendered by @grafana/scenes ControlsLabel in the Drilldown apps, but it emits the same core selector template — the exact-match form is safe. |
| `a[data-testid='data-testid button-select-service']:first-of-type` | highlight | external | — | — | owner: grafana-app-observability-app. Not fixable in grafana/grafana — owned by grafana-app-observability-app. Not in core or node_modules; e2ePath match to pages.AddDashboard.itemButton is spurious (that selector is the generic `data-testid ${title}` pattern); 'select service' points at the Application Observability service list (inferred). |
| `input[data-testid='data-testid search-services-input']` | highlight | external | — | — | owner: grafana-app-observability-app. Not fixable in grafana/grafana — owned by grafana-app-observability-app. Service inventory search input in Application Observability; not in core source or bundles. |

## drilldown-metrics-lj/add-metric-dashboard

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[role='menuitem']:contains('Add to dashboard')` | highlight | no-change | `[data-testid="data-testid explore-toolbar-add-button Add to dashboard"]` | `grafana:pages.Explore.toolbar.add:Add to dashboard` | Pre-existing parameterized selector (12.4.0); param = extension title. |
| `div[data-testid='data-testid Explore'] button:nth-match(4)` | highlight | no-change | `[data-testid="data-testid explore-toolbar-add-dropdown-button"]` | `grafana:pages.Explore.toolbar.addTo` | Pre-existing selector (12.4.0), already wired on the Explore toolbar add dropdown. |

## drilldown-metrics-lj/analyze-data

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `button[data-testid='select-action-asserts:resource:threshold']` | highlight | external | — | — | owner: grafana-asserts-app. Not fixable in grafana/grafana — owned by grafana-asserts-app. |

## drilldown-metrics-lj/open-metrics-explore

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `button[title='Menu']:nth-match(1)` | highlight | no-change | `button[data-testid='panel-menu-button']` | — | Untitled scenes panels render the hardcoded literal panel-menu-button (PanelChrome/PanelMenu.tsx); when a panel has a title the testid is components.Panels.Panel.menu(title). The literal is NOT registered in the e2e-selectors package — no grafana: token available (flagged as a future version-key candidate). |

## drilldown-metrics-lj/search-metrics

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `input[placeholder='Filter by label values']` | highlight | external | — | — | owner: @grafana/scenes AdHocFiltersVariable (rendered by the Drilldown apps). Ad-hoc filter input is scenes-library markup — fix belongs in grafana/scenes or the drilldown apps. |

## drilldown-traces-lj/view-distribution

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `input[data-testid*='Dashboard template variables Variable Value DropDown value link text']` | highlight | no-change | `[data-testid*="Dashboard template variables Variable Value DropDown value link text"]` | `grafana:pages.Dashboard.SubMenu.submenuItemValueDropDownValueLinkTexts:<variable value>` | Pre-existing parameterized selector; param = current variable value (instance data), hence the substring-match CSS form. |
| `label:contains('All spans')` | highlight | external | — | — | owner: grafana-exploretraces-app. Traces drilldown filter UI. |

## dynamic-dashboards-tour

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `#pageContent button:text('New')` | highlight | ready | `[data-testid="data-testid CreateNewButton New button"]` | `grafana:components.CreateNewButton.newButton` | Wired by programme PR #129698 (CreateNewButton.tsx). |
| `[role='menuitem']:text('New dashboard')` | highlight | ready | `[data-testid="data-testid CreateNewButton New dashboard link"]` | `grafana:components.CreateNewButton.newDashboardLink` | Wired by programme PR #129698. |
| `button:text('Group into rows')` | highlight x2 | ready | `[data-testid="data-testid sidebar add new row button"]` | `grafana:components.Sidebar.addNewRowButton` | Label flips between "Add row" / "Group into rows"; the testid is stable. |
| `button:text('Group into tabs')` | highlight x2 | ready | `[data-testid="data-testid sidebar add new tab button"]` | `grafana:components.Sidebar.addNewTabButton` | — |
| `button:text('Variable')` | highlight | ready | `[data-testid="data-testid sidebar add new variable button"]` | `grafana:components.Sidebar.addNewVariableButton` | — |
| `button[aria-label='Code']` | highlight | ready | `[data-testid="data-testid Dashboard Sidebar code button"]` | `grafana:pages.Dashboard.Sidebar.codeButton` | — |
| `div[data-testid='data-testid Sidebar container'] button:text('Configure')` | highlight | ready | `[data-testid="data-testid sidebar configure panel button"]` | `grafana:components.Sidebar.configurePanelButton` | — |
| `input[aria-label='layout-selection-option-Auto']` | highlight | ready | `[data-testid="data-testid radio-button-option AutoGridLayout"]` | `grafana:components.RadioButton.option:AutoGridLayout` | DashboardLayoutSelector option values switched to stable layout ids (AutoGridLayout, GridLayout, RowsLayout, TabsLayout); aria-labels preserved. RadioButton.option is unique within a group, not across a page — scope to the owning group container. |
| `input[aria-label='layout-selection-option-Tabs']` | highlight | ready | `[data-testid="data-testid radio-button-option TabsLayout"]` | `grafana:components.RadioButton.option:TabsLayout` | RadioButton.option is unique within a group, not across a page — scope to the owning group container. |
| `input[value='New dashboard']` | formfill | ready | `[data-testid="data-testid Save dashboard title field"]` | `grafana:components.Drawer.DashboardSaveDrawer.saveAsTitleInput` | Entry pre-existed un-prefixed (11.1.0); programme PR #129723/#129749 added the prefixed 13.2.0 key and wired the provisioned drawer, so at >=13.2 the DOM value is the prefixed string. |
| `label:text('YAML')` | highlight | ready | `[data-testid="data-testid radio-button-option yaml"]` | `grafana:components.RadioButton.option:yaml` | Export drawer format radio (ResourceExport uses string values). RadioButton.option is unique within a group, not across a page — scope to the owning group container. |
| `button:text('Add variable')` | highlight | no-change | `[data-testid="data-testid Call to action button Add variable"]` | `grafana:components.CallToActionCard.buttonV2:Add variable` | Pre-existing parameterized selector (VariableEditorList empty state). |
| `button:text('Discard')` | highlight | no-change | `[data-testid="data-testid Discard changes button"]` | `grafana:components.NavToolbar.editDashboard.discardChangesButton` | Pre-existing selector, already wired. |
| `button[aria-label='Expand Repeat options category']` | highlight | no-change | `[data-testid="data-testid Options group Repeat options toggle"]` | `grafana:components.OptionsGroup.toggle:Repeat options` | Pre-existing parameterized selector; param = options category id. |

## enable-block-editor

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `#dev-mode` | highlight | external | — | — | owner: grafana-pathfinder-app. Pathfinder settings/terminal UI lives in the pathfinder app plugin. |
| `button[data-testid='docs-panel-tab-devtools']` | highlight | external | — | — | owner: grafana-pathfinder-app. Not fixable in grafana/grafana — owned by grafana-pathfinder-app. Docs panel tabs are part of Grafana Pathfinder. |

## enable-coda

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `#dev-mode` | highlight | external | — | — | owner: grafana-pathfinder-app. Pathfinder settings/terminal UI lives in the pathfinder app plugin. |
| `[role='button']:contains('TerminalDisconnected')` | highlight | external | — | — | owner: grafana-pathfinder-app. Pathfinder settings/terminal UI lives in the pathfinder app plugin. |
| `button[data-testid='config-submit']` | highlight | external | — | — | owner: grafana-pathfinder-app. Not fixable in grafana/grafana — owned by grafana-pathfinder-app. Submit button on /plugins/grafana-pathfinder-app?page=configuration (enable-coda guide configures the Pathfinder coda terminal there). |
| `div[data-testid='input-wrapper']:nth-match(5)` | highlight | external | — | — | owner: grafana-pathfinder-app. Pathfinder settings/terminal UI lives in the pathfinder app plugin. |
| `div[data-testid='input-wrapper']:nth-match(6)` | highlight | external | — | — | owner: grafana-pathfinder-app. Pathfinder settings/terminal UI lives in the pathfinder app plugin. |
| `div[data-testid='input-wrapper']:nth-match(7)` | highlight | external | — | — | owner: grafana-pathfinder-app. Pathfinder settings/terminal UI lives in the pathfinder app plugin. |
| `label[for='enable-coda-terminal']` | highlight | external | — | — | owner: grafana-pathfinder-app. Pathfinder settings/terminal UI lives in the pathfinder app plugin. |

## explore-drilldowns-101

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `button[aria-label="Log menu"]:first-of-type` | highlight | ready | `[data-testid="data-testid Log line menu button"]` | `grafana:components.Logs.logLineMenu.menuButton` | Added by PR #129669. Repeated per log line — keep :first-of-type/:nth-match scoping. |
| `label[data-testid*="Data source"]` | highlight | no-change | `label[data-testid="data-testid Dashboard template variables submenu Label Data source"]` | `grafana:pages.Dashboard.SubMenu.submenuItemLabels:Data source` | Rendered by @grafana/scenes ControlsLabel in the Drilldown apps, but it emits the same core selector template — the exact-match form is safe. |
| `section[data-testid*="Panel header Logs"]` | highlight | no-change | `section[data-testid*="data-testid Panel header Logs"]` | `grafana:components.Panels.Panel.title:Logs` | Pre-existing parameterized selector; keep the substring match if the full title varies (title is app/dashboard data). |
| `section[data-testid*="data-testid Panel header"]:first-of-type` | highlight | no-change | `section[data-testid="data-testid Panel header <panel title>"]` | `grafana:components.Panels.Panel.title:<panel title>` | Pre-existing parameterized selector; supply the actual panel title instead of :first-of-type. |
| `div[data-testid="uplot-main-div"]:first-of-type` | highlight | not-fixable | — | — | Positional uPlot canvas pick. Re-scope via components.Panels.Panel.title(<panel title>) + components.UPlotChart.container instead of global :nth-match — panel titles are dashboard data. |
| `a[data-testid="data-testid button-select-service"]:first-of-type` | highlight | external | — | — | owner: grafana-app-observability-app. Not fixable in grafana/grafana — owned by grafana-app-observability-app. Not in core or node_modules; e2ePath match to pages.AddDashboard.itemButton is spurious (that selector is the generic `data-testid ${title}` pattern); 'select service' points at the Application Observability service list (inferred). |
| `a[data-testid="data-testid tab-fields"]` | highlight | external | — | — | owner: grafana-lokiexplore-app. Not fixable in grafana/grafana — owned by grafana-lokiexplore-app. Logs Drilldown 'Fields' tab; not selectors.pages.AddDashboard.itemButton despite matching prefix. |
| `a[data-testid="data-testid tab-labels"]` | highlight | external | — | — | owner: grafana-lokiexplore-app. Not fixable in grafana/grafana — owned by grafana-lokiexplore-app. Labels tab (with sibling tab-fields/tab-logs/tab-patterns) in the Logs Drilldown app service view at /a/grafana-lokiexplore-app/explore. |
| `a[data-testid="data-testid tab-patterns"]` | highlight | external | — | — | owner: grafana-lokiexplore-app. Not fixable in grafana/grafana — owned by grafana-lokiexplore-app. Patterns tab of Logs Drilldown; workfile e2ePath was a spurious match |
| `div[data-testid="metrics-list"] div[data-testid="with-usage-data-preview-panel"]:first-child` | highlight | external | — | — | owner: grafana-metricsdrilldown-app. Not fixable in grafana/grafana — owned by grafana-metricsdrilldown-app. Core hit (SignalExplorer/MetricsList.tsx:74) is only an emotion css label, not a testid; sibling testid with-usage-data-preview-panel belongs to Metrics Drilldown. |
| `div[data-testid="metrics-list"] div[data-testid="with-usage-data-preview-panel"]:first-child button[data-testid*="select-action"]` | highlight | external | — | — | owner: grafana-metricsdrilldown-app. Not fixable in grafana/grafana — owned by grafana-metricsdrilldown-app. Core hit (SignalExplorer/MetricsList.tsx:74) is only an emotion css label, not a testid; sibling testid with-usage-data-preview-panel belongs to Metrics Drilldown. |
| `div[id="ds"]` | highlight | external | — | — | owner: grafana-metricsdrilldown-app (@grafana/scenes variable Select). Scenes variable Select passes id=key; rendered by the Drilldown app. |
| `input[placeholder="Filter by label values"]` | highlight x2 | external | — | — | owner: @grafana/scenes AdHocFiltersVariable (rendered by the Drilldown apps). Ad-hoc filter input is scenes-library markup — fix belongs in grafana/scenes or the drilldown apps. |

## first-dashboard

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[href='/plugins/volkovlabs-rss-datasource']` | highlight | ready | `[data-testid="data-testid Plugins list item volkovlabs-rss-datasource"]` | `grafana:pages.PluginsList.listItem:volkovlabs-rss-datasource` | Dormant entry revived and parameterized on the catalog card anchor; param = plugin id from the old href. |
| `input[aria-label="Save dashboard title field"]` | formfill | ready | `[data-testid="data-testid Save dashboard title field"]` | `grafana:components.Drawer.DashboardSaveDrawer.saveAsTitleInput` | Entry pre-existed un-prefixed (11.1.0); programme PR #129723/#129749 added the prefixed 13.2.0 key and wired the provisioned drawer, so at >=13.2 the DOM value is the prefixed string. |
| `input[type='text']` | formfill x2 | ready | `[data-testid="data-testid Search field input"]` | `grafana:components.SearchField.searchInput` | 13.2.0 selector on the catalog SearchField. Never anchor on input-wrapper (grafana-ui Input internal). |
| `a[href='/connections/datasources/volkovlabs-rss-datasource']` | highlight | no-change | `[data-testid="data-testid Connections plugin card Business News"] a` | `{grafana:pages.Connections.AddNewConnection.pluginCard:Business News} a` | Pre-existing pluginCard(name); param = catalog display name of volkovlabs-rss-datasource ("Business News"). Testid on the Card wrapper; append " a" to click. |
| `a[href='/plugins']` | highlight | no-change | `a[data-testid="data-testid Nav menu item"][href='/plugins']` | `a{grafana:components.NavMenu.item}[href='/plugins']` | Old anchor already resolves to core nav markup; adopt the pre-existing components.NavMenu.item compound (add the data-testid half, keep the href). |
| `div[aria-label="Plugin visualization item Table"]` | highlight | no-change | `[data-testid="data-testid Plugin visualization item Table"]` | `grafana:components.PluginVisualization.item:Table` | aria-label form is the pre-12.4 legacy resolution; use the data-testid form. |
| `input[id='basic-settings-name']` | formfill | stale | `[data-testid="data-testid Editable title input"]` | `grafana:components.EditableTitle.titleInput` | STALE: the basic-settings-name input was deleted (#123965); the datasource name is now the page-header EditableTitle. Guide flow change required: click components.EditableTitle.editButton (data-testid Editable title edit button) to reveal the titleInput. |
| `input[placeholder='https://feed']` | formfill | external | — | — | owner: volkovlabs-rss-datasource. RSS datasource config editor field. |

## fleet-management-onboarding

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `button[aria-label="Close"]` | highlight | ready | `[data-testid="data-testid Modal close button"]` | `grafana:components.Modal.closeButton` | grafana-ui Modal header close IconButton. If the surface is a Drawer, use the pre-existing components.Drawer.General.close (data-testid Drawer close) instead. |
| `button:contains("Copy to clipboard"):nth-match(2)` | highlight | external | — | — | owner: grafana-collector-app / grafana-easystart-app. The ClipboardButton instance the guide targets lives in the external onboarding app. |
| `button[aria-label='Expand terminal']` | highlight | external | — | — | owner: grafana-collector-app. Not fixable in grafana/grafana — owned by grafana-collector-app. Expands the embedded xterm terminal (canvas.xterm-link-layer) on the Fleet Management onboarding flow at /a/grafana-collector-app/fleet-management. |
| `button[data-testid='fleet-inventory-add-collector-button']` | highlight | external | — | — | owner: grafana-collector-app (Fleet Management). Not fixable in grafana/grafana — owned by grafana-collector-app (Fleet Management). |
| `button[data-testid='generate-token-submit-button']` | highlight | external | — | — | owner: grafana-collector-app. Not fixable in grafana/grafana — owned by grafana-collector-app. Token generation in Fleet Management (collector app); pairs with the fleet-management-page anchor. |
| `button[data-testid='tab-fleet-inventory']` | highlight | external | — | — | owner: grafana-collector-app. Not fixable in grafana/grafana — owned by grafana-collector-app. Fleet Management inventory tab. |
| `canvas.xterm-link-layer:nth-of-type(1)` | highlight | external | — | — | owner: external (owner not recorded in analysis). Not fixable in grafana/grafana — owned by external (owner not recorded in analysis). Rendered by the xterm.js terminal library; not bundled in core Grafana — comes from an app plugin embedding a terminal (owning plugin not identifiable from the selector). |
| `div[data-testid^="collector-row-"]:nth-match(1)` | highlight | external | — | — | owner: grafana-collector-app (Fleet Management). Not fixable in grafana/grafana — owned by grafana-collector-app (Fleet Management). collector-* testids belong to the Fleet Management collector app. |
| `input[data-testid='generate-token-name-input']` | formfill | external | — | — | owner: grafana-collector-app. Not fixable in grafana/grafana — owned by grafana-collector-app. token generation input, most likely Fleet Management collector token flow (inference) |

## fleet-mgt-monitor-health-lj/check-health-status

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `#collector-status-filter` | highlight | external | — | — | owner: grafana-collector-app (Fleet Management). Not fixable in grafana/grafana — owned by grafana-collector-app (Fleet Management). |
| `tr:has([data-testid^="collector-row-"]) td:nth-child(3) [aria-label="Healthy"], tr:has([data-testid^="collector-row-"]) td:nth-child(3) [aria-label="Warning"], tr:has([data-testid^="collector-row-"]) td:nth-child(3) [aria-label="Warning, inactive"], tr:has([data-testid^="collector-row-"]) td:nth-child(3) [aria-label="Error"], tr:has([data-testid^="collector-row-"]) td:nth-child(3) [aria-label="Status unavailable"], tr:has([data-testid^="collector-row-"]) td:nth-child(3) [aria-label="Applying configuration"], tr:has([data-testid^="collector-row-"]) td:nth-child(3) [aria-label="Unresponsive"], tr:has([data-testid^="collector-row-"]) td:nth-child(3) [aria-label="Configuration error"], tr:has([data-testid^="collector-row-"]) td:nth-child(2) [aria-label="Healthy"], tr:has([data-testid^="collector-row-"]) td:nth-child(2) [aria-label="Warning"], tr:has([data-testid^="collector-row-"]) td:nth-child(2) [aria-label="Warning, inactive"], tr:has([data-testid^="collector-row-"]) td:nth-child(2) [aria-label="Error"], tr:has([data-testid^="collector-row-"]) td:nth-child(2) [aria-label="Status unavailable"], tr:has([data-testid^="collector-row-"]) td:nth-child(2) [aria-label="Applying configuration"], tr:has([data-testid^="collector-row-"]) td:nth-child(2) [aria-label="Unresponsive"], tr:has([data-testid^="collector-row-"]) td:nth-child(2) [aria-label="Configuration error"]` | hover | external | — | — | owner: grafana-collector-app (Fleet Management). Not fixable in grafana/grafana — owned by grafana-collector-app (Fleet Management). collector-* testids belong to the Fleet Management collector app. |

## fleet-mgt-monitor-health-lj/determine-config

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `#collector-status-filter` | highlight | external | — | — | owner: grafana-collector-app (Fleet Management). Not fixable in grafana/grafana — owned by grafana-collector-app (Fleet Management). |
| `[aria-label="Search collectors"]` | highlight | external | — | — | owner: grafana-collector-app. Not fixable in grafana/grafana — owned by grafana-collector-app. Fleet Management app collectors search field |
| `[data-testid="fleet-inventory-filter-button"]` | highlight | external | — | — | owner: grafana-collector-app. Not fixable in grafana/grafana — owned by grafana-collector-app. Fleet Management inventory UI |
| `[data-testid="tab-fleet-inventory"]` | highlight | external | — | — | owner: grafana-collector-app. Not fixable in grafana/grafana — owned by grafana-collector-app. Fleet Management inventory tab. |

## fleet-mgt-monitor-health-lj/register-collector

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[data-testid="api-access-page"] > h3 + br + br + p + div` | highlight | external | — | — | owner: external (owner not recorded in analysis). Not fixable in grafana/grafana — owned by external (owner not recorded in analysis). Not in this repo; owning Cloud app uncertain (candidates: k6-app, synthetic-monitoring) |
| `[data-testid="api-access-page"] > h3 + br + p + div` | highlight | external | — | — | owner: external (owner not recorded in analysis). Not fixable in grafana/grafana — owned by external (owner not recorded in analysis). Not in this repo; owning Cloud app uncertain (candidates: k6-app, synthetic-monitoring) |
| `[data-testid="tab-api-access"]` | highlight | external | — | — | owner: external (owner not recorded in analysis). Not fixable in grafana/grafana — owned by external (owner not recorded in analysis). Not in core source or bundles; tab-* testid on an app settings page (candidates: Fleet Management, k6, IRM) — confirm via live DOM |
| `[data-testid="tab-fleet-inventory"]` | highlight | external | — | — | owner: grafana-collector-app. Not fixable in grafana/grafana — owned by grafana-collector-app. Fleet Management inventory tab. |

## fleet-mgt-monitor-health-lj/view-health-dashboards

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `tr:has([data-testid^="collector-row-"]) td:nth-child(2) [data-testid^="collector-row-"], tr:has([data-testid^="collector-row-"]) td:nth-child(1) [data-testid^="collector-row-"]` | highlight | external | — | — | owner: grafana-collector-app (Fleet Management). Not fixable in grafana/grafana — owned by grafana-collector-app (Fleet Management). collector-* testids belong to the Fleet Management collector app. |

## git-sync-guide

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `#floating-boundary>div:nth-child(5) button:text('Save')` | highlight | ready | `[data-testid="data-testid Save dashboard drawer button"]` | `grafana:components.Drawer.DashboardSaveDrawer.saveButton` | Selector pre-existed for the plain save drawer; the programme additionally wired it onto the provisioned drawer's Save button (SaveProvisionedDashboardForm) — only one drawer renders at a time. |
| `#pageContent button:text('New')` | highlight | ready | `[data-testid="data-testid CreateNewButton New button"]` | `grafana:components.CreateNewButton.newButton` | Wired by programme PR #129698 (CreateNewButton.tsx). |
| `[role='menuitem']:contains('Use Template')` | highlight | ready | `[data-testid="data-testid CreateNewButton New template dashboard link"]` | `grafana:components.CreateNewButton.newTemplateDashboardLink` | — |
| `a[href='/admin/provisioning/repository-4301603']` | highlight | ready | `[data-testid="data-testid Provisioning repository view link repository-4301603"]` | `grafana:pages.Provisioning.RepositoryList.viewLink:repository-4301603` | Param = provisioned repository name, taken from the old href slug (instance data — each environment has its own repository name). |
| `div[data-testid='data-testid Card heading']:contains('Health')` | highlight | ready | `[data-testid="data-testid Provisioning repository overview health card"]` | `grafana:pages.Provisioning.RepositoryOverview.healthCard` | — |
| `div[data-testid='data-testid Card heading']:contains('Pull status')` | highlight | ready | `[data-testid="data-testid Provisioning repository overview pull status card"]` | `grafana:pages.Provisioning.RepositoryOverview.pullStatusCard` | — |
| `div[data-testid='data-testid Card heading']:contains('Resources')` | highlight | ready | `[data-testid="data-testid Provisioning repository overview resources card"]` | `grafana:pages.Provisioning.RepositoryOverview.resourcesCard` | — |
| `div[data-testid='manage-actions'] button:text('Delete')` | highlight | ready | `[data-testid="data-testid browse dashboards delete button"]` | `grafana:pages.BrowseDashboards.actions.deleteButton` | Sibling moveButton also added. |
| `input[role='combobox']` | formfill | ready | `[data-testid="data-testid folder-picker-input"]` | `grafana:components.FolderPicker.input` | Dormant entry (defined 10.4.0, never wired) revived and wired on the NestedFolderPicker open-state search input. Trigger button: components.FolderPicker.triggerButton. |
| `[role="dialog"] button:text('Delete')` | highlight | no-change | `[data-testid="data-testid Confirm Modal Danger Button"]` | `grafana:pages.ConfirmModal.delete` | Pre-existing selector, already wired. |
| `a[data-testid='data-testid git-sync-dashboards/ breadcrumb']` | highlight | no-change | `[data-testid="data-testid git-sync-dashboards/ breadcrumb"]` | `grafana:components.Breadcrumbs.breadcrumb:git-sync-dashboards/` | Already strong — pre-existing parameterized breadcrumb selector; param = breadcrumb title (instance data). |
| `input[aria-label='Select']` | highlight | no-change | `[data-testid="data-testid <uid> checkbox"]` | `grafana:pages.BrowseDashboards.table.checkbox:<uid>` | Pre-existing selector (10.0.0). Param = dashboard/folder UID of the row being ticked — not derivable from the old anchor; guide author must supply it (or keep row-scoped matching). |

## git-sync-setup

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `#:r2cr:` | highlight | ready | `[data-testid="data-testid folder-picker-input"]` | `grafana:components.FolderPicker.input` | Old anchor was an unstable React useId. Search input of NestedFolderPicker; the closed-state trigger is components.FolderPicker.triggerButton (data-testid folder-picker-trigger-button). |
| `#appID` | formfill | ready | `[data-testid="data-testid Provisioning connection form app id input"]` | `grafana:pages.Provisioning.ConnectionForm.appIdInput` | — |
| `#dashboard-title` | formfill | ready | `[data-testid="data-testid Save dashboard title field"]` | `grafana:components.Drawer.DashboardSaveDrawer.saveAsTitleInput` | Entry pre-existed un-prefixed (11.1.0); programme PR #129723/#129749 added the prefixed 13.2.0 key and wired the provisioned drawer, so at >=13.2 the DOM value is the prefixed string. |
| `#installationID` | formfill | ready | `[data-testid="data-testid Provisioning connection form installation id input"]` | `grafana:pages.Provisioning.ConnectionForm.installationIdInput` | — |
| `#pageContent button:contains('New')` | highlight | ready | `[data-testid="data-testid CreateNewButton New button"]` | `grafana:components.CreateNewButton.newButton` | Wired by programme PR #129698 (CreateNewButton.tsx). |
| `#privateKey` | formfill | ready | `[data-testid="data-testid Provisioning connection form private key input"]` | `grafana:pages.Provisioning.ConnectionForm.privateKeyInput` | — |
| `#repository-title` | formfill | ready | `[data-testid="data-testid Provisioning wizard repository title input"]` | `grafana:pages.Provisioning.Wizard.repositoryTitleInput` | — |
| `#title` | formfill | ready | `[data-testid="data-testid Provisioning connection form title input"]` | `grafana:pages.Provisioning.ConnectionForm.titleInput` | — |
| `[role="dialog"] button:contains('Save')` | highlight x3 | ready | `[data-testid="data-testid Save dashboard drawer button"]` | `grafana:components.Drawer.DashboardSaveDrawer.saveButton` | Selector pre-existed for the plain save drawer; the programme additionally wired it onto the provisioned drawer's Save button (SaveProvisionedDashboardForm) — only one drawer renders at a time. |
| `[role='menuitem']:contains('New dashboard')` | highlight | ready | `[data-testid="data-testid CreateNewButton New dashboard link"]` | `grafana:components.CreateNewButton.newDashboardLink` | Wired by programme PR #129698. |
| `[role='menuitem']:contains('Save as copy')` | highlight | ready | `[data-testid="data-testid Save as copy button"]` | `grafana:components.NavToolbar.editDashboard.saveAsCopyButton` | — |
| `a[href='/admin/provisioning/connect/github']` | highlight | ready | `[data-testid="data-testid Provisioning repository type card github"]` | `grafana:pages.Provisioning.repositoryTypeCard:github` | Param = repository type from the old href slug (github\|gitlab\|bitbucket\|git\|local). |
| `div[data-testid='data-testid Card heading']:contains('Health')` | highlight | ready | `[data-testid="data-testid Provisioning repository overview health card"]` | `grafana:pages.Provisioning.RepositoryOverview.healthCard` | — |
| `div[data-testid='data-testid Card heading']:contains('Jobs')` | highlight | ready | `[data-testid="data-testid Provisioning repository overview jobs card"]` | `grafana:pages.Provisioning.RepositoryOverview.jobsCard` | — |
| `div[data-testid='data-testid Card heading']:contains('Pull status')` | highlight | ready | `[data-testid="data-testid Provisioning repository overview pull status card"]` | `grafana:pages.Provisioning.RepositoryOverview.pullStatusCard` | — |
| `div[data-testid='data-testid Card heading']:contains('Resources')` | highlight | ready | `[data-testid="data-testid Provisioning repository overview resources card"]` | `grafana:pages.Provisioning.RepositoryOverview.resourcesCard` | — |
| `div[data-testid='data-testid Card heading']:contains('Webhook')` | highlight | ready | `[data-testid="data-testid Provisioning repository overview webhook card"]` | `grafana:pages.Provisioning.RepositoryOverview.webhookCard` | — |
| `div[data-testid='data-testid Nav toolbar'] svg:nth-match(2)` | highlight | ready | `[data-testid="data-testid More save options button"]` | `grafana:components.NavToolbar.editDashboard.moreSaveOptionsButton` | "More save options" chevron Button, wired in both toolbars. |
| `input[placeholder='https://github.com/owner/repository']` | highlight | ready | `[data-testid="data-testid Provisioning wizard repository url input"]` | `grafana:pages.Provisioning.Wizard.repositoryUrlInput` | Wired on both the GitHub-App Combobox and PAT Input branches (mutually exclusive). |
| `label:contains('Connect to a new app')` | highlight | ready | `[data-testid="data-testid radio-button-option new"]` | `grafana:components.RadioButton.option:new` | Generic option value — MUST be scoped to the wizard step. RadioButton.option is unique within a group, not across a page — scope to the owning group container. |
| `label:contains('Connect with GitHub App')` | highlight | ready | `[data-testid="data-testid radio-button-option github-app"]` | `grafana:components.RadioButton.option:github-app` | RadioButton.option is unique within a group, not across a page — scope to the owning group container. |
| `textarea[name="comment"]` | formfill | ready | `[data-testid="data-testid provisioned resource form comment input"]` | `grafana:components.ProvisionedResourceForm.commentInput` | Both mutually exclusive TextArea branches wired (shared save/delete drawers for dashboards + folders). |
| `div[data-testid='data-testid Built in data source list'] div:nth-match(27) button` | highlight | no-change | `[data-testid="data-testid Built in data source list"] [data-testid="data-testid data source card <data source name>"]` | `{grafana:components.DataSourcePicker.advancedModal.builtInDataSourceList} {grafana:components.DataSourcePicker.dataSourceCard:<data source name>}` | Replace the positional pick with the built-in list scope + dataSourceCard(name). The 27th item cannot be derived from the old anchor — a human must name the intended data source. |
| `Open pull request in GitHub` | button x3 | not-fixable | — | — | grafana-ui API gap: Alert exposes no test-id prop for its action button (PreviewBannerViewPR buttonContent). Interim: scope components.Alert.alertV2("info") + button. Follow-up candidate. |

## github-data-source-lj/config-github-datasource

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `input[placeholder='Personal Access Token']` | formfill | external | — | — | owner: grafana-github-datasource. Not fixable in grafana/grafana — owned by grafana-github-datasource. Core provisioning token field uses placeholder 'ghp_xxx...' (fields.ts), so this placeholder is the GitHub datasource config editor. |

## github-data-source-lj/install-github-plugin

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[href='/plugins/grafana-github-datasource']` | highlight | ready | `[data-testid="data-testid Plugins list item grafana-github-datasource"]` | `grafana:pages.PluginsList.listItem:grafana-github-datasource` | Param = plugin id from the old href. |
| `input[placeholder='Filter by name or type']` | formfill | ready | `[data-testid="data-testid Add data source search input"]` | `grafana:pages.AddDataSource.searchInput` | — |
| `input[placeholder='Search Grafana plugins']` | formfill | ready | `[data-testid="data-testid Search field input"]` | `grafana:components.SearchField.searchInput` | 13.2.0 selector on the catalog SearchField. Never anchor on input-wrapper (grafana-ui Input internal). |
| `a[href='/connections/datasources']` | highlight | no-change | `a[data-testid="data-testid Nav menu item"][href='/connections/datasources']` | `a{grafana:components.NavMenu.item}[href='/connections/datasources']` | Old anchor already resolves to core nav markup; adopt the pre-existing components.NavMenu.item compound (add the data-testid half, keep the href). |

## github-visualize-lj/build-issues-panel

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[aria-label='Query editor owner']` | highlight | external | — | — | owner: grafana-github-datasource. Not fixable in grafana/grafana — owned by grafana-github-datasource. Owner input in the GitHub datasource query editor (guide also uses sibling 'Query editor repository'). |
| `[aria-label='Query editor repository']` | highlight | external | — | — | owner: grafana-github-datasource. Not fixable in grafana/grafana — owned by grafana-github-datasource. Not in this repo, its history, deps, or bundles; 'repository' query editor field points to the GitHub datasource plugin. |

## github-visualize-lj/build-pr-panel

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[aria-label='Query editor owner']` | highlight | external | — | — | owner: grafana-github-datasource. Not fixable in grafana/grafana — owned by grafana-github-datasource. Owner input in the GitHub datasource query editor (guide also uses sibling 'Query editor repository'). |
| `[aria-label='Query editor repository']` | highlight | external | — | — | owner: grafana-github-datasource. Not fixable in grafana/grafana — owned by grafana-github-datasource. Not in this repo, its history, deps, or bundles; 'repository' query editor field points to the GitHub datasource plugin. |

## github-visualize-lj/build-repository-panel

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[aria-label='Query editor owner']` | highlight | external | — | — | owner: grafana-github-datasource. Not fixable in grafana/grafana — owned by grafana-github-datasource. Owner input in the GitHub datasource query editor (guide also uses sibling 'Query editor repository'). |
| `[aria-label='Query editor repository']` | highlight | external | — | — | owner: grafana-github-datasource. Not fixable in grafana/grafana — owned by grafana-github-datasource. Not in this repo, its history, deps, or bundles; 'repository' query editor field points to the GitHub datasource plugin. |

## grafana-13-tour-learn

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `#pageContent button:text('New')` | highlight | ready | `[data-testid="data-testid CreateNewButton New button"]` | `grafana:components.CreateNewButton.newButton` | Wired by programme PR #129698 (CreateNewButton.tsx). |
| `[role='menuitem']:text('From suggestions')` | highlight | ready | `[data-testid="data-testid BuildDashboardButton from suggestions button"]` | `grafana:components.BuildDashboardButton.fromSuggestionsButton` | — |
| `[role='menuitem']:text('Use template')` | highlight | ready | `[data-testid="data-testid CreateNewButton New template dashboard link"]` | `grafana:components.CreateNewButton.newTemplateDashboardLink` | — |
| `button:text('Build a dashboard'):nth-match(1)` | highlight | ready | `[data-testid="data-testid BuildDashboardButton trigger button"]` | `grafana:components.BuildDashboardButton.triggerButton` | Tagged on the dropdown Button (suggestedDashboards flag on); flag-off LinkButton variant untagged. |
| `button[aria-label='Close']` | highlight | ready | `[data-testid="data-testid Modal close button"]` | `grafana:components.Modal.closeButton` | grafana-ui Modal header close IconButton. If the surface is a Drawer, use the pre-existing components.Drawer.General.close (data-testid Drawer close) instead. |
| `input[placeholder='Search by name or type']` | formfill | ready | `[data-testid="data-testid PageActionBar search input"]` | `grafana:components.PageActionBar.searchInput` | — |
| `label:contains('Code')` | highlight | ready | `[data-testid="data-testid radio-button-option code"]` | `grafana:components.RadioButton.option:code` | Builder/Code editor-mode toggle. Generic value — scope to the owning editor-mode radiogroup. RadioButton.option is unique within a group, not across a page — scope to the owning group container. |
| `div[data-testid='data-testid Card heading']:nth-match(10)` | highlight | stale | — | — | Template gallery was re-rendered as DashboardCard (<article>, no Card heading testid) — the old anchor no longer matches main. Guide-side re-record needed; a parameterized card selector can be added later if the guide must pick a specific template. |
| `div[data-testid='data-testid Card heading']:nth-match(2)` | highlight | stale | — | — | Template gallery was re-rendered as DashboardCard (<article>, no Card heading testid) — the old anchor no longer matches main. Guide-side re-record needed; a parameterized card selector can be added later if the guide must pick a specific template. |
| `button:text('Save')` | highlight | external | — | — | owner: grafana-enterprise (Query Library). Query-library save flow is grafana-enterprise UI — not in grafana/grafana. |
| `button[aria-label='Delete']` | highlight | external | — | — | owner: grafana-enterprise (Query Library). Query-library delete button is grafana-enterprise UI — not in grafana/grafana. |

## grafana-13-tour-play

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `div[data-testid='data-testid radio-button'] label:contains('Autodetect')` | highlight | ready | `[data-testid="data-testid radio-button-option auto"]` | `grafana:components.RadioButton.option:auto` | PARAM UNCERTAIN: 'Autodetect' label no longer exists on main; nearest match is the XY chart series-mapping option (value 'auto', now labelled 'Auto'). Verify against the recorded step. RadioButton.option is unique within a group, not across a page — scope to the owning group container. |
| `div[data-testid='data-testid radio-button'] label:nth-match(6)` | highlight | ready | `[data-testid="data-testid radio-button-option <option value>"]` | `grafana:components.RadioButton.option:<option value>` | Positional pick (6th radio label on the page) — the option value cannot be derived from the old anchor; a human must identify which option the guide meant. RadioButton.option is unique within a group, not across a page — scope to the owning group container. |
| `label:contains('Circle')` | highlight | ready | `[data-testid="data-testid radio-button-option circle"]` | `grafana:components.RadioButton.option:circle` | XY chart point-shape option (PointShape.Circle = 'circle'). RadioButton.option is unique within a group, not across a page — scope to the owning group container. |
| `label[aria-label='Center glow']` | highlight | ready | `[data-testid="data-testid Gauge effects editor center glow switch"]` | `grafana:components.PanelEditor.Gauge.centerGlowSwitch` | Lands on the Switch <input>. NOTE: mapping doc placed this under a top-level GaugeEffectsEditor group; review moved it to components.PanelEditor.Gauge.* on main (siblings: gradientSwitch, barGlowSwitch). |
| `div[data-testid='data-testid portal-container'] div:text('Copy styles')` | highlight | no-change | `[data-testid="data-testid Panel menu item Copy styles"]` | `grafana:components.Panels.Panel.menuItems:Copy styles` | Pre-existing selector (9.5.0); param = menu item label from the old :text(). |
| `div[data-testid='data-testid portal-container'] div:text('Paste styles')` | highlight | no-change | `[data-testid="data-testid Panel menu item Paste styles"]` | `grafana:components.Panels.Panel.menuItems:Paste styles` | Pre-existing selector (9.5.0); param = menu item label from the old :text(). |
| `#gauge-segmentCount` | formfill | not-fixable | — | — | Auto-generated option-editor htmlId (getVisualizationOptions); no clean selector home without touching the option registry. Id is already semi-stable. |
| `div:text('abandon') button` | highlight | not-fixable | — | — | Node ids / log text are instance data, not core JSX. |
| `div:text('abandon_checkout') button` | highlight | not-fixable | — | — | Node ids / log text are instance data, not core JSX. |
| `div:text('bounce') button` | highlight | not-fixable | — | — | Node ids / log text are instance data, not core JSX. |
| `g#abandon_checkout` | highlight x2 | not-fixable | — | — | Node ids / log text are instance data, not core JSX. |
| `[role='menuitem']:text('Fill Color')` | highlight | external | — | — | owner: RCA demo node-graph panel plugin (not grafana/grafana). 'Override edge/node property' / 'Field config thresholds' strings do not exist in grafana/grafana — the node/edge override editor ships in a panel plugin outside the repo. |
| `[role='menuitem']:text('Stroke Color')` | highlight x2 | external | — | — | owner: RCA demo node-graph panel plugin (not grafana/grafana). 'Override edge/node property' / 'Field config thresholds' strings do not exist in grafana/grafana — the node/edge override editor ships in a panel plugin outside the repo. |
| `div[data-testid='data-testid Edge overrides Edge override rules field property editor'] input:nth-match(5)` | formfill | external | — | — | owner: RCA demo node-graph panel plugin (not grafana/grafana). 'Override edge/node property' / 'Field config thresholds' strings do not exist in grafana/grafana — the node/edge override editor ships in a panel plugin outside the repo. |
| `div[data-testid='data-testid Node overrides Node override rules field property editor'] button:text('All')` | highlight | external | — | — | owner: RCA demo node-graph panel plugin (not grafana/grafana). 'Override edge/node property' / 'Field config thresholds' strings do not exist in grafana/grafana — the node/edge override editor ships in a panel plugin outside the repo. |
| `div[data-testid='data-testid Node overrides Node override rules field property editor'] input:nth-match(1)` | highlight | external | — | — | owner: RCA demo node-graph panel plugin (not grafana/grafana). 'Override edge/node property' / 'Field config thresholds' strings do not exist in grafana/grafana — the node/edge override editor ships in a panel plugin outside the repo. |
| `div[data-testid='data-testid Node overrides Node override rules field property editor'] input:nth-match(4)` | formfill | external | — | — | owner: RCA demo node-graph panel plugin (not grafana/grafana). 'Override edge/node property' / 'Field config thresholds' strings do not exist in grafana/grafana — the node/edge override editor ships in a panel plugin outside the repo. |
| `div[data-testid='data-testid Node overrides Node override rules field property editor'] input:nth-match(6)` | formfill | external | — | — | owner: RCA demo node-graph panel plugin (not grafana/grafana). 'Override edge/node property' / 'Field config thresholds' strings do not exist in grafana/grafana — the node/edge override editor ships in a panel plugin outside the repo. |
| `div[data-testid='graphviz-panel-rendered'] div[data-testid='graphviz-panel-rendered-svg']` | highlight x2 | external | — | — | owner: external (owner not recorded in analysis). Not fixable in grafana/grafana — owned by external (owner not recorded in analysis). Not in core or bundles; from a Graphviz panel plugin (community/third-party panel). |
| `div[data-testid='input-wrapper'] input[placeholder="Field config thresholds"]:nth-match(1)` | formfill | external | — | — | owner: RCA demo node-graph panel plugin (not grafana/grafana). 'Override edge/node property' / 'Field config thresholds' strings do not exist in grafana/grafana — the node/edge override editor ships in a panel plugin outside the repo. |
| `div[data-testid='input-wrapper'] input[placeholder="Field config thresholds"]:nth-match(2)` | formfill | external | — | — | owner: RCA demo node-graph panel plugin (not grafana/grafana). 'Override edge/node property' / 'Field config thresholds' strings do not exist in grafana/grafana — the node/edge override editor ships in a panel plugin outside the repo. |
| `div[data-testid='input-wrapper'] input[placeholder="Field config thresholds"]:nth-match(3)` | formfill | external | — | — | owner: RCA demo node-graph panel plugin (not grafana/grafana). 'Override edge/node property' / 'Field config thresholds' strings do not exist in grafana/grafana — the node/edge override editor ships in a panel plugin outside the repo. |

## grafana-cloud-tour-lj/explore-connect-data

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[role='button']:has([data-testid='icon-plus-circle'])` | highlight | external | — | — | owner: Grafana Cloud console / grafana-easystart-app. Clickable wrapper is Cloud console UI; icon-plus-circle is a generic grafana-ui Icon testid. |
| `a:has([data-testid='datasource-mysql-card'])` | highlight | external | — | — | owner: grafana-easystart-app. datasource-mysql-card testid is not emitted by grafana/grafana. |
| `input[data-testid='search-input-input']` | formfill | external | — | — | owner: grafana-easystart-app (Grafana Cloud Connections console). Not fixable in grafana/grafana — owned by grafana-easystart-app (Grafana Cloud Connections console). Search box on the Cloud /connections/add-new-connection catalog and integration setup (select-platform) pages, which the Cloud connections/onboarding app renders; OSS core uses SearchField with id, not this testid. |

## grafana-cloud-tour-lj/explore-dashboards

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[href='/dashboard/new']` | highlight | ready | `[data-testid="data-testid CreateNewButton New dashboard link"]` | `grafana:components.CreateNewButton.newDashboardLink` | Wired by programme PR #129698. |
| `a[href='/dashboard/recently-deleted'] + button` | highlight | ready | `[data-testid="data-testid CreateNewButton New button"]` | `grafana:components.CreateNewButton.newButton` | Wired by programme PR #129698. |

## grafana-cloud-tour-lj/explore-send-data

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[href='/connections/add-new-connection/hmInstancePromId']` | highlight | no-change | `[data-testid="data-testid Connections plugin card Prometheus"] a` | `{grafana:pages.Connections.AddNewConnection.pluginCard:Prometheus} a` | Group 6 — zero core code: card already carries the pre-existing pluginCard(name) testid (CardGrid.tsx). PARAM = Cloud catalog display name, derived best-effort from the href slug "hmInstancePromId" — verify the exact display name in the Cloud connections catalog. Testid sits on the Card wrapper; append " a" to click the anchor. |
| `[role='button']:has([data-testid='icon-plus-circle'])` | highlight | external | — | — | owner: Grafana Cloud console / grafana-easystart-app. Clickable wrapper is Cloud console UI; icon-plus-circle is a generic grafana-ui Icon testid. |
| `input[data-testid='search-input-input']` | formfill | external | — | — | owner: grafana-easystart-app (Grafana Cloud Connections console). Not fixable in grafana/grafana — owned by grafana-easystart-app (Grafana Cloud Connections console). Search box on the Cloud /connections/add-new-connection catalog and integration setup (select-platform) pages, which the Cloud connections/onboarding app renders; OSS core uses SearchField with id, not this testid. |

## grafana-irm-configuration-lj/connect-alert-rule

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[data-testid="contact-point-picker"]` | highlight | ready | `[data-testid="data-testid alert-rule contact-point-picker"]` | `grafana:components.AlertRules.contactPointPicker` | Literal promoted: bare contact-point-picker is the MIN resolution; at >=13.2 the DOM value is the prefixed string. |
| `[data-testid="routing-options-contact-point"]` | highlight | ready | `[data-testid="data-testid alert-rule routing-options-contact-point"]` | `grafana:components.AlertRules.routingOptions:contact-point` | Literal promoted; param = routing mode (contact-point \| notification-policy). |
| `button[data-testid="save-rule"]` | button | ready | `[data-testid="data-testid alert-rule save-rule-button"]` | `grafana:components.AlertRules.saveRuleButton` | Literal promoted from save-rule (MIN preserved). |
| `input[data-testid="search-query-input"]` | highlight | ready | `[data-testid="data-testid alerting search-input"]` | `grafana:pages.Alerting.searchInput` | Literal promoted from search-query-input; 4 core components emit it on different alerting routes. |

## grafana-irm-configuration-lj/connect-grafana-alerting

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[data-pathfinder="add-integration-button"]` | button | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. data-pathfinder attributes are instrumented in app UIs for Pathfinder tutorials; 'add integration' is an IRM/OnCall concept (uncertain). |
| `[data-pathfinder="escalation-chain-option-0"]` | highlight | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. data-pathfinder attribute not in core; escalation chains are IRM/OnCall concepts |
| `[data-pathfinder="integration-grafanaalerting"]` | highlight | external | — | — | owner: grafana-pathfinder-app. Not fixable in grafana/grafana — owned by grafana-pathfinder-app. data-pathfinder attributes are injected by the Pathfinder app |
| `[data-pathfinder="integration-name-input"]` | formfill | external | — | — | owner: grafana-pathfinder-app. Not fixable in grafana/grafana — owned by grafana-pathfinder-app. data-pathfinder attributes are Pathfinder tutorial hooks; not present in this repo. |
| `[data-pathfinder="new-contact-point-input"]` | formfill | external | — | — | owner: grafana-pathfinder-app. Not fixable in grafana/grafana — owned by grafana-pathfinder-app. data-pathfinder attribute does not exist in core source; presumably injected/expected by the Pathfinder app. |
| `[data-pathfinder="route-heading-0"]` | highlight | external | — | — | owner: grafana-pathfinder-app. Not fixable in grafana/grafana — owned by grafana-pathfinder-app. data-pathfinder attributes are injected by the Pathfinder app itself |
| `[data-pathfinder="save-integration-button"]` | button | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. data-pathfinder anchor attribute (Pathfinder guide convention) on an IRM 'save integration' button; not present anywhere in this repo. |
| `[data-testid="escalation-chain-select"]` | highlight | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. OnCall/IRM escalation chain picker. |

## grafana-irm-configuration-lj/create-escalation-chain

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[data-pathfinder="escalation-chain-name-input"]` | formfill | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. data-pathfinder tutorial anchor attribute on IRM escalation chain UI |
| `[data-pathfinder="new-escalation-chain-button"]` | button | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. data-pathfinder tutorial anchor on IRM/OnCall escalation chains page. |
| `[data-pathfinder="save-escalation-chain-button"]` | button | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. data-pathfinder attribute added in the IRM app (OnCall escalation chain save button) specifically for Pathfinder tutorials. |
| `[data-pathfinder="timeline-item-1"]` | highlight | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. data-pathfinder attribute not in core; incident timeline is IRM |
| `[data-pathfinder="timeline-item-2"]` | highlight | external | — | — | owner: grafana-pathfinder-app. Not fixable in grafana/grafana — owned by grafana-pathfinder-app. data-pathfinder attributes are injected by the Pathfinder app |
| `[data-pathfinder="timeline-item-3"]` | highlight | external | — | — | owner: grafana-pathfinder-app. Not fixable in grafana/grafana — owned by grafana-pathfinder-app. data-pathfinder attributes are Pathfinder tutorial hooks; not present in this repo. |
| `div:text("Notify users from on-call schedule")` | highlight | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. OnCall escalation-chain step text in the IRM app. |
| `div:text("Notify users")` | highlight | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. 'Notify users' text not in this repo; matches IRM/OnCall escalation step wording — attribution uncertain. |
| `div:text("Wait")` | highlight | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. Wait step in the IRM escalation-chain timeline editor (surrounded by 'Notify users from on-call schedule' and data-pathfinder timeline-item anchors). |
| `div[data-testid="input-wrapper"] input[placeholder="Select Schedule"]` | highlight | external | — | — | owner: grafana-irm-app. IRM escalation-chain form; input-wrapper is a generic grafana-ui Input internal. |

## grafana-irm-configuration-lj/create-on-call-schedule

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[data-pathfinder="add-user-select"]` | highlight | external | — | — | owner: grafana-pathfinder-app. Not fixable in grafana/grafana — owned by grafana-pathfinder-app. data-pathfinder attributes belong to the Pathfinder app/demo |
| `[data-pathfinder="create-web-schedule-button"]` | button | external | — | — | owner: grafana-pathfinder-app. Not fixable in grafana/grafana — owned by grafana-pathfinder-app. data-pathfinder demo anchor attribute; not present in core. |
| `[data-pathfinder="new-schedule-button"]` | button | external | — | — | owner: external (owner not recorded in analysis). Not fixable in grafana/grafana — owned by external (owner not recorded in analysis). data-pathfinder is guide instrumentation added inside a target app; not in OSS source — schedule UI, likely grafana-irm-app (OnCall schedules), k6, or enterprise reporting. |
| `[data-pathfinder="save-rotation-button"]` | button | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. data-pathfinder tutorial hook on the IRM schedule rotation save button; attribute not in core source or bundles. |
| `[data-pathfinder="save-schedule-button"]` | button | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. OnCall schedules save button instrumented with data-pathfinder for Pathfinder tutorials (uncertain). |
| `[data-pathfinder="schedule-name"]` | formfill | external | — | — | owner: grafana-pathfinder-app. Not fixable in grafana/grafana — owned by grafana-pathfinder-app. data-pathfinder attributes belong to the Pathfinder app/demo |
| `div[data-testid="schedule-rotations"] button:first-of-type` | highlight | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. OnCall/IRM schedule rotations UI; not in core source or bundles. |

## grafana-irm-configuration-lj/run-end-to-end-test

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[data-pathfinder="send-demo-alert-button"]` | button | external | — | — | owner: grafana-pathfinder-app. Not fixable in grafana/grafana — owned by grafana-pathfinder-app. data-pathfinder demo anchor attribute; not present in core. |
| `[data-pathfinder="submit-send-alert-button"]` | button | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. data-pathfinder tutorial anchor attribute on IRM send-alert UI |
| `[data-testid="integration-url"]:nth-match(1) a` | highlight | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. OnCall/IRM integration endpoint URL field. |
| `button:text("Acknowledge")` | highlight | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. No core 'Acknowledge' button; matches the IRM/OnCall alert-group acknowledge action. |

## haproxy-load-balancer-lj/install-alloy

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `button[data-testid='agent-config-button']` | highlight | external | — | — | owner: grafana-collector-app. Not fixable in grafana/grafana — owned by grafana-collector-app. Fleet Management (Alloy/collector) UI; not in this repo |

## haproxy-load-balancer-lj/install-dashboards

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[href='/connections/add-new-connection/haproxy']` | highlight | no-change | `[data-testid="data-testid Connections plugin card HAProxy"] a` | `{grafana:pages.Connections.AddNewConnection.pluginCard:HAProxy} a` | Group 6 — zero core code: card already carries the pre-existing pluginCard(name) testid (CardGrid.tsx). PARAM = Cloud catalog display name, derived best-effort from the href slug "haproxy" — verify the exact display name in the Cloud connections catalog. Testid sits on the Card wrapper; append " a" to click the anchor. |
| `[aria-label='Search connections by name']` | formfill | external | — | — | owner: grafana-easystart-app. Not fixable in grafana/grafana — owned by grafana-easystart-app. Not in core; likely the Cloud onboarding/Connections console search input (uncertain). |
| `[data-testid='install-button']` | highlight | external | — | — | owner: grafana-easystart-app. Not fixable in grafana/grafana — owned by grafana-easystart-app. Not in core source/bundles; likely the Connections integration install button in the cloud onboarding app (low confidence). The VersionInstallButton grep hit is an unrelated i18n key. |
| `a[data-testid='view-dashboards-button']` | highlight | external | — | — | owner: grafana-easystart-app. Not fixable in grafana/grafana — owned by grafana-easystart-app. Not in core or bundles; likely the Cloud onboarding/integrations app 'View dashboards' button after installing an integration (uncertain). |

## haproxy-load-balancer-lj/select-platform

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[href='/connections/add-new-connection/haproxy']` | highlight | no-change | `[data-testid="data-testid Connections plugin card HAProxy"] a` | `{grafana:pages.Connections.AddNewConnection.pluginCard:HAProxy} a` | Group 6 — zero core code: card already carries the pre-existing pluginCard(name) testid (CardGrid.tsx). PARAM = Cloud catalog display name, derived best-effort from the href slug "haproxy" — verify the exact display name in the Cloud connections catalog. Testid sits on the Card wrapper; append " a" to click the anchor. |
| `div[data-testid='collector-arch-selection'] input` | highlight | external | — | — | owner: grafana-collector-app (Fleet Management). Not fixable in grafana/grafana — owned by grafana-collector-app (Fleet Management). |
| `div[data-testid='collector-os-selection'] input` | highlight | external | — | — | owner: grafana-collector-app. Not fixable in grafana/grafana — owned by grafana-collector-app. Fleet Management (Alloy collector) Cloud app. |
| `input[data-testid='search-input-input']` | formfill | external | — | — | owner: grafana-easystart-app (Grafana Cloud Connections console). Not fixable in grafana/grafana — owned by grafana-easystart-app (Grafana Cloud Connections console). Search box on the Cloud /connections/add-new-connection catalog and integration setup (select-platform) pages, which the Cloud connections/onboarding app renders; OSS core uses SearchField with id, not this testid. |

## how-to-import-external-alerting-resource-5e08

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `#pageContent a[href='/alerting/list']` | highlight | ready | `[data-testid="data-testid alerting welcome-cta-link /alerting/list"]` | `grafana:pages.Alerting.Home.welcomeCtaLink:/alerting/list` | Param = CTA href from the old anchor (one parameterized selector across the 4 welcome CTA boxes). |
| `#pageContent input[role='combobox']` | formfill | ready | `[data-testid="data-testid import-to-gma alertmanager-datasource-field"] input` | `{grafana:pages.Alerting.ImportToGMA.alertmanagerDataSourceField} input` | Selector is on the Field wrapper — scope " input" inside to reach the combobox. |
| `[role='menuitem']:contains('Import to Grafana Alerting')` | highlight | ready | `[data-testid="data-testid rule-list import-to-gma-link"]` | `grafana:pages.Alerting.RuleList.moreMenu.importToGmaLink` | — |
| `button:contains('More'):nth-match(1)` | highlight | ready | `[data-testid="data-testid rule-list more-menu-trigger-button"]` | `grafana:pages.Alerting.RuleList.moreMenu.triggerButton` | — |
| `button[data-testid='wizard-next-button']` | highlight x2 | ready | `[data-testid="data-testid import-to-gma next-button"]` | `grafana:pages.Alerting.ImportToGMA.nextButton` | Literal promoted from wizard-next-button (MIN preserved); sibling skipButton also migrated. |
| `input[placeholder='All groups']` | highlight | ready | `[data-testid="data-testid import-to-gma group-input"]` | `grafana:pages.Alerting.ImportToGMA.groupInput` | — |
| `input[placeholder='All namespaces']` | highlight | ready | `[data-testid="data-testid import-to-gma namespace-input"]` | `grafana:pages.Alerting.ImportToGMA.namespaceInput` | — |
| `input[placeholder='Select a policy tree']` | highlight | ready | `[data-testid="data-testid import-to-gma policy-tree-input"]` | `grafana:pages.Alerting.ImportToGMA.policyTreeInput` | — |
| `div[data-testid='input-wrapper'] #data-source-picker` | formfill | no-change | `[data-testid="data-testid Select a data source"]` | `grafana:components.DataSourcePicker.inputV2` | Pre-existing selector, already wired. |
| `label[title='Import from an Alertmanager data source']` | highlight | not-fixable | — | — | grafana-ui API gap: RadioButtonList/RadioButtonDot forward no test id (RadioButton.option does not apply — different component). Follow-up candidate (grafana-ui change). |

## how-to-setup-secrets-tutorial

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `#mega-menu-toggle` | highlight | ready | `[data-testid="data-testid Toggle menu"]` | `grafana:components.NavBar.Toggle.button` | Dormant entry (10.2.3, zero bindings) wired on the SingleTopBar ToolbarButton (PR #129818). |
| `#secret-description` | formfill x2 | external | — | — | owner: k6-app. Not fixable in grafana/grafana — owned by k6-app. Not in core (only unrelated i18n key hit); matches the Grafana Cloud k6 secrets management form (pairs with the quickpizza secret anchor). |
| `#secret-name` | formfill x2 | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. not in core source or bundles; most likely the Synthetic Monitoring secrets UI name input (inference — verify via live DOM) |
| `#secret-value` | formfill x2 | external | — | — | owner: external (owner not recorded in analysis). Not fixable in grafana/grafana — owned by external (owner not recorded in analysis). Not in core source or bundles; likely a Cloud app secrets form (e.g. Synthetic Monitoring secrets management) — plugin not confidently identifiable. |
| `[data-testid='action create check']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check-creation action button |
| `button:contains('Save')` | highlight x3 | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Save button of the Create secret form on the SM Config > Secrets tab (guide fills #secret-name/#secret-value immediately before). |
| `button[aria-label='Delete quickpizza-password']` | highlight | external | — | — | owner: k6-app. Not fixable in grafana/grafana — owned by k6-app. quickpizza is the k6 demo service; likely the Cloud k6 secrets management delete button. |
| `button[aria-label='Delete quickpizza-username']` | highlight | external | — | — | owner: k6-app. Not fixable in grafana/grafana — owned by k6-app. quickpizza is the k6 demo service; secret delete button in k6 Cloud secrets management. |
| `button[data-testid='checkEditor form submit']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor submit button |
| `button[data-testid='checkEditor navigation execution']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor section navigation |
| `div[data-testid='check-group-card-browser'] a:nth-match(1)` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Check-type group card on the Synthetic Monitoring add-check page |
| `form[data-testid='checkEditor form'] label:nth-match(5)` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor form. |
| `input[data-testid='checkEditor form instance']` | formfill | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor form field. |
| `input[data-testid='checkEditor form job']` | formfill | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor job name input |
| `section[data-testid='config-content'] button:nth-match(2)` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Content section of the Secrets tab under /a/grafana-synthetic-monitoring-app/config (guide edits a secret via the section's second button). |

## iis-web-server-lj/install-alloy

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[data-testid='agent-config-button']` | highlight | external | — | — | owner: grafana-collector-app. Not fixable in grafana/grafana — owned by grafana-collector-app. Fleet Management (Alloy/collector) UI; not in this repo |

## iis-web-server-lj/install-dashboards

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[data-testid='install-button']` | button | external | — | — | owner: grafana-easystart-app. Not fixable in grafana/grafana — owned by grafana-easystart-app. Not in core source/bundles; likely the Connections integration install button in the cloud onboarding app (low confidence). The VersionInstallButton grep hit is an unrelated i18n key. |
| `a[data-testid='view-dashboards-button']` | highlight | external | — | — | owner: grafana-easystart-app. Not fixable in grafana/grafana — owned by grafana-easystart-app. Not in core or bundles; likely the Cloud onboarding/integrations app 'View dashboards' button after installing an integration (uncertain). |

## iis-web-server-lj/select-integration

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[href='/connections/add-new-connection/microsoft-iis']` | highlight | no-change | `[data-testid="data-testid Connections plugin card Microsoft IIS"] a` | `{grafana:pages.Connections.AddNewConnection.pluginCard:Microsoft IIS} a` | Group 6 — zero core code: card already carries the pre-existing pluginCard(name) testid (CardGrid.tsx). PARAM = Cloud catalog display name, derived best-effort from the href slug "microsoft-iis" — verify the exact display name in the Cloud connections catalog. Testid sits on the Card wrapper; append " a" to click the anchor. |
| `[aria-label='Search connections by name']` | formfill | external | — | — | owner: grafana-easystart-app. Not fixable in grafana/grafana — owned by grafana-easystart-app. Not in core; likely the Cloud onboarding/Connections console search input (uncertain). |

## iis-web-server-lj/verify-metrics

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[data-testid='test-connection-button']` | button | external | — | — | owner: grafana-easystart-app. Not fixable in grafana/grafana — owned by grafana-easystart-app. Cloud onboarding integration install flow (test connection step) |

## infinity-csv-lj/add-data-source

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[placeholder='Filter by name or type']` | formfill | ready | `[data-testid="data-testid Add data source search input"]` | `grafana:pages.AddDataSource.searchInput` | — |
| `button[aria-label='Add new data source Infinity']` | highlight | no-change | `[data-testid="data-testid Add new data source Infinity"]` | `grafana:pages.AddDataSource.dataSourcePluginsV2:Infinity` | Pre-existing selector; the aria-label form is the legacy 9.3.1 resolution — retarget to the testid. |

## infinity-csv-lj/build-dashboard

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `input[placeholder='Search for...']` | formfill | ready | `[data-testid="data-testid Panel editor viz type picker search input"]` | `grafana:components.PanelEditor.VizTypePicker.searchInput` | — |
| `[data-testid='infinity-query-field-label-method']` | highlight | external | — | — | owner: yesoreyeram-infinity-datasource. Infinity datasource editor UI ships in the external plugin. |
| `[data-testid='infinity-query-field-label-type']` | highlight | external | — | — | owner: yesoreyeram-infinity-datasource. Infinity datasource editor UI ships in the external plugin. |
| `[data-testid='infinity-query-url-input']` | formfill | external | — | — | owner: yesoreyeram-infinity-datasource. Infinity datasource editor UI ships in the external plugin. |
| `button[aria-label='Toggle Parsing options & Result fields']` | highlight | external | — | — | owner: yesoreyeram-infinity-datasource. Infinity datasource editor UI ships in the external plugin. |
| `input[placeholder=',']` | formfill | external | — | — | owner: yesoreyeram-infinity-datasource. Infinity datasource editor UI ships in the external plugin. |

## infinity-csv-lj/select-private-connection

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[aria-label='Private data source connect']` | highlight | external | — | — | owner: grafana-pdc-app. PDC select on the datasource config page is injected via UI extensions; no core match. |

## influxdb-data-source-lj/add-data-source

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `input[placeholder='Filter by name or type']` | formfill | ready | `[data-testid="data-testid Add data source search input"]` | `grafana:pages.AddDataSource.searchInput` | — |
| `a[href='/connections/datasources']` | highlight | no-change | `a[data-testid="data-testid Nav menu item"][href='/connections/datasources']` | `a{grafana:components.NavMenu.item}[href='/connections/datasources']` | Old anchor already resolves to core nav markup; adopt the pre-existing components.NavMenu.item compound (add the data-testid half, keep the href). |

## influxdb-data-source-lj/configure-connection

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[data-testid='influxdb-v2-config-product-select']` | highlight | ready | `[data-testid="data-testid influxdb-v2-config-product-select"]` | `grafana:components.DataSource.InfluxDB.configPage.productSelect` | **gate: plugin rollout.** PR #129814; influxdb config UI is plugin-bundle code — applies once the NEW influxdb plugin asset is what the stack loads. Literal promoted: the bare influxdb-v2-config-* value is preserved as the MIN resolution; at >=13.2 (new bundle) the DOM value is the prefixed string. |
| `[data-testid='influxdb-v2-config-query-language-select']` | highlight | ready | `[data-testid="data-testid influxdb-v2-config-query-language-select"]` | `grafana:components.DataSource.InfluxDB.configPage.queryLanguageSelect` | **gate: plugin rollout.** PR #129814; influxdb config UI is plugin-bundle code — applies once the NEW influxdb plugin asset is what the stack loads. Literal promoted: the bare influxdb-v2-config-* value is preserved as the MIN resolution; at >=13.2 (new bundle) the DOM value is the prefixed string. |
| `[data-testid='influxdb-v2-config-url-input']` | highlight | ready | `[data-testid="data-testid influxdb-v2-config-url-input"]` | `grafana:components.DataSource.InfluxDB.configPage.urlInput` | **gate: plugin rollout.** PR #129814; influxdb config UI is plugin-bundle code — applies once the NEW influxdb plugin asset is what the stack loads. Literal promoted: the bare influxdb-v2-config-* value is preserved as the MIN resolution; at >=13.2 (new bundle) the DOM value is the prefixed string. |
| `input#default-bucket` | highlight | ready | `[data-testid="data-testid influxdb-v2-config-default-bucket-input"]` | `grafana:components.DataSource.InfluxDB.configPage.defaultBucketInput` | **gate: plugin rollout.** PR #129814; influxdb config UI is plugin-bundle code — applies once the NEW influxdb plugin asset is what the stack loads. |
| `input#organization` | highlight | ready | `[data-testid="data-testid influxdb-v2-config-organization-input"]` | `grafana:components.DataSource.InfluxDB.configPage.organizationInput` | **gate: plugin rollout.** PR #129814; influxdb config UI is plugin-bundle code — applies once the NEW influxdb plugin asset is what the stack loads. |
| `input#token` | highlight | ready | `[data-testid="data-testid influxdb-v2-config-token-input"]` | `grafana:components.DataSource.InfluxDB.configPage.tokenInput` | **gate: plugin rollout.** PR #129814; influxdb config UI is plugin-bundle code — applies once the NEW influxdb plugin asset is what the stack loads. Wired in both mutually exclusive Flux/SQL connection branches. The old #token id collided with the provisioning wizard token input across pages — exactly why the id anchor was weak. |

## influxdb-data-source-lj/explore-data

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[data-testid='query-editor-rows']` | highlight | no-change | `[data-testid='query-editor-rows']` | — | Hardcoded core literal (QueryEditorRows.tsx), still on main — anchor keeps working, but it is NOT registered in the e2e-selectors package, so no grafana: token exists (future version-key candidate). Per-row container: components.QueryEditorRows.rows (data-testid Query editor row). |
| `button[aria-label='Run query']` | highlight | no-change | `[data-testid="data-testid RefreshPicker run button"]` | `grafana:components.RefreshPicker.runButtonV2` | Pre-existing selector, already wired. |

## infrastructure-alerting-lj/build-your-query

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[href="/alerting/new/alerting"]` | highlight | ready | `[data-testid="data-testid rule-list new-alert-rule-link"]` | `grafana:pages.Alerting.RuleList.newAlertRuleLink` | Toolbar "New alert rule" LinkButton (RuleList.v2) — a different element from the empty-state CTA. |

## infrastructure-alerting-lj/notification-settings

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[href='/alerting/notifications']` | highlight | ready | `[data-testid="data-testid alert-rule view-contact-points-link"]` | `grafana:components.AlertRules.viewContactPointsLink` | Same href, different element: inside the rule editor this is the "View contact points" TextLink (both form versions wired), NOT the nav-menu anchor. |

## infrastructure-alerting-lj/save-and-activate

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `input[placeholder='Give your alert rule a name']` | highlight | no-change | `[data-testid="data-testid alert-rule name-field"]` | `grafana:components.AlertRules.ruleNameField` | Pre-existing selector, already wired. |

## irm-configuration

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[data-pathfinder="add-integration-button"]` | button | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. data-pathfinder attributes are instrumented in app UIs for Pathfinder tutorials; 'add integration' is an IRM/OnCall concept (uncertain). |
| `[data-pathfinder="add-user-select"]` | highlight | external | — | — | owner: grafana-pathfinder-app. Not fixable in grafana/grafana — owned by grafana-pathfinder-app. data-pathfinder attributes belong to the Pathfinder app/demo |
| `[data-pathfinder="create-web-schedule-button"]` | button | external | — | — | owner: grafana-pathfinder-app. Not fixable in grafana/grafana — owned by grafana-pathfinder-app. data-pathfinder demo anchor attribute; not present in core. |
| `[data-pathfinder="escalation-chain-name-input"]` | formfill | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. data-pathfinder tutorial anchor attribute on IRM escalation chain UI |
| `[data-pathfinder="escalation-chain-option-0"]` | highlight | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. data-pathfinder attribute not in core; escalation chains are IRM/OnCall concepts |
| `[data-pathfinder="integration-grafanaalerting"]` | highlight | external | — | — | owner: grafana-pathfinder-app. Not fixable in grafana/grafana — owned by grafana-pathfinder-app. data-pathfinder attributes are injected by the Pathfinder app |
| `[data-pathfinder="integration-name-input"]` | formfill | external | — | — | owner: grafana-pathfinder-app. Not fixable in grafana/grafana — owned by grafana-pathfinder-app. data-pathfinder attributes are Pathfinder tutorial hooks; not present in this repo. |
| `[data-pathfinder="new-contact-point-input"]` | formfill | external | — | — | owner: grafana-pathfinder-app. Not fixable in grafana/grafana — owned by grafana-pathfinder-app. data-pathfinder attribute does not exist in core source; presumably injected/expected by the Pathfinder app. |
| `[data-pathfinder="new-escalation-chain-button"]` | button | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. data-pathfinder tutorial anchor on IRM/OnCall escalation chains page. |
| `[data-pathfinder="new-schedule-button"]` | button | external | — | — | owner: external (owner not recorded in analysis). Not fixable in grafana/grafana — owned by external (owner not recorded in analysis). data-pathfinder is guide instrumentation added inside a target app; not in OSS source — schedule UI, likely grafana-irm-app (OnCall schedules), k6, or enterprise reporting. |
| `[data-pathfinder="route-heading-0"]` | highlight | external | — | — | owner: grafana-pathfinder-app. Not fixable in grafana/grafana — owned by grafana-pathfinder-app. data-pathfinder attributes are injected by the Pathfinder app itself |
| `[data-pathfinder="save-escalation-chain-button"]` | button | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. data-pathfinder attribute added in the IRM app (OnCall escalation chain save button) specifically for Pathfinder tutorials. |
| `[data-pathfinder="save-integration-button"]` | button | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. data-pathfinder anchor attribute (Pathfinder guide convention) on an IRM 'save integration' button; not present anywhere in this repo. |
| `[data-pathfinder="save-rotation-button"]` | button | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. data-pathfinder tutorial hook on the IRM schedule rotation save button; attribute not in core source or bundles. |
| `[data-pathfinder="save-schedule-button"]` | button | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. OnCall schedules save button instrumented with data-pathfinder for Pathfinder tutorials (uncertain). |
| `[data-pathfinder="schedule-name"]` | formfill | external | — | — | owner: grafana-pathfinder-app. Not fixable in grafana/grafana — owned by grafana-pathfinder-app. data-pathfinder attributes belong to the Pathfinder app/demo |
| `[data-pathfinder="send-demo-alert-button"]` | button | external | — | — | owner: grafana-pathfinder-app. Not fixable in grafana/grafana — owned by grafana-pathfinder-app. data-pathfinder demo anchor attribute; not present in core. |
| `[data-pathfinder="submit-send-alert-button"]` | button | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. data-pathfinder tutorial anchor attribute on IRM send-alert UI |
| `[data-pathfinder="timeline-item-1"]` | highlight | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. data-pathfinder attribute not in core; incident timeline is IRM |
| `[data-pathfinder="timeline-item-2"]` | highlight | external | — | — | owner: grafana-pathfinder-app. Not fixable in grafana/grafana — owned by grafana-pathfinder-app. data-pathfinder attributes are injected by the Pathfinder app |
| `[data-pathfinder="timeline-item-3"]` | highlight | external | — | — | owner: grafana-pathfinder-app. Not fixable in grafana/grafana — owned by grafana-pathfinder-app. data-pathfinder attributes are Pathfinder tutorial hooks; not present in this repo. |
| `div:text("Notify users from on-call schedule")` | highlight | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. OnCall escalation-chain step text in the IRM app. |
| `div:text("Notify users")` | highlight | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. 'Notify users' text not in this repo; matches IRM/OnCall escalation step wording — attribution uncertain. |
| `div:text("Wait")` | highlight | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. Wait step in the IRM escalation-chain timeline editor (surrounded by 'Notify users from on-call schedule' and data-pathfinder timeline-item anchors). |
| `div[data-testid="input-wrapper"] input[placeholder="Select Schedule"]` | highlight | external | — | — | owner: grafana-irm-app. IRM escalation-chain form; input-wrapper is a generic grafana-ui Input internal. |
| `div[data-testid="schedule-rotations"] button:first-of-type` | highlight | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. OnCall/IRM schedule rotations UI; not in core source or bundles. |
| `div[data-testid='escalation-chain-select']` | highlight | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. OnCall/IRM escalation chain picker. |

## k6-extensions-grafana-cloud

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[data-testid="project-listing-layout-table"] a:nth-match(1)` | highlight | external | — | — | owner: k6-app. Not fixable in grafana/grafana — owned by k6-app. k6 project listing table. |

## k8s-cpu

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `section[data-testid*='Alignment: Container Usage/Requests']` | highlight | no-change | `section[data-testid*='Alignment: Container Usage/Requests']` | `grafana:components.Panels.Panel.title:<full panel title>` | Pre-existing parameterized selector; the panel title comes from the Kubernetes Monitoring app scene — substring match is the pragmatic form. |
| `a[data-testid='data-testid Data link'][href^='/a/grafana-k8s-app/navigation/namespace/'][href*='/quickpizza']` | highlight | not-fixable | — | — | components.DataLinksContextMenu.singleLink exists, but link identity (href/row) is dashboard/instance data — no per-link stable key available in core. |
| `canvas:nth-of-type(2):nth-match(3)` | highlight | not-fixable | — | — | Positional uPlot canvas pick. Re-scope via components.Panels.Panel.title(<panel title>) + components.UPlotChart.container instead of global :nth-match — panel titles are dashboard data. |
| `div[data-testid='uplot-main-div']:nth-match(6)` | highlight | not-fixable | — | — | Positional uPlot canvas pick. Re-scope via components.Panels.Panel.title(<panel title>) + components.UPlotChart.container instead of global :nth-match — panel titles are dashboard data. |
| `div[role='gridcell'][aria-colindex='1'] a[data-testid='data-testid Data link']:nth-match(1)` | highlight x2 | not-fixable | — | — | components.DataLinksContextMenu.singleLink exists, but link identity (href/row) is dashboard/instance data — no per-link stable key available in core. |
| `div[role='row'][aria-rowindex='2'] div[role='gridcell'][aria-colindex='1'] a[data-testid='data-testid Data link']` | highlight | not-fixable | — | — | components.DataLinksContextMenu.singleLink exists, but link identity (href/row) is dashboard/instance data — no per-link stable key available in core. |

## k8s-mem

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `section[data-testid*='Alignment: Container Usage/Requests']` | highlight | no-change | `section[data-testid*='Alignment: Container Usage/Requests']` | `grafana:components.Panels.Panel.title:<full panel title>` | Pre-existing parameterized selector; the panel title comes from the Kubernetes Monitoring app scene — substring match is the pragmatic form. |
| `a[data-testid='data-testid Data link']:nth-match(1)` | highlight | not-fixable | — | — | components.DataLinksContextMenu.singleLink exists, but link identity (href/row) is dashboard/instance data — no per-link stable key available in core. |
| `canvas:nth-of-type(2):nth-match(2)` | highlight | not-fixable | — | — | Positional uPlot canvas pick. Re-scope via components.Panels.Panel.title(<panel title>) + components.UPlotChart.container instead of global :nth-match — panel titles are dashboard data. |
| `canvas:nth-of-type(2):nth-match(4)` | highlight | not-fixable | — | — | Positional uPlot canvas pick. Re-scope via components.Panels.Panel.title(<panel title>) + components.UPlotChart.container instead of global :nth-match — panel titles are dashboard data. |
| `div[data-testid='uplot-main-div']:nth-match(5)` | highlight | not-fixable | — | — | Positional uPlot canvas pick. Re-scope via components.Panels.Panel.title(<panel title>) + components.UPlotChart.container instead of global :nth-match — panel titles are dashboard data. |
| `div[data-testid='uplot-main-div']:nth-match(6)` | highlight | not-fixable | — | — | Positional uPlot canvas pick. Re-scope via components.Panels.Panel.title(<panel title>) + components.UPlotChart.container instead of global :nth-match — panel titles are dashboard data. |
| `div[role='gridcell'][aria-colindex='1'] a[data-testid='data-testid Data link']:nth-match(1)` | highlight x2 | not-fixable | — | — | components.DataLinksContextMenu.singleLink exists, but link identity (href/row) is dashboard/instance data — no per-link stable key available in core. |
| `div[role='row'][aria-rowindex='2'] div[role='gridcell'][aria-colindex='1'] a[data-testid='data-testid Data link']` | highlight | not-fixable | — | — | components.DataLinksContextMenu.singleLink exists, but link identity (href/row) is dashboard/instance data — no per-link stable key available in core. |

## kafka-monitoring-lj/install-dashboards

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[data-testid='install-button']` | highlight | external | — | — | owner: grafana-easystart-app. Not fixable in grafana/grafana — owned by grafana-easystart-app. Not in core source/bundles; likely the Connections integration install button in the cloud onboarding app (low confidence). The VersionInstallButton grep hit is an unrelated i18n key. |
| `[data-testid='view-dashboards-button']` | highlight | external | — | — | owner: grafana-easystart-app. Not fixable in grafana/grafana — owned by grafana-easystart-app. Not in core or bundles; likely the Cloud onboarding/integrations app 'View dashboards' button after installing an integration (uncertain). |

## kafka-monitoring-lj/install-grafana-alloy

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[href='/connections/add-new-connection/kafka']` | highlight | no-change | `[data-testid="data-testid Connections plugin card Kafka"] a` | `{grafana:pages.Connections.AddNewConnection.pluginCard:Kafka} a` | Group 6 — zero core code: card already carries the pre-existing pluginCard(name) testid (CardGrid.tsx). PARAM = Cloud catalog display name, derived best-effort from the href slug "kafka" — verify the exact display name in the Cloud connections catalog. Testid sits on the Card wrapper; append " a" to click the anchor. |
| `[data-testid='agent-config-button']` | highlight | external | — | — | owner: grafana-collector-app. Not fixable in grafana/grafana — owned by grafana-collector-app. Fleet Management (Alloy/collector) UI; not in this repo |
| `[data-testid='search-input-input']` | formfill | external | — | — | owner: grafana-easystart-app (Grafana Cloud Connections console). Not fixable in grafana/grafana — owned by grafana-easystart-app (Grafana Cloud Connections console). Search box on the Cloud /connections/add-new-connection catalog and integration setup (select-platform) pages, which the Cloud connections/onboarding app renders; OSS core uses SearchField with id, not this testid. |

## knowledge-graph-guide

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[data-testid='assertions-graph-tab']` | highlight | external | — | — | owner: grafana-asserts-app. Not fixable in grafana/grafana — owned by grafana-asserts-app. 'assertions' graph tab belongs to the Asserts app. |
| `[data-testid='assertions-mindmap-tab']` | highlight | external | — | — | owner: grafana-asserts-app. Not fixable in grafana/grafana — owned by grafana-asserts-app. |
| `[data-testid='assertions-summary-tab']` | highlight | external | — | — | owner: grafana-asserts-app. Not fixable in grafana/grafana — owned by grafana-asserts-app. Assertions summary is an Asserts app concept. |
| `[data-testid='catalog-entity-name-btn']:nth-match(1)` | highlight | external | — | — | owner: grafana-asserts-app. Not fixable in grafana/grafana — owned by grafana-asserts-app. not in core; 'catalog entity' matches the Asserts entity catalog (inference — verify via live DOM) |
| `[data-testid='empty-assertions-top-services-link']` | highlight | external | — | — | owner: grafana-asserts-app. Not fixable in grafana/grafana — owned by grafana-asserts-app. Asserts app empty-state link. |
| `[data-testid='entity-drawer-apps-tab-serviceOverview']` | button, highlight | external | — | — | owner: grafana-asserts-app. Not fixable in grafana/grafana — owned by grafana-asserts-app. Asserts entity drawer apps tab |
| `[data-testid='entity-drawer-kpis-tab']` | button | external | — | — | owner: grafana-asserts-app. Not fixable in grafana/grafana — owned by grafana-asserts-app. Asserts entity drawer KPIs tab |
| `[data-testid='entity-drawer-logs-tab']` | button x2 | external | — | — | owner: grafana-asserts-app. Not fixable in grafana/grafana — owned by grafana-asserts-app. Entity drawer is Asserts terminology; not in core source or bundles |
| `[data-testid='entity-drawer-overview-tab']` | button x2 | external | — | — | owner: grafana-asserts-app. Not fixable in grafana/grafana — owned by grafana-asserts-app. Entity drawer terminology matches Asserts; possibly grafana-k8s-app |
| `[data-testid='entity-drawer-traces-tab']` | button x2 | external | — | — | owner: grafana-k8s-app. Not fixable in grafana/grafana — owned by grafana-k8s-app. Not in core; entity drawer with traces tab — likely Kubernetes Monitoring (possibly grafana-asserts-app). |
| `[data-testid='insight-type-filter']:nth-match(1)` | highlight | external | — | — | owner: k6-app. Not fixable in grafana/grafana — owned by k6-app. Likely k6 Performance Insights type filter; not found in core or bundles. |
| `[data-testid='insight-type-filter']:nth-match(6)` | highlight | external | — | — | owner: k6-app. Not fixable in grafana/grafana — owned by k6-app. Likely k6 Performance Insights type filter; not found in core or bundles. |
| `[data-testid='insights-circle']` | highlight | external | — | — | owner: external (owner not recorded in analysis). Not fixable in grafana/grafana — owned by external (owner not recorded in analysis). Not in core or bundles; likely grafana-slo-app (home/insights) or grafana-asserts-app UI — verify in live DOM. |
| `button[data-testid='assertions-timeline-tab']` | highlight | external | — | — | owner: grafana-asserts-app. Not fixable in grafana/grafana — owned by grafana-asserts-app. |
| `div[data-cy='wb-list-item']:has(p:contains('frontend')):nth-match(1)` | highlight, hover | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('frontend')):nth-match(1) [data-testid='assertions-dir-view-kpi-btn']` | highlight | external | — | — | owner: grafana-asserts-app. Not fixable in grafana/grafana — owned by grafana-asserts-app. Asserts RCA workbench (wb- data-cy values) |
| `input[placeholder='Search entity']` | highlight | external | — | — | owner: grafana-asserts-app. Not fixable in grafana/grafana — owned by grafana-asserts-app. Entity search terminology matches Asserts. |
| `label:has([data-testid='catalog-type-Node-radio'])` | highlight | external | — | — | owner: grafana-asserts-app. Not fixable in grafana/grafana — owned by grafana-asserts-app. Node entity-type radio on the Asserts Entity catalog at /a/grafana-asserts-app/catalog (sibling catalog-type-Service-radio). |
| `label:has([data-testid='catalog-type-Service-radio'])` | highlight x2 | external | — | — | owner: grafana-asserts-app. Not fixable in grafana/grafana — owned by grafana-asserts-app. Asserts entity catalog type radio (testid on input inside label, RadioButtonGroup pattern) |

## linux-server-integration-lj/configure-alloy

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `div[data-testid='alloy-simple-block']+button` | highlight | external | — | — | owner: grafana-easystart-app. Not fixable in grafana/grafana — owned by grafana-easystart-app. Alloy config snippet block in Cloud onboarding integration instructions |

## linux-server-integration-lj/install-alloy

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `button[data-testid='agent-config-button']` | highlight | external | — | — | owner: grafana-collector-app. Not fixable in grafana/grafana — owned by grafana-collector-app. Fleet Management (Alloy/collector) UI; not in this repo |

## linux-server-integration-lj/install-dashboards-alerts

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[data-testid='view-dashboards-button']` | highlight | external | — | — | owner: grafana-easystart-app. Not fixable in grafana/grafana — owned by grafana-easystart-app. Not in core or bundles; likely the Cloud onboarding/integrations app 'View dashboards' button after installing an integration (uncertain). |
| `button[data-testid='install-button']` | highlight | external | — | — | owner: grafana-easystart-app. Not fixable in grafana/grafana — owned by grafana-easystart-app. Not in core source/bundles; likely the Connections integration install button in the cloud onboarding app (low confidence). The VersionInstallButton grep hit is an unrelated i18n key. |

## linux-server-integration-lj/restart-test-connection

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `button[data-testid='test-connection-button']` | highlight | external | — | — | owner: grafana-easystart-app. Not fixable in grafana/grafana — owned by grafana-easystart-app. Cloud onboarding integration install flow (test connection step) |

## linux-server-integration-lj/select-platform

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[href='/connections/add-new-connection/linux-node']` | highlight | no-change | `[data-testid="data-testid Connections plugin card Linux Server"] a` | `{grafana:pages.Connections.AddNewConnection.pluginCard:Linux Server} a` | Group 6 — zero core code: card already carries the pre-existing pluginCard(name) testid (CardGrid.tsx). PARAM = Cloud catalog display name, derived best-effort from the href slug "linux-node" — verify the exact display name in the Cloud connections catalog. Testid sits on the Card wrapper; append " a" to click the anchor. |
| `div[data-testid='collector-arch-selection'] input` | highlight | external | — | — | owner: grafana-collector-app (Fleet Management). Not fixable in grafana/grafana — owned by grafana-collector-app (Fleet Management). |
| `div[data-testid='collector-os-selection'] input` | highlight | external | — | — | owner: grafana-collector-app. Not fixable in grafana/grafana — owned by grafana-collector-app. Fleet Management (Alloy collector) Cloud app. |
| `input[data-testid='search-input-input']` | formfill | external | — | — | owner: grafana-easystart-app (Grafana Cloud Connections console). Not fixable in grafana/grafana — owned by grafana-easystart-app (Grafana Cloud Connections console). Search box on the Cloud /connections/add-new-connection catalog and integration setup (select-platform) pages, which the Cloud connections/onboarding app renders; OSS core uses SearchField with id, not this testid. |

## logql-101

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `button:has(span:contains("loki_nginx"))` | highlight | ready | `[data-testid="data-testid data source card loki_nginx"]` | `grafana:components.DataSourcePicker.dataSourceCard:loki_nginx` | 13.2.0 selector on DataSourceCardItem; param = data source name from the old anchor (instance data). |
| `div[data-testid="QueryEditorModeToggle"] label[for^="option-code-radiogroup"]` | highlight | ready | `[data-testid="data-testid QueryEditorModeToggle"] [data-testid="data-testid radio-button-option code"]` | `{grafana:components.DataSource.Prometheus.queryEditor.editorToggle} {grafana:components.RadioButton.option:code}` | Scope with components.DataSource.Prometheus.queryEditor.editorToggle (pre-existing wrapper). RadioButton.option is unique within a group, not across a page — scope to the owning group container. |
| `button[aria-label="Run query"]` | highlight | no-change | `[data-testid="data-testid RefreshPicker run button"]` | `grafana:components.RefreshPicker.runButtonV2` | Pre-existing selector, already wired. |
| `textarea.inputarea` | formfill x4 | not-fixable | — | — | Monaco editor internal — not taggable in grafana/grafana. Scope the surrounding CodeEditor container (data-testid Code editor container) and drive input via keyboard instead. |

## macos-integration-lj/configure-alloy

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `div[data-testid='alloy-simple-block']+button` | highlight | external | — | — | owner: grafana-easystart-app. Not fixable in grafana/grafana — owned by grafana-easystart-app. Alloy config snippet block in Cloud onboarding integration instructions |

## macos-integration-lj/install-alloy

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `button[data-testid='agent-config-button']` | highlight | external | — | — | owner: grafana-collector-app. Not fixable in grafana/grafana — owned by grafana-collector-app. Fleet Management (Alloy/collector) UI; not in this repo |

## macos-integration-lj/install-dashboards-alerts

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[data-testid='view-dashboards-button']` | highlight | external | — | — | owner: grafana-easystart-app. Not fixable in grafana/grafana — owned by grafana-easystart-app. Not in core or bundles; likely the Cloud onboarding/integrations app 'View dashboards' button after installing an integration (uncertain). |
| `button[data-testid='install-button']` | highlight | external | — | — | owner: grafana-easystart-app. Not fixable in grafana/grafana — owned by grafana-easystart-app. Not in core source/bundles; likely the Connections integration install button in the cloud onboarding app (low confidence). The VersionInstallButton grep hit is an unrelated i18n key. |

## macos-integration-lj/select-architecture

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[href='/connections/add-new-connection/macos-node']` | highlight | no-change | `[data-testid="data-testid Connections plugin card macOS"] a` | `{grafana:pages.Connections.AddNewConnection.pluginCard:macOS} a` | Group 6 — zero core code: card already carries the pre-existing pluginCard(name) testid (CardGrid.tsx). PARAM = Cloud catalog display name, derived best-effort from the href slug "macos-node" — verify the exact display name in the Cloud connections catalog. Testid sits on the Card wrapper; append " a" to click the anchor. |
| `div[data-testid='collector-arch-selection'] input` | highlight | external | — | — | owner: grafana-collector-app (Fleet Management). Not fixable in grafana/grafana — owned by grafana-collector-app (Fleet Management). |
| `div[data-testid='collector-installation-method'] input` | highlight | external | — | — | owner: grafana-collector-app (Fleet Management). Not fixable in grafana/grafana — owned by grafana-collector-app (Fleet Management). |
| `input[data-testid='search-input-input']` | formfill | external | — | — | owner: grafana-easystart-app (Grafana Cloud Connections console). Not fixable in grafana/grafana — owned by grafana-easystart-app (Grafana Cloud Connections console). Search box on the Cloud /connections/add-new-connection catalog and integration setup (select-platform) pages, which the Cloud connections/onboarding app renders; OSS core uses SearchField with id, not this testid. |

## macos-integration-lj/test-connection

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `button[data-testid='test-connection-button']` | highlight | external | — | — | owner: grafana-easystart-app. Not fixable in grafana/grafana — owned by grafana-easystart-app. Cloud onboarding integration install flow (test connection step) |

## mongodb-integration-lj/configure-alloy

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `div[data-testid='alloy-advanced-integrations-block']+button` | highlight | external | — | — | owner: grafana-collector-app. Not fixable in grafana/grafana — owned by grafana-collector-app. Alloy onboarding UI in the collector (Fleet Management) app. |

## mongodb-integration-lj/install-alloy

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `button[data-testid='agent-config-button']` | highlight | external | — | — | owner: grafana-collector-app. Not fixable in grafana/grafana — owned by grafana-collector-app. Fleet Management (Alloy/collector) UI; not in this repo |

## mongodb-integration-lj/select-platform

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[href='/connections/add-new-connection/mongodb']` | highlight | no-change | `[data-testid="data-testid Connections plugin card MongoDB"] a` | `{grafana:pages.Connections.AddNewConnection.pluginCard:MongoDB} a` | Group 6 — zero core code: card already carries the pre-existing pluginCard(name) testid (CardGrid.tsx). PARAM = Cloud catalog display name, derived best-effort from the href slug "mongodb" — verify the exact display name in the Cloud connections catalog. Testid sits on the Card wrapper; append " a" to click the anchor. |
| `input[data-testid='search-input-input']` | formfill | external | — | — | owner: grafana-easystart-app (Grafana Cloud Connections console). Not fixable in grafana/grafana — owned by grafana-easystart-app (Grafana Cloud Connections console). Search box on the Cloud /connections/add-new-connection catalog and integration setup (select-platform) pages, which the Cloud connections/onboarding app renders; OSS core uses SearchField with id, not this testid. |

## mongodb-integration-lj/test-connection

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `button[data-testid='test-connection-button']` | highlight | external | — | — | owner: grafana-easystart-app. Not fixable in grafana/grafana — owned by grafana-easystart-app. Cloud onboarding integration install flow (test connection step) |

## mysql-data-source-lj/add-data-source

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `input[placeholder='Filter by name or type']` | formfill | ready | `[data-testid="data-testid Add data source search input"]` | `grafana:pages.AddDataSource.searchInput` | — |
| `a[href='/connections/datasources']` | highlight | no-change | `a[data-testid="data-testid Nav menu item"][href='/connections/datasources']` | `a{grafana:components.NavMenu.item}[href='/connections/datasources']` | Old anchor already resolves to core nav markup; adopt the pre-existing components.NavMenu.item compound (add the data-testid half, keep the href). |
| `input[placeholder='Name']` | formfill | stale | `[data-testid="data-testid Editable title input"]` | `grafana:components.EditableTitle.titleInput` | STALE: replaced by the page-header EditableTitle (click editButton first). Interim strong anchor: input#page-editable-title. |

## mysql-data-source-lj/configure-datasource

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `input[name='host']` | formfill | external | — | — | owner: externalized Grafana MySQL datasource plugin. MySQL was removed from grafana/grafana core in #129439 (2026-07-30); the config UI (host input) now belongs to the externalized plugin. |
| `input[placeholder='Password']` | formfill | external | — | — | owner: externalized Grafana MySQL datasource plugin. MySQL was removed from grafana/grafana core in #129439 (2026-07-30); the config UI (password input) now belongs to the externalized plugin. |
| `input[placeholder='Username']` | formfill | external | — | — | owner: externalized Grafana MySQL datasource plugin. MySQL was removed from grafana/grafana core in #129439 (2026-07-30); the config UI (username input) now belongs to the externalized plugin. |

## mysql-data-source-lj/test-connection

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `input[aria-label='Private data source connect']` | highlight | external | — | — | owner: grafana-pdc-app. PDC select on the datasource config page is injected via UI extensions; no core match. |

## mysql-data-source-lj/verify-mysql-data

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[data-testid='query-editor-rows']` | highlight | no-change | `[data-testid='query-editor-rows']` | — | Hardcoded core literal (QueryEditorRows.tsx), still on main — anchor keeps working, but it is NOT registered in the e2e-selectors package, so no grafana: token exists (future version-key candidate). Per-row container: components.QueryEditorRows.rows (data-testid Query editor row). |
| `a[href='/explore']` | highlight | no-change | `a[data-testid="data-testid Nav menu item"][href='/explore']` | `a{grafana:components.NavMenu.item}[href='/explore']` | Old anchor already resolves to core nav markup; adopt the pre-existing components.NavMenu.item compound (add the data-testid half, keep the href). |
| `button[aria-label='Run query']` | highlight | no-change | `[data-testid="data-testid RefreshPicker run button"]` | `grafana:components.RefreshPicker.runButtonV2` | Pre-existing selector, already wired. |

## mysql-db-olly-lj/explore-queries

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `button[aria-label*='section: Database']` | highlight | ready | `[data-testid="data-testid navigation mega-menu section toggle <Database section nav URL>"]` | `grafana:components.NavMenu.sectionToggleButton:<Database section nav URL>` | Same new selector; confirm the Database section nav URL on a Cloud stack. GD-5 compound: keep the href half; a section rendered in both the pinned box and the main nav can double-match — scope with components.NavMenu.Menu ([data-testid="data-testid navigation mega-menu"]) when needed. |
| `button[aria-label*='section: Observability']` | highlight | ready | `[data-testid="data-testid navigation mega-menu section toggle <Observability section nav URL>"]` | `grafana:components.NavMenu.sectionToggleButton:<Observability section nav URL>` | New 13.2.0 selector on the mega-menu expand/collapse IconButton. Param = the section's nav URL, which Cloud nav registration supplies — confirm the Observability section URL on a Cloud stack. GD-5 compound: keep the href half; a section rendered in both the pinned box and the main nav can double-match — scope with components.NavMenu.Menu ([data-testid="data-testid navigation mega-menu"]) when needed. |

## mysql-db-olly-lj/verify-telemetry

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `button[aria-label*='section: Observability']` | highlight | ready | `[data-testid="data-testid navigation mega-menu section toggle <Observability section nav URL>"]` | `grafana:components.NavMenu.sectionToggleButton:<Observability section nav URL>` | New 13.2.0 selector on the mega-menu expand/collapse IconButton. Param = the section's nav URL, which Cloud nav registration supplies — confirm the Observability section URL on a Cloud stack. GD-5 compound: keep the href half; a section rendered in both the pinned box and the main nav can double-match — scope with components.NavMenu.Menu ([data-testid="data-testid navigation mega-menu"]) when needed. |

## mysql-integration-lj/install-alloy

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `button[data-testid='agent-config-button']` | highlight | external | — | — | owner: grafana-collector-app. Not fixable in grafana/grafana — owned by grafana-collector-app. Fleet Management (Alloy/collector) UI; not in this repo |

## mysql-integration-lj/install-dashboards-alerts

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[data-testid='view-dashboards-button']` | highlight | external | — | — | owner: grafana-easystart-app. Not fixable in grafana/grafana — owned by grafana-easystart-app. Not in core or bundles; likely the Cloud onboarding/integrations app 'View dashboards' button after installing an integration (uncertain). |
| `button[data-testid='install-button']` | highlight | external | — | — | owner: grafana-easystart-app. Not fixable in grafana/grafana — owned by grafana-easystart-app. Not in core source/bundles; likely the Connections integration install button in the cloud onboarding app (low confidence). The VersionInstallButton grep hit is an unrelated i18n key. |

## mysql-integration-lj/select-platform

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[href='/connections/add-new-connection/mysql']` | highlight | no-change | `[data-testid="data-testid Connections plugin card MySQL"] a` | `{grafana:pages.Connections.AddNewConnection.pluginCard:MySQL} a` | Group 6 — zero core code: card already carries the pre-existing pluginCard(name) testid (CardGrid.tsx). PARAM = Cloud catalog display name, derived best-effort from the href slug "mysql" — verify the exact display name in the Cloud connections catalog. Testid sits on the Card wrapper; append " a" to click the anchor. |
| `div[data-testid='collector-arch-selection'] input` | highlight | external | — | — | owner: grafana-collector-app (Fleet Management). Not fixable in grafana/grafana — owned by grafana-collector-app (Fleet Management). |
| `div[data-testid='collector-os-selection'] input` | highlight | external | — | — | owner: grafana-collector-app. Not fixable in grafana/grafana — owned by grafana-collector-app. Fleet Management (Alloy collector) Cloud app. |
| `input[data-testid='search-input-input']` | formfill | external | — | — | owner: grafana-easystart-app (Grafana Cloud Connections console). Not fixable in grafana/grafana — owned by grafana-easystart-app (Grafana Cloud Connections console). Search box on the Cloud /connections/add-new-connection catalog and integration setup (select-platform) pages, which the Cloud connections/onboarding app renders; OSS core uses SearchField with id, not this testid. |

## mysql-integration-lj/test-connection

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `button[data-testid='test-connection-button']` | highlight | external | — | — | owner: grafana-easystart-app. Not fixable in grafana/grafana — owned by grafana-easystart-app. Cloud onboarding integration install flow (test connection step) |

## otel-fleet-management

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `#pageContent div[data-testid='data-testid Card heading']:nth-match(2) button:text('OpenTelemetry')` | highlight | no-change | `[data-testid="data-testid Connections plugin card OpenTelemetry (OTLP)"] a` | `{grafana:pages.Connections.AddNewConnection.pluginCard:OpenTelemetry (OTLP)} a` | Pre-existing pluginCard(name); PARAM = Cloud catalog display name (best-effort from the card text — verify in the Cloud connections catalog). Testid is on the Card wrapper; append " a" to click. |
| `div[data-testid='data-testid Card heading']:contains('Application Observability') button:contains('Application Observability')` | highlight | no-change | `[data-testid="data-testid Connections plugin card Application Observability"] a` | `{grafana:pages.Connections.AddNewConnection.pluginCard:Application Observability} a` | Pre-existing pluginCard(name); param = catalog display name from the old anchor text. |
| `button:text('Next')` | highlight x2 | external | — | — | owner: grafana-collector-app. Not fixable in grafana/grafana — owned by grafana-collector-app. Next button in the Create configuration pipeline wizard at /a/grafana-collector-app/fleet-management (remote-configuration-* testids surround it). |
| `button[data-testid='remote-config-delete-pipeline-application_o11y_linux'] svg[data-testid='icon-trash-alt']` | highlight | external | — | — | owner: grafana-collector-app. Fleet Management pipeline delete; suffix is instance data. |
| `div[data-testid='fleet-management-page'] button[data-testid='tab-remote-configuration']` | highlight | external | — | — | owner: grafana-collector-app. Not fixable in grafana/grafana — owned by grafana-collector-app. Fleet Management app page container. |
| `div[data-testid='remote-configuration-page'] button[data-testid='remote-configuration-create-button']` | highlight | external | — | — | owner: grafana-collector-app. Not fixable in grafana/grafana — owned by grafana-collector-app. Fleet Management (collector) remote configuration UI. |
| `div[data-testid='remote-configuration-page'] span:nth-match(3)` | highlight | external | — | — | owner: grafana-collector-app. Not fixable in grafana/grafana — owned by grafana-collector-app. Fleet Management (collector) remote configuration UI. |

## play-5k-run-results

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `div[data-testid='infinity-query-row-wrapper-query-options']` | highlight | external | — | — | owner: yesoreyeram-infinity-datasource. Infinity datasource editor UI ships in the external plugin. |

## play-carbon-intensity

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `div[data-testid="query-editor-row"] > :first-child` | highlight | stale | `[data-testid="data-testid Query editor row"] > :first-child` | `{grafana:components.QueryEditorRows.rows} > :first-child` | STALE: the hardcoded query-editor-row testid was removed (Apr 2026, d1e243ebe0d); rows now emit the registered components.QueryEditorRows.rows value. Guide-side retarget only. |
| `button[data-testid='infinity-query-row-collapse-show-parsing-options-&-result-fields'] svg` | highlight | external | — | — | owner: yesoreyeram-infinity-datasource. Infinity datasource editor UI ships in the external plugin. |
| `div[data-testid='infinity-query-field-wrapper-rows/root'] textarea` | highlight | external | — | — | owner: yesoreyeram-infinity-datasource. Infinity datasource editor UI ships in the external plugin. |

## play-gb-railway-usage

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `div[data-testid='infinity-query-row-wrapper-query-options']` | highlight | external | — | — | owner: yesoreyeram-infinity-datasource. Infinity datasource editor UI ships in the external plugin. |

## play-nz-geonet-tour

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `div[data-testid="query-editor-row"] > :first-child` | highlight | stale | `[data-testid="data-testid Query editor row"] > :first-child` | `{grafana:components.QueryEditorRows.rows} > :first-child` | STALE: the hardcoded query-editor-row testid was removed (Apr 2026, d1e243ebe0d); rows now emit the registered components.QueryEditorRows.rows value. Guide-side retarget only. |
| `button[data-testid='infinity-query-row-collapse-show-parsing-options-&-result-fields']` | highlight | external | — | — | owner: yesoreyeram-infinity-datasource. Infinity datasource editor UI ships in the external plugin. |
| `div[data-testid='infinity-query-field-wrapper-rows/root'] textarea` | highlight | external | — | — | owner: yesoreyeram-infinity-datasource. Infinity datasource editor UI ships in the external plugin. |
| `div[data-testid='infinity-query-row-wrapper-query-options']` | highlight | external | — | — | owner: yesoreyeram-infinity-datasource. Infinity datasource editor UI ships in the external plugin. |

## play-traitors-uk-tour

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `label[aria-label='Table view']` | highlight x2 | no-change | `[data-testid="data-testid toggle-table-view"]` | `grafana:components.PanelEditor.toggleTableView` | Pre-existing selector on the table-view Switch input; retarget from the Switch label to the input. |

## postgresql-db-olly-lj/explore-queries

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `button[aria-label*='section: Database']` | highlight | ready | `[data-testid="data-testid navigation mega-menu section toggle <Database section nav URL>"]` | `grafana:components.NavMenu.sectionToggleButton:<Database section nav URL>` | Same new selector; confirm the Database section nav URL on a Cloud stack. GD-5 compound: keep the href half; a section rendered in both the pinned box and the main nav can double-match — scope with components.NavMenu.Menu ([data-testid="data-testid navigation mega-menu"]) when needed. |
| `button[aria-label*='section: Observability']` | highlight | ready | `[data-testid="data-testid navigation mega-menu section toggle <Observability section nav URL>"]` | `grafana:components.NavMenu.sectionToggleButton:<Observability section nav URL>` | New 13.2.0 selector on the mega-menu expand/collapse IconButton. Param = the section's nav URL, which Cloud nav registration supplies — confirm the Observability section URL on a Cloud stack. GD-5 compound: keep the href half; a section rendered in both the pinned box and the main nav can double-match — scope with components.NavMenu.Menu ([data-testid="data-testid navigation mega-menu"]) when needed. |

## postgresql-db-olly-lj/verify-telemetry

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `button[aria-label*='section: Observability']` | highlight | ready | `[data-testid="data-testid navigation mega-menu section toggle <Observability section nav URL>"]` | `grafana:components.NavMenu.sectionToggleButton:<Observability section nav URL>` | New 13.2.0 selector on the mega-menu expand/collapse IconButton. Param = the section's nav URL, which Cloud nav registration supplies — confirm the Observability section URL on a Cloud stack. GD-5 compound: keep the href half; a section rendered in both the pinned box and the main nav can double-match — scope with components.NavMenu.Menu ([data-testid="data-testid navigation mega-menu"]) when needed. |

## postgresql-integration-lj/configure-alloy

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `div[data-testid='alloy-simple-block']+button` | highlight | external | — | — | owner: grafana-easystart-app. Not fixable in grafana/grafana — owned by grafana-easystart-app. Alloy config snippet block in Cloud onboarding integration instructions |

## postgresql-integration-lj/install-alloy

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `button[data-testid='agent-config-button']` | highlight | external | — | — | owner: grafana-collector-app. Not fixable in grafana/grafana — owned by grafana-collector-app. Fleet Management (Alloy/collector) UI; not in this repo |

## postgresql-integration-lj/install-dashboards-alerts

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[data-testid='install-button']` | highlight | external | — | — | owner: grafana-easystart-app. Not fixable in grafana/grafana — owned by grafana-easystart-app. Not in core source/bundles; likely the Connections integration install button in the cloud onboarding app (low confidence). The VersionInstallButton grep hit is an unrelated i18n key. |
| `[data-testid='view-dashboards-button']` | highlight | external | — | — | owner: grafana-easystart-app. Not fixable in grafana/grafana — owned by grafana-easystart-app. Not in core or bundles; likely the Cloud onboarding/integrations app 'View dashboards' button after installing an integration (uncertain). |

## postgresql-integration-lj/select-platform

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[href='/connections/add-new-connection/postgres']` | highlight | no-change | `[data-testid="data-testid Connections plugin card PostgreSQL"] a` | `{grafana:pages.Connections.AddNewConnection.pluginCard:PostgreSQL} a` | Group 6 — zero core code: card already carries the pre-existing pluginCard(name) testid (CardGrid.tsx). PARAM = Cloud catalog display name, derived best-effort from the href slug "postgres" — verify the exact display name in the Cloud connections catalog. Testid sits on the Card wrapper; append " a" to click the anchor. |
| `div[data-testid='collector-arch-selection']` | highlight | external | — | — | owner: grafana-collector-app (Fleet Management). Not fixable in grafana/grafana — owned by grafana-collector-app (Fleet Management). |
| `div[data-testid='collector-os-selection']` | highlight | external | — | — | owner: grafana-collector-app. Not fixable in grafana/grafana — owned by grafana-collector-app. Fleet Management (Alloy collector) Cloud app. |
| `input[data-testid='search-input-input']` | formfill | external | — | — | owner: grafana-easystart-app (Grafana Cloud Connections console). Not fixable in grafana/grafana — owned by grafana-easystart-app (Grafana Cloud Connections console). Search box on the Cloud /connections/add-new-connection catalog and integration setup (select-platform) pages, which the Cloud connections/onboarding app renders; OSS core uses SearchField with id, not this testid. |

## postgresql-integration-lj/test-connection

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[data-testid='test-connection-button']` | highlight | external | — | — | owner: grafana-easystart-app. Not fixable in grafana/grafana — owned by grafana-easystart-app. Cloud onboarding integration install flow (test connection step) |

## prom-remote-write-lj/verify-metrics-query-works

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[href="/a/grafana-metricsdrilldown-app/drilldown"]` | highlight | external | — | — | owner: grafana-metricsdrilldown-app. Not fixable in grafana/grafana — owned by grafana-metricsdrilldown-app. Plugin nav include path from the app's plugin.json; core only renders it as a nav item |

## prometheus-lj/add-data-source

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[aria-label="Add new data source Prometheus"]` | highlight | no-change | `[data-testid="data-testid Add new data source Prometheus"]` | `grafana:pages.AddDataSource.dataSourcePluginsV2:Prometheus` | Pre-existing selector; aria-label form is the legacy 9.3.1 resolution — retarget to the testid. |
| `a[href='/connections/datasources']` | highlight | no-change | `a[data-testid="data-testid Nav menu item"][href='/connections/datasources']` | `a{grafana:components.NavMenu.item}[href='/connections/datasources']` | Old anchor already resolves to core nav markup; adopt the pre-existing components.NavMenu.item compound (add the data-testid half, keep the href). |

## prometheus-lj/add-data-source-url

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `#connection-url` | formfill | external | — | — | owner: @grafana/plugin-ui (bundled into datasource plugins). ConnectionSettings URL input comes from @grafana/plugin-ui, bundled inside the datasource plugin. |

## prometheus-lj/config-authentication

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `#auth-method-select` | highlight | external | — | — | owner: @grafana/plugin-ui (bundled into datasource plugins). Auth component method select comes from @grafana/plugin-ui, bundled inside the datasource plugin — fix belongs in grafana/plugin-ui. |

## prometheus-lj/select-private-connection

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[aria-label="Private data source connect"]` | highlight | external | — | — | owner: grafana-pdc-app. PDC select on the datasource config page is injected via UI extensions; no core match. |

## prometheus-lj/verify-ds-connection

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[href="/a/grafana-metricsdrilldown-app/drilldown"]` | highlight | external | — | — | owner: grafana-metricsdrilldown-app. Not fixable in grafana/grafana — owned by grafana-metricsdrilldown-app. Plugin nav include path from the app's plugin.json; core only renders it as a nav item |

## rca-demo

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `button[aria-label='Wrap lines']` | highlight | not-fixable | — | — | grafana-ui API gap: LogListControlsSelectOption renders a hardcoded <button> and forwards rest props to the inner Icon, not the button — no test-id prop. Follow-up candidate (grafana-ui change). |
| `div:contains('panic')` | highlight | not-fixable | — | — | Node ids / log text are instance data, not core JSX. |
| `div[data-viz-panel-key='75903a26-8a1b-4df1-b56a-daa3a11c5b8a']` | highlight | not-fixable | — | — | data-viz-panel-key is a @grafana/scenes panel key — instance data of the RCA demo dashboard. |
| `button:has(span:contains('productcatalogservice'))` | highlight | external | — | — | owner: grafana-app-observability-app. Not fixable in grafana/grafana — owned by grafana-app-observability-app. Service name from OpenTelemetry demo shown in Application Observability |
| `button[aria-label='Workbench AI (Preview)']` | highlight | external | — | — | owner: RCA workbench app (demo). Not fixable in grafana/grafana — owned by RCA workbench app (demo). Not in core source or bundles; 'Workbench' matches the RCA workbench demo app. |
| `div.grid.wb-item:has(p:contains('PostgreSQLHighConnections'))` | highlight | external | — | — | owner: rca-workbench-demo-app. Not fixable in grafana/grafana — owned by rca-workbench-demo-app. wb- class prefix indicates the RCA workbench demo app. |
| `div.grid.wb-item:has(p[data-original='KubePodCrashLooping'])` | highlight | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb-* classes belong to the RCA workbench demo app. |
| `div.h-full.w-full.overflow-y-scroll.block` | highlight | external | — | — | owner: grafana-asserts-app. Not fixable in grafana/grafana — owned by grafana-asserts-app. Tailwind-classed insights timeline container in the Asserts RCA workbench (guide labels it 'Timeline'; Asserts is the Tailwind-using app in these guides). |
| `div[data-cy='entity-list-item']:has(p:contains('frontendproxy'))` | hover | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. data-cy attributes belong to the RCA workbench demo app. |
| `div[data-cy='wb-list-item']:has(p:contains('FeatureFlagStateChange'))` | highlight, hover | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('FeatureFlagStateChange')) button:nth-of-type(1)` | hover | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('PostgreSQLHighConnections'))` | highlight | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('amend'))` | highlight | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('anomaly'))` | highlight | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('checkoutservice'))` | hover | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('checkoutservice')) button:nth-of-type(4)` | hover | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('failure'))` | highlight x2 | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('flagd'))` | highlight | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('frontend'))` | highlight, hover | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('frontend')) button:nth-of-type(3)` | hover | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('productcatalog-postgres'))` | highlight, hover | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('productcatalog-postgres')) button:nth-of-type(4)` | hover | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('productcatalogservice'))` | highlight, hover | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('productcatalogservice')) button:nth-of-type(4)` | hover | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p[data-original='KubePodCrashLooping'])` | highlight | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p[data-original='outbound - grpc.oteldemo.ProductCatalogService/GetProduct'])` | highlight | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[role='dialog'] button[type='button']:has(div:contains('Frontend'))` | hover | external | — | — | owner: RCA workbench demo app / grafana-asserts-app. Container roles are core/grafana-ui, but the targeted contents are external demo-app markup. |
| `div[role='dialog'] button[type='button']:has(div:contains('Service'))` | hover | external | — | — | owner: RCA workbench demo app / grafana-asserts-app. Container roles are core/grafana-ui, but the targeted contents are external demo-app markup. |
| `div[role='dialog'] div[data-cy='entity-list-item']:has(p:contains('frontend-client'))` | hover | external | — | — | owner: RCA workbench demo app / grafana-asserts-app. Container roles are core/grafana-ui, but the targeted contents are external demo-app markup. |
| `div[role='dialog'] div[data-cy='entity-list-item']:has(p:contains('frontend-client')) button:nth-of-type(3)` | hover | external | — | — | owner: RCA workbench demo app / grafana-asserts-app. Container roles are core/grafana-ui, but the targeted contents are external demo-app markup. |

## rca-demo-ops

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `section[data-testid*="Panel header Logs"]` | highlight | no-change | `section[data-testid*="data-testid Panel header Logs"]` | `grafana:components.Panels.Panel.title:Logs` | Pre-existing parameterized selector; keep the substring match if the full title varies (title is app/dashboard data). |
| `button[aria-label='Wrap lines']` | highlight | not-fixable | — | — | grafana-ui API gap: LogListControlsSelectOption renders a hardcoded <button> and forwards rest props to the inner Icon, not the button — no test-id prop. Follow-up candidate (grafana-ui change). |
| `button:has(span:contains('productcatalogservice'))` | highlight | external | — | — | owner: grafana-app-observability-app. Not fixable in grafana/grafana — owned by grafana-app-observability-app. Service name from OpenTelemetry demo shown in Application Observability |
| `button[aria-label='Workbench AI (Preview)']` | highlight | external | — | — | owner: RCA workbench app (demo). Not fixable in grafana/grafana — owned by RCA workbench app (demo). Not in core source or bundles; 'Workbench' matches the RCA workbench demo app. |
| `div.grid.wb-item:has(p:contains('PostgreSQLHighConnections'))` | highlight | external | — | — | owner: rca-workbench-demo-app. Not fixable in grafana/grafana — owned by rca-workbench-demo-app. wb- class prefix indicates the RCA workbench demo app. |
| `div.grid.wb-item:has(p[data-original='KubePodCrashLooping'])` | highlight | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb-* classes belong to the RCA workbench demo app. |
| `div.h-full.w-full.overflow-y-scroll.block` | highlight | external | — | — | owner: grafana-asserts-app. Not fixable in grafana/grafana — owned by grafana-asserts-app. Tailwind-classed insights timeline container in the Asserts RCA workbench (guide labels it 'Timeline'; Asserts is the Tailwind-using app in these guides). |
| `div.text-xs:has(span:contains('Sort By'))` | highlight | external | — | — | owner: grafana-asserts-app. Not fixable in grafana/grafana — owned by grafana-asserts-app. text-xs is a Tailwind utility class not used in core; 'Sort By' most plausibly the Asserts app UI (unconfirmed) |
| `div[data-cy='entity-list-item']:has(p:contains('frontendproxy'))` | highlight | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. data-cy attributes belong to the RCA workbench demo app. |
| `div[data-cy='wb-list-item']:has(p:contains('FeatureFlagStateChange'))` | highlight, hover | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('FeatureFlagStateChange')) button:nth-of-type(1)` | hover | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('PostgreSQLHighConnections'))` | highlight | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('amend'))` | highlight | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('anomaly'))` | highlight | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('checkoutservice')):nth-match(1)` | hover | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('checkoutservice')):nth-match(1) button:nth-of-type(4)` | hover | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('failure'))` | highlight x2 | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('flagd'))` | highlight | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('frontend'))` | highlight, hover | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('frontend')) button:nth-of-type(3)` | highlight | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('productcatalog-postgres'))` | highlight | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('productcatalog-postgres')):nth-match(1)` | hover | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('productcatalog-postgres')):nth-match(1) button:nth-of-type(4)` | hover | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('productcatalogservice'))` | highlight | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('productcatalogservice')):nth-match(1)` | hover | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('productcatalogservice')):nth-match(1) button:nth-of-type(4)` | hover | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p[data-original='KubePodCrashLooping'])` | highlight | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p[data-original='outbound - grpc.oteldemo.ProductCatalogService/GetProduct'])` | highlight | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-testid="data-testid panel content"] div[role="button"]:has(span:contains("1"))` | highlight | external | — | — | owner: RCA workbench demo app. Inner content is external app markup; the container already has components.Panels.Panel.content. |
| `div[role="grid"] div[role="row"][aria-rowindex="2"] div.cell-link` | highlight | external | — | — | owner: RCA workbench demo app / grafana-asserts-app. Container roles are core/grafana-ui, but the targeted contents are external demo-app markup. |
| `div[role="menu"] button[role="menuitem"]:has(span:contains("Time"))` | highlight | external | — | — | owner: RCA workbench demo app / grafana-asserts-app. Container roles are core/grafana-ui, but the targeted contents are external demo-app markup. |
| `div[role='dialog'] div[data-cy='entity-list-item']:has(p:contains('frontend-client'))` | hover | external | — | — | owner: RCA workbench demo app / grafana-asserts-app. Container roles are core/grafana-ui, but the targeted contents are external demo-app markup. |
| `div[role='dialog'] div[data-cy='entity-list-item']:has(p:contains('frontend-client')) button:nth-of-type(3)` | highlight | external | — | — | owner: RCA workbench demo app / grafana-asserts-app. Container roles are core/grafana-ui, but the targeted contents are external demo-app markup. |
| `div[role='dialog'] div[role='group'] div:contains('Frontend')` | highlight | external | — | — | owner: RCA workbench demo app / grafana-asserts-app. Container roles are core/grafana-ui, but the targeted contents are external demo-app markup. |
| `div[role='dialog'] div[role='group'] div:contains('Service')` | highlight | external | — | — | owner: RCA workbench demo app / grafana-asserts-app. Container roles are core/grafana-ui, but the targeted contents are external demo-app markup. |
| `td.title a[href="/a/grafana-irm-app/incidents/1"]:contains("Day in the Life Demo")` | highlight | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. |

## rca-demo-v2

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `section[data-testid*="Panel header Logs"]` | highlight | no-change | `section[data-testid*="data-testid Panel header Logs"]` | `grafana:components.Panels.Panel.title:Logs` | Pre-existing parameterized selector; keep the substring match if the full title varies (title is app/dashboard data). |
| `button:has(span:contains('productcatalogservice'))` | highlight | external | — | — | owner: grafana-app-observability-app. Not fixable in grafana/grafana — owned by grafana-app-observability-app. Service name from OpenTelemetry demo shown in Application Observability |
| `button[aria-label='Workbench AI (Preview)']` | highlight | external | — | — | owner: RCA workbench app (demo). Not fixable in grafana/grafana — owned by RCA workbench app (demo). Not in core source or bundles; 'Workbench' matches the RCA workbench demo app. |
| `div.grid.wb-item:has(p:contains('PostgreSQLHighConnections'))` | highlight | external | — | — | owner: rca-workbench-demo-app. Not fixable in grafana/grafana — owned by rca-workbench-demo-app. wb- class prefix indicates the RCA workbench demo app. |
| `div.grid.wb-item:has(p[data-original='KubePodCrashLooping'])` | highlight | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb-* classes belong to the RCA workbench demo app. |
| `div.h-full.w-full.overflow-y-scroll.block` | highlight | external | — | — | owner: grafana-asserts-app. Not fixable in grafana/grafana — owned by grafana-asserts-app. Tailwind-classed insights timeline container in the Asserts RCA workbench (guide labels it 'Timeline'; Asserts is the Tailwind-using app in these guides). |
| `div.text-xs:has(span:contains('Sort By'))` | highlight | external | — | — | owner: grafana-asserts-app. Not fixable in grafana/grafana — owned by grafana-asserts-app. text-xs is a Tailwind utility class not used in core; 'Sort By' most plausibly the Asserts app UI (unconfirmed) |
| `div[data-cy='entity-list-item']:has(p:contains('frontendproxy'))` | highlight | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. data-cy attributes belong to the RCA workbench demo app. |
| `div[data-cy='wb-list-item']:has(p:contains('FeatureFlagStateChange'))` | highlight, hover | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('FeatureFlagStateChange')) button:nth-of-type(1)` | hover | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('PostgreSQLHighConnections'))` | highlight | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('amend'))` | highlight | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('anomaly'))` | highlight | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('checkoutservice')):nth-match(1)` | hover | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('checkoutservice')):nth-match(1) button:nth-of-type(4)` | highlight | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('failure'))` | highlight x2 | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('flagd'))` | highlight x2 | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('frontend'))` | highlight x2, hover | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('frontend')) button:nth-of-type(3)` | highlight | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('productcatalog-postgres'))` | highlight x2 | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('productcatalog-postgres')):nth-match(1)` | hover | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('productcatalog-postgres')):nth-match(1) button:nth-of-type(4)` | highlight | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('productcatalogservice'))` | highlight x2 | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('productcatalogservice')):nth-match(1)` | hover | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p:contains('productcatalogservice')):nth-match(1) button:nth-of-type(4)` | hover | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p[data-original='KubePodCrashLooping'])` | highlight | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-cy='wb-list-item']:has(p[data-original='outbound - grpc.oteldemo.ProductCatalogService/GetProduct'])` | highlight | external | — | — | owner: RCA workbench demo app. Not fixable in grafana/grafana — owned by RCA workbench demo app. wb- prefixed data-cy values belong to the RCA workbench demo app; not in this repo or bundles. |
| `div[data-testid="data-testid panel content"] div[role="button"]:has(span:contains("1"))` | highlight | external | — | — | owner: RCA workbench demo app. Inner content is external app markup; the container already has components.Panels.Panel.content. |
| `div[role="grid"] div[role="row"][aria-rowindex="2"] div.cell-link` | highlight | external | — | — | owner: RCA workbench demo app / grafana-asserts-app. Container roles are core/grafana-ui, but the targeted contents are external demo-app markup. |
| `div[role="menu"] button[role="menuitem"]:has(span:contains("Time"))` | highlight | external | — | — | owner: RCA workbench demo app / grafana-asserts-app. Container roles are core/grafana-ui, but the targeted contents are external demo-app markup. |
| `div[role='dialog'] div[data-cy='entity-list-item']:has(p:contains('frontend-client'))` | hover | external | — | — | owner: RCA workbench demo app / grafana-asserts-app. Container roles are core/grafana-ui, but the targeted contents are external demo-app markup. |
| `div[role='dialog'] div[data-cy='entity-list-item']:has(p:contains('frontend-client')) button:nth-of-type(3)` | highlight | external | — | — | owner: RCA workbench demo app / grafana-asserts-app. Container roles are core/grafana-ui, but the targeted contents are external demo-app markup. |
| `div[role='dialog'] div[role='group'] div:contains('Frontend')` | highlight | external | — | — | owner: RCA workbench demo app / grafana-asserts-app. Container roles are core/grafana-ui, but the targeted contents are external demo-app markup. |
| `div[role='dialog'] div[role='group'] div:contains('Service')` | highlight | external | — | — | owner: RCA workbench demo app / grafana-asserts-app. Container roles are core/grafana-ui, but the targeted contents are external demo-app markup. |
| `td.title a[href="/a/grafana-irm-app/incidents/1"]:contains("Day in the Life Demo")` | highlight | external | — | — | owner: grafana-irm-app. Not fixable in grafana/grafana — owned by grafana-irm-app. |

## semantic-layer-data-model-config

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `#pageContent [role='button']:text('grafana_play_cube')` | highlight | not-fixable | — | — | grafana_play_cube is instance data (Cube schema name) inside the semantic-layer (Cube) UI. |
| `#pageContent button:contains('Files')` | highlight | external | — | — | owner: grafana-cube-datasource. #pageContent is core, but the Files button belongs to the Cube data-model config UI. |

## semantic-layer-tutorial

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `div[role="gridcell"]:contains("Qualification") button[aria-label="Filter for value"]` | highlight | ready | `div[role="gridcell"]:contains(<cell text>) [data-testid="data-testid tableng cell-actions filter-for-button"]` | `div[role="gridcell"]:contains(<cell text>) {grafana:components.Panels.Visualization.TableNG.cellActions.filterForButton}` | Button renders only in the hovered cell; the cell itself still needs content scoping (instance data). Siblings filterOutButton / inspectButton also added. |
| `div[role="gridcell"]:contains("R.") button[aria-label="Filter for value"]` | highlight | ready | `div[role="gridcell"]:contains(<cell text>) [data-testid="data-testid tableng cell-actions filter-for-button"]` | `div[role="gridcell"]:contains(<cell text>) {grafana:components.Panels.Visualization.TableNG.cellActions.filterForButton}` | Button renders only in the hovered cell; the cell itself still needs content scoping (instance data). Siblings filterOutButton / inspectButton also added. |
| `[data-testid="data-testid template variable"]:nth-match(3)` | formfill | no-change | `[data-testid="data-testid Dashboard template variables submenu Label Dimensions"]` | `grafana:pages.Dashboard.SubMenu.submenuItemLabels:Dimensions` | Pre-existing parameterized label selector replaces the positional pick; param = variable label from the guide flow (semantic-layer uses "Dimensions"). submenuItem was deliberately not parameterized. |
| `div[data-testid='data-testid template variable'] input:nth-match(3)` | formfill | no-change | `[data-testid="data-testid Dashboard template variables submenu Label Dimensions"]` | `grafana:pages.Dashboard.SubMenu.submenuItemLabels:Dimensions` | Pre-existing parameterized label selector replaces the positional pick; param = variable label from the guide flow (semantic-layer uses "Dimensions"). submenuItem was deliberately not parameterized. |
| `div[data-viz-panel-key='panel-2579'] > button[data-testid='panel-menu-button']` | highlight | no-change | `div[data-viz-panel-key='panel-2579'] > button[data-testid='panel-menu-button']` | — | panel-menu-button is the core fallback literal for untitled panels (unregistered — no token; future version-key candidate); the data-viz-panel-key half is dashboard instance data. Titled panels: use components.Panels.Panel.menu(title). |
| `div[data-testid='data-testid panel content'] > div[data-testid='uplot-main-div']:nth-match(3)` | highlight | not-fixable | — | — | Positional pick inside panel content; re-scope via components.Panels.Panel.title(<panel title>). |
| `div[data-testid='data-testid panel content'] div:nth-match(14)` | highlight | not-fixable | — | — | Positional pick inside panel content; re-scope via components.Panels.Panel.title(<panel title>). |
| `div[role="gridcell"]:contains("Qualification")` | highlight | not-fixable | — | — | Cell content is query-result (instance) data — no core selector can identify a value cell. |
| `div[role="gridcell"]:contains("R.")` | highlight | not-fixable | — | — | Cell content is query-result (instance) data — no core selector can identify a value cell. |
| `div[aria-label="Generated SQL query"]:contains('payment_method')` | highlight | external | — | — | owner: grafana-cube-datasource. Semantic-layer query editor UI ships in the Cube datasource plugin. |
| `div[aria-label='Generated SQL query']` | highlight x4 | external | — | — | owner: grafana-cube-datasource. Semantic-layer query editor UI ships in the Cube datasource plugin. |
| `input[aria-label='Dimensions']` | highlight | external | — | — | owner: grafana-cube-datasource. Semantic-layer query editor UI ships in the Cube datasource plugin. |

## send-logs-alloy-loki-lj/install-alloy

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[data-testid='home-install-alloy-button']` | highlight | external | — | — | owner: grafana-collector-app. Not fixable in grafana/grafana — owned by grafana-collector-app. Fleet Management home 'Install Alloy' button. |

## slo-quickstart

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `#generate-alerts` | highlight | external | — | — | owner: grafana-slo-app. Not fixable in grafana/grafana — owned by grafana-slo-app. Burn-rate alert generation checkbox on the SLO creation wizard at /a/grafana-slo-app/wizard/new. |
| `[data-testid='query-type-ratio']` | highlight | external | — | — | owner: grafana-slo-app. Not fixable in grafana/grafana — owned by grafana-slo-app. 'ratio' is an SLO query type; not in core source or bundles (inference) |
| `[data-testid='run-queries-btn']` | highlight | external | — | — | owner: grafana-slo-app. run queries — SLO app UI, not grafana/grafana. |
| `[data-testid='success-metric-field'] textarea.inputarea.monaco-mouse-cursor-text` | formfill | external | — | — | owner: grafana-slo-app. Not fixable in grafana/grafana — owned by grafana-slo-app. SLO wizard success metric field; inner textarea is monaco-editor |
| `[data-testid='total-metric-field'] textarea.inputarea.monaco-mouse-cursor-text` | formfill | external | — | — | owner: grafana-slo-app. Not fixable in grafana/grafana — owned by grafana-slo-app. SLO wizard ratio-query total metric field (Monaco editor inside) |
| `[data-testid='walk-next-button']` | highlight x4 | external | — | — | owner: grafana-slo-app. wizard stepper — SLO app UI, not grafana/grafana. |
| `[data-testid='walk-save-button']` | highlight | external | — | — | owner: grafana-slo-app. Not fixable in grafana/grafana — owned by grafana-slo-app. 'Save and view all SLOs' button on the SLO wizard at /a/grafana-slo-app/wizard/new (sibling testids walk-next-button, slo-name-input confirm the app). |
| `input[data-testid='slo-name-input']` | formfill | external | — | — | owner: grafana-slo-app. Not fixable in grafana/grafana — owned by grafana-slo-app. |
| `input[data-testid='target-input']` | formfill | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Check target field in the SM check editor; not in core source or bundles |
| `input[data-testid='time-window-input']` | highlight | external | — | — | owner: grafana-slo-app. Not fixable in grafana/grafana — owned by grafana-slo-app. Likely SLO wizard evaluation window input; not in this repo |
| `textarea[data-testid='slo-description-input']` | formfill | external | — | — | owner: grafana-slo-app. Not fixable in grafana/grafana — owned by grafana-slo-app. SLO creation form description textarea. |

## sm-dns-check-tutorial

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `input[id^='option-60000-radiogroup-']` | highlight | stale | `[data-testid="data-testid radio-button-option 60000"]` | `grafana:components.RadioButton.option:60000` | STALE: the option-${value}-radiogroup-${n} id scheme was replaced with useId (#124384). grafana-ui RadioButtonGroup options now carry radio-button-option testids (PR #129669) — applies inside the SM app's frequency group too since apps share core grafana-ui at runtime. Scope to the frequency radiogroup. RadioButton.option is unique within a group, not across a page — scope to the owning group container. |
| `[aria-label="timeout seconds input"]` | formfill | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor timeout field (co-occurs with checkEditor anchors) |
| `[id='pageContent'] a[href='/a/grafana-synthetic-monitoring-app/home']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. #pageContent is core; the SM home link is rendered by the SM app. |
| `[name="target"]` | formfill | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. No core hit; matches the react-hook-form 'target' field in the Synthetic Monitoring check editor (uncertain). |
| `a[data-testid='action create check']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check-creation action button |
| `a[href='/a/grafana-synthetic-monitoring-app/checks/new/api-endpoint']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. |
| `button[data-testid='checkEditor feat-adhoc-check testButton']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. checkEditor namespace is the Synthetic Monitoring check editor |
| `button[data-testid='checkEditor form submit']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor submit button |
| `button[data-testid='checkEditor navigation alerting']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. checkEditor testids belong to Synthetic Monitoring's check editor. |
| `button[data-testid='checkEditor navigation execution']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor section navigation |
| `button[data-testid='checkEditor navigation labels']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor navigation button |
| `button[data-testid='checkEditor navigation uptime']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor section navigation |
| `input[data-testid='checkEditor alerts ProbeFailedExecutionsTooHigh selectedCheckbox']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor per-alert checkbox |
| `input[data-testid='checkEditor form job']` | formfill | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor job name input |
| `input[placeholder='name']` | formfill | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Label name input in the Labels section of the SM check editor (guide fills 'env' right after 'checkEditor navigation labels'). |
| `input[placeholder='value']` | formfill | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Label value input in the Labels section of the SM check editor (paired with the placeholder 'name' input). |
| `label:contains('DNS')` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Inferred: DNS check-type label in the Synthetic Monitoring check editor; generic text selector, verify in live DOM. |
| `label[data-testid='checkEditor form probeLabel']:first-of-type` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor probes field. |

## sm-ping-check-tutorial

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `input[id^='option-60000-radiogroup-']` | highlight | stale | `[data-testid="data-testid radio-button-option 60000"]` | `grafana:components.RadioButton.option:60000` | STALE: the option-${value}-radiogroup-${n} id scheme was replaced with useId (#124384). grafana-ui RadioButtonGroup options now carry radio-button-option testids (PR #129669) — applies inside the SM app's frequency group too since apps share core grafana-ui at runtime. Scope to the frequency radiogroup. RadioButton.option is unique within a group, not across a page — scope to the owning group container. |
| `[id='pageContent'] a[href='/a/grafana-synthetic-monitoring-app/home']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. #pageContent is core; the SM home link is rendered by the SM app. |
| `a[data-testid='action create check']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check-creation action button |
| `a[href='/a/grafana-synthetic-monitoring-app/checks/new/api-endpoint']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. |
| `button[data-testid='checkEditor feat-adhoc-check testButton']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. checkEditor namespace is the Synthetic Monitoring check editor |
| `button[data-testid='checkEditor form submit']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor submit button |
| `button[data-testid='checkEditor navigation alerting']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. checkEditor testids belong to Synthetic Monitoring's check editor. |
| `button[data-testid='checkEditor navigation execution']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor section navigation |
| `button[data-testid='checkEditor navigation labels']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor navigation button |
| `button[data-testid='checkEditor navigation uptime']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor section navigation |
| `form[data-testid='checkEditor form']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor form. |
| `input[aria-label='Custom labels 1 name']` | formfill | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Not in core; matches Synthetic Monitoring check editor custom labels fields (uncertain). |
| `input[aria-label='Custom labels 1 value']` | formfill | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. not in core; 'Custom labels' with indexed value inputs matches the Synthetic Monitoring check editor labels field (inference) |
| `input[data-testid='checkEditor alerts ProbeFailedExecutionsTooHigh selectedCheckbox']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor per-alert checkbox |
| `input[data-testid='checkEditor form job']` | formfill | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor job name input |
| `input[name='target'][placeholder='grafana.com']` | formfill | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. No core hit; matches the react-hook-form 'target' field in the Synthetic Monitoring check editor (uncertain). |
| `label[data-testid='checkEditor form probeLabel']:first-of-type` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor probes field. |
| `label[title='Check a host for availability and response time.']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Ping check-type description in the Synthetic Monitoring check editor. |

## sm-scripted-check-tutorial

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[role='menuitemradio'][aria-label='5 seconds']` | button | ready | `[data-testid="data-testid ButtonSelect option 5s"]` | `grafana:components.ButtonSelect.option:5s` | RefreshPicker interval options carry the interval string as value. NOTE (post-doc change on main): the param is now optional — options without a scalar value render the bare "data-testid ButtonSelect option". |
| `[aria-labelledby='form-section-alerting'] [data-testid='checkEditor formTabs content']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor form tabs |
| `[data-testid='checkEditor form'] > div:last-child > div:last-child  button[type='button']` | button x3 | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor form. |
| `[data-testid='checkEditor form'] > div:last-child button[type='button']` | button | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor form. |
| `[data-testid='checkEditor genericLabelContent']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor testid. |
| `[data-testid='frequency-component'] [role='radiogroup'] label:contains('1m')` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. SM check editor. App-side fix available since PR #129669: RadioButton.option('60') scoped to the frequency radiogroup, once the app adopts it. |
| `a[data-testid='action create check']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check-creation action button |
| `div[data-testid='check-group-card-scripted'] a:nth-match(1)` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check-type group card (scripted checks). |
| `div[data-testid='input-wrapper'] input[data-testid='checkEditor form instance']` | formfill | external | — | — | owner: grafana-synthetic-monitoring-app. SM check editor form. |
| `form[data-testid='checkEditor form'] button[data-testid='checkEditor form submit']` | button | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor form. |
| `form[data-testid='checkEditor form'] div[data-testid='timeout']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor form. |
| `form[data-testid='checkEditor form'] label:nth-match(47)` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor form. |
| `input[data-testid='checkEditor form job']` | formfill | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor job name input |

## sm-setting-up-your-first-check

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `input[id^='option-60000-radiogroup-']` | highlight | stale | `[data-testid="data-testid radio-button-option 60000"]` | `grafana:components.RadioButton.option:60000` | STALE: the option-${value}-radiogroup-${n} id scheme was replaced with useId (#124384). grafana-ui RadioButtonGroup options now carry radio-button-option testids (PR #129669) — applies inside the SM app's frequency group too since apps share core grafana-ui at runtime. Scope to the frequency radiogroup. RadioButton.option is unique within a group, not across a page — scope to the owning group container. |
| `[data-testid='checkEditor genericLabelContent']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor testid. |
| `[id='pageContent'] a[href='/a/grafana-synthetic-monitoring-app/home']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. #pageContent is core; the SM home link is rendered by the SM app. |
| `a[data-testid='action create check']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check-creation action button |
| `a[href='/a/grafana-synthetic-monitoring-app/checks/new/api-endpoint']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. |
| `button[data-testid='app-init init-button']` | highlight | external | — | — | owner: external (owner not recorded in analysis). Not fixable in grafana/grafana — owned by external (owner not recorded in analysis). Not in core source or bundles; looks like an app plugin's initialization button — owning plugin not identifiable from this repo. |
| `button[data-testid='checkEditor feat-adhoc-check testButton']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. checkEditor namespace is the Synthetic Monitoring check editor |
| `button[data-testid='checkEditor form submit']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor submit button |
| `button[data-testid='checkEditor navigation alerting']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. checkEditor testids belong to Synthetic Monitoring's check editor. |
| `button[data-testid='checkEditor navigation execution']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor section navigation |
| `button[data-testid='checkEditor navigation labels']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor navigation button |
| `button[data-testid='checkEditor navigation uptime']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor section navigation |
| `input[data-testid='checkEditor alerts ProbeFailedExecutionsTooHigh selectedCheckbox']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor per-alert checkbox |
| `input[data-testid='checkEditor form instance']` | formfill | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor form field. |
| `input[data-testid='checkEditor form job']` | formfill | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor job name input |
| `input[data-testid='checkEditor form validStatusCodes']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor HTTP settings field. |
| `label[data-testid='checkEditor form probeLabel']:first-of-type` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor probes field. |

## sm-tcp-check-tutorial

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `input[id^='option-60000-radiogroup-']` | highlight | stale | `[data-testid="data-testid radio-button-option 60000"]` | `grafana:components.RadioButton.option:60000` | STALE: the option-${value}-radiogroup-${n} id scheme was replaced with useId (#124384). grafana-ui RadioButtonGroup options now carry radio-button-option testids (PR #129669) — applies inside the SM app's frequency group too since apps share core grafana-ui at runtime. Scope to the frequency radiogroup. RadioButton.option is unique within a group, not across a page — scope to the owning group container. |
| `[aria-label="Query to send 1"]` | formfill | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. First query input of the TCP check Query/Response section in the SM check editor (paired with 'Response to expect 1'). |
| `[aria-label="Response to expect 1"]` | formfill | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. 'Response to expect' is the TCP check Query/Response field in Synthetic Monitoring. |
| `[aria-label="timeout seconds input"]` | formfill | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor timeout field (co-occurs with checkEditor anchors) |
| `[id='pageContent'] a[href='/a/grafana-synthetic-monitoring-app/home']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. #pageContent is core; the SM home link is rendered by the SM app. |
| `[name='target']` | formfill | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. No core hit; matches the react-hook-form 'target' field in the Synthetic Monitoring check editor (uncertain). |
| `a[data-testid='action create check']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check-creation action button |
| `a[href='/a/grafana-synthetic-monitoring-app/checks/new/api-endpoint']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. |
| `button[data-testid='checkEditor feat-adhoc-check testButton']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. checkEditor namespace is the Synthetic Monitoring check editor |
| `button[data-testid='checkEditor form submit']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor submit button |
| `button[data-testid='checkEditor navigation alerting']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. checkEditor testids belong to Synthetic Monitoring's check editor. |
| `button[data-testid='checkEditor navigation execution']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor section navigation |
| `button[data-testid='checkEditor navigation labels']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor navigation button |
| `button[data-testid='checkEditor navigation uptime']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor section navigation |
| `input[data-testid='checkEditor alerts ProbeFailedExecutionsTooHigh selectedCheckbox']` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor per-alert checkbox |
| `input[data-testid='checkEditor form job']` | formfill | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor job name input |
| `input[placeholder='name']` | formfill | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Label name input in the Labels section of the SM check editor (guide fills 'env' right after 'checkEditor navigation labels'). |
| `input[placeholder='value']` | formfill | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Label value input in the Labels section of the SM check editor (paired with the placeholder 'name' input). |
| `label:contains('TCP')` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. TCP check-type option label in Synthetic Monitoring; the only core hit is descriptive card text, not a label. |
| `label[data-testid='checkEditor form probeLabel']:first-of-type` | highlight | external | — | — | owner: grafana-synthetic-monitoring-app. Not fixable in grafana/grafana — owned by grafana-synthetic-monitoring-app. Synthetic Monitoring check editor probes field. |

## transform-data

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[href='/dashboard/new']` | highlight | ready | `[data-testid="data-testid CreateNewButton New dashboard link"]` | `grafana:components.CreateNewButton.newDashboardLink` | Wired by programme PR #129698. |
| `button[aria-label='New']` | highlight | ready | `[data-testid="data-testid Quick add button"]` | `grafana:components.NavToolbar.quickAddButton` | — |
| `input:nth-of-type(1):nth-match(2)` | formfill x2 | ready | `[data-testid="data-testid transformation filter topic select"] input` | `{grafana:components.Transforms.filterEditor.topicSelect} input` | Selector lands on the Select container div — scope " input" inside. |
| `input:nth-of-type(1):nth-match(3)` | formfill | ready | `[data-testid="data-testid transformation filter editor container"] input` | `{grafana:components.Transforms.filterEditor.container} input` | Frame multi-select forwards nothing — scope inside the new wrapper container. |
| `input[name='seriesCount']` | formfill | ready | `[data-testid="data-testid TestData series count"]` | `grafana:components.DataSource.TestData.QueryTab.seriesCount` | **gate: plugin rollout.** Dormant entry upgraded with a prefixed 13.2.0 key and wired in RandomWalkEditor (PR #129768). grafana-testdata-datasource is a decoupled plugin bundle — the testid only appears once the NEW plugin asset is what the stack loads. Legacy aria-label matching keeps working on older bundles. |

## understanding-the-four-golden-signals-of-observability

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[href='/d/a581fb5a-df38-45d7-83cb-d10835930fa1/performance-stats']` | highlight | external | — | — | owner: instance-content (provisioned dashboard/demo data). Not fixable in grafana/grafana — owned by instance-content (provisioned dashboard/demo data). Link to the provisioned Performance Stats demo dashboard used by the golden-signals course; the anchor is instance dashboard content. |
| `button[data-testid='install-quickpizza']` | highlight | external | — | — | owner: k6-app. Not fixable in grafana/grafana — owned by k6-app. QuickPizza is the k6 demo app; button could also come from the Pathfinder demo environment |

## visualization-logs/add-visualization

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[href='/dashboard/new']` | highlight | ready | `[data-testid="data-testid CreateNewButton New dashboard link"]` | `grafana:components.CreateNewButton.newDashboardLink` | Wired by programme PR #129698. |

## visualization-logs/write-query

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[data-testid="label-browser-button"]` | highlight | external | — | — | owner: loki datasource frontend (@grafana/loki, decoupled from grafana/grafana). Not fixable in grafana/grafana — owned by loki datasource frontend (@grafana/loki, decoupled from grafana/grafana). The Loki query editor 'Label browser' toggle button; loki datasource sources are no longer in this repo or its node_modules. |

## visualization-metrics-lj/add-visualization

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[href="/dashboard/new"]` | highlight | ready | `[data-testid="data-testid CreateNewButton New dashboard link"]` | `grafana:components.CreateNewButton.newDashboardLink` | Wired by programme PR #129698. |
| `ul[aria-label="Navigation"] a[href="/dashboards"]` | highlight | no-change | `a[data-testid="data-testid Nav menu item"][href='/dashboards']` | `a{grafana:components.NavMenu.item}[href='/dashboards']` | GD-5 compound: keep the href half; a section rendered in both the pinned box and the main nav can double-match — scope with components.NavMenu.Menu ([data-testid="data-testid navigation mega-menu"]) when needed. |

## visualization-traces-lj/add-traces-panel

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `label[for^='option-traceql-']` | highlight | stale | `[data-testid="data-testid radio-button-option traceql"]` | `grafana:components.RadioButton.option:traceql` | STALE: legacy option-${value}-${n} id pattern replaced by useId (#124384). Use RadioButton.option ('traceql') scoped to the Tempo query-type radiogroup (PR #129669). RadioButton.option is unique within a group, not across a page — scope to the owning group container. |

## visualization-traces-lj/add-traces-table

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `label[for*='traceqlSearch']` | highlight | external | — | — | owner: tempo (Tempo datasource plugin, decoupled from core). Not fixable in grafana/grafana — owned by tempo (Tempo datasource plugin, decoupled from core). public/app/plugins/datasource/tempo no longer exists in this repo; TraceQL search editor lives in the external Tempo datasource repo |

## visualization-traces-lj/add-visualization

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[href='/dashboard/new']` | highlight | ready | `[data-testid="data-testid CreateNewButton New dashboard link"]` | `grafana:components.CreateNewButton.newDashboardLink` | Wired by programme PR #129698. |

## welcome-to-play/datasource-page

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[href*="/d/T512JVH7z/loki-nginx-service-mesh-json-version"]` | highlight | not-fixable | — | — | Provisioned Play dashboard UID — instance data (Play demo content, not core JSX). |
| `a[href*="/d/ddkar8yanj56oa/visualizing-google-sheets-data"]` | highlight | not-fixable | — | — | Provisioned Play dashboard UID — instance data (Play demo content, not core JSX). |
| `a[href*="/d/infinity/2dc7103"]` | highlight | not-fixable | — | — | Provisioned Play dashboard UID — instance data (Play demo content, not core JSX). |

## welcome-to-play/main-page

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[href*="/d/ma79mqp/visualization-examples"]` | highlight | not-fixable | — | — | Provisioned Play dashboard UID — instance data (Play demo content, not core JSX). |
| `a[href*="/d/mabjzp6/grafana-arcade"]` | highlight | not-fixable | — | — | Provisioned Play dashboard UID — instance data (Play demo content, not core JSX). |
| `a[href*="/d/mamnq22/data-source-examples"]` | highlight | not-fixable | — | — | Provisioned Play dashboard UID — instance data (Play demo content, not core JSX). |
| `iframe[src*="youtube.com/embed"]` | highlight | not-fixable | — | — | Embedded iframe — not a core UI element. |
| `a[href*="a/grafana-app-observability-app"]` | highlight | external | — | — | owner: grafana-app-observability-app. Link into an external Cloud app. |
| `a[href*="a/grafana-k8s-app"]` | highlight | external | — | — | owner: grafana-k8s-app. Link into an external Cloud app. |

## welcome-to-play/visualization-page

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[href*="/d/cdl34qv4zzg8wa/flame-graphs"]` | highlight | not-fixable | — | — | Provisioned Play dashboard UID — instance data (Play demo content, not core JSX). |
| `a[href*="/d/000000016/time-series-graphs"]` | highlight | external | — | — | owner: instance-content (provisioned dashboard/demo data). Not fixable in grafana/grafana — owned by instance-content (provisioned dashboard/demo data). Link on Play's provisioned 'visualization examples' navigation dashboard pointing at the Time series graphs demo dashboard. |
| `a[href*="/d/c9ea65f5-ed5a-45cf-8fb7-f82af7c3afdf/canvas-visualization"]` | highlight | external | — | — | owner: instance-content (provisioned dashboard/demo data). Not fixable in grafana/grafana — owned by instance-content (provisioned dashboard/demo data). Link on Play's provisioned visualization-examples navigation dashboard pointing at the Canvas demo dashboard. |
| `a[href*="/d/panel-geomap/geomap-examples"]` | highlight | external | — | — | owner: instance-content (provisioned dashboard/demo data). Not fixable in grafana/grafana — owned by instance-content (provisioned dashboard/demo data). Link on Play's provisioned visualization-examples navigation dashboard pointing at the Geomap examples dashboard. |

## windows-integration/install-alloy

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `[data-testid="agent-config-button"]` | highlight | external | — | — | owner: grafana-collector-app. Not fixable in grafana/grafana — owned by grafana-collector-app. Fleet Management (Alloy/collector) UI; not in this repo |

## windows-integration/install-dashboards-alerts

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[data-testid='view-dashboards-button']` | highlight | external | — | — | owner: grafana-easystart-app. Not fixable in grafana/grafana — owned by grafana-easystart-app. Not in core or bundles; likely the Cloud onboarding/integrations app 'View dashboards' button after installing an integration (uncertain). |

## windows-integration/select-platform

| oldReftarget | action | status | newCss | newToken | notes |
|---|---|---|---|---|---|
| `a[href="/connections/add-new-connection/windows-exporter"]` | highlight | no-change | `[data-testid="data-testid Connections plugin card Windows"] a` | `{grafana:pages.Connections.AddNewConnection.pluginCard:Windows} a` | Group 6 — zero core code: card already carries the pre-existing pluginCard(name) testid (CardGrid.tsx). PARAM = Cloud catalog display name, derived best-effort from the href slug "windows-exporter" — verify the exact display name in the Cloud connections catalog. Testid sits on the Card wrapper; append " a" to click the anchor. |
| `[aria-label="Search connections by name"]` | formfill | external | — | — | owner: grafana-easystart-app. Not fixable in grafana/grafana — owned by grafana-easystart-app. Not in core; likely the Cloud onboarding/Connections console search input (uncertain). |
