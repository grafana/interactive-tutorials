# Selector repair disposition — 22 September 2026

This batch repairs public guide content and records the remaining work from the selector investigation. It does not establish that every reported interaction failed, or that the corrected guides have been deployed. Preview, synthetic, and unattributed traffic must remain separate when evaluating results.

## Changes and remaining work

| Plan family | Content changes | Remaining validation or owner |
| --- | --- | --- |
| Synthetic Monitoring secrets | Direct Secrets route, permission/page guards, fully manual credential creation/editing, mandatory saved-name confirmation, distinct section IDs. | Walk fresh/existing-secret paths. Restricted users are explicitly directed to an administrator; the gated workflow cannot complete without that role. Secrets were not created during validation. |
| Synthetic Monitoring labels and hidden controls | Visible radio/checkbox labels across Ping, DNS, TCP and introductory guides; optional manual label creation supports both **Label** and **Add label** without overwriting existing rows. | Labels are deliberately manual. Check selected-state behavior in full guide execution. |
| Saved queries | Require the panel editor and editor permission; scope Save/Replace controls; open the menu before selecting Add saved query; explicit manual confirmation of dialog outcomes. | Final save/replace/add outcomes need a resource-changing walkthrough. Literal `on-page` matching cannot safely express both `/d/` and `/dashboard/new`, so actual editor controls gate these steps. |
| First dashboard | Direct plugin/connection routes, editor guards, stable datasource inputs, datasource health prerequisite, dashboard save verification. | Fresh install, restricted role and saved-dashboard walkthrough remain. Business News is still available on learn but marked deprecated; migrating this guide to another datasource is separate work. |
| Hidden targets and hover | Instrumented and Code choices target visible labels. Snapshot panel menu follows a header hover. | Pathfinder owns general hidden-control and hover behavior; warning records alone do not prove a failed action. Bundled `first-dashboard-cloud` content belongs to Pathfinder. |
| Navigation | Direct routes replace hidden menu chains in Secrets, SM overview, first-dashboard setup, IRM and k6 Assistant entry; route verification added. | Pathfinder owns mobile menu/toggle behavior. No engine change or mobile walkthrough in this batch. |
| Frontend Observability | Optional search/empty-list guidance, visible radio labels, guided below-fold observations with `lazyRender` and `#pageContent`, explicit manual scrolling and touch skip instructions. | Automatic guided lazy discovery remains a Pathfinder runtime gap (below). No complete telemetry-dependent tour walkthrough. |
| Embedded selector tokens | Retained valid tokens after inspecting resolver/source support. | No confirmed current token drift. Historical preview failures need the exact serving revision before an engine change. |
| Transform/Fleet ambiguity | Fleet health indicator scoped to collector rows and known status labels; guided observation. Current transform-data source already lacks the two reported legacy targets, so it is unchanged. | Verify serving revisions before calling transform failures resolved; Fleet automatic lazy scrolling has the runtime limitation below. |
| Private/unattributed targets | No speculative public-guide replacements. | Backend/draft guide owners must identify Standing state / Run now / network breadcrumb sources. Pathfinder diagnostics need sufficient private-safe attribution. Public QuickPizza code blocks inspected did not reproduce the reported missing-refTarget shape. |
| Synthetic-only coverage | IRM route/rotation compatibility selector and snapshot dashboard context/header/expiration controls repaired. | Pathfinder test-fixture owners must map remaining Prometheus prerequisites and datasource auto-completion signals to fixtures. Synthetic counts are not customer failure counts. |

## Evidence and validation

- Source review covers Grafana radio labels, panel headers, datasource settings/pickers and Assistant controls; Synthetic Monitoring form/modal/status components; Business News config test IDs; IRM rotation controls; Frontend Observability and Fleet page structure.
- Connected Chrome checks on learn confirmed the installed Business News connection and its **Add new data source** action. An unsaved Ping form confirmed **Label** creates **Custom labels 1 name/value** fields. Newer Synthetic Monitoring source uses **Add label** and different field naming, so a speculative global selector replacement would break the serving version. No datasource, check or secret was saved in these checks.
- All 17 changed guide packages pass the local Pathfinder CLI package validator and all 17 content files pass strict validation. Local schema checks do not prove live selector resolution. Final validation used the CLI and source review, with the limited connected-browser checks described above.
- Independent diff review covered the changed guides. Block IDs and references are preserved except an existing duplicate Secrets section ID was disambiguated. `index.json` and manifests are unchanged.
- Full Admin/restricted-role, desktop/mobile, Show me/Do it and resource-creation acceptance remains unexecuted. Do not interpret this report as a completed live acceptance matrix.

## Confirmed Pathfinder runtime gap

At Pathfinder `origin/main` commit `339cd31d95c636b82b66f27e3496eb1f49aa0fa4`, `src/docs-retrieval/json-parser.ts::convertGuidedBlock` does not forward step `lazyRender` or `scrollContainer` into internal actions. `src/interactive-engine/action-handlers/guided-handler.ts` does not implement guided lazy discovery or evaluate the internal step requirements.

The guide changes retain the documented lazy fields, lift applicable page/version prerequisites to guided blocks, and tell learners to scroll first. Optional observations can be skipped. This is a content mitigation, not a fix for automatic scrolling. Pathfinder must forward the fields and implement/test guided discovery before that acceptance criterion can be closed. Do not add a block-level existence gate to an initially unrendered target: that would prevent discovery from starting.

The section runner also executes ordinary actions with `buttonType: do` without honoring each step's `doIt: false` flag. The Secrets guide therefore has no executable credential-form steps: creation and editing are manual prose, and mandatory non-action saved-name targets gate progress. Pathfinder owns fixing the section runner; `doIt: false` alone must not be treated as that fix.

## Release follow-through

After review and deployment, verify the serving guide revisions and Pathfinder version. Recheck the original failure families using deduplicated session/action/step outcomes, separating named public guides, previews and synthetic traffic. Close runtime and private-guide items only when their owning changes and serving behavior are verified; absence of traffic is not proof of repair.
