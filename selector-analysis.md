# Selector reftarget analysis — interactive-tutorials

Generated 2026-07-30 from every `content.json` in this repo (1,484 reftargets; 774 unique CSS selectors after excluding 94 button-text and 58 navigate reftargets), cross-referenced against `grafana/grafana` source (`packages/grafana-e2e-selectors`, `public/app`, `packages/`) and built bundles (`public/build` + sourcemaps).

Full machine-readable dataset: [`selector-analysis.json`](selector-analysis.json) — per selector: occurrence count, guides, actions, and source resolution per anchor.

Source column: `core` = attribute emitted by code in grafana/grafana; `library` = attribute emitted at runtime by `@grafana/scenes` or `@grafana/plugin-ui` from node_modules (the `emittedBy` field in the JSON), even when the e2e selector value is defined in this repo; `external` = plugin app, decoupled datasource, or instance content.

## Totals

| Priority | Category | Unique selectors | Occurrences |
|---|---|---|---|
| 0 | e2e-selector | 295 | 586 |
| 1 | data-testid | 202 | 360 |
| 2 | Semantic attributes | 199 | 262 |
| 3 | :contains()/:text() text matching | 39 | 52 |
| 4 | :has() structural matching | 1 | 3 |
| 5 | CSS class / tag selectors | 38 | 69 |

## Priority 0: e2e-selector

_targets a value defined in @grafana/e2e-selectors (highest stability)_ — 295 unique selectors, 586 occurrences.

