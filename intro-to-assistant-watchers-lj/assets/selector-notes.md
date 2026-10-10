# Selector notes: intro-to-assistant-watchers-lj

Live DOM checks on `learn.grafana.net` (2026-09-17). Empty fleet had no Watcher detail page. **Start scanning** and **Run now** were confirmed later on a calibrated Watcher.

| Element | Selector / target | Notes |
| --- | --- | --- |
| Watchers page | navigate `/a/grafana-assistant-app/watchers` | Confirmed. Title: Watchers - AI - Grafana |
| New watcher form | navigate `/a/grafana-assistant-app/watchers/new` | Opens after **New watcher** → **Set up manually** |
| AI nav section | `button[data-testid='data-testid navigation mega-menu section toggle /a/grafana-assistant-app']` | Parent label is **AI**, not Assistant |
| Watchers nav item | `a[data-testid='data-testid Nav menu item'][href='/a/grafana-assistant-app/watchers']` | Requires **AI** expanded; use `navmenu-open` |
| New watcher | button text `New watcher` | No testid. Opens `[data-testid='popover-menu']` in `data-testid portal-container` |
| Create with Assistant | first `button[role='menuitem']` in the popover | Label is in a nested span, so `action: "button"` + text fails. Conversation path; this LP uses the form |
| Set up manually | `[data-testid='popover-menu'] button[role='menuitem']:last-of-type` | Same nested-span issue. Combined with **New watcher** in a multistep so the menu is still open. Opens `/watchers/new` |
| Name | `input[placeholder='Checkout service']` | Label **Name ***. No testid; ids are generated |
| Context | `textarea[placeholder^='Watch my checkout service']` | Label **Give the watcher context *** |
| Datasources | `input[placeholder='Select datasources']` | Combobox. Learner must pick a source; **Calibrate** stays disabled until then |
| Repeats | `input[role='combobox'][value='Every 15 minutes']` | Default on a fresh form. Skippable if changed |
| Sensitivity | `input[role='combobox'][value='Balanced: escalate on clear deviations']` | Default on a fresh form. Skippable if changed |
| Calibrate | button text `Calibrate` | On `/watchers/new`. Disabled until required fields are filled |
| Cancel | button text `Cancel` | Returns to the list without creating |
| List empty state | status **No watchers yet** | Assessment labels are not visible until a run exists |
| Explainer **Calibrate** | not a button | Empty-list explainer cards. Do not target with `action: "button"` |
| Open Watcher | noop | Open the Watcher you created. Lands on **Overview** |
| Overview contents | noop | Confirmed 2026-09-23 on a Watcher with one completed run. Left: **Run history** list; expanding a run shows **Why this verdict**, **Run summary**, **What it'll watch next**, and **Telemetry evidence**. Right: **Standing state** card with the latest assessment (for example **All clear**), the **Ready**/**Active** switch, **Run now**, **Cadence**, **Last run**; then **Calibration** (**Recalibrate**, **Last calibrated**, **Checks**) and **Token consumption** |
| Calibration tab | `[data-testid='data-testid Tab Calibration']` | Confirmed. Click **Calibration**. Skip if already on this tab. **Review calibration** on Overview also works |
| Start scanning | button text `scanning` (partial) | Calibration banner on the **Calibration** tab. Both the button label and the banner title are state-dependent, and flip on the same condition: `detail/tabs/calibration/WatcherCalibrationTab.tsx` (grafana-assistant-app `origin/main` `e47587c369`) renders `resumeAfterCalibration \|\| terminalRuns.length > 0 ? 'Resume scanning' : 'Start scanning'` for the button, and titles the banner **Recalibration complete** instead of **Calibration complete** under the same test. A finished **Run now** one-off is a terminal run, so this path's order (Run now, then start) always lands on **Resume scanning** under a **Recalibration complete** banner — don't tell the learner to look for "Calibration complete". Partial `scanning` matches both labels. Do not use `Start` (partial match hits Block Editor and **Start a new conversation**) or exact `Start scanning` (misses after a run). Verified live 2026-09-25 on a calibrated Watcher with one completed **Run now**: exactly one button matches on every tab (Overview, Calibration, Notifications, Versions, Configuration), reading **Resume scanning**. Two traps: the banner unmounts while a run is in flight, so the step blocks until the run finishes; and the Calibration tab panel stays mounted on other tabs, so from **Overview** the button still matches but is `display:none` and "Show me" highlights a 0×0 element — keep the Calibration tab step |
| Run now | button text `Run now` | Standing state card on the Watcher detail page. Confirmed 2026-09-23: enabled while the switch reads **Ready**, before **Start scanning**. Tooltip: "Run a one-off check now, outside the schedule" |
| Active / pause | noop | Click **Active** in Standing state yourself. Pathfinder can find **Run now** (button text) but not this Grafana Switch. CSS `:has` / `role=switch` / sibling-of-Run-now all failed in Block Editor. Don't target **Delete** |

Do not automate Slack, webhook secrets, or **Delete**. The create form on this stack has **Post to Slack**, **Send to a webhook**, and **Launch on a critical assessment**. There is no Grafana Alerting toggle on the form.

Do not verify this page from the `grafana-assistant-app` checkout alone. The deployed plugin (2.0.70, 2026-09-25) carries a **Stop scanning** string that the local tree lacks — it is Archive-row prose on the **Configuration** tab, not a button, but the divergence means source-only checks can miss a candidate label. Check the served chunk instead. Note also that `findButtonByText` matches `document.querySelectorAll('button')` by tag and reads text nodes only, so `aria-label`, `title`, and `div[role="button"]` never match, and it applies no visibility filter.

Code check in grafana-assistant-app (2026-09-23): **Send to Grafana Alerting** renders in the create form's Notifications section and on the post-create **Notifications** tab only when the `assistant.watcher-agents-alerting-notifications` feature flag is on (default off). Clicking **Calibrate** is the only submit: it creates the watcher, then starts calibration. Filling the form saves nothing. If calibration fails after create, the watcher exists and **Calibrate** retries.
