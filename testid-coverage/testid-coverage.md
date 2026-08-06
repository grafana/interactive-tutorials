# data-testid coverage — provisioned plugins

Generated 2026-08-06. AST scan (TypeScript compiler API) of every non-test `.tsx` file in each
provisioned plugin's source (`PROVISIONED_PLUGINS` in react-detect-plugins/constants.ts), flagging
interactive JSX elements whose opening tag has no `data-testid`/`data-cy`/`data-pathfinder`/`testId`.

- **none** — no stable identifier at all
- **partial** — reachable via a weaker attr (`aria-label`, `id`, `inputId`, `name`)
- **spread** — props spread (`{...props}`) may or may not deliver a testid

Interactive = grafana-ui inputs/buttons/selects/menu items/tabs, native `button|a|input|select|textarea`,
or any element with `onClick`/`onSubmit`. Full per-element detail (file:line) in [`testid-coverage.json`](testid-coverage.json).

| plugin | repo | files | uncovered | none | partial | spread |
|---|---|---|---|---|---|---|
| grafana-assistant-app | grafana/grafana-assistant-app | 573 | 1173 | 845 | 294 | 34 |
| grafana-irm-app | grafana/irm | 837 | 1082 | 795 | 202 | 85 |
| grafana-sigil-app | ? | 285 | 841 | 606 | 235 | 0 |
| k6-app | ? | 687 | 617 | 443 | 128 | 46 |
| grafana-asserts-app | ? | 706 | 613 | 407 | 82 | 124 |
| grafana-kowalski-app | ? | 398 | 440 | 327 | 111 | 2 |
| grafana-pathfinder-app | ? | 164 | 429 | 368 | 60 | 1 |
| grafana-synthetic-monitoring-app | ? | 409 | 377 | 262 | 107 | 8 |
| grafana-ml-app | grafana/machine-learning | 220 | 364 | 244 | 63 | 57 |
| grafana-setupguide-app | ? | 228 | 346 | 239 | 92 | 15 |
| grafana-easystart-app | grafana/grafana-connections-app | 220 | 262 | 198 | 60 | 4 |
| grafana-collector-app | ? | 326 | 242 | 190 | 52 | 0 |
| grafana-csp-app | ? | 387 | 198 | 139 | 54 | 5 |
| grafana-slo-app | ? | 156 | 196 | 164 | 31 | 1 |
| grafana-cmab-app | ? | 480 | 193 | 145 | 46 | 2 |
| grafana-lokiexplore-app | grafana/logs-drilldown | 183 | 171 | 111 | 54 | 6 |
| grafana-adaptivelogs-app | ? | 163 | 156 | 102 | 49 | 5 |
| grafana-adaptive-metrics-app | ? | 108 | 153 | 86 | 59 | 8 |
| grafana-pyroscope-app | ? | 166 | 153 | 82 | 63 | 8 |
| grafana-k8s-app | grafana/grafana-k8s-plugin | 122 | 125 | 111 | 13 | 1 |
| grafana-agentictesting-app | ? | 72 | 106 | 57 | 48 | 1 |
| grafana-dbo11y-app | ? | 138 | 106 | 88 | 17 | 1 |
| grafana-app-observability-app | grafana/app-observability-plugin | 113 | 89 | 80 | 8 | 1 |
| grafana-servicecenter-app | ? | 76 | 89 | 59 | 29 | 1 |
| grafana-metricsdrilldown-app | ? | 93 | 75 | 48 | 27 | 0 |
| grafana-exploretraces-app | grafana/traces-drilldown | 76 | 71 | 50 | 21 | 0 |
| grafana-adaptivetraces-app | ? | 60 | 50 | 41 | 7 | 2 |
| grafana-pdc-app | ? | 50 | 50 | 37 | 13 | 0 |
| tempo | grafana/grafana-tempo-datasource | 31 | 46 | 27 | 19 | 0 |
| grafana-llm-app | grafana/grafana-llm-app | 22 | 34 | 29 | 5 | 0 |
| mssql | grafana/grafana-mssql-datasource | 5 | 31 | 19 | 12 | 0 |
| stackdriver | grafana/grafana-cloudmonitoring-datasource | 27 | 26 | 7 | 19 | 0 |
| opentsdb | grafana/grafana-opentsdb-datasource | 9 | 24 | 11 | 13 | 0 |
| clexporter-app | ? | 22 | 19 | 11 | 8 | 0 |
| grafanacloud-cardinality-management-app | ? | 7 | 15 | 9 | 6 | 0 |
| grafana-advisor-app | ? | 20 | 14 | 8 | 5 | 1 |
| grafana-logvolumeexplorer-app | ? | 25 | 9 | 8 | 0 | 1 |
| grafana-auth-app | ? | 15 | 3 | 3 | 0 | 0 |
| zipkin | grafana/grafana-zipkin-datasource | 2 | 2 | 2 | 0 | 0 |
| grafana-demodashboards-app | ? | 6 | 1 | 1 | 0 | 0 |
| **total (40 plugins)** | | | **8991** | **6459** | **2112** | **420** |