| # | Selector | Uses | Guides | Source | Where |
|---|---|---|---|---|---|
| 1 | `button[data-testid='data-testid Back to dashboard button']` | 17 | 8 | core | components.NavToolbar.editDashboard.backToDashboardButton |
| 2 | `a[data-testid='data-testid Panel menu item Edit']` | 16 | 7 | library | components.Panels.Panel.menuItems (emitted by @grafana/scenes) |
| 3 | `a[data-testid='data-testid Nav menu item'][href='/dashboards']` | 15 | 13 | core | components.NavMenu.item; public/app/core/components/AppChrome/MegaMenu/MegaMenuItemText.tsx:127 |
| 4 | `button[data-testid='data-testid Drawer close']` | 14 | 6 | core | components.Drawer.General.close |
| 5 | `a[data-testid='data-testid Nav menu item'][href='/connections']` | 12 | 12 | core | components.NavMenu.item; pkg/services/navtree/navtreeimpl/navtree.go:573 |
| 6 | `a[data-testid='data-testid Nav menu item'][href='/testing-and-synthetics']` | 11 | 11 | core | components.NavMenu.item |
| 7 | `[data-testid='data-testid Select a data source']` | 10 | 10 | core | components.DataSourcePicker.inputV2 |
| 8 | `a[data-testid='data-testid Nav menu item'][href='/connections/add-new-connection']` | 10 | 10 | core | components.NavMenu.item |
| 9 | `a[data-testid='data-testid Nav menu item'][href='/alerting']` | 8 | 8 | core | components.NavMenu.item; public/app/features/alerting/routes.tsx:21 |
| 10 | `button[data-testid='data-testid Edit dashboard button']` | 8 | 7 | core | components.NavToolbar.editDashboard.editButton |
| 11 | `button[data-testid='data-testid Tab Transformations']` | 8 | 5 | core | components.Tab.title |
| 12 | `a[data-testid='data-testid Nav menu item'][href='/alerting/list']` | 7 | 7 | core | components.NavMenu.item; public/app/features/alerting/routes.tsx:33 |
| 13 | `a[data-testid='data-testid Nav menu item'][href='/alerts-and-incidents']` | 6 | 6 | core | components.NavMenu.item; pkg/services/navtree/navtreeimpl/applinks.go:452 |
| 14 | `button[data-testid='data-testid Tab Graph']` | 6 | 3 | core | components.Tab.title |
| 15 | `button[data-testid='data-testid Tab Logs']` | 6 | 3 | core | components.Tab.title |
| 16 | `button[data-testid='data-testid Tab Properties']` | 6 | 3 | core | components.Tab.title |
| 17 | `button[data-testid='data-testid Tab Queries']` | 6 | 4 | core | components.Tab.title |
| 18 | `button[data-testid='data-testid Tab Timeline']` | 6 | 3 | core | components.Tab.title |
| 19 | `div[data-testid='data-testid Code editor container']` | 6 | 5 | core | components.CodeEditor.container |
| 20 | `[data-testid='data-testid Plugin visualization item Table']` | 5 | 5 | core | components.PluginVisualization.item |
| 21 | `a[data-testid='data-testid Nav menu item'][href='/a/grafana-adaptive-metrics-app/overvi...` | 5 | 4 | core | components.NavMenu.item |
| 22 | `a[data-testid='data-testid Nav menu item'][href='/explore']` | 5 | 5 | core | components.NavMenu.item |
| 23 | `button[data-testid='data-testid RefreshPicker run button']` | 5 | 4 | core | components.RefreshPicker.runButtonV2 |
| 24 | `button[data-testid='data-testid Save dashboard button']` | 5 | 4 | core | components.NavToolbar.editDashboard.saveButton |
| 25 | `input[data-testid='data-testid Select a data source']` | 5 | 5 | core | components.DataSourcePicker.inputV2 |
| 26 | `[data-testid='data-testid data-source-add-button']` | 4 | 4 | core | pages.DataSources.dataSourceAddButton |
| 27 | `a[data-testid='data-testid Nav menu item'][href='/a/k6-app']` | 4 | 4 | external | components.NavMenu.item; k6-app |
| 28 | `a[data-testid='data-testid Nav menu item'][href='adaptive-telemetry']` | 4 | 4 | core | components.NavMenu.item; public/app/routes/routes.tsx:247 |
| 29 | `button[data-testid='data-testid Dashboard Sidebar new button']` | 4 | 2 | core | pages.Dashboard.Sidebar.addButton |
| 30 | `button[data-testid='data-testid TimePicker Open Button']` | 4 | 4 | core | components.TimePicker.openButton |
| 31 | `div[role='gridcell'][aria-colindex='1'] a[data-testid='data-testid Data link']:nth-matc...` | 4 | 2 | core | components.DataLinksContextMenu.singleLink; packages/grafana-ui/src/components/Table/TableNG/hooks.ts |
| 32 | `[data-testid='data-testid Panel editor option pane field input Title']` | 3 | 3 | core | components.PanelEditor.OptionsPane.fieldInput |
| 33 | `[data-testid='data-testid Tab All visualizations']` | 3 | 3 | core | components.Tab.title |
| 34 | `[data-testid='data-testid Tab Visualizations']` | 3 | 3 | core | components.Tab.title |
| 35 | `[data-testid='data-testid TimePicker Open Button']` | 3 | 3 | core | components.TimePicker.openButton |
| 36 | `[data-testid='data-testid metric select']` | 3 | 3 | core | components.DataSource.Prometheus.queryEditor.builder.metricSelect |
| 37 | `a[data-testid="data-testid Nav menu item"][href="/a/grafana-irm-app/alert-groups"]` | 3 | 2 | external | components.NavMenu.item; grafana-irm-app |
| 38 | `a[data-testid="data-testid Nav menu item"][href="/a/grafana-irm-app/integrations"]` | 3 | 3 | external | components.NavMenu.item; grafana-irm-app |
| 39 | `a[data-testid='data-testid Nav menu item'][href='/a/grafana-collector-app/fleet-managem...` | 3 | 3 | external | components.NavMenu.item; grafana-collector-app |
| 40 | `a[data-testid='data-testid Nav menu item'][href='/a/grafana-irm-app/incidents']` | 3 | 3 | core | components.NavMenu.item |
| 41 | `a[data-testid='data-testid Nav menu item'][href='/a/grafana-lokiexplore-app/explore']` | 3 | 3 | core | components.NavMenu.item |
| 42 | `a[data-testid='data-testid Nav menu item'][href='/a/grafana-synthetic-monitoring-app/co...` | 3 | 2 | external | components.NavMenu.item; grafana-synthetic-monitoring-app |
| 43 | `a[data-testid='data-testid Nav menu item'][href='/drilldown']` | 3 | 3 | core | components.NavMenu.item; pkg/services/navtree/navtreeimpl/navtree.go:146 |
| 44 | `button[data-testid="data-testid RefreshPicker run button"]` | 3 | 1 | core | components.RefreshPicker.runButtonV2 |
| 45 | `button[data-testid='data-testid Confirm Modal Danger Button']` | 3 | 2 | core | pages.ConfirmModal.delete |
| 46 | `button[data-testid='data-testid Tab Business']` | 3 | 3 | core | components.Tab.title |
| 47 | `button[data-testid='data-testid Tab Comparison']` | 3 | 3 | core | components.Tab.title |
| 48 | `button[data-testid='data-testid Tab Errored traces']` | 3 | 3 | core | components.Tab.title |
| 49 | `button[data-testid='data-testid Tab Kubernetes']` | 3 | 3 | core | components.Tab.title |
| 50 | `button[data-testid='data-testid Tab PostgreSQL Database']` | 3 | 3 | core | components.Tab.title |
| 51 | `button[data-testid='data-testid Tab Service overview']` | 3 | 3 | core | components.Tab.title |
| 52 | `button[data-testid='data-testid Tab Traces']` | 3 | 3 | core | components.Tab.title |
| 53 | `div[data-testid='data-testid Query editor row'] div:nth-match(58)` | 3 | 1 | core | components.QueryEditorRows.rows |
| 54 | `div[data-testid='data-testid portal-container'] button[data-testid='data-testid Confirm...` | 3 | 2 | core | components.Portal.container; pages.ConfirmModal.delete |
| 55 | `div[data-testid='data-testid sidebar add new panel']` | 3 | 2 | core | components.Sidebar.newPanelButton |
| 56 | `[data-testid="data-testid Back to dashboard button"]` | 2 | 2 | core | components.NavToolbar.editDashboard.backToDashboardButton |
| 57 | `[data-testid="data-testid Edit dashboard button"]` | 2 | 2 | core | components.NavToolbar.editDashboard.editButton |
| 58 | `[data-testid="data-testid Save dashboard button"]` | 2 | 2 | core | components.NavToolbar.editDashboard.saveButton |
| 59 | `[data-testid='data-testid Data source settings page name input field']` | 2 | 2 | core | pages.DataSource.name |
| 60 | `[data-testid='data-testid Drawer close']` | 2 | 1 | core | components.Drawer.General.close |
| 61 | `[data-testid='data-testid RefreshPicker interval button']` | 2 | 2 | core | components.RefreshPicker.intervalButtonV2 |
| 62 | `[data-testid='data-testid RefreshPicker run button']` | 2 | 2 | core | components.RefreshPicker.runButtonV2 |
| 63 | `[data-testid='data-testid Tab Exemptions']` | 2 | 2 | core | components.Tab.title |
| 64 | `[data-testid='data-testid Tab Patterns']` | 2 | 2 | core | components.Tab.title |
| 65 | `[data-testid='data-testid Tab Segments']` | 2 | 2 | core | components.Tab.title |
| 66 | `a[data-testid="data-testid Nav menu item"][href="/a/grafana-asserts-app/assertions"]` | 2 | 2 | external | components.NavMenu.item; grafana-asserts-app |
| 67 | `a[data-testid="data-testid Nav menu item"][href="/a/grafana-irm-app/escalations"]` | 2 | 2 | external | components.NavMenu.item; grafana-irm-app |
| 68 | `a[data-testid="data-testid Nav menu item"][href="/a/grafana-irm-app/schedules"]` | 2 | 2 | external | components.NavMenu.item; grafana-irm-app |
| 69 | `a[data-testid="data-testid Nav menu item"][href="/a/grafana-slo-app/home/insights"]` | 2 | 2 | core | components.NavMenu.item |
| 70 | `a[data-testid="data-testid Nav menu item"][href="/alerts-and-incidents"]` | 2 | 2 | core | components.NavMenu.item; pkg/services/navtree/navtreeimpl/applinks.go:452 |
| 71 | `a[data-testid='data-testid Nav menu item'][href='/a/grafana-adaptive-metrics-app/segmen...` | 2 | 2 | external | components.NavMenu.item; grafana-adaptive-metrics-app |
| 72 | `a[data-testid='data-testid Nav menu item'][href='/a/grafana-adaptivelogs-app/overview']` | 2 | 2 | external | components.NavMenu.item; grafana-adaptivelogs-app |
| 73 | `a[data-testid='data-testid Nav menu item'][href='/a/grafana-dbo11y-app/']` | 2 | 2 | external | components.NavMenu.item; grafana-dbo11y-app |
| 74 | `a[data-testid='data-testid Nav menu item'][href='/a/grafana-dbo11y-app/configuration']` | 2 | 2 | external | components.NavMenu.item; grafana-dbo11y-app |
| 75 | `a[data-testid='data-testid Nav menu item'][href='/a/grafana-dbo11y-app/overview']` | 2 | 2 | core | components.NavMenu.item |
| 76 | `a[data-testid='data-testid Nav menu item'][href='/a/grafana-k8s-app/navigation/namespace']` | 2 | 2 | core | components.NavMenu.item |
| 77 | `a[data-testid='data-testid Nav menu item'][href='/a/grafana-metricsdrilldown-app/drilld...` | 2 | 2 | external | components.NavMenu.item; grafana-metricsdrilldown-app |
| 78 | `a[data-testid='data-testid Nav menu item'][href='/a/grafana-synthetic-monitoring-app/ch...` | 2 | 2 | external | components.NavMenu.item; grafana-synthetic-monitoring-app |
| 79 | `a[data-testid='data-testid Nav menu item'][href='/a/grafana-synthetic-monitoring-app/ho...` | 2 | 2 | external | components.NavMenu.item; grafana-synthetic-monitoring-app |
| 80 | `a[data-testid='data-testid Nav menu item'][href='/a/k6-app/settings']` | 2 | 2 | external | components.NavMenu.item; k6-app |
| 81 | `a[data-testid='data-testid Tab Secrets']` | 2 | 1 | core | components.Tab.title |
| 82 | `button[data-testid='data-testid Hide response'] svg:nth-match(1)` | 2 | 1 | core | components.QueryEditorRow.actionButton |
| 83 | `button[data-testid='data-testid add transformation button']` | 2 | 1 | core | components.Transforms.addTransformationButton |
| 84 | `div[data-testid="data-testid panel content"] div[role="button"]:has(span:contains("1"))` | 2 | 2 | external | components.Panels.Panel.content; mixed (grafana-pathfinder-app; grafana-cube-datasource; instance content; core PageCard) |
| 85 | `div[data-testid="data-testid radio-button"]:nth-match(2)` | 2 | 2 | core | components.RadioButton.container |
| 86 | `div[data-testid='data-testid Card heading']:contains('Health')` | 2 | 2 | core | components.Card.heading |
| 87 | `div[data-testid='data-testid Card heading']:contains('Pull status')` | 2 | 2 | core | components.Card.heading |
| 88 | `div[data-testid='data-testid Card heading']:contains('Resources')` | 2 | 2 | core | components.Card.heading |
| 89 | `div[data-testid='data-testid Cell options Cell type field property editor'] input[role=...` | 2 | 1 | core | components.PanelEditor.OptionsPane.fieldLabel; packages/grafana-ui/src/components/Combobox/Combobox.tsx:291 |
| 90 | `div[data-testid='data-testid Explore'] button:nth-match(4)` | 2 | 2 | core | pages.Explore.General.container |
| 91 | `div[data-testid='data-testid Nav toolbar'] button[data-testid='extension-toolbar-button...` | 2 | 2 | core | components.NavToolbar.container |
| 92 | `div[data-testid='data-testid portal-container'] div[data-testid='data-testid Panel menu...` | 2 | 1 | core+library | components.Portal.container; components.Panels.Panel.menuItems (emitted by @grafana/scenes) |
| 93 | `div[role='row'][aria-rowindex='2'] div[role='gridcell'][aria-colindex='1'] a[data-testi...` | 2 | 2 | core | components.DataLinksContextMenu.singleLink; packages/grafana-ui/src/components/Table/TableNG/hooks.ts |
| 94 | `input[data-testid='data-testid Confirm Modal Input']` | 2 | 1 | core | pages.ConfirmModal.input |
| 95 | `section[data-testid='data-testid Panel header Alignment: Pod Usage/Requests (%)'] > div...` | 2 | 2 | core | components.Panels.Panel.title; components.Panels.Panel.content |
| 96 | `section[data-testid='data-testid Panel header Errors rate']` | 2 | 2 | core | components.Panels.Panel.title |
| 97 | `section[data-testid='data-testid Panel header Raw Data'] svg[data-testid='icon-ellipsis...` | 2 | 2 | core | components.Panels.Panel.title |
| 98 | `#pageContent div[data-testid='data-testid Card heading']:nth-match(2) button:text('Open...` | 1 | 1 | core | components.Card.heading; public/app/core/components/AppChrome/AppChrome.tsx:196 |
| 99 | `[aria-label="Add new data source Prometheus"]` | 1 | 1 | core | pages.AddDataSource.dataSourcePluginsV2 |
| 100 | `[data-testid="data-testid Data source settings page name input field"]` | 1 | 1 | core | pages.DataSource.name |
| 101 | `[data-testid="data-testid RefreshPicker interval button"]` | 1 | 1 | core | components.RefreshPicker.intervalButtonV2 |
| 102 | `[data-testid="data-testid RefreshPicker run button"]` | 1 | 1 | core | components.RefreshPicker.runButtonV2 |
| 103 | `[data-testid="data-testid Select label"]` | 1 | 1 | core | components.QueryBuilder.labelSelect |
| 104 | `[data-testid="data-testid TimePicker Open Button"]` | 1 | 1 | core | components.TimePicker.openButton |
| 105 | `[data-testid="data-testid data-source-add-button"]` | 1 | 1 | core | pages.DataSources.dataSourceAddButton |
| 106 | `[data-testid="data-testid metric select"]` | 1 | 1 | core | components.DataSource.Prometheus.queryEditor.builder.metricSelect |
| 107 | `[data-testid="data-testid template variable"]:nth-match(3)` | 1 | 1 | core | pages.Dashboard.SubMenu.submenuItem |
| 108 | `[data-testid="data-testid visualization picker"]` | 1 | 1 | core | components.PanelEditor.toggleVizPicker |
| 109 | `[data-testid='data-testid Back to dashboard button']` | 1 | 1 | core | components.NavToolbar.editDashboard.backToDashboardButton |
| 110 | `[data-testid='data-testid Dashboard Sidebar new button']` | 1 | 1 | core | pages.Dashboard.Sidebar.addButton |
| 111 | `[data-testid='data-testid Edit dashboard button']` | 1 | 1 | core | components.NavToolbar.editDashboard.editButton |
| 112 | `[data-testid='data-testid Panel header Current Billable Usage Cost by Product']` | 1 | 1 | core | components.Panels.Panel.title |
| 113 | `[data-testid='data-testid Panel menu item Edit']` | 1 | 1 | library | components.Panels.Panel.menuItems (emitted by @grafana/scenes) |
| 114 | `[data-testid='data-testid Plugin visualization item Logs']` | 1 | 1 | core | components.PluginVisualization.item |
| 115 | `[data-testid='data-testid Plugin visualization item Traces']` | 1 | 1 | core | components.PluginVisualization.item |
| 116 | `[data-testid='data-testid Tab Data Model']` | 1 | 1 | core | components.Tab.title |
| 117 | `[data-testid='data-testid alert-rule name-field']` | 1 | 1 | core | components.AlertRules.ruleNameField |
| 118 | `[data-testid='data-testid alert-rule preview-button']` | 1 | 1 | core | components.AlertRules.previewButton |
| 119 | `[data-testid='data-testid alert-rule step-2'] input[type='number']` | 1 | 1 | core | components.AlertRules.step |
| 120 | `[data-testid='data-testid sidebar add new panel']` | 1 | 1 | core | components.Sidebar.newPanelButton |
| 121 | `[data-testid='data-testid template variable']` | 1 | 1 | core | pages.Dashboard.SubMenu.submenuItem |
| 122 | `a[data-testid="data-testid Nav menu item"][href="/alerting"]` | 1 | 1 | core | components.NavMenu.item; public/app/features/alerting/routes.tsx:21 |
| 123 | `a[data-testid="data-testid Nav menu item"][href="/alerting/list"]` | 1 | 1 | core | components.NavMenu.item; public/app/features/alerting/routes.tsx:33 |
| 124 | `a[data-testid="data-testid Nav menu item"][href="/drilldown"]` | 1 | 1 | core | components.NavMenu.item; pkg/services/navtree/navtreeimpl/navtree.go:146 |
| 125 | `a[data-testid="data-testid Nav menu item"][href="/explore"]` | 1 | 1 | core | components.NavMenu.item |
| 126 | `a[data-testid='data-testid Data link']:nth-match(1)` | 1 | 1 | core | components.DataLinksContextMenu.singleLink |
| 127 | `a[data-testid='data-testid Data link'][href^='/a/grafana-k8s-app/navigation/namespace/'...` | 1 | 1 | external | components.DataLinksContextMenu.singleLink; grafana-k8s-app |
| 128 | `a[data-testid='data-testid Nav menu item'][href='/a/grafana-adaptive-metrics-app/config...` | 1 | 1 | external | components.NavMenu.item; grafana-adaptive-metrics-app |
| 129 | `a[data-testid='data-testid Nav menu item'][href='/a/grafana-adaptive-metrics-app/rule-m...` | 1 | 1 | external | components.NavMenu.item; grafana-adaptive-metrics-app |
| 130 | `a[data-testid='data-testid Nav menu item'][href='/a/grafana-cmab-app/']` | 1 | 1 | external | components.NavMenu.item; grafana-cmab-app |
| 131 | `a[data-testid='data-testid Nav menu item'][href='/a/grafana-collector-app/alloy']` | 1 | 1 | core | components.NavMenu.item; public/app/core/components/AppChrome/MegaMenu/MegaMenuItemText.tsx:127 |
| 132 | `a[data-testid='data-testid Nav menu item'][href='/a/grafana-demodashboards-app']` | 1 | 1 | external | components.NavMenu.item; grafana-demodashboards-app |
| 133 | `a[data-testid='data-testid Nav menu item'][href='/a/grafana-exploretraces-app/']` | 1 | 1 | external | components.NavMenu.item; grafana-exploretraces-app |
| 134 | `a[data-testid='data-testid Nav menu item'][href='/a/grafana-ml-app/home']` | 1 | 1 | external | components.NavMenu.item; grafana-ml-app (Machine Learning) |
| 135 | `a[data-testid='data-testid Nav menu item'][href='/a/grafana-synthetic-monitoring-app/al...` | 1 | 1 | external | components.NavMenu.item; grafana-synthetic-monitoring-app |
| 136 | `a[data-testid='data-testid Nav menu item'][href='/a/grafana-synthetic-monitoring-app/pr...` | 1 | 1 | core | components.NavMenu.item |
| 137 | `a[data-testid='data-testid Nav menu item'][href='/a/k6-app/learn']` | 1 | 1 | external | components.NavMenu.item; k6-app |
| 138 | `a[data-testid='data-testid Nav menu item'][href='/a/k6-app/projects']` | 1 | 1 | external | components.NavMenu.item; k6-app |
| 139 | `a[data-testid='data-testid Nav menu item'][href='/adaptive-telemetry']` | 1 | 1 | core | components.NavMenu.item; public/app/routes/routes.tsx:247 |
| 140 | `a[data-testid='data-testid Nav menu item'][href='/admin/plugins']` | 1 | 1 | core | components.NavMenu.item; public/app/routes/routes.tsx:271 |
| 141 | `a[data-testid='data-testid Nav menu item'][href='/connections/datasources']` | 1 | 1 | core | components.NavMenu.item; pkg/services/navtree/navtreeimpl/navtree.go:588-591 |
| 142 | `a[data-testid='data-testid Nav menu item'][href='/connections/private-data-source-conne...` | 1 | 1 | core | components.NavMenu.item |
| 143 | `a[data-testid='data-testid Nav menu item'][href='/plugins']` | 1 | 1 | core | components.NavMenu.item |
| 144 | `a[data-testid='data-testid Panel menu item Explore']` | 1 | 1 | library | components.Panels.Panel.menuItems (emitted by @grafana/scenes) |
| 145 | `a[data-testid='data-testid Tab CPU']` | 1 | 1 | core | components.Tab.title |
| 146 | `a[data-testid='data-testid Tab HTTP']` | 1 | 1 | core | components.Tab.title |
| 147 | `a[data-testid='data-testid Tab Memory']` | 1 | 1 | core | components.Tab.title |
| 148 | `a[data-testid='data-testid Tab Patterns']` | 1 | 1 | core | components.Tab.title |
| 149 | `a[data-testid='data-testid Tab Resources']` | 1 | 1 | core | components.Tab.title |
| 150 | `a[data-testid='data-testid Tab Rules']` | 1 | 1 | core | components.Tab.title |
| 151 | `a[data-testid='data-testid Tab THRESHOLDS']` | 1 | 1 | core | components.Tab.title |
| 152 | `a[data-testid='data-testid git-sync-dashboards/ breadcrumb']` | 1 | 1 | core | components.Breadcrumbs.breadcrumb |
| 153 | `button[aria-label='Add new data source Infinity']` | 1 | 1 | core | pages.AddDataSource.dataSourcePluginsV2 |
| 154 | `button[data-testid="data-testid Tab Related logs"]` | 1 | 1 | core | components.Tab.title |
| 155 | `button[data-testid="data-testid Tab Related metrics"]` | 1 | 1 | core | components.Tab.title |
| 156 | `button[data-testid="data-testid toggle-viz-picker"]` | 1 | 1 | core | components.PanelEditor.toggleVizPicker |
| 157 | `button[data-testid='data-testid CanvasGridAddActions add-panel']` | 1 | 1 | core | components.CanvasGridAddActions.addPanel |
| 158 | `button[data-testid='data-testid Create new panel button']` | 1 | 1 | core | pages.AddDashboard.itemButton |
| 159 | `button[data-testid='data-testid Dashboard Sidebar options button']` | 1 | 1 | core | pages.Dashboard.Sidebar.optionsButton |
| 160 | `button[data-testid='data-testid Dashboard Sidebar outline button']` | 1 | 1 | core | pages.Dashboard.Sidebar.outlineButton |
| 161 | `button[data-testid='data-testid Filter']:nth-match(1)` | 1 | 1 | core | components.QueryEditorRow.actionButton('Filter') |
| 162 | `button[data-testid='data-testid Panel menu Status'] svg:nth-match(1)` | 1 | 1 | core | components.Panels.Panel.menu |
| 163 | `button[data-testid='data-testid Panel menu item Explore']` | 1 | 1 | library | components.Panels.Panel.menuItems (emitted by @grafana/scenes) |
| 164 | `button[data-testid='data-testid RefreshPicker interval button']` | 1 | 1 | core | components.RefreshPicker.intervalButtonV2 |
| 165 | `button[data-testid='data-testid Remove']:nth-match(2)` | 1 | 1 | core | components.QueryEditorRow.actionButton |
| 166 | `button[data-testid='data-testid Show transform help']` | 1 | 1 | core | components.QueryEditorRow.actionButton |
| 167 | `button[data-testid='data-testid Tab All visualizations']` | 1 | 1 | core | components.Tab.title |
| 168 | `button[data-testid='data-testid Tab Breakdown']` | 1 | 1 | core | components.Tab.title |
| 169 | `button[data-testid='data-testid Tab Related metrics']` | 1 | 1 | core | components.Tab.title |
| 170 | `button[data-testid='data-testid Tab Slow traces']` | 1 | 1 | core | components.Tab.title |
| 171 | `button[data-testid='data-testid Tab Visualizations']` | 1 | 1 | core | components.Tab.title |
| 172 | `button[data-testid='data-testid Value picker button Add rule']` | 1 | 1 | core | components.ValuePicker.button |
| 173 | `button[data-testid='data-testid alert-rule preview-button']` | 1 | 1 | core | components.AlertRules.previewButton |
| 174 | `button[data-testid='data-testid remove all transformations button']` | 1 | 1 | core | components.Transforms.removeAllTransformationsButton |
| 175 | `button[data-testid='data-testid toggle-viz-picker']` | 1 | 1 | core | components.PanelEditor.toggleVizPicker |
| 176 | `div[data-onboarding='breakdown'] a[data-testid='data-testid Tab LOGS']` | 1 | 1 | core | components.Tab.title |
| 177 | `div[data-testid="data-testid panel content"]` | 1 | 1 | core | components.Panels.Panel.content |
| 178 | `div[data-testid='data-testid Built in data source list'] div:nth-match(27) button` | 1 | 1 | core | components.DataSourcePicker.advancedModal.builtInDataSourceList |
| 179 | `div[data-testid='data-testid Card heading']:contains('Application Observability') butto...` | 1 | 1 | core | components.Card.heading |
| 180 | `div[data-testid='data-testid Card heading']:contains('Jobs')` | 1 | 1 | core | components.Card.heading |
| 181 | `div[data-testid='data-testid Card heading']:contains('Webhook')` | 1 | 1 | core | components.Card.heading |
| 182 | `div[data-testid='data-testid Card heading']:nth-match(10)` | 1 | 1 | core | components.Card.heading |
| 183 | `div[data-testid='data-testid Card heading']:nth-match(2)` | 1 | 1 | core | components.Card.heading |
| 184 | `div[data-testid='data-testid Edge overrides Edge override rules field property editor']...` | 1 | 1 | core | components.PanelEditor.OptionsPane.fieldLabel |
| 185 | `div[data-testid='data-testid Layout container row Details for $component'] section:nth-...` | 1 | 1 | core | components.LayoutContainer |
| 186 | `div[data-testid='data-testid Nav toolbar'] svg:nth-match(2)` | 1 | 1 | core | components.NavToolbar.container |
| 187 | `div[data-testid='data-testid Node overrides Node override rules field property editor']...` | 1 | 1 | core | components.PanelEditor.OptionsPane.fieldLabel |
| 188 | `div[data-testid='data-testid Node overrides Node override rules field property editor']...` | 1 | 1 | core | components.PanelEditor.OptionsPane.fieldLabel |
| 189 | `div[data-testid='data-testid Node overrides Node override rules field property editor']...` | 1 | 1 | core | components.PanelEditor.OptionsPane.fieldLabel |
| 190 | `div[data-testid='data-testid Node overrides Node override rules field property editor']...` | 1 | 1 | core | components.PanelEditor.OptionsPane.fieldLabel |
| 191 | `div[data-testid='data-testid Panel editor content'] div[data-testid='data-testid Option...` | 1 | 1 | core | components.PanelEditor.General.content; components.OptionsGroup.group |
| 192 | `div[data-testid='data-testid Panel editor content'] div[data-testid='data-testid Option...` | 1 | 1 | core | components.PanelEditor.General.content; components.OptionsGroup.group |
| 193 | `div[data-testid='data-testid Plugin visualization item Time series']` | 1 | 1 | core | components.PluginVisualization.item |
| 194 | `div[data-testid='data-testid Query editor row'] button[data-testid='data-testid saved q...` | 1 | 1 | external | components.QueryEditorRows.rows; grafana-enterprise (Query Library) |
| 195 | `div[data-testid='data-testid Query editor row']:nth-match(1)` | 1 | 1 | core | components.QueryEditorRows.rows |
| 196 | `div[data-testid='data-testid Query field'] section[data-testid='data-testid ReactMonaco...` | 1 | 1 | core | components.QueryField.container; components.ReactMonacoEditor.editorLazy |
| 197 | `div[data-testid='data-testid Sidebar container'] button:text('Configure')` | 1 | 1 | core | components.Sidebar.container |
| 198 | `div[data-testid='data-testid Sidebar container'] ul[role='tree']` | 1 | 1 | core | components.Sidebar.container; public/app/features/dashboard-scene/sidebar/outline/DashboardOutlineRenderer.tsx:47 |
| 199 | `div[data-testid='data-testid browse-dashboards-table'] div[data-testid='data-testid bro...` | 1 | 1 | core | pages.BrowseDashboards.table.body; pages.BrowseDashboards.table.row |
| 200 | `div[data-testid='data-testid dashboard controls'] button[data-testid='data-testid Edit ...` | 1 | 1 | core | pages.Dashboard.Controls; components.NavToolbar.editDashboard.editButton |
| 201 | `div[data-testid='data-testid dashboard controls'] button[data-testid='data-testid Save ...` | 1 | 1 | core | pages.Dashboard.Controls; components.NavToolbar.editDashboard.saveButton |
| 202 | `div[data-testid='data-testid dashboard-row-wrapper-for-Adam: Overview']` | 1 | 1 | core | components.DashboardRow.wrapper |
| 203 | `div[data-testid='data-testid dashboard-row-wrapper-for-Earthquakes']` | 1 | 1 | core | components.DashboardRow.wrapper |
| 204 | `div[data-testid='data-testid dashboard-row-wrapper-for-North East England']` | 1 | 1 | core | components.DashboardRow.wrapper |
| 205 | `div[data-testid='data-testid dashboard-row-wrapper-for-Raw Data']` | 1 | 1 | core | components.DashboardRow.wrapper |
| 206 | `div[data-testid='data-testid dashboard-row-wrapper-for-Volcanoes']` | 1 | 1 | core | components.DashboardRow.wrapper |
| 207 | `div[data-testid='data-testid header-container'] button[data-testid='data-testid Panel m...` | 1 | 1 | core | components.Panels.Panel.headerContainer; components.Panels.Panel.menu |
| 208 | `div[data-testid='data-testid header-container'] button[data-testid='data-testid Panel m...` | 1 | 1 | core | components.Panels.Panel.headerContainer; components.Panels.Panel.menu |
| 209 | `div[data-testid='data-testid panel content']` | 1 | 1 | core | components.Panels.Panel.content |
| 210 | `div[data-testid='data-testid panel content'] > div[data-testid='uplot-main-div']:nth-ma...` | 1 | 1 | core | components.Panels.Panel.content |
| 211 | `div[data-testid='data-testid panel content'] div:nth-match(14)` | 1 | 1 | core | components.Panels.Panel.content |
| 212 | `div[data-testid='data-testid portal-container'] button[data-testid='data-testid save to...` | 1 | 1 | external | components.Portal.container; grafana-enterprise |
| 213 | `div[data-testid='data-testid portal-container'] div:text('Copy styles')` | 1 | 1 | core | components.Portal.container |
| 214 | `div[data-testid='data-testid portal-container'] div:text('Paste styles')` | 1 | 1 | core | components.Portal.container |
| 215 | `div[data-testid='data-testid prometheus options'] button[aria-expanded='false']` | 1 | 1 | core | components.DataSource.Prometheus.queryEditor.options |
| 216 | `div[data-testid='data-testid radio-button'] label:contains('Autodetect')` | 1 | 1 | core | components.RadioButton.container |
| 217 | `div[data-testid='data-testid radio-button'] label:nth-match(6)` | 1 | 1 | core | components.RadioButton.container |
| 218 | `div[data-testid='data-testid suggestion-Bar gauge - LCD']` | 1 | 1 | core | components.VisualizationPreview.card |
| 219 | `div[data-testid='data-testid template variable']` | 1 | 1 | core | pages.Dashboard.SubMenu.submenuItem |
| 220 | `div[data-testid='data-testid template variable'] input:nth-match(3)` | 1 | 1 | core | pages.Dashboard.SubMenu.submenuItem |
| 221 | `div[data-testid='data-testid template variable']:has(label[data-testid*='Label Filters'])` | 1 | 1 | core | pages.Dashboard.SubMenu.submenuItem |
| 222 | `div[data-testid='data-testid template variable']:has(label[data-testid*='Label Group by'])` | 1 | 1 | core | pages.Dashboard.SubMenu.submenuItem |
| 223 | `div[data-testid='query-editor-rows']>div:nth-child(1) input[data-testid='data-testid Se...` | 1 | 1 | core | components.DataSourcePicker.inputV2 |
| 224 | `div[data-viz-panel-key='panel-1'] section[data-testid='data-testid Panel header Custome...` | 1 | 1 | core | components.Panels.Panel.title |
| 225 | `div[data-viz-panel-key='panel-2'] section[data-testid='data-testid Panel header Documen...` | 1 | 1 | core | components.Panels.Panel.title |
| 226 | `div[data-viz-panel-key='panel-2579'] div[data-testid='data-testid panel content']` | 1 | 1 | core | components.Panels.Panel.content |
| 227 | `div[data-viz-panel-key='panel-3'] section[data-testid='data-testid Panel header Base Qu...` | 1 | 1 | core | components.Panels.Panel.title |
| 228 | `div[data-viz-panel-key='panel-4'] section[data-testid='data-testid Panel header 1. SQL:...` | 1 | 1 | core | components.Panels.Panel.title |
| 229 | `div[data-viz-panel-key='panel-59679'] section[data-testid='data-testid Panel header Ope...` | 1 | 1 | core | components.Panels.Panel.title |
| 230 | `div[data-viz-panel-key='panel-8'] section[data-testid='data-testid Panel header Gauge w...` | 1 | 1 | core | components.Panels.Panel.title |
| 231 | `input[aria-label="Save dashboard title field"]` | 1 | 1 | core | pages.SaveDashboardAsModal.newName; components.Drawer.DashboardSaveDrawer.saveAsTitleInput |
| 232 | `input[data-testid="data-testid Select a data source"]` | 1 | 1 | core | components.DataSourcePicker.inputV2 |
| 233 | `input[data-testid='data-testid Dashboard template variables Variable Value DropDown val...` | 1 | 1 | library | pages.Dashboard.SubMenu.submenuItemValueDropDownValueLinkTexts (emitted by @grafana/scenes) |
| 234 | `input[data-testid='data-testid Dashboard template variables Variable Value DropDown val...` | 1 | 1 | library | pages.Dashboard.SubMenu.submenuItemValueDropDownValueLinkTexts (emitted by @grafana/scenes) |
| 235 | `input[data-testid='data-testid alert-rule name-folder-name-field']` | 1 | 1 | core | components.AlertRules.newFolderNameField |
| 236 | `input[data-testid='data-testid alert-rule new-evaluation-group-name']` | 1 | 1 | core | components.AlertRules.newEvaluationGroupName |
| 237 | `input[data-testid='data-testid tab title input']` | 1 | 1 | core | components.PanelEditor.ElementEditPane.TabsLayout.titleInput |
| 238 | `section[data-testid*="data-testid Panel header"]:first-of-type` | 1 | 1 | core | components.Panels.Panel.title |
| 239 | `section[data-testid='data-testid Panel header ']` | 1 | 1 | core | components.Panels.Panel.title |
| 240 | `section[data-testid='data-testid Panel header '] div:nth-match(19)` | 1 | 1 | core | components.Panels.Panel.title |
| 241 | `section[data-testid='data-testid Panel header '] div:nth-match(29)` | 1 | 1 | core | components.Panels.Panel.title |
| 242 | `section[data-testid='data-testid Panel header 1. SQL: Basic SELECT * (Passthrough)'] di...` | 1 | 1 | core | components.Panels.Panel.title; components.Panels.Panel.content |
| 243 | `section[data-testid='data-testid Panel header Active Traitors']` | 1 | 1 | core | components.Panels.Panel.title |
| 244 | `section[data-testid='data-testid Panel header Alignment: usage/requests (p95)'] > div[d...` | 1 | 1 | core | components.Panels.Panel.title; components.Panels.Panel.content |
| 245 | `section[data-testid='data-testid Panel header Average latency']` | 1 | 1 | core | components.Panels.Panel.title |
| 246 | `section[data-testid='data-testid Panel header CPU throttling']` | 1 | 1 | core | components.Panels.Panel.title |
| 247 | `section[data-testid='data-testid Panel header Color Changes per Hour']` | 1 | 1 | core | components.Panels.Panel.title |
| 248 | `section[data-testid='data-testid Panel header Color Changes per Hour'] svg[data-testid=...` | 1 | 1 | core | components.Panels.Panel.title |
| 249 | `section[data-testid='data-testid Panel header Combined Time']` | 1 | 1 | core | components.Panels.Panel.title |
| 250 | `section[data-testid='data-testid Panel header Container restart history'] > div[data-te...` | 1 | 1 | core | components.Panels.Panel.title; components.Panels.Panel.content |
| 251 | `section[data-testid='data-testid Panel header Container restarts'] > div[data-testid='d...` | 1 | 1 | core | components.Panels.Panel.title; components.Panels.Panel.content |
| 252 | `section[data-testid='data-testid Panel header Current Color']` | 1 | 1 | core | components.Panels.Panel.title |
| 253 | `section[data-testid='data-testid Panel header Current Color'] svg[data-testid='icon-ell...` | 1 | 1 | core | components.Panels.Panel.title |
| 254 | `section[data-testid='data-testid Panel header Customer Purchasing Process (traffic, rev...` | 1 | 1 | core | components.Panels.Panel.title; components.Panels.Panel.content |
| 255 | `section[data-testid='data-testid Panel header End Game Round 2']` | 1 | 1 | core | components.Panels.Panel.title |
| 256 | `section[data-testid='data-testid Panel header England']` | 1 | 1 | core | components.Panels.Panel.title |
| 257 | `section[data-testid='data-testid Panel header Entries and Exits by Region']` | 1 | 1 | core | components.Panels.Panel.title |
| 258 | `section[data-testid='data-testid Panel header Finishers by 5 Minute Period'] svg[data-t...` | 1 | 1 | core | components.Panels.Panel.title |
| 259 | `section[data-testid='data-testid Panel header Frontend Response Latency'] div:nth-match(7)` | 1 | 1 | core | components.Panels.Panel.title |
| 260 | `section[data-testid='data-testid Panel header GeoJSON Feed Example'] svg[data-testid='i...` | 1 | 1 | core | components.Panels.Panel.title |
| 261 | `section[data-testid='data-testid Panel header Histogram by duration']` | 1 | 1 | core | components.Panels.Panel.title |
| 262 | `section[data-testid='data-testid Panel header Largest Recent']` | 1 | 1 | core | components.Panels.Panel.title |
| 263 | `section[data-testid='data-testid Panel header Last 100 Changes']` | 1 | 1 | core | components.Panels.Panel.title |
| 264 | `section[data-testid='data-testid Panel header Last 100 Changes'] svg[data-testid='icon-...` | 1 | 1 | core | components.Panels.Panel.title |
| 265 | `section[data-testid='data-testid Panel header Last 100 by Color']` | 1 | 1 | core | components.Panels.Panel.title |
| 266 | `section[data-testid='data-testid Panel header Last Color Change']` | 1 | 1 | core | components.Panels.Panel.title |
| 267 | `section[data-testid='data-testid Panel header Last terminated reason'] > div[data-testi...` | 1 | 1 | core | components.Panels.Panel.title; components.Panels.Panel.content |
| 268 | `section[data-testid='data-testid Panel header Latest Episode'] svg[data-testid='icon-el...` | 1 | 1 | core | components.Panels.Panel.title |
| 269 | `section[data-testid='data-testid Panel header Main Origin/Destination']:nth-match(1)` | 1 | 1 | core | components.Panels.Panel.title |
| 270 | `section[data-testid='data-testid Panel header Main Origin/Destination']:nth-match(2) sv...` | 1 | 1 | core | components.Panels.Panel.title |
| 271 | `section[data-testid='data-testid Panel header Mean Time']` | 1 | 1 | core | components.Panels.Panel.title |
| 272 | `section[data-testid='data-testid Panel header Most Recent']` | 1 | 1 | core | components.Panels.Panel.title |
| 273 | `section[data-testid='data-testid Panel header Most Votes Received (Grey = inactive play...` | 1 | 1 | core | components.Panels.Panel.title |
| 274 | `section[data-testid='data-testid Panel header Most Votes Received (Grey = inactive play...` | 1 | 1 | core | components.Panels.Panel.title |
| 275 | `section[data-testid='data-testid Panel header Number of Recent Earthquakes by Magnitude...` | 1 | 1 | core | components.Panels.Panel.title |
| 276 | `section[data-testid='data-testid Panel header Orders: Amount and Count, by First Name']...` | 1 | 1 | core | components.Panels.Panel.title; components.Panels.Panel.content |
| 277 | `section[data-testid='data-testid Panel header Orders: Amount, by First Name'] button[da...` | 1 | 1 | core | components.Panels.Panel.title; components.Panels.Panel.menu |
| 278 | `section[data-testid='data-testid Panel header Orders: Amount, by First Name'] div[data-...` | 1 | 1 | core | components.Panels.Panel.title |
| 279 | `section[data-testid='data-testid Panel header Player Status by Episode (Fiona was hidde...` | 1 | 1 | core | components.Panels.Panel.title |
| 280 | `section[data-testid='data-testid Panel header Prize Awarded (max £120k)']` | 1 | 1 | core | components.Panels.Panel.title |
| 281 | `section[data-testid='data-testid Panel header Reachability']` | 1 | 1 | core | components.Panels.Panel.title |
| 282 | `section[data-testid='data-testid Panel header Recent Earthquakes']` | 1 | 1 | core | components.Panels.Panel.title |
| 283 | `section[data-testid='data-testid Panel header Recent Earthquakes'] svg[data-testid='ico...` | 1 | 1 | core | components.Panels.Panel.title |
| 284 | `section[data-testid='data-testid Panel header Renewables by Region']` | 1 | 1 | core | components.Panels.Panel.title |
| 285 | `section[data-testid='data-testid Panel header Request Volume']` | 1 | 1 | core | components.Panels.Panel.title |
| 286 | `section[data-testid='data-testid Panel header Results'] svg[data-testid='icon-ellipsis-v']` | 1 | 1 | core | components.Panels.Panel.title |
| 287 | `section[data-testid='data-testid Panel header Scheduling: Containers with Memory reques...` | 1 | 1 | core | components.Panels.Panel.title; components.Panels.Panel.content |
| 288 | `section[data-testid='data-testid Panel header Stations with highest percentage of full ...` | 1 | 1 | core | components.Panels.Panel.title |
| 289 | `section[data-testid='data-testid Panel header Stations with highest percentage of seaso...` | 1 | 1 | core | components.Panels.Panel.title |
| 290 | `section[data-testid='data-testid Panel header Stations with highest percentage of seaso...` | 1 | 1 | core | components.Panels.Panel.title |
| 291 | `section[data-testid='data-testid Panel header Uptime']` | 1 | 1 | core | components.Panels.Panel.title |
| 292 | `section[data-testid='data-testid Panel header Volcanic Alert Status']` | 1 | 1 | core | components.Panels.Panel.title |
| 293 | `section[data-testid='data-testid Panel header Volcano Alert Summary']` | 1 | 1 | core | components.Panels.Panel.title |
| 294 | `section[data-testid='data-testid Panel header Winners!']` | 1 | 1 | core | components.Panels.Panel.title |
| 295 | `section[data-testid='data-testid Panel header Winning Time']` | 1 | 1 | core | components.Panels.Panel.title |

