# Selector repair disposition — 22 September 2026

This batch repairs 17 public guides. Source checks and local validation are not proof of deployed behavior or a complete live walkthrough. Preview, synthetic, and unattributed signals remain separate from named public-guide traffic.

## Changes and remaining work

| Plan family | Disposition |
| --- | --- |
| Synthetic Monitoring secrets | Direct Secrets navigation and page/permission guards. Automate non-secret form actions, pause for user-entered credential values, then save and require the named saved secret before continuing. Existing secrets can bypass creation. Restricted users need an administrator. |
| Synthetic Monitoring labels and hidden controls | Create the label row before filling its registered name/value controls; preserve existing rows and stop at the label limit. Visible labels replace hidden inputs, with target-state handling for alert toggles. |
| Saved queries | User chooses the starting panel/query and an unused saved-query name. Automate the save dialog, persistence confirmation, exact-name lookup, replacement and addition. Editor controls gate both existing and new dashboard routes. |
| First dashboard | Direct plugin/connection navigation, current datasource picker and save controls, datasource health prerequisite and dashboard save verification. Business News remains the guide's datasource; replacing the deprecated plugin is separate work. |
| Hidden targets and hover | Instrumented and Code choices target visible labels. Snapshot menus retain genuine CSS hover; finding an unmounted panel header has an automatic standalone action. Bundled first-dashboard-cloud belongs to Pathfinder. |
| Navigation | Direct routes replace hidden menu chains in Secrets, SM overview, first-dashboard setup, IRM and k6 entry. No general mobile-menu engine change is claimed. |
| Frontend Observability | Keep ordinary observations as standalone Show me actions, with automatic lazy discovery in the verified main scrolling container. Search remains optional. No added requirement to manually hover or scroll through observations. |
| Embedded selector tokens | Retained valid tokens after resolver/source inspection. Historical preview failures require the exact serving revision before attributing a current engine defect. |
| Transform/Fleet ambiguity | Scope Fleet status to collector rows and known status labels, with standalone automatic discovery. Current transform-data already lacks the reported legacy targets; verify its serving revision before closing those signals. |
| Private/unattributed targets | No speculative replacements. Backend/draft guide owners must identify Standing state, Run now and network breadcrumb sources. Pathfinder diagnostics need private-safe attribution. |
| Synthetic-only coverage | Repair IRM route/rotation targeting and snapshot page/header/expiration controls. Remaining Prometheus prerequisites and datasource auto-completion signals require fixture ownership in Pathfinder. |

## Guided user input

User-entered values and choices use guided interactions where the app exposes a verified control. The surrounding actions stay automatic. A reusable saved-query name is collected once in a guide input so later selectors and form fills can use it.

| Guide | Remaining human action |
| --- | --- |
| how-to-setup-secrets-tutorial | Guided credential entry, optional updates and named-secret deletion confirmation. Creation fields and saving are automated; the guide never supplies credential values. |
| saved-queries-panel-edit | Choose the existing dashboard/panel/query and provide an unused name once. Subsequent dialog actions use that name automatically. |
| dashboard-snapshot-guide | Real pointer hover for the panel menu/submenu; choose a snapshot name and any optional snapshot to delete. Discovery of the initial header is automatic. |
| irm-configuration | Choose actual on-call users, schedule/escalation details and integration configuration in the existing guided workflow. These cannot be inferred safely from this selector repair. |
| k6-script-authoring-assistant-lj/generate-from-prompt | Guided prompt entry and explicit Send, followed by draft review and the user’s project choice. Known Assistant mode navigation is automated. |
| knowledge-graph-explore-service-relationships / grafana-quickpizza-working-filters | Existing user-paced relationship and query-inspector walkthroughs retain reading pauses; the modal can trap focus. Automatic navigation/discovery is used outside those walkthroughs. |
| Synthetic Monitoring check guides | Choose instance-specific probes and optional thresholds where the lesson leaves them to the user. Known navigation, label fields and alert controls need no prose-only workaround. |

Reading query-inspector results and relationship context remains user-paced teaching content. It is not a requirement to manually find a missing element. Existing data, permissions and optional instrumentation are prerequisites; automation cannot manufacture them.

## Corrected runtime findings

Rechecked against Pathfinder `origin/main` **339cd31d95c636b82b66f27e3496eb1f49aa0fa4**:

- Standalone `interactive` blocks **do support automatic lazy discovery**, including inside sections. `convertInteractiveBlock` forwards the flags, `lazyScrollAvailable` keeps the individual controls usable, and both Show me and Do it call `executeWithLazyScroll`. The earlier guided-only recommendation was incorrect; authoring guidance is corrected in this PR.
- Guided actions scroll existing targets into view, but their parser drops lazy-scroll fields and their handler cannot discover unmounted targets. It also does not evaluate internal step requirements. This is not a reason to turn an ordinary automated action into a manual guided action.
- **Do section** bypasses standalone lazy discovery and drops individual `doIt: false` intent. For lazy targets use their individual Show me / Do it controls. Secrets use a guided credential-entry pause, which stops bulk execution before a value is requested; the guided handler listens for user input without writing it.
- Lazy discovery searches forward in the specified scrolling container; it does not change pagination pages, handle every nested scroller, or guarantee finding an unmounted target above the current position. `#pageContent` is verified for Grafana's main content with the extension sidebar open.

The remaining engine work is therefore guided discovery/requirements and consistent bulk-section behavior. No changes to the Synthetic Monitoring, Frontend Observability, Fleet or IRM applications are established as necessary for these selector repairs.

## Evidence and validation boundaries

Source inspection covers Grafana controls and runtime handlers, Synthetic Monitoring Checkster and secret forms, enterprise Saved queries, Business News, IRM, Frontend Observability and Fleet.

Connected Chrome checks on learn confirmed the installed Business News connection and Add new data source control. In an unsaved Ping form, clicking Label created Custom labels 1 name/value. **This is current Checkster behavior, not proof of an older UI:** the source contains both Checkster and the other NameValueInput implementation. The original label failure is consistent with targeting a registered row before it exists. No datasource, check or secret was saved in those checks.

All changed guides are checked with the local Pathfinder package validator and strict content validation, with independent diff/source review, block ID/reference checks and diff checks. The existing InteractiveStep and guided-handler unit suites pass 55 tests; 14 parsed DOM fixture cases cover label-row selection and secret-form guards. Selector fixture checks and source support do not replace browser-native or end-to-end verification. No Playwright is used for this follow-up.

Full resource-creation, restricted-role, mobile and deployed-guide walkthroughs remain unexecuted. After deployment, verify guide/runtime revisions and deduplicated session/action/step outcomes. Absence of traffic is not proof of repair; runtime and private-guide items stay open until their owners and serving behavior are verified.