No source available: elasticsearch, grafana-labelmanagement-app, grafana-labels-app

## Top uncovered component types

| component | count |
|---|---|
| `Button` | 2150 |
| `Input` | 789 |
| `IconButton` | 659 |
| `button` | 574 |
| `a` | 473 |
| `TextLink` | 425 |
| `LinkButton` | 390 |
| `Select` | 314 |
| `div` | 301 |
| `Menu.Item` | 295 |
| `Combobox` | 232 |
| `RadioButtonGroup` | 200 |
| `Tab` | 187 |
| `Checkbox` | 176 |
| `form` | 172 |

## Hotspot files per plugin (top 5 by uncovered elements)

<details><summary><b>grafana-assistant-app</b> — 1173 uncovered</summary>

- `pages/for-developers/PlaygroundCanvas.tsx` — 25
- `components/settings/IRMWebhookForm.tsx` — 23
- `components/config/quickstarts/Quickstarts.tsx` — 22
- `pages/automations/AutomationForm.tsx` — 22
- `pages/watcher-agents/WatcherAgentDetailPage.tsx` — 19
</details>

<details><summary><b>grafana-irm-app</b> — 1082 uncovered</summary>

- `components/src/components/IrmNavigation.tsx` — 18
- `grafana-irm-app/src/pages/EscalationChains/EscalationChainModals.tsx` — 14
- `grafana-oncall-app/src/containers/OutgoingWebhookForm/OutgoingWebhookForm.tsx` — 14
- `grafana-oncall-app/src/containers/RotationForm/RotationForm.tsx` — 14
- `grafana-oncall-app/src/pages/schedule/Schedule.tsx` — 14
</details>

<details><summary><b>grafana-sigil-app</b> — 841 uncovered</summary>

- `pages/EvaluationDetailPage.tsx` — 24
- `pages/EvaluatorsPage.tsx` — 21
- `components/agents/AgentRatingPanel.tsx` — 20
- `components/evaluation/EvaluatorForm.tsx` — 19
- `components/evaluation/TemplateForm.tsx` — 19
</details>

<details><summary><b>k6-app</b> — 617 uncovered</summary>

- `components/Devtools/Devtools.tsx` — 13
- `pages/TestRunPage/components/Breakdown/Breakdown.tsx` — 12
- `pages/NewTest/components/RunTestFlow.tsx` — 11
- `pages/SettingsPage/tabs/SecretsManagementTab/SecretEditModal.tsx` — 10
- `components/ScheduledTests/ScheduledTestsModal.tsx` — 9
</details>

<details><summary><b>grafana-asserts-app</b> — 613 uncovered</summary>

- `features/Configuration/components/ConnectData/ConnectData.container.tsx` — 21
- `features/ManageAssertions/components/NotificationResource/components/NotificationResourceForm/NotificationResourceForm.component.tsx` — 16
- `features/Configuration/TelemetryMappings/LogsConfig/components/LogConfigForm.tsx` — 15
- `features/ManageAssertions/components/NotificationRequest/components/NotificationRequestForm/NotificationRequestForm.component.tsx` — 15
- `kgdatasource/components/AdvancedQueryEditor.tsx` — 15
</details>