## Priority 1: data-testid

_data-testid / data-cy attributes not defined in @grafana/e2e-selectors_ — 202 unique selectors, 360 occurrences.

| # | Selector | Uses | Guides | Source | Where |
|---|---|---|---|---|---|
| 1 | `input[data-testid='search-input-input']` | 9 | 9 | external | grafana-easystart-app (Grafana Cloud Connections console) |
| 2 | `div[data-cy='wb-list-item']:has(p:contains('frontend'))` | 7 | 3 | external | RCA workbench demo app |
| 3 | `input[data-testid='checkEditor form job']` | 7 | 7 | external | grafana-synthetic-monitoring-app |
| 4 | `a[data-testid='action create check']` | 6 | 6 | external | grafana-synthetic-monitoring-app |
| 5 | `a[data-testid='view-dashboards-button']` | 6 | 6 | external | grafana-easystart-app |
| 6 | `button[data-testid='agent-config-button']` | 6 | 6 | external | grafana-collector-app |
| 7 | `button[data-testid='checkEditor form submit']` | 6 | 6 | external | grafana-synthetic-monitoring-app |
| 8 | `button[data-testid='checkEditor navigation execution']` | 6 | 6 | external | grafana-synthetic-monitoring-app |
| 9 | `div[data-cy='wb-list-item']:has(p:contains('FeatureFlagStateChange'))` | 6 | 3 | external | RCA workbench demo app |
| 10 | `div[data-cy='wb-list-item']:has(p:contains('failure'))` | 6 | 3 | external | RCA workbench demo app |
| 11 | `div[data-cy='wb-list-item']:has(p:contains('productcatalog-postgres'))` | 5 | 3 | external | RCA workbench demo app |
| 12 | `div[data-cy='wb-list-item']:has(p:contains('productcatalogservice'))` | 5 | 3 | external | RCA workbench demo app |
| 13 | `[data-testid='install-button']` | 4 | 4 | external | grafana-easystart-app |
| 14 | `[data-testid='walk-next-button']` | 4 | 1 | external | grafana-pathfinder-app |
| 15 | `button[data-testid='checkEditor feat-adhoc-check testButton']` | 4 | 4 | external | grafana-synthetic-monitoring-app |
| 16 | `button[data-testid='checkEditor navigation alerting']` | 4 | 4 | external | grafana-synthetic-monitoring-app |
| 17 | `button[data-testid='checkEditor navigation labels']` | 4 | 4 | external | grafana-synthetic-monitoring-app |
| 18 | `button[data-testid='checkEditor navigation uptime']` | 4 | 4 | external | grafana-synthetic-monitoring-app |
| 19 | `button[data-testid='test-connection-button']` | 4 | 4 | external | grafana-easystart-app |
| 20 | `div[data-cy='wb-list-item']:has(p:contains('flagd'))` | 4 | 3 | external | RCA workbench demo app |
| 21 | `div[data-testid='collector-arch-selection'] input` | 4 | 4 | external | grafana-collector-app (Fleet Management) |
| 22 | `input[data-testid='checkEditor alerts ProbeFailedExecutionsTooHigh selectedCheckbox']` | 4 | 4 | external | grafana-synthetic-monitoring-app |
| 23 | `label[data-testid='checkEditor form probeLabel']:first-of-type` | 4 | 4 | external | grafana-synthetic-monitoring-app |
| 24 | `[data-testid='checkEditor form'] > div:last-child > div:last-child  button[type='button']` | 3 | 1 | external | grafana-synthetic-monitoring-app |
| 25 | `button[data-testid='install-button']` | 3 | 3 | external | grafana-easystart-app |
| 26 | `div[data-cy='entity-list-item']:has(p:contains('frontendproxy'))` | 3 | 3 | external | RCA workbench demo app |
| 27 | `div[data-cy='wb-list-item']:has(p:contains('FeatureFlagStateChange')) button:nth-of-typ...` | 3 | 3 | external | RCA workbench demo app |
| 28 | `div[data-cy='wb-list-item']:has(p:contains('PostgreSQLHighConnections'))` | 3 | 3 | external | RCA workbench demo app |
| 29 | `div[data-cy='wb-list-item']:has(p:contains('amend'))` | 3 | 3 | external | RCA workbench demo app |
| 30 | `div[data-cy='wb-list-item']:has(p:contains('anomaly'))` | 3 | 3 | external | RCA workbench demo app |
| 31 | `div[data-cy='wb-list-item']:has(p:contains('frontend')) button:nth-of-type(3)` | 3 | 3 | external | RCA workbench demo app |
| 32 | `div[data-cy='wb-list-item']:has(p[data-original='KubePodCrashLooping'])` | 3 | 3 | external | RCA workbench demo app |
| 33 | `div[data-cy='wb-list-item']:has(p[data-original='outbound - grpc.oteldemo.ProductCatalo...` | 3 | 3 | external | RCA workbench demo app |
| 34 | `div[data-testid='alloy-simple-block']+button` | 3 | 3 | external | grafana-easystart-app |
| 35 | `div[data-testid='collector-os-selection'] input` | 3 | 3 | external | grafana-collector-app |
| 36 | `div[data-testid='infinity-query-row-wrapper-query-options']` | 3 | 3 | external | yesoreyeram-infinity-datasource |
| 37 | `div[role='dialog'] div[data-cy='entity-list-item']:has(p:contains('frontend-client'))` | 3 | 3 | external | packages/grafana-ui/src/components/Modal/ModalBase.tsx:72; RCA workbench demo app |
| 38 | `div[role='dialog'] div[data-cy='entity-list-item']:has(p:contains('frontend-client')) b...` | 3 | 3 | external | packages/grafana-ui/src/components/Modal/ModalBase.tsx:72; RCA workbench demo app |
| 39 | `section[data-testid*="Panel header Logs"]` | 3 | 3 | core | components.Panels.Panel.title |
| 40 | `[data-testid="tab-fleet-inventory"]` | 2 | 2 | external | grafana-collector-app |
| 41 | `[data-testid='agent-config-button']` | 2 | 2 | external | grafana-collector-app |
| 42 | `[data-testid='checkEditor genericLabelContent']` | 2 | 2 | external | grafana-synthetic-monitoring-app |
| 43 | `[data-testid='entity-drawer-apps-tab-serviceOverview']` | 2 | 1 | external | grafana-asserts-app |
| 44 | `[data-testid='entity-drawer-logs-tab']` | 2 | 1 | external | grafana-asserts-app |
| 45 | `[data-testid='entity-drawer-overview-tab']` | 2 | 1 | external | grafana-asserts-app |
| 46 | `[data-testid='entity-drawer-traces-tab']` | 2 | 1 | external | grafana-k8s-app |
| 47 | `[data-testid='query-editor-rows']` | 2 | 2 | core | public/app/features/query/components/QueryEditorRows.tsx:257 |
| 48 | `[data-testid='test-connection-button']` | 2 | 2 | external | grafana-easystart-app |
| 49 | `[data-testid='view-dashboards-button']` | 2 | 2 | external | grafana-easystart-app |
| 50 | `[role='button']:has([data-testid='icon-plus-circle'])` | 2 | 2 | external | packages/grafana-ui/src/components/Icon/Icon.tsx:122; mixed (grafana-pathfinder-app; grafana-cube-datasource; instance content; core PageCar |
| 51 | `a[data-testid='data-testid tab-logs']` | 2 | 2 | external | grafana-lokiexplore-app |
| 52 | `button[data-testid='app-init init-button']` | 2 | 2 | external | external plugin |
| 53 | `button[data-testid='wizard-next-button']` | 2 | 1 | core | public/app/features/alerting/unified/components/import-to-gma/Wizard/NextButton.tsx:67 |
| 54 | `div[data-cy='wb-list-item']:has(p:contains('checkoutservice')):nth-match(1)` | 2 | 2 | external | RCA workbench demo app |
| 55 | `div[data-cy='wb-list-item']:has(p:contains('checkoutservice')):nth-match(1) button:nth-...` | 2 | 2 | external | RCA workbench demo app |
| 56 | `div[data-cy='wb-list-item']:has(p:contains('frontend')):nth-match(1)` | 2 | 1 | external | RCA workbench demo app |
| 57 | `div[data-cy='wb-list-item']:has(p:contains('productcatalog-postgres')):nth-match(1)` | 2 | 2 | external | RCA workbench demo app |
| 58 | `div[data-cy='wb-list-item']:has(p:contains('productcatalog-postgres')):nth-match(1) but...` | 2 | 2 | external | RCA workbench demo app |
| 59 | `div[data-cy='wb-list-item']:has(p:contains('productcatalogservice')):nth-match(1)` | 2 | 2 | external | RCA workbench demo app |
| 60 | `div[data-cy='wb-list-item']:has(p:contains('productcatalogservice')):nth-match(1) butto...` | 2 | 2 | external | RCA workbench demo app |
| 61 | `div[data-testid="input-wrapper"] input[placeholder="Select Schedule"]` | 2 | 2 | external | packages/grafana-ui/src/components/Input/Input.tsx:97; grafana-irm-app |
| 62 | `div[data-testid="query-editor-row"] > :first-child` | 2 | 2 | core | components.QueryEditorRows.rows |
| 63 | `div[data-testid="schedule-rotations"] button:first-of-type` | 2 | 2 | external | grafana-irm-app |
| 64 | `div[data-testid='graphviz-panel-rendered'] div[data-testid='graphviz-panel-rendered-svg']` | 2 | 1 | external | external plugin; graphviz panel plugin (exact plugin id uncertain) |
| 65 | `div[data-testid='infinity-query-field-wrapper-rows/root'] textarea` | 2 | 2 | external | yesoreyeram-infinity-datasource |
| 66 | `div[data-testid='uplot-main-div']:nth-match(6)` | 2 | 2 | core | components.Panels.Visualization.Graph.container |
| 67 | `input[data-testid='checkEditor form instance']` | 2 | 2 | external | grafana-synthetic-monitoring-app |
| 68 | `label:has([data-testid='catalog-type-Service-radio'])` | 2 | 1 | external | grafana-asserts-app |
| 69 | `section[data-testid*='Alignment: Container Usage/Requests']` | 2 | 2 | core | components.Panels.Panel.title |
| 70 | `[aria-labelledby='form-section-alerting'] [data-testid='checkEditor formTabs content']` | 1 | 1 | external | grafana-synthetic-monitoring-app |
| 71 | `[data-testid="agent-config-button"]` | 1 | 1 | external | grafana-collector-app |
| 72 | `[data-testid="api-access-page"] > h3 + br + br + p + div` | 1 | 1 | external | external plugin |
| 73 | `[data-testid="api-access-page"] > h3 + br + p + div` | 1 | 1 | external | external plugin |
| 74 | `[data-testid="contact-point-picker"]` | 1 | 1 | core | public/app/features/alerting/unified/components/rule-editor/alert-rule-form/simplifiedRouting/contactPoint/ContactPointSelector.tsx:51 |
| 75 | `[data-testid="escalation-chain-select"]` | 1 | 1 | external | grafana-irm-app |
| 76 | `[data-testid="fleet-inventory-filter-button"]` | 1 | 1 | external | grafana-collector-app |
| 77 | `[data-testid="integration-url"]:nth-match(1) a` | 1 | 1 | external | grafana-irm-app |
| 78 | `[data-testid="label-browser-button"]` | 1 | 1 | external | loki datasource frontend (@grafana/loki, decoupled from grafana/grafana) |
| 79 | `[data-testid="project-listing-layout-table"] a:nth-match(1)` | 1 | 1 | external | k6-app |
| 80 | `[data-testid="routing-options-contact-point"]` | 1 | 1 | core | public/app/features/alerting/unified/components/rule-editor/NotificationsStep.tsx:189 |
| 81 | `[data-testid="tab-api-access"]` | 1 | 1 | external | external plugin |
| 82 | `[data-testid='action create check']` | 1 | 1 | external | grafana-synthetic-monitoring-app |
| 83 | `[data-testid='add-labels-button']` | 1 | 1 | core | public/app/features/alerting/unified/components/rule-editor/labels/LabelsFieldInForm.tsx:74 |
| 84 | `[data-testid='assertions-graph-tab']` | 1 | 1 | external | grafana-asserts-app |
| 85 | `[data-testid='assertions-mindmap-tab']` | 1 | 1 | external | grafana-asserts-app |
| 86 | `[data-testid='assertions-summary-tab']` | 1 | 1 | external | grafana-asserts-app |
| 87 | `[data-testid='catalog-entity-name-btn']:nth-match(1)` | 1 | 1 | external | grafana-asserts-app |
| 88 | `[data-testid='checkEditor form'] > div:last-child button[type='button']` | 1 | 1 | external | grafana-synthetic-monitoring-app |
| 89 | `[data-testid='contact-point-picker']` | 1 | 1 | core | public/app/features/alerting/unified/components/rule-editor/alert-rule-form/simplifiedRouting/contactPoint/ContactPointSelector.tsx:51 |
| 90 | `[data-testid='empty-assertions-top-services-link']` | 1 | 1 | external | grafana-asserts-app |
| 91 | `[data-testid='entity-drawer-kpis-tab']` | 1 | 1 | external | grafana-asserts-app |
| 92 | `[data-testid='folder-picker']` | 1 | 1 | core | public/app/features/alerting/unified/components/rule-editor/FolderSelector.tsx:45 |
| 93 | `[data-testid='frequency-component'] [role='radiogroup'] label:contains('1m')` | 1 | 1 | external | grafana-synthetic-monitoring-app; packages/grafana-ui/src/components/Forms/RadioButtonGroup/RadioButtonGroup.tsx:95 |
| 94 | `[data-testid='group-picker']` | 1 | 1 | core | public/app/features/alerting/unified/components/rule-editor/GroupAndNamespaceFields.tsx:80 |
| 95 | `[data-testid='home-install-alloy-button']` | 1 | 1 | external | grafana-collector-app |
| 96 | `[data-testid='infinity-query-field-label-method']` | 1 | 1 | external | yesoreyeram-infinity-datasource |
| 97 | `[data-testid='infinity-query-field-label-type']` | 1 | 1 | external | grafana-infinity-datasource |
| 98 | `[data-testid='infinity-query-url-input']` | 1 | 1 | external | yesoreyeram-infinity-datasource |
| 99 | `[data-testid='influxdb-v2-config-product-select']` | 1 | 1 | core | public/app/plugins/datasource/influxdb/components/editor/config-v2/UrlAndAuthenticationSection.tsx:253 |
| 100 | `[data-testid='influxdb-v2-config-query-language-select']` | 1 | 1 | core | public/app/plugins/datasource/influxdb/components/editor/config-v2/UrlAndAuthenticationSection.tsx:272 |
| 101 | `[data-testid='influxdb-v2-config-url-input']` | 1 | 1 | core | public/app/plugins/datasource/influxdb/components/editor/config-v2/UrlAndAuthenticationSection.tsx:216 |
| 102 | `[data-testid='insight-type-filter']:nth-match(1)` | 1 | 1 | external | k6-app |
| 103 | `[data-testid='insight-type-filter']:nth-match(6)` | 1 | 1 | external | k6-app |
| 104 | `[data-testid='insights-circle']` | 1 | 1 | external | external plugin |
| 105 | `[data-testid='query-type-ratio']` | 1 | 1 | external | grafana-slo-app |
| 106 | `[data-testid='run-queries-btn']` | 1 | 1 | external | external plugin |
| 107 | `[data-testid='save-rule']` | 1 | 1 | core | public/app/features/alerting/unified/components/rule-editor/alert-rule-form/AlertRuleForm.tsx:353 |
| 108 | `[data-testid='search-input-input']` | 1 | 1 | external | grafana-easystart-app (Grafana Cloud Connections console) |
| 109 | `[data-testid='stream-selector-input']` | 1 | 1 | external | grafana-lokiexplore-app |
| 110 | `[data-testid='success-metric-field'] textarea.inputarea.monaco-mouse-cursor-text` | 1 | 1 | external | grafana-slo-app |
| 111 | `[data-testid='tab-fleet-inventory']` | 1 | 1 | external | grafana-collector-app |
| 112 | `[data-testid='timepoint-viewer']` | 1 | 1 | external | grafana-synthetic-monitoring-app |
| 113 | `[data-testid='total-metric-field'] textarea.inputarea.monaco-mouse-cursor-text` | 1 | 1 | external | grafana-slo-app |
| 114 | `[data-testid='walk-save-button']` | 1 | 1 | external | grafana-slo-app |
| 115 | `[role='dialog'] section[data-testid*='Panel header']:nth-match(1)` | 1 | 1 | core | components.Panels.Panel.title; packages/grafana-ui/src/components/Modal/ModalBase.tsx:72 |
| 116 | `a:has([data-testid='datasource-mysql-card'])` | 1 | 1 | external | grafana-easystart-app |
| 117 | `a[data-testid="data-testid button-select-service"]:first-of-type` | 1 | 1 | external | grafana-app-observability-app |
| 118 | `a[data-testid="data-testid tab-fields"]` | 1 | 1 | external | grafana-lokiexplore-app |
| 119 | `a[data-testid="data-testid tab-labels"]` | 1 | 1 | external | grafana-lokiexplore-app |
| 120 | `a[data-testid="data-testid tab-patterns"]` | 1 | 1 | external | grafana-lokiexplore-app |
| 121 | `a[data-testid='data-testid button-select-service']:first-of-type` | 1 | 1 | external | grafana-app-observability-app |
| 122 | `a[data-testid='data-testid tab-fields']` | 1 | 1 | external | grafana-lokiexplore-app |
| 123 | `a[data-testid='data-testid tab-labels']` | 1 | 1 | external | grafana-lokiexplore-app |
| 124 | `a[data-testid='data-testid tab-patterns']` | 1 | 1 | external | grafana-lokiexplore-app |
| 125 | `a[data-testid='walk-next-button']` | 1 | 1 | external | grafana-pathfinder-app |
| 126 | `button[data-testid*='Panel menu Log volume']` | 1 | 1 | core | components.Panels.Panel.menu |
| 127 | `button[data-testid="save-rule"]` | 1 | 1 | core | public/app/features/alerting/unified/components/rule-editor/alert-rule-form/AlertRuleForm.tsx:353 |
| 128 | `button[data-testid='assertions-timeline-tab']` | 1 | 1 | external | grafana-asserts-app |
| 129 | `button[data-testid='config-submit']` | 1 | 1 | external | grafana-pathfinder-app |
| 130 | `button[data-testid='docs-panel-tab-devtools']` | 1 | 1 | external | grafana-pathfinder-app |
| 131 | `button[data-testid='fleet-inventory-add-collector-button']` | 1 | 1 | external | grafana-collector-app (Fleet Management) |
| 132 | `button[data-testid='generate-token-submit-button']` | 1 | 1 | external | grafana-collector-app |
| 133 | `button[data-testid='infinity-query-row-collapse-show-parsing-options-&-result-fields']` | 1 | 1 | external | yesoreyeram-infinity-datasource |
| 134 | `button[data-testid='infinity-query-row-collapse-show-parsing-options-&-result-fields'] svg` | 1 | 1 | external | yesoreyeram-infinity-datasource |
| 135 | `button[data-testid='install-quickpizza']` | 1 | 1 | external | k6-app |
| 136 | `button[data-testid='remote-config-delete-pipeline-application_o11y_linux'] svg[data-tes...` | 1 | 1 | external | grafana-collector-app; packages/grafana-ui/src/components/Icon/Icon.tsx:122 |
| 137 | `button[data-testid='run-queries-btn']` | 1 | 1 | external | external plugin |
| 138 | `button[data-testid='select-action-asserts:resource:threshold']` | 1 | 1 | external | grafana-asserts-app |
| 139 | `button[data-testid='tab-fleet-inventory']` | 1 | 1 | external | grafana-collector-app |
| 140 | `div[data-cy='wb-list-item']:has(p:contains('checkoutservice'))` | 1 | 1 | external | RCA workbench demo app |
| 141 | `div[data-cy='wb-list-item']:has(p:contains('checkoutservice')) button:nth-of-type(4)` | 1 | 1 | external | RCA workbench demo app |
| 142 | `div[data-cy='wb-list-item']:has(p:contains('frontend')):nth-match(1) [data-testid='asse...` | 1 | 1 | external | grafana-asserts-app; RCA workbench demo app |
| 143 | `div[data-cy='wb-list-item']:has(p:contains('productcatalog-postgres')) button:nth-of-ty...` | 1 | 1 | external | RCA workbench demo app |
| 144 | `div[data-cy='wb-list-item']:has(p:contains('productcatalogservice')) button:nth-of-type(4)` | 1 | 1 | external | RCA workbench demo app |
| 145 | `div[data-testid="QueryEditorModeToggle"] label[for^="option-code-radiogroup"]` | 1 | 1 | core+library | components.DataSource.Prometheus.queryEditor.editorToggle (emitted by @grafana/plugin-ui); packages/grafana-ui/src/components/Forms/RadioBut |
| 146 | `div[data-testid="data-source-card"]:has(small:contains("Prometheus")) button:nth-match(1)` | 1 | 1 | core | components.DataSourcePicker.dataSourceCard |
| 147 | `div[data-testid="metrics-list"] div[data-testid="with-usage-data-preview-panel"]:first-...` | 1 | 1 | external | grafana-metricsdrilldown-app |
| 148 | `div[data-testid="metrics-list"] div[data-testid="with-usage-data-preview-panel"]:first-...` | 1 | 1 | external | grafana-metricsdrilldown-app |
| 149 | `div[data-testid="uplot-main-div"]:first-of-type` | 1 | 1 | core | components.Panels.Visualization.Graph.container |
| 150 | `div[data-testid='QueryEditorModeToggle'] label:contains('Code')` | 1 | 1 | library | components.DataSource.Prometheus.queryEditor.editorToggle (emitted by @grafana/plugin-ui) |
| 151 | `div[data-testid='alloy-advanced-integrations-block']+button` | 1 | 1 | external | grafana-collector-app |
| 152 | `div[data-testid='check-group-card-browser'] a:nth-match(1)` | 1 | 1 | external | grafana-synthetic-monitoring-app |
| 153 | `div[data-testid='check-group-card-scripted'] a:nth-match(1)` | 1 | 1 | external | grafana-synthetic-monitoring-app |
| 154 | `div[data-testid='collector-arch-selection']` | 1 | 1 | external | grafana-collector-app (Fleet Management) |
| 155 | `div[data-testid='collector-installation-method'] input` | 1 | 1 | external | grafana-collector-app (Fleet Management) |
| 156 | `div[data-testid='collector-os-selection']` | 1 | 1 | external | grafana-collector-app |
| 157 | `div[data-testid='contact-point-picker'] div[data-testid='input-wrapper']` | 1 | 1 | core | public/app/features/alerting/unified/components/rule-editor/alert-rule-form/simplifiedRouting/contactPoint/ContactPointSelector.tsx:51; pack |
| 158 | `div[data-testid='escalation-chain-select']` | 1 | 1 | external | grafana-irm-app |
| 159 | `div[data-testid='filter-field'] div:nth-match(5)` | 1 | 1 | external | grafana-adaptive-metrics-app |
| 160 | `div[data-testid='fleet-management-page'] button[data-testid='tab-remote-configuration']` | 1 | 1 | external | grafana-collector-app |
| 161 | `div[data-testid='groups-container']` | 1 | 1 | core | public/app/features/alerting/unified/triage/Workbench.tsx:243 |
| 162 | `div[data-testid='input-wrapper'] #data-source-picker` | 1 | 1 | core | packages/grafana-ui/src/components/Input/Input.tsx:97; packages/grafana-runtime/src/components/DataSourcePicker.tsx:157 |
| 163 | `div[data-testid='input-wrapper'] input:nth-match(1)` | 1 | 1 | core | packages/grafana-ui/src/components/Input/Input.tsx:97 |
| 164 | `div[data-testid='input-wrapper'] input[data-testid='checkEditor form instance']` | 1 | 1 | external | packages/grafana-ui/src/components/Input/Input.tsx:97; grafana-synthetic-monitoring-app |
| 165 | `div[data-testid='input-wrapper'] input[placeholder="Field config thresholds"]:nth-match(1)` | 1 | 1 | external | packages/grafana-ui/src/components/Input/Input.tsx:97; graphviz panel plugin (not in core; Play 'graphviz-panel-showcase') |
| 166 | `div[data-testid='input-wrapper'] input[placeholder="Field config thresholds"]:nth-match(2)` | 1 | 1 | external | packages/grafana-ui/src/components/Input/Input.tsx:97; graphviz panel plugin (not in core; Play 'graphviz-panel-showcase') |
| 167 | `div[data-testid='input-wrapper'] input[placeholder="Field config thresholds"]:nth-match(3)` | 1 | 1 | external | packages/grafana-ui/src/components/Input/Input.tsx:97; graphviz panel plugin (not in core; Play 'graphviz-panel-showcase') |
| 168 | `div[data-testid='input-wrapper'] input[placeholder='Search Grafana plugins']` | 1 | 1 | core | packages/grafana-ui/src/components/Input/Input.tsx:97; public/app/features/plugins/admin/components/SearchField.tsx:49 |
| 169 | `div[data-testid='input-wrapper']:nth-match(5)` | 1 | 1 | core | packages/grafana-ui/src/components/Input/Input.tsx:97 |
| 170 | `div[data-testid='input-wrapper']:nth-match(6)` | 1 | 1 | core | packages/grafana-ui/src/components/Input/Input.tsx:97 |
| 171 | `div[data-testid='input-wrapper']:nth-match(7)` | 1 | 1 | core | packages/grafana-ui/src/components/Input/Input.tsx:97 |
| 172 | `div[data-testid='manage-actions'] button:text('Delete')` | 1 | 1 | core | public/app/features/browse-dashboards/components/BrowseActions/BrowseActions.tsx:143 |
| 173 | `div[data-testid='plugin-list'] a[href='/plugins/grafana-assistant-app']` | 1 | 1 | core | public/app/features/plugins/admin/components/PluginList.tsx:35; public/app/features/plugins/admin/components/PluginListItem.tsx:35 |
| 174 | `div[data-testid='recommendation-type']` | 1 | 1 | external | grafana-adaptive-metrics-app |
| 175 | `div[data-testid='remote-configuration-page'] button[data-testid='remote-configuration-c...` | 1 | 1 | external | grafana-collector-app |
| 176 | `div[data-testid='remote-configuration-page'] span:nth-match(3)` | 1 | 1 | external | grafana-collector-app |
| 177 | `div[data-testid='timepoint-list']` | 1 | 1 | external | grafana-synthetic-monitoring-app |
| 178 | `div[data-testid='uplot-main-div']:nth-match(5)` | 1 | 1 | core | components.Panels.Visualization.Graph.container |
| 179 | `div[data-testid^="collector-row-"]:nth-match(1)` | 1 | 1 | external | grafana-collector-app (Fleet Management) |
| 180 | `div[data-viz-panel-key='panel-2579'] > button[data-testid='panel-menu-button']` | 1 | 1 | core | packages/grafana-ui/src/components/PanelChrome/PanelMenu.tsx:30 |
| 181 | `fieldset[data-testid='data-testid prometheus type'] label:contains('Instant')` | 1 | 1 | external | grafana-prometheus-datasource (@grafana/prometheus) |
| 182 | `form[data-testid='checkEditor form']` | 1 | 1 | external | grafana-synthetic-monitoring-app |
| 183 | `form[data-testid='checkEditor form'] button[data-testid='checkEditor form submit']` | 1 | 1 | external | grafana-synthetic-monitoring-app |
| 184 | `form[data-testid='checkEditor form'] div[data-testid='timeout']` | 1 | 1 | external | grafana-synthetic-monitoring-app |
| 185 | `form[data-testid='checkEditor form'] label:nth-match(47)` | 1 | 1 | external | grafana-synthetic-monitoring-app |
| 186 | `form[data-testid='checkEditor form'] label:nth-match(5)` | 1 | 1 | external | grafana-synthetic-monitoring-app |
| 187 | `input[data-testid*='Dashboard template variables Variable Value DropDown value link text']` | 1 | 1 | core | pages.Dashboard.SubMenu.submenuItemValueDropDownValueLinkTexts |
| 188 | `input[data-testid="search-query-input"]` | 1 | 1 | core | public/app/features/alerting/unified/components/rules/Filter/RulesFilter.v1.tsx:307 |
| 189 | `input[data-testid='checkEditor form validStatusCodes']` | 1 | 1 | external | grafana-synthetic-monitoring-app |
| 190 | `input[data-testid='data-testid search-services-input']` | 1 | 1 | external | grafana-app-observability-app |
| 191 | `input[data-testid='generate-token-name-input']` | 1 | 1 | external | grafana-collector-app |
| 192 | `input[data-testid='pattern-filter']` | 1 | 1 | external | grafana-lokiexplore-app |
| 193 | `input[data-testid='slo-name-input']` | 1 | 1 | external | grafana-slo-app |
| 194 | `input[data-testid='target-input']` | 1 | 1 | external | grafana-synthetic-monitoring-app |
| 195 | `input[data-testid='time-window-input']` | 1 | 1 | external | grafana-slo-app |
| 196 | `label:has([data-testid='catalog-type-Node-radio'])` | 1 | 1 | external | grafana-asserts-app |
| 197 | `label[data-testid*="Data source"]` | 1 | 1 | library | pages.Dashboard.SubMenu.submenuItemLabels('Data source') (emitted by @grafana/scenes) |
| 198 | `label[data-testid*='Data source']` | 1 | 1 | library | pages.Dashboard.SubMenu.submenuItemLabels('Data source') (emitted by @grafana/scenes) |
| 199 | `section[data-testid='config-content'] button:nth-match(2)` | 1 | 1 | external | grafana-synthetic-monitoring-app |
| 200 | `textarea[data-testid='slo-description-input']` | 1 | 1 | external | grafana-slo-app |
| 201 | `tr:has([data-testid^="collector-row-"]) td:nth-child(2) [data-testid^="collector-row-"]...` | 1 | 1 | external | grafana-collector-app (Fleet Management) |
| 202 | `tr:has([data-testid^="collector-row-"]) td:nth-child(3) [aria-label="Healthy"], tr:has(...` | 1 | 1 | external | grafana-collector-app (Fleet Management); grafana-collector-app |

## Priority 2: Semantic attributes

_href, aria-*, id, role, name, placeholder_ — 199 unique selectors, 262 occurrences.

| # | Selector | Uses | Guides | Source | Where |
|---|---|---|---|---|---|
| 1 | `[id='pageContent'] a[href='/a/grafana-synthetic-monitoring-app/home']` | 5 | 5 | external | public/app/core/components/AppChrome/AppChrome.tsx:196; grafana-synthetic-monitoring-app |
| 2 | `a[href='/a/grafana-synthetic-monitoring-app/checks/new/api-endpoint']` | 5 | 5 | external | grafana-synthetic-monitoring-app |
| 3 | `a[href='/connections/datasources']` | 4 | 4 | core | pkg/services/navtree/navtreeimpl/navtree.go:588-591 |
| 4 | `a[href='/dashboard/new']` | 4 | 4 | core | public/app/features/browse-dashboards/components/CreateNewButton.tsx:114 |
| 5 | `button[aria-label*='section: Observability']` | 4 | 4 | core | public/app/core/components/AppChrome/MegaMenu/MegaMenuItem.tsx:242-245 |
| 6 | `div[aria-label='Generated SQL query']` | 4 | 1 | external | grafana-cube-datasource |
| 7 | `input[id^='option-60000-radiogroup-']` | 4 | 4 | core | packages/grafana-ui/src/components/Forms/RadioButtonGroup/RadioButton.tsx:59 |
| 8 | `#pageContent button:text('New')` | 3 | 3 | core | public/app/core/components/AppChrome/AppChrome.tsx:196 |
| 9 | `[aria-label='Query editor owner']` | 3 | 3 | external | grafana-github-datasource |
| 10 | `[aria-label='Query editor repository']` | 3 | 3 | external | grafana-github-datasource |
| 11 | `[role="dialog"] button:contains('Save')` | 3 | 1 | core | packages/grafana-ui/src/components/Modal/ModalBase.tsx:72 |
| 12 | `button[aria-label='Workbench AI (Preview)']` | 3 | 3 | external | RCA workbench app (demo) |
| 13 | `input[placeholder='Filter by name or type']` | 3 | 3 | core | public/app/features/datasources/components/NewDataSource.tsx:70 |
| 14 | `#collector-status-filter` | 2 | 2 | external | grafana-collector-app (Fleet Management) |
| 15 | `#dev-mode` | 2 | 2 | external | grafana-pathfinder-app |
| 16 | `#secret-description` | 2 | 1 | external | k6-app |
| 17 | `#secret-name` | 2 | 1 | external | grafana-synthetic-monitoring-app |
| 18 | `#secret-value` | 2 | 1 | external | external plugin |
| 19 | `[aria-label="timeout seconds input"]` | 2 | 2 | external | grafana-synthetic-monitoring-app |
| 20 | `[aria-label='Search connections by name']` | 2 | 2 | external | grafana-easystart-app |
| 21 | `[role='menuitem']:contains('Add to dashboard')` | 2 | 2 | core | packages/grafana-ui/src/components/Menu/MenuItem.tsx:204 |
| 22 | `[role='menuitem']:text('Stroke Color')` | 2 | 1 | core | packages/grafana-ui/src/components/Menu/MenuItem.tsx:204 |
| 23 | `a[href="/a/grafana-metricsdrilldown-app/drilldown"]` | 2 | 2 | external | grafana-metricsdrilldown-app |
| 24 | `a[href='/alerting/notifications']` | 2 | 2 | core | public/app/features/alerting/routes.tsx:159 |
| 25 | `a[href='/connections/add-new-connection/haproxy']` | 2 | 2 | external | grafana-easystart-app |
| 26 | `a[href='/connections/add-new-connection/hmInstancePromId']` | 2 | 2 | core | public/app/features/connections/tabs/ConnectData/hooks/usePluginFiltering.ts:62 |
| 27 | `button[aria-label*='section: Database']` | 2 | 2 | core | public/app/core/components/AppChrome/MegaMenu/MegaMenuItem.tsx:242 |
| 28 | `button[aria-label='Run query']` | 2 | 2 | core | packages/grafana-ui/src/components/RefreshPicker/RefreshPicker.tsx:120 |
| 29 | `button[aria-label='Wrap lines']` | 2 | 2 | core | public/app/features/logs/components/panel/LogListControls.tsx:698 |
| 30 | `div[role="grid"] div[role="row"][aria-rowindex="2"] div.cell-link` | 2 | 2 | core | packages/grafana-ui/src/components/Table/TableNG/refactored/TableFlat.tsx:304; components.DataLinksContextMenu.singleLink |
| 31 | `div[role="menu"] button[role="menuitem"]:has(span:contains("Time"))` | 2 | 2 | core | packages/grafana-ui/src/components/Menu/Menu.tsx:49; packages/grafana-ui/src/components/Menu/MenuItem.tsx:204 |
| 32 | `div[role='dialog'] div[role='group'] div:contains('Frontend')` | 2 | 2 | external | packages/grafana-ui/src/components/Modal/ModalBase.tsx:72; grafana-asserts-app |
| 33 | `div[role='dialog'] div[role='group'] div:contains('Service')` | 2 | 2 | external | packages/grafana-ui/src/components/Modal/ModalBase.tsx:72; grafana-asserts-app |
| 34 | `input[id='name']` | 2 | 1 | core | public/app/features/alerting/unified/components/receivers/form/ReceiverForm.tsx:168; public/app/features/alerting/unified/components/rule-ed |
| 35 | `input[name='target'][placeholder='grafana.com']` | 2 | 2 | external | grafana-synthetic-monitoring-app |
| 36 | `input[placeholder="Filter by label values"]` | 2 | 1 | library | @grafana/scenes |
| 37 | `input[placeholder='name']` | 2 | 2 | external | grafana-synthetic-monitoring-app |
| 38 | `input[placeholder='value']` | 2 | 2 | external | grafana-synthetic-monitoring-app |
| 39 | `input[type='text']` | 2 | 1 | core | public/app/features/plugins/admin/components/SearchField.tsx |
| 40 | `label[aria-label='Table view']` | 2 | 1 | core | public/app/features/dashboard-scene/panel-edit/PanelEditControls.tsx:25 |
| 41 | `td.title a[href="/a/grafana-irm-app/incidents/1"]:contains("Day in the Life Demo")` | 2 | 2 | external | grafana-irm-app |
| 42 | `#appID` | 1 | 1 | core | public/app/features/provisioning/components/Shared/GitHubConnectionFields.tsx:104 |
| 43 | `#auth-method-select` | 1 | 1 | library | @grafana/plugin-ui |
| 44 | `#connection-url` | 1 | 1 | library | @grafana/plugin-ui |
| 45 | `#dashboard-title` | 1 | 1 | core | public/app/features/provisioning/components/Dashboards/SaveProvisionedDashboardForm.tsx:467 |
| 46 | `#eval-for-input` | 1 | 1 | core | public/app/features/alerting/unified/components/rule-editor/GrafanaEvaluationBehavior.tsx:711 |
| 47 | `#floating-boundary>div:nth-child(5) button:text('Save')` | 1 | 1 | core | packages/grafana-ui/src/utils/floating.ts:3 |
| 48 | `#gauge-segmentCount` | 1 | 1 | core | public/app/plugins/panel/gauge/module.tsx:93 |
| 49 | `#generate-alerts` | 1 | 1 | external | grafana-slo-app |
| 50 | `#installationID` | 1 | 1 | core | public/app/features/provisioning/components/Shared/GitHubConnectionFields.tsx:125 |
| 51 | `#mega-menu-toggle` | 1 | 1 | core | public/app/core/constants.ts:20 |
| 52 | `#pageContent [role='button']:text('grafana_play_cube')` | 1 | 1 | external | mixed (grafana-pathfinder-app; grafana-cube-datasource; instance content; core PageCard); public/app/core/components/AppChrome/AppChrome.tsx |
| 53 | `#pageContent a[href='/alerting/list']` | 1 | 1 | core | public/app/features/alerting/routes.tsx:33; public/app/core/components/AppChrome/AppChrome.tsx:196 |
| 54 | `#pageContent button:contains('Files')` | 1 | 1 | core | public/app/core/components/AppChrome/AppChrome.tsx:196 |
| 55 | `#pageContent button:contains('New')` | 1 | 1 | core | public/app/core/components/AppChrome/AppChrome.tsx:196 |
| 56 | `#pageContent input[role='combobox']` | 1 | 1 | core | packages/grafana-ui/src/components/Combobox/Combobox.tsx:291; public/app/core/components/AppChrome/AppChrome.tsx:196 |
| 57 | `#privateKey` | 1 | 1 | core | public/app/features/provisioning/components/Shared/GitHubConnectionFields.tsx:155 |
| 58 | `#repository-title` | 1 | 1 | core | public/app/features/provisioning/Wizard/BootstrapStep.tsx:224 |
| 59 | `#title` | 1 | 1 | core | public/app/features/dashboard-scene/settings/links/DashboardLinkForm.tsx:73 |
| 60 | `[aria-label="Expand section: Adaptive Telemetry"]` | 1 | 1 | core | public/app/core/components/AppChrome/MegaMenu/MegaMenuItem.tsx:245 |
| 61 | `[aria-label="Private data source connect"]` | 1 | 1 | core | public/app/core/utils/navBarItem-translations.ts:201 |
| 62 | `[aria-label="Query to send 1"]` | 1 | 1 | external | grafana-synthetic-monitoring-app |
| 63 | `[aria-label="Response to expect 1"]` | 1 | 1 | external | grafana-synthetic-monitoring-app |
| 64 | `[aria-label="Search collectors"]` | 1 | 1 | external | grafana-collector-app |
| 65 | `[aria-label="Search connections by name"]` | 1 | 1 | external | grafana-easystart-app |
| 66 | `[aria-label='Private data source connect']` | 1 | 1 | core | public/app/core/utils/navBarItem-translations.ts:201 |
| 67 | `[name="target"]` | 1 | 1 | external | grafana-synthetic-monitoring-app |
| 68 | `[name='target']` | 1 | 1 | external | grafana-synthetic-monitoring-app |
| 69 | `[placeholder='Filter by name or type']` | 1 | 1 | core | public/app/features/datasources/components/NewDataSource.tsx:70 |
| 70 | `[role="dialog"] button:text('Delete')` | 1 | 1 | core | packages/grafana-ui/src/components/Modal/ModalBase.tsx:72 |
| 71 | `[role='button']:contains('TerminalDisconnected')` | 1 | 1 | external | mixed (grafana-pathfinder-app; grafana-cube-datasource; instance content; core PageCard) |
| 72 | `[role='dialog'] [role='radiogroup']` | 1 | 1 | core | packages/grafana-ui/src/components/Modal/ModalBase.tsx:72; packages/grafana-ui/src/components/Forms/RadioButtonGroup/RadioButtonGroup.tsx:95 |
| 73 | `[role='dialog'] button[aria-label='Toggle notification details']:nth-match(1)` | 1 | 1 | core | packages/grafana-ui/src/components/Modal/ModalBase.tsx:72; public/app/features/alerting/unified/triage/instance-details/InstanceTimeline.tsx |
| 74 | `[role='menuitem']:contains('Import to Grafana Alerting')` | 1 | 1 | core | packages/grafana-ui/src/components/Menu/MenuItem.tsx:204 |
| 75 | `[role='menuitem']:contains('New dashboard')` | 1 | 1 | core | packages/grafana-ui/src/components/Menu/MenuItem.tsx:204 |
| 76 | `[role='menuitem']:contains('Save as copy')` | 1 | 1 | core | packages/grafana-ui/src/components/Menu/MenuItem.tsx:204 |
| 77 | `[role='menuitem']:contains('Use Template')` | 1 | 1 | core | packages/grafana-ui/src/components/Menu/MenuItem.tsx:204 |
| 78 | `[role='menuitem']:text('Fill Color')` | 1 | 1 | core | packages/grafana-ui/src/components/Menu/MenuItem.tsx:204 |
| 79 | `[role='menuitem']:text('From suggestions')` | 1 | 1 | core | packages/grafana-ui/src/components/Menu/MenuItem.tsx:204 |
| 80 | `[role='menuitem']:text('New dashboard')` | 1 | 1 | core | packages/grafana-ui/src/components/Menu/MenuItem.tsx:204 |
| 81 | `[role='menuitem']:text('Use template')` | 1 | 1 | core | packages/grafana-ui/src/components/Menu/MenuItem.tsx:204 |
| 82 | `[role='menuitemradio'][aria-label='5 seconds']` | 1 | 1 | core | packages/grafana-ui/src/components/Dropdown/ButtonSelect.tsx:48; packages/grafana-ui/src/components/RefreshPicker/RefreshPicker.tsx:203 |
| 83 | `a[aria-label='Select detected_level']` | 1 | 1 | external | grafana-lokiexplore-app |
| 84 | `a[aria-label='add contact point']` | 1 | 1 | core | public/app/features/alerting/unified/components/contact-points/ContactPoints.tsx:114 |
| 85 | `a[href*="/d/000000016/time-series-graphs"]` | 1 | 1 | external | instance-content (provisioned dashboard/demo data) |
| 86 | `a[href*="/d/T512JVH7z/loki-nginx-service-mesh-json-version"]` | 1 | 1 | core |  |
| 87 | `a[href*="/d/c9ea65f5-ed5a-45cf-8fb7-f82af7c3afdf/canvas-visualization"]` | 1 | 1 | external | instance-content (provisioned dashboard/demo data) |
| 88 | `a[href*="/d/cdl34qv4zzg8wa/flame-graphs"]` | 1 | 1 | core |  |
| 89 | `a[href*="/d/ddkar8yanj56oa/visualizing-google-sheets-data"]` | 1 | 1 | core |  |
| 90 | `a[href*="/d/infinity/2dc7103"]` | 1 | 1 | core | dashboard search/list link (data-driven) |
| 91 | `a[href*="/d/ma79mqp/visualization-examples"]` | 1 | 1 | external | instance-content (provisioned dashboard/demo data) |
| 92 | `a[href*="/d/mabjzp6/grafana-arcade"]` | 1 | 1 | core | public/app/features/browse-dashboards/components/NameCell.tsx:104 |
| 93 | `a[href*="/d/mamnq22/data-source-examples"]` | 1 | 1 | external | grafana-demodashboards-app |
| 94 | `a[href*="/d/panel-geomap/geomap-examples"]` | 1 | 1 | external | instance-content (provisioned dashboard/demo data) |
| 95 | `a[href*="a/grafana-app-observability-app"]` | 1 | 1 | external | grafana-app-observability-app |
| 96 | `a[href*="a/grafana-k8s-app"]` | 1 | 1 | external | grafana-k8s-app |
| 97 | `a[href*='adaptive-logs']` | 1 | 1 | external | grafana-adaptivelogs-app |
| 98 | `a[href*='adaptive-metrics']` | 1 | 1 | external | grafana-adaptive-metrics-app |
| 99 | `a[href*='billingusage']` | 1 | 1 | external | external plugin |
| 100 | `a[href="/a/grafana-adaptive-metrics-app/overview"]` | 1 | 1 | core | components.NavMenu.item |
| 101 | `a[href="/a/grafana-adaptive-metrics-app/rule-management"]` | 1 | 1 | external | grafana-adaptive-metrics-app |
| 102 | `a[href="/a/grafana-slo-app/wizard/alerts"]` | 1 | 1 | external | grafana-slo-app |
| 103 | `a[href="/a/grafana-slo-app/wizard/new"]` | 1 | 1 | core | public/app/features/gops/configuration-tracker/irmHooks.ts:240 |
| 104 | `a[href="/a/grafana-slo-app/wizard/review"]` | 1 | 1 | external | grafana-slo-app |
| 105 | `a[href="/alerting/new/alerting"]` | 1 | 1 | core | public/app/features/alerting/unified/rule-list/RuleList.v2.tsx:151 |
| 106 | `a[href="/connections/add-new-connection/windows-exporter"]` | 1 | 1 | core | public/app/features/connections/tabs/ConnectData/CardGrid/CardGrid.tsx:91 |
| 107 | `a[href="/dashboard/new"]` | 1 | 1 | core | public/app/features/browse-dashboards/components/CreateNewButton.tsx:114 |
| 108 | `a[href='/admin/provisioning/connect/github']` | 1 | 1 | core | public/app/features/provisioning/Shared/RepositoryTypeCards.tsx:37 |
| 109 | `a[href='/admin/provisioning/repository-4301603']` | 1 | 1 | core | public/app/features/provisioning/Repository/RepositoryListItem.tsx:108 |
| 110 | `a[href='/connections/add-new-connection/kafka']` | 1 | 1 | core | public/app/features/connections/tabs/ConnectData/CardGrid/CardGrid.tsx:91 |
| 111 | `a[href='/connections/add-new-connection/linux-node']` | 1 | 1 | core | public/app/features/connections/tabs/ConnectData/CardGrid/CardGrid.tsx:91 |
| 112 | `a[href='/connections/add-new-connection/macos-node']` | 1 | 1 | core | public/app/features/connections/tabs/ConnectData/CardGrid/CardGrid.tsx:91 |
| 113 | `a[href='/connections/add-new-connection/microsoft-iis']` | 1 | 1 | external | grafana-easystart-app (Cloud connections catalog) |
| 114 | `a[href='/connections/add-new-connection/mongodb']` | 1 | 1 | core | public/app/features/connections/tabs/ConnectData/CardGrid/CardGrid.tsx:91 |
| 115 | `a[href='/connections/add-new-connection/mysql']` | 1 | 1 | core | public/app/features/connections/tabs/ConnectData/CardGrid/CardGrid.tsx:91 |
| 116 | `a[href='/connections/add-new-connection/postgres']` | 1 | 1 | core | public/app/features/connections/tabs/ConnectData/CardGrid/CardGrid.tsx:91 |
| 117 | `a[href='/connections/datasources/volkovlabs-rss-datasource']` | 1 | 1 | core | public/app/features/connections/tabs/ConnectData/hooks/usePluginFiltering.ts:64 |
| 118 | `a[href='/d/a581fb5a-df38-45d7-83cb-d10835930fa1/performance-stats']` | 1 | 1 | external | instance-content (provisioned dashboard/demo data) |
| 119 | `a[href='/dashboard/recently-deleted'] + button` | 1 | 1 | core | public/app/features/browse-dashboards/components/FolderDetailsActions/FolderDetailsActions.tsx:63 |
| 120 | `a[href='/explore']` | 1 | 1 | core | components.NavMenu.item |
| 121 | `a[href='/plugins']` | 1 | 1 | core | components.NavMenu.item |
| 122 | `a[href='/plugins/grafana-github-datasource']` | 1 | 1 | core | public/app/features/plugins/admin/components/PluginListItem.tsx:35 |
| 123 | `a[href='/plugins/volkovlabs-rss-datasource']` | 1 | 1 | core | public/app/features/plugins/admin/components/PluginListItem.tsx:35 |
| 124 | `a[href='alerting/new/alerting']` | 1 | 1 | core | public/app/features/alerting/unified/components/rules/NoRulesCTA.tsx:77 |
| 125 | `button[aria-label="Close"]` | 1 | 1 | core | packages/grafana-ui/src/components/Modal/Modal.tsx:89 |
| 126 | `button[aria-label="Log menu"]:first-of-type` | 1 | 1 | core | public/app/features/logs/components/panel/LogLineMenu.tsx:176 |
| 127 | `button[aria-label="Run query"]` | 1 | 1 | core | packages/grafana-ui/src/components/RefreshPicker/RefreshPicker.tsx:120 |
| 128 | `button[aria-label='Close']` | 1 | 1 | core | packages/grafana-ui/src/components/Modal/Modal.tsx:89 |
| 129 | `button[aria-label='Code']` | 1 | 1 | core | public/app/features/dashboard-scene/sidebar/DashboardSidebarRenderer.tsx:118 |
| 130 | `button[aria-label='Collapse sidebar'], button[aria-label='Expand sidebar']` | 1 | 1 | core | public/app/features/alerting/unified/triage/scene/filters/LabelsColumn.tsx:88; public/app/features/alerting/unified/triage/scene/filters/Lab |
| 131 | `button[aria-label='Delete quickpizza-password']` | 1 | 1 | external | k6-app |
| 132 | `button[aria-label='Delete quickpizza-username']` | 1 | 1 | external | k6-app |
| 133 | `button[aria-label='Delete']` | 1 | 1 | external | query library module (enterprise/cloud, not in OSS) |
| 134 | `button[aria-label='Expand Repeat options category']` | 1 | 1 | core | public/app/features/dashboard/components/PanelEditor/OptionsPaneCategory.tsx:188 |
| 135 | `button[aria-label='Expand folder GrafanaCloud'] ~ div a` | 1 | 1 | core | public/app/features/browse-dashboards/components/NameCell.tsx:81 |
| 136 | `button[aria-label='Expand terminal']` | 1 | 1 | external | grafana-collector-app |
| 137 | `button[aria-label='New']` | 1 | 1 | core | public/app/core/components/AppChrome/QuickAdd/QuickAdd.tsx:136 |
| 138 | `button[aria-label='Open in sidebar']:contains('Instance details')` | 1 | 1 | core | public/app/features/alerting/unified/triage/rows/InstanceRow.tsx:112 |
| 139 | `button[aria-label='Toggle Parsing options & Result fields']` | 1 | 1 | external | yesoreyeram-infinity-datasource |
| 140 | `button[title='Menu']:nth-match(1)` | 1 | 1 | core | packages/grafana-ui/src/components/PanelChrome/PanelMenu.tsx:50 |
| 141 | `button[type='submit']` | 1 | 1 | core | public/app/features/alerting/unified/components/receivers/form/ReceiverForm.tsx:236 |
| 142 | `div:contains('ServiceHealth') > button[aria-label='Toggle group']` | 1 | 1 | core | public/app/features/alerting/unified/triage/rows/GenericRow.tsx:134 |
| 143 | `div[aria-label="Generated SQL query"]:contains('payment_method')` | 1 | 1 | external | grafana-cube-datasource |
| 144 | `div[aria-label="Plugin visualization item Table"]` | 1 | 1 | core | components.PluginVisualization.item |
| 145 | `div[id="ds"]` | 1 | 1 | library | @grafana/scenes |
| 146 | `div[role="gridcell"]:contains("Qualification")` | 1 | 1 | core | packages/grafana-ui/src/components/Table/TableNG/hooks.ts |
| 147 | `div[role="gridcell"]:contains("Qualification") button[aria-label="Filter for value"]` | 1 | 1 | core | packages/grafana-ui/src/components/Table/TableNG/hooks.ts; packages/grafana-ui/src/components/Table/TableNG/components/TableCellActions.tsx: |
| 148 | `div[role="gridcell"]:contains("R.")` | 1 | 1 | core | packages/grafana-ui/src/components/Table/TableNG/hooks.ts |
| 149 | `div[role="gridcell"]:contains("R.") button[aria-label="Filter for value"]` | 1 | 1 | core | packages/grafana-ui/src/components/Table/TableNG/hooks.ts; packages/grafana-ui/src/components/Table/TableNG/components/TableCellActions.tsx: |
| 150 | `div[role='dialog'] button[type='button']:has(div:contains('Frontend'))` | 1 | 1 | core | packages/grafana-ui/src/components/Modal/ModalBase.tsx:72 |
| 151 | `div[role='dialog'] button[type='button']:has(div:contains('Service'))` | 1 | 1 | core | packages/grafana-ui/src/components/Modal/ModalBase.tsx:72 |
| 152 | `input[aria-label="Select a data source"]` | 1 | 1 | core | components.DataSourcePicker.inputV2 (legacy value) |
| 153 | `input[aria-label='Custom labels 1 name']` | 1 | 1 | external | grafana-synthetic-monitoring-app |
| 154 | `input[aria-label='Custom labels 1 value']` | 1 | 1 | external | grafana-synthetic-monitoring-app |
| 155 | `input[aria-label='Dimensions']` | 1 | 1 | external | grafana-cube-datasource |
| 156 | `input[aria-label='Private data source connect']` | 1 | 1 | core | public/app/core/utils/navBarItem-translations.ts:201 |
| 157 | `input[aria-label='Select']` | 1 | 1 | core | public/app/features/browse-dashboards/components/CheckboxCell.tsx:90 |
| 158 | `input[aria-label='layout-selection-option-Auto']` | 1 | 1 | core | public/app/features/dashboard-scene/scene/layouts-shared/DashboardLayoutSelector.tsx:89 |
| 159 | `input[aria-label='layout-selection-option-Tabs']` | 1 | 1 | core | public/app/features/dashboard-scene/scene/layouts-shared/DashboardLayoutSelector.tsx:89 |
| 160 | `input[id='basic-settings-name']` | 1 | 1 | core | pages.DataSource.name |
| 161 | `input[id='contact-point-type-items.0.']` | 1 | 1 | core | public/app/features/alerting/unified/components/receivers/form/ChannelSubForm.tsx:241 |
| 162 | `input[id='eval-for-input']` | 1 | 1 | core | public/app/features/alerting/unified/components/rule-editor/GrafanaEvaluationBehavior.tsx:711 |
| 163 | `input[name="name"]` | 1 | 1 | external | grafana-slo-app |
| 164 | `input[name="objective"]` | 1 | 1 | external | grafana-slo-app |
| 165 | `input[name="timeWindow"]` | 1 | 1 | external | grafana-slo-app |
| 166 | `input[name='host']` | 1 | 1 | core | public/app/plugins/datasource/mysql/configuration/ConfigurationEditor.tsx:80 |
| 167 | `input[name='seriesCount']` | 1 | 1 | core | public/app/plugins/datasource/grafana-testdata-datasource/components/RandomWalkEditor.tsx:16 |
| 168 | `input[placeholder="Metric name"]` | 1 | 1 | external | grafana-adaptive-metrics-app |
| 169 | `input[placeholder=',']` | 1 | 1 | external | yesoreyeram-infinity-datasource |
| 170 | `input[placeholder='All groups']` | 1 | 1 | core | public/app/features/alerting/unified/components/import-to-gma/steps/Step2AlertRules.tsx:354 |
| 171 | `input[placeholder='All namespaces']` | 1 | 1 | core | public/app/features/alerting/unified/components/import-to-gma/steps/Step2AlertRules.tsx:328 |
| 172 | `input[placeholder='Filter by label values']` | 1 | 1 | library | @grafana/scenes |
| 173 | `input[placeholder='Give your alert rule a name']` | 1 | 1 | core | public/app/features/alerting/unified/components/rule-editor/AlertRuleNameInput.tsx:78 |
| 174 | `input[placeholder='Name']` | 1 | 1 | core | public/app/core/components/Page/EditableTitle.tsx:115 |
| 175 | `input[placeholder='Password']` | 1 | 1 | core | public/app/plugins/datasource/mysql/configuration/ConfigurationEditor.tsx:116 |
| 176 | `input[placeholder='Personal Access Token']` | 1 | 1 | external | grafana-github-datasource |
| 177 | `input[placeholder='Search Grafana plugins']` | 1 | 1 | core | public/app/features/plugins/admin/components/SearchField.tsx:49 |
| 178 | `input[placeholder='Search by name or type']` | 1 | 1 | core | public/app/core/components/PageActionBar/PageActionBar.tsx:33 |
| 179 | `input[placeholder='Search entity']` | 1 | 1 | external | grafana-asserts-app |
| 180 | `input[placeholder='Search for...']` | 1 | 1 | core | public/app/features/dashboard-scene/panel-edit/PanelVizTypePicker.tsx:164 |
| 181 | `input[placeholder='Select a policy tree']` | 1 | 1 | core | public/app/features/alerting/unified/components/import-to-gma/steps/Step2AlertRules.tsx:233 |
| 182 | `input[placeholder='Username']` | 1 | 1 | core | public/app/plugins/datasource/mysql/configuration/ConfigurationEditor.tsx:108 |
| 183 | `input[placeholder='https://feed']` | 1 | 1 | external | volkovlabs-rss-datasource |
| 184 | `input[placeholder='https://github.com/owner/repository']` | 1 | 1 | core | public/app/features/provisioning/Wizard/fields.ts:118 |
| 185 | `input[role='combobox']` | 1 | 1 | core | packages/grafana-ui/src/components/Combobox/Combobox.tsx:291 |
| 186 | `input[type='number']` | 1 | 1 | core | packages/grafana-ui/src/components/Input/Input.tsx:176 |
| 187 | `input[value='New dashboard']` | 1 | 1 | core | public/app/features/dashboard-scene/serialization/buildNewDashboardSaveModel.ts |
| 188 | `label[aria-label='Center glow']` | 1 | 1 | core | public/app/plugins/panel/gauge/EffectsEditor.tsx:53 |
| 189 | `label[aria-label^='Show early detection patterns']` | 1 | 1 | external | grafana-adaptivelogs-app |
| 190 | `label[for*='traceqlSearch']` | 1 | 1 | external | tempo (Tempo datasource plugin, decoupled from core) |
| 191 | `label[for='enable-coda-terminal']` | 1 | 1 | external | grafana-pathfinder-app |
| 192 | `label[for^='option-ping-radiogroup-']` | 1 | 1 | external | grafana-synthetic-monitoring-app |
| 193 | `label[for^='option-traceql-']` | 1 | 1 | core | packages/grafana-ui/src/components/Forms/RadioButtonGroup/RadioButton.tsx:72 |
| 194 | `label[title='Check a host for availability and response time.']` | 1 | 1 | external | grafana-synthetic-monitoring-app |
| 195 | `label[title='Import from an Alertmanager data source']` | 1 | 1 | core | public/app/features/alerting/unified/components/import-to-gma/Wizard/steps.ts:114 |
| 196 | `textarea[id='items.0.settings.addresses']` | 1 | 1 | core | public/app/features/alerting/unified/components/receivers/form/fields/OptionField.tsx:115-118 |
| 197 | `textarea[name="comment"]` | 1 | 1 | core | public/app/features/alerting/unified/components/silences/SilencesEditor.tsx:263 |
| 198 | `textarea[name="description"]` | 1 | 1 | core | public/app/features/dashboard-scene/saving/SaveDashboardAsForm.tsx:239 |
| 199 | `ul[aria-label="Navigation"] a[href="/dashboards"]` | 1 | 1 | core | public/app/core/components/AppChrome/MegaMenu/MegaMenu.tsx:103; public/app/core/components/AppChrome/MegaMenu/MegaMenuItemText.tsx:127 |

## Priority 3: :contains()/:text() text matching

_text-content matching_ — 39 unique selectors, 52 occurrences.

| # | Selector | Uses | Guides | Source | Where |
|---|---|---|---|---|---|
| 1 | `button:contains('Save')` | 3 | 1 | external | grafana-synthetic-monitoring-app |
| 2 | `button:has(span:contains('productcatalogservice'))` | 3 | 3 | external | grafana-app-observability-app |
| 3 | `div.grid.wb-item:has(p:contains('PostgreSQLHighConnections'))` | 3 | 3 | external | rca-workbench-demo-app |
| 4 | `button:text('Group into rows')` | 2 | 1 | core | public/app/features/dashboard-scene/sidebar/add-new/AddRow.tsx:38 |
| 5 | `button:text('Group into tabs')` | 2 | 1 | core | public/app/features/dashboard-scene/sidebar/add-new/AddTab.tsx:37 |
| 6 | `button:text('Next')` | 2 | 1 | external | grafana-collector-app |
| 7 | `div.text-xs:has(span:contains('Sort By'))` | 2 | 2 | external | grafana-asserts-app |
| 8 | `div:text("Notify users from on-call schedule")` | 2 | 2 | external | grafana-irm-app |
| 9 | `div:text("Notify users")` | 2 | 2 | external | grafana-irm-app |
| 10 | `div:text("Wait")` | 2 | 2 | external | grafana-irm-app |
| 11 | `button:contains("Apply all recommendations")` | 1 | 1 | external | grafana-adaptive-metrics-app |
| 12 | `button:contains("Copy to clipboard"):nth-match(2)` | 1 | 1 | core | packages/grafana-ui/src/components/ClipboardButton/ClipboardButton.tsx |
| 13 | `button:contains('Clear filters')` | 1 | 1 | core | public/app/features/alerting/unified/components/alert-groups/AlertGroupFilter.tsx:72 |
| 14 | `button:contains('Include')` | 1 | 1 | external | grafana-lokiexplore-app |
| 15 | `button:contains('More'):nth-match(1)` | 1 | 1 | core | public/app/features/alerting/unified/rule-list/RuleList.v2.tsx:158 |
| 16 | `button:has(span:contains("loki_nginx"))` | 1 | 1 | external | grafana-lokiexplore-app |
| 17 | `button:has(span:contains('Critical'))` | 1 | 1 | external | grafana-irm-app |
| 18 | `button:has(span:contains('Firing'))` | 1 | 1 | core | public/app/features/alerting/unified/components/rules/RuleListStateView.tsx:77 |
| 19 | `button:has(span:contains('Pending'))` | 1 | 1 | core | public/app/features/alerting/unified/rule-list/filter/RulesFilterSidebar.tsx:174 |
| 20 | `button:text("Acknowledge")` | 1 | 1 | external | grafana-irm-app |
| 21 | `button:text('Add variable')` | 1 | 1 | core | public/app/features/dashboard-scene/settings/variables/VariableEditorList.tsx:130 |
| 22 | `button:text('Build a dashboard'):nth-match(1)` | 1 | 1 | core | public/app/features/datasources/components/BuildDashboardButton.tsx:46 |
| 23 | `button:text('Discard')` | 1 | 1 | core | public/app/features/dashboard-scene/scene/DashboardControls.tsx:395 |
| 24 | `button:text('Save')` | 1 | 1 | external | query library module (enterprise/cloud, not in OSS) |
| 25 | `button:text('Variable')` | 1 | 1 | core | components.Sidebar.addNewVariableButton |
| 26 | `div:contains('panic')` | 1 | 1 | external | instance-content (demo log data) in grafana-asserts-app Logs tab |
| 27 | `div:text('abandon') button` | 1 | 1 | external | graphviz panel plugin (instance/demo data) |
| 28 | `div:text('abandon_checkout') button` | 1 | 1 | external | graphviz panel plugin (instance/demo data) |
| 29 | `div:text('bounce') button` | 1 | 1 | external | graphviz panel plugin (instance/demo data) |
| 30 | `label:contains('1m')` | 1 | 1 | external | grafana-synthetic-monitoring-app |
| 31 | `label:contains('All spans')` | 1 | 1 | external | grafana-exploretraces-app |
| 32 | `label:contains('Circle')` | 1 | 1 | core | public/app/plugins/panel/xychart/config.ts:128 |
| 33 | `label:contains('Code')` | 1 | 1 | core | packages/grafana-ui/src/components/Forms/RadioButtonGroup/RadioButtonGroup.tsx |
| 34 | `label:contains('Connect to a new app')` | 1 | 1 | core | public/app/features/provisioning/Wizard/GitHubAppFields.tsx:170 |
| 35 | `label:contains('Connect with GitHub App')` | 1 | 1 | core | public/app/features/provisioning/Wizard/AuthTypeStep.tsx:31 |
| 36 | `label:contains('DNS')` | 1 | 1 | external | grafana-synthetic-monitoring-app |
| 37 | `label:contains('TCP')` | 1 | 1 | external | grafana-synthetic-monitoring-app |
| 38 | `label:text('YAML')` | 1 | 1 | core | public/app/features/alerting/unified/components/export/providers.ts:24 |
| 39 | `select, div:has(label:contains('Segment'))` | 1 | 1 | core | public/app/plugins/panel/gauge/module.tsx:94 |

## Priority 4: :has() structural matching

_descendant-based structural matching_ — 1 unique selectors, 3 occurrences.

| # | Selector | Uses | Guides | Source | Where |
|---|---|---|---|---|---|
| 1 | `div.grid.wb-item:has(p[data-original='KubePodCrashLooping'])` | 3 | 3 | external | RCA workbench demo app |

## Priority 5: CSS class / tag selectors

_least stable_ — 38 unique selectors, 69 occurrences.

| # | Selector | Uses | Guides | Source | Where |
|---|---|---|---|---|---|
| 1 | `textarea.inputarea` | 7 | 3 | core | packages/grafana-ui/src/components/Monaco/CodeEditor.tsx:179 |
| 2 | `div.h-full.w-full.overflow-y-scroll.block` | 3 | 3 | external | grafana-asserts-app |
| 3 | `[data-pathfinder="add-integration-button"]` | 2 | 2 | external | grafana-irm-app |
| 4 | `[data-pathfinder="add-user-select"]` | 2 | 2 | external | grafana-pathfinder-app |
| 5 | `[data-pathfinder="create-web-schedule-button"]` | 2 | 2 | external | grafana-pathfinder-app |
| 6 | `[data-pathfinder="escalation-chain-name-input"]` | 2 | 2 | external | grafana-irm-app |
| 7 | `[data-pathfinder="escalation-chain-option-0"]` | 2 | 2 | external | grafana-irm-app |
| 8 | `[data-pathfinder="integration-grafanaalerting"]` | 2 | 2 | external | grafana-pathfinder-app |
| 9 | `[data-pathfinder="integration-name-input"]` | 2 | 2 | external | grafana-pathfinder-app |
| 10 | `[data-pathfinder="new-contact-point-input"]` | 2 | 2 | external | grafana-pathfinder-app |
| 11 | `[data-pathfinder="new-escalation-chain-button"]` | 2 | 2 | external | grafana-irm-app |
| 12 | `[data-pathfinder="new-schedule-button"]` | 2 | 2 | external | external plugin |
| 13 | `[data-pathfinder="route-heading-0"]` | 2 | 2 | external | grafana-pathfinder-app |
| 14 | `[data-pathfinder="save-escalation-chain-button"]` | 2 | 2 | external | grafana-irm-app |
| 15 | `[data-pathfinder="save-integration-button"]` | 2 | 2 | external | grafana-irm-app |
| 16 | `[data-pathfinder="save-rotation-button"]` | 2 | 2 | external | grafana-irm-app |
| 17 | `[data-pathfinder="save-schedule-button"]` | 2 | 2 | external | grafana-irm-app |
| 18 | `[data-pathfinder="schedule-name"]` | 2 | 2 | external | grafana-pathfinder-app |
| 19 | `[data-pathfinder="send-demo-alert-button"]` | 2 | 2 | external | grafana-pathfinder-app |
| 20 | `[data-pathfinder="submit-send-alert-button"]` | 2 | 2 | external | grafana-irm-app |
| 21 | `[data-pathfinder="timeline-item-1"]` | 2 | 2 | external | grafana-irm-app |
| 22 | `[data-pathfinder="timeline-item-2"]` | 2 | 2 | external | grafana-pathfinder-app |
| 23 | `[data-pathfinder="timeline-item-3"]` | 2 | 2 | external | grafana-pathfinder-app |
| 24 | `g#abandon_checkout` | 2 | 1 | external | graphviz panel plugin (instance/demo data) |
| 25 | `input:nth-of-type(1):nth-match(2)` | 2 | 1 | core | public/app/features/dashboard/components/TransformationsEditor/TransformationFilter.tsx |
| 26 | `#:r2cr:` | 1 | 1 | core | public/app/features/dashboard-scene/saving/SaveDashboardAsForm.tsx |
| 27 | `canvas.xterm-link-layer:nth-of-type(1)` | 1 | 1 | external | external plugin |
| 28 | `canvas:nth-of-type(2):nth-match(2)` | 1 | 1 | core | packages/grafana-ui/src/components/uPlot/Plot.tsx |
| 29 | `canvas:nth-of-type(2):nth-match(3)` | 1 | 1 | core | packages/grafana-ui/src/components/uPlot |
| 30 | `canvas:nth-of-type(2):nth-match(4)` | 1 | 1 | core | packages/grafana-ui/src/components/uPlot |
| 31 | `div[class*='connectionBanner']` | 1 | 1 | external | grafana-assistant-app |
| 32 | `div[data-viz-panel-key='75903a26-8a1b-4df1-b56a-daa3a11c5b8a']` | 1 | 1 | library | @grafana/scenes |
| 33 | `grafana:components.DataSourcePicker.inputV2` | 1 | 1 | core | components.DataSourcePicker.inputV2 |
| 34 | `iframe[src*="youtube.com/embed"]` | 1 | 1 | external | instance-content (provisioned dashboard/demo data) |
| 35 | `input#default-bucket` | 1 | 1 | core | public/app/plugins/datasource/influxdb/components/editor/config-v2/InfluxFluxDBConnection.tsx:83 |
| 36 | `input#organization` | 1 | 1 | core | public/app/plugins/datasource/influxdb/components/editor/config-v2/InfluxFluxDBConnection.tsx:67 |
| 37 | `input#token` | 1 | 1 | core | public/app/features/provisioning/Wizard/components/RepositoryTokenInput.tsx:51 |
| 38 | `input:nth-of-type(1):nth-match(3)` | 1 | 1 | core | public/app/features/dashboard/components/TransformationsEditor/TransformationFilter.tsx |