<details><summary><b>grafana-kowalski-app</b> — 440 uncovered</summary>

- `scenes/components/funnels/JourneyDiscover.tsx` — 18
- `scenes/components/apps/alerting/components/AlertThresholdConfigModal.tsx` — 13
- `scenes/components/errors-v2/summary/suspect-commits/SuspectCommitsSection.tsx` — 12
- `scenes/components/funnels/JourneyForm.tsx` — 12
- `scenes/components/errors-v2/attribute-explorer/AttributeDistribution.tsx` — 10
</details>

<details><summary><b>grafana-pathfinder-app</b> — 429 uncovered</summary>

- `components/block-editor/forms/StepEditor.tsx` — 41
- `components/block-editor/forms/InteractiveBlockForm.tsx` — 27
- `components/block-editor/forms/BranchBlocksEditor.tsx` — 23
- `components/block-editor/forms/MarkdownBlockForm.tsx` — 21
- `components/block-editor/forms/QuizBlockForm.tsx` — 18
</details>

<details><summary><b>grafana-synthetic-monitoring-app</b> — 377 uncovered</summary>

- `page/ConfigPageLayout/tabs/SecretsManagementTab/SecretEditModal.tsx` — 11
- `components/AlertRuleForm.tsx` — 10
- `components/Checkster/components/form/FormHttpRegExpValidationField.tsx` — 7
- `components/ProbeEditor/ProbeEditor.tsx` — 7
- `page/AlertingPage.tsx` — 7
</details>

<details><summary><b>grafana-ml-app</b> — 364 uncovered</summary>

- `projects/Forecasting/InteractiveCreate/ProphetConfig.tsx` — 18
- `projects/Forecasting/Tabs/List/JobListItem.tsx` — 14
- `projects/Forecasting/Tabs/Holidays/Create/CreateUpdateHolidayContent.tsx` — 13
- `projects/Home/Home.tsx` — 12
- `projects/Forecasting/Create/CreateJobModal.tsx` — 9
</details>

<details><summary><b>grafana-setupguide-app</b> — 346 uncovered</summary>

- `components/datasources/postgres/authentication-form.tsx` — 12
- `components/datasources/prometheus/authentication-form.tsx` — 10
- `feature/overlay/modals/supabase-tour.tsx` — 10
- `components/assistant-feedback.tsx` — 9
- `components/getting-started/otel/service-form.tsx` — 9
</details>

<details><summary><b>grafana-easystart-app</b> — 262 uncovered</summary>

- `features/infinity-page/WizardPanel.tsx` — 15
- `features/catalog/CardContent/CardContent.tsx` — 9
- `pages/Source/ConfigurationDetails/Local/AgentIntegrations/Beyla/BeylaInstructions.tsx` — 8
- `features/hosted-data-integrations/OpenTelemetry/OpenTelemetryInstructions.tsx` — 7
- `features/integrations-page/IntegrationsTable.tsx` — 7
</details>

<details><summary><b>grafana-collector-app</b> — 242 uncovered</summary>

- `feature/instrumentation-hub/pages/app-monitoring/ActivateAppO11y.tsx` — 10
- `extensions/Pyroscope/components/CollectorSettings/components/EditRule/EditRule.tsx` — 8
- `feature/instrumentation-hub/pages/k8s-monitoring/ActivateK8sMonitoring.tsx` — 8
- `feature/api-access/components/PrivateConnectivityCard.tsx` — 6
- `feature/collector-setup/otel/OtelInstallationInstructions.tsx` — 6
</details>

<details><summary><b>grafana-csp-app</b> — 198 uncovered</summary>

- `feature/AWS/components/SaasIntegrations/ALBLogsInstructions/utils.tsx` — 5
- `feature/common/components/Resources/ConfigureResourcesTable/EditResourceMetrics.tsx` — 5
- `feature/common/pages/ServiceHub/ConfigureMetricsSection/SelectionList.tsx` — 5
- `feature/AWS/components/SaasIntegrations/CloudWatchLogsFirehoseInstructions/utils.tsx` — 4
- `feature/AWS/components/SaasIntegrations/CloudWatchLogsInstructions/utils.tsx` — 4
</details>

<details><summary><b>grafana-slo-app</b> — 196 uncovered</summary>

- `components/SloListItem/SloListUnifiedViewMoreMenu.tsx` — 10
- `components/AppConfig/OrgPreferences.tsx` — 8
- `components/SloEditDrawer/SloEditDrawer.tsx` — 8
- `components/SloListItem/SloListViewMoreMenu.tsx` — 8
- `components/Home/GetStarted.tsx` — 6
</details>

<details><summary><b>grafana-cmab-app</b> — 193 uncovered</summary>

- `components/DevTools/DevDrawer.tsx` — 38
- `components/UsageAlertsList/index.tsx` — 8
- `components/UsageAlertsDrawers/components/ActionBar.tsx` — 4
- `components/UsageAlertsForms/components/CustomPercentages.tsx` — 4
- `components/AlertStarterMenu/AlertStarterMenu.tsx` — 3
</details>

<details><summary><b>grafana-lokiexplore-app</b> — 171 uncovered</summary>

- `Components/AttributeDistribution/AttributeDistribution.tsx` — 10
- `Components/Header/PluginInfo.tsx` — 8
- `Components/ServiceScene/LogListControls.tsx` — 8
- `Components/SavedSearches/SaveSearchModal.tsx` — 6
- `Components/ServiceScene/Breakdowns/NumericFilterPopoverScene.tsx` — 6
</details>

<details><summary><b>grafana-adaptivelogs-app</b> — 156 uncovered</summary>

- `borrowed/segment-config/AddEditSegment/index.tsx` — 8
- `components/ArchiveDestinationConfig/ArchiveDestinationWizard/WizardNavigationButtons.tsx` — 8
- `pages/ArchivesPage/index.tsx` — 6
- `components/ArchiveRulesCreateButton/index.tsx` — 5
- `components/DropRulesForm/DropRulesForm.tsx` — 5
</details>

<details><summary><b>grafana-adaptive-metrics-app</b> — 153 uncovered</summary>

- `components/Configuration/Segments/AddEditSegment/index.tsx` — 10
- `components/Exemptions/AddEditExemption.tsx` — 10
- `components/FeedbackForm/index.tsx` — 9
- `components/Configuration/Segments/ConfigureSegment/index.tsx` — 8
- `components/Overview/AutoApplyNudge/index.tsx` — 7
</details>

<details><summary><b>grafana-pyroscope-app</b> — 153 uncovered</summary>

- `pages/ProfilesExplorerView/components/SceneExploreServiceFlameGraph/components/SceneFunctionDetailsPanel/ui/OverrideRepositoryDetailsButton.tsx` — 10
- `pages/ProfilesExplorerView/components/SceneCreateMetricModal/SceneCreateRecordingRuleModal.tsx` — 8
- `shared/ui/PluginInfo.tsx` — 8
- `pages/SettingsView/components/UISettingsView/UISettingsView.tsx` — 6
- `shared/components/SavedSearches/SaveSearchModal.tsx` — 6
</details>

<details><summary><b>grafana-k8s-app</b> — 125 uncovered</summary>

- `components/scenes/Config/ClusterConfig/ClusterFeatures.tsx` — 17
- `components/HomeScene/HomeNoData.tsx` — 9
- `components/IntegrationsList/IntegrationModal.tsx` — 5
- `components/NodesList/NodesList.tsx` — 5
- `components/workloads/WorkloadList/WorkloadTable.tsx` — 5
</details>

<details><summary><b>grafana-agentictesting-app</b> — 106 uncovered</summary>

- `components/Feedback/Creation/RunCreationFeedbackPanel.tsx` — 10
- `pages/Settings/tabs/SecretsManagement/SecretEditModal.tsx` — 10
- `components/GifPlayer/GifPlayer.tsx` — 7
- `pages/Settings/tabs/EnvironmentVariables/EnvVarEditModal.tsx` — 6
- `pages/CreateTest/components/CreateTestHeader.tsx` — 5
</details>

<details><summary><b>grafana-dbo11y-app</b> — 106 uncovered</summary>

- `features/configuration/setup/components/ConfigureDatabaseStep.tsx` — 22
- `features/overview/components/SavedViews/SavedViewsPopover.tsx` — 9
- `features/overview/components/SavedViews/SavedViewsViewRow.tsx` — 6
- `features/fleet-overview/components/InsightDrawer/RecommendationsDrawer.tsx` — 5
- `features/product-activation/ui/ActivateButton.tsx` — 5
</details>

<details><summary><b>grafana-app-observability-app</b> — 89 uncovered</summary>

- `modules/initialize/components/LearnMore.tsx` — 8
- `modules/config/tabs/LogsQueryTab.tsx` — 6
- `components/MenuControl.tsx` — 5
- `modules/config/tabs/ClientOnlyServicesConfigScene.tsx` — 4
- `modules/config/tabs/DataSourceTab.tsx` — 4
</details>

<details><summary><b>grafana-servicecenter-app</b> — 89 uncovered</summary>

- `components/List/ServiceFilter.tsx` — 6
- `components/ServicePage/LinkField.tsx` — 5
- `components/Discovery/DiscoveryPage.tsx` — 4
- `components/Discovery/DiscoveryTable/DiscoveryTable.tsx` — 4
- `components/ServicePage/AdditionalIdentifier.tsx` — 4
</details>

<details><summary><b>grafana-metricsdrilldown-app</b> — 75 uncovered</summary>

- `AppDataTrail/header/PluginInfo/PluginInfo.tsx` — 7
- `shared/savedQueries/SaveQueryModal.tsx` — 5
- `App/Onboarding.tsx` — 3
- `AppDataTrail/header/PluginHeaderToolbar.tsx` — 3
- `MetricsReducer/SideBar/sections/MetricsFilterSection/MetricsFilterSection.tsx` — 3
</details>

<details><summary><b>grafana-exploretraces-app</b> — 71 uncovered</summary>

- `components/App/header/PluginInfo.tsx` — 7
- `components/Explore/AttributesSidebar.tsx` — 7
- `components/Explore/TracesByService/Tabs/Exceptions/ExceptionsTable.tsx` — 7
- `components/Explore/seeker/TimeSeekerControls.tsx` — 7
- `components/Explore/SavedSearches/SaveSearchModal.tsx` — 6
</details>

<details><summary><b>grafana-adaptivetraces-app</b> — 50 uncovered</summary>

- `components/PolicyDrawer/CreateEditForm.tsx` — 8
- `components/Recommendations/index.tsx` — 4
- `components/Semconv/SemconvDrawer/index.tsx` — 4
- `components/Empty/PolicyRulesBox.tsx` — 3
- `components/Empty/PolicyTemplateColumn.tsx` — 3
</details>

<details><summary><b>grafana-pdc-app</b> — 50 uncovered</summary>

- `feature/private-networks/components/PrivateNetworkDetail/ConfigurationTab/ConfigurationInstructions/ConfigurationInstructionsDeploymentLimitHosts.tsx` — 5
- `feature/private-networks/components/PrivateNetworkDetail/ConfigurationTab/ConfigurationInstructions/ConfigurationInstructionsAssignDataSource.tsx` — 4
- `feature/private-networks/components/PrivateNetworkList/CreatePrivateNetworkModal.tsx` — 4
- `feature/private-networks/components/PrivateNetworkList/EditPrivateNetworkModal.tsx` — 4
- `feature/private-networks/components/PrivateNetworkList/PrivateNetworks.tsx` — 4
</details>

<details><summary><b>tempo</b> — 46 uncovered</summary>

- `traceql/TempoQueryBuilderOptions.tsx` — 6
- `SearchTraceQLEditor/SearchField.tsx` — 5
- `SearchTraceQLEditor/TraceQLSearch.tsx` — 4
- `CheatSheet.tsx` — 3
- `configuration/StreamingSection.tsx` — 3
</details>

<details><summary><b>grafana-llm-app</b> — 34 uncovered</summary>

- `components/AppConfig/LLMConfig.tsx` — 8
- `components/AppConfig/DevSandbox/DevSandbox.tsx` — 5
- `components/AppConfig/DevSandbox/DevSandboxToolInspector.tsx` — 5
- `components/AppConfig/AzureConfig.tsx` — 4
- `components/AppConfig/Vector.tsx` — 4
</details>

<details><summary><b>mssql</b> — 31 uncovered</summary>

- `configuration/ConfigurationEditor.tsx` — 12
- `azureauth/AzureCredentialsForm.tsx` — 10
- `configuration/Kerberos.tsx` — 9
</details>

<details><summary><b>stackdriver</b> — 26 uncovered</summary>

- `components/LabelFilter.tsx` — 4
- `components/AnnotationQueryEditor.tsx` — 2
- `components/ConfigEditor/ConfigEditor.tsx` — 2
- `components/PromQLEditor.tsx` — 2
- `components/VisualMetricQueryEditor.tsx` — 2
</details>

<details><summary><b>opentsdb</b> — 24 uncovered</summary>

- `components/FilterSection.tsx` — 8
- `components/TagSection.tsx` — 6
- `components/DownSample.tsx` — 3
- `components/OpenTsdbDetails.tsx` — 3
- `components/AnnotationEditor.tsx` — 2
</details>

<details><summary><b>clexporter-app</b> — 19 uncovered</summary>

- `components/LogsExportConfig/Form/index.tsx` — 7
- `components/Filters/AddEditFilterButton.tsx` — 4
- `components/CodeSnippet/index.tsx` — 1
- `components/DashboardLink/index.tsx` — 1
- `components/DocumentationLink/index.tsx` — 1
</details>

<details><summary><b>grafanacloud-cardinality-management-app</b> — 15 uncovered</summary>

- `cardinality-datasource/components/UnusedMetricsResources.tsx` — 8
- `cardinality-datasource/components/CardinalityQueryEditor.tsx` — 5
- `cardinality-datasource/components/ParameterList.tsx` — 1
- `cardinality-datasource/components/SelectorField.tsx` — 1
</details>

<details><summary><b>grafana-advisor-app</b> — 14 uncovered</summary>

- `components/Actions/Actions.tsx` — 4
- `components/CheckDrillDown/IssueDescription.tsx` — 3
- `components/CheckDrillDown/LLMSuggestionContent.tsx` — 2
- `components/NoChecksEmptyState/NoChecksEmptyState.tsx` — 2
- `components/CheckDrillDown/CheckDrillDown.tsx` — 1
</details>

<details><summary><b>grafana-logvolumeexplorer-app</b> — 9 uncovered</summary>

- `components/PluginWrapper/index.tsx` — 3
- `components/LogVolume/ActionBar.tsx` — 2
- `components/LogVolume/LabelSelect.tsx` — 1
- `components/LogVolume/LabelValueSelect.tsx` — 1
- `components/LogVolume/Labels.tsx` — 1
</details>

<details><summary><b>grafana-auth-app</b> — 3 uncovered</summary>

- `feature/data-source/components/DataSourcesWarning.tsx` — 1
- `feature/data-source/components/NewTokenDataSource.tsx` — 1
- `feature/data-source/components/TokenDataSource.tsx` — 1
</details>

<details><summary><b>zipkin</b> — 2 uncovered</summary>

- `QueryField.tsx` — 2
</details>

<details><summary><b>grafana-demodashboards-app</b> — 1 uncovered</summary>

- `pages/RootPage.tsx` — 1
</details>
