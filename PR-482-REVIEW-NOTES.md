# PR #482 review notes

Rationale for the 16 commits stacked on top of `docs/lp-basic-alerting` (PR #377). Organized by what was **added** (net-new content) vs what was **changed** (existing content reworked).

## What's in this PR

**Added:**

- New learning path: **`alerting-query-language-lj`** (12 milestones).
- New milestone in `alerting-first-rule-lj`: **`install-datasources`**.
- New milestone in `alerting-first-rule-lj`: **`configure-notification`**.
- New section in `alerting-first-rule-lj/set-evaluation-behavior`: **`set-keep-firing-for`**.

**Changed:**

- **`alerting-first-rule-lj`** — 10 existing milestones reworked end to end for concrete QuickPizza copy, plain language, and stable selectors.
- **`alerting-create-silence-lj/create-silence`** — reworked for updated UI vocabulary, step splitting so **Show me** follows the ask, and a matcher example that aligns with the earlier LJs.

## Stack shape

- PR #377 (JohnnyK-Grafana): `main` ← `docs/lp-basic-alerting` — original first-rule learning path packages.
- PR #482 (Beverly): `docs/lp-basic-alerting` ← `docs/lp-basic-alerting-install-datasources` — everything documented here.

PR #482 targets the branch PR #377 is landing, not `main` directly. See [Reviewer requests](#reviewer-requests) for the merge order.

## Guiding principles

Every rework in this PR follows the same rules. Each is tagged as a **learner-experience** improvement (a choice about wording, structure, or specificity that makes the tutorial easier for a person to follow), a **Pathfinder workaround** (compensating for a constraint in how the Pathfinder sidebar renders steps), or a **Pathfinder feature used intentionally**.

1. **Concrete over generic.** _(Learner experience.)_ Every step targets QuickPizza with real metric names, threshold values, and annotation copy — not `<service_name>` or "your metric here." Dictated examples keep the learner focused on the flow (build a rule end to end) instead of stalling to compare options. "What threshold should I pick?" or "what label should I add?" is a distraction on a first pass — the goal is learning how alert rules are structured, not choosing the perfect values. A specific recommendation (`severity=critical`, `1m` interval, threshold `0`) lets the learner move through the whole flow once, then explore variations on their own afterward.
   - **Before:** "enter your metric name in the query field."
   - **After:** "In the query field, enter `quickpizza_server_http_requests_total` and filter `status=~\"5..\"` to catch server errors."
2. **Concept-first, plain language.** _(Learner experience.)_ Jargon like "responders," "template variables," "rule-level labels ride along," "comparison operator," "signal," "annotations," and "service_name" was removed and replaced with what the reader is doing and why.
   - **Before:** "Configure the comparison operator and threshold for the alert condition to define the signal."
   - **After:** "Choose when the alert fires. Set it to fire whenever the count of 5xx errors is above `0`."
3. **One numbered step per action.** _(Pathfinder workaround.)_ The Pathfinder sidebar auto-numbers every block as a step in the checklist, whether the block has an action button attached or not. Standalone `markdown` blocks between interactive steps render as their own numbered step with no button — a floating sentence with nothing for the learner to click. Section intros were folded into the following interactive step's `content` field, so every numbered step in the sidebar has a matching **Do it** or **Show me** button next to it.
   - **Before:** a section starts with a `markdown` block ("Now you'll configure the alert condition.") followed by an `interactive` block that highlights **Is above**. The sidebar shows step 1 with the intro sentence and no button, and step 2 with the button. Step 1 looks broken — there's nothing to click.
   - **After:** the intro sentence is prepended to the `interactive` block's `content` field. The sidebar shows one step: "Now you'll configure the alert condition. Click **Is above**." — with a button attached. No orphan sentences.
4. **Single path, no branching prose.** _(Learner experience.)_ "If the picker is enabled do X, otherwise do Y" was reduced to the path the learner will actually see. Reference tables (Urgency/Interval, Alert type/Pending period) were dropped in favor of one concrete recommendation.
   - **Before:** a table listing five urgency levels mapped to five evaluation intervals, asking the learner to choose.
   - **After:** "Set the evaluation interval to `1m`. Short intervals catch issues quickly; longer intervals reduce query load."
5. **UI wording matches current Grafana docs (v11.1+).** _(Learner experience.)_ The alerting UI is called "the **new alert rule** page" (not "form"); the silence UI is called "the **Silences** page." Wire-level IDs, folder names, section IDs, and requirement tokens were not touched.
   - **Before:** "In the silence form, enter the labels you want to match."
   - **After:** "On the **Silences** page, click **Create silence** to open the new silence page."
6. **Stable selectors.** _(Pathfinder workaround.)_ Ambiguous text-based `reftarget` (e.g. multiple **Save** buttons on the page) was replaced with `[data-testid=...]` verified against a live Grafana instance. Pathfinder resolves `reftarget` by first DOM match, so ambiguous text sends **Show me** to the wrong element.
   - **Before:** `"reftarget": "Save"` — matched the header **Save** button, the folder-modal **Save** button, and the rule-page **Save** button.
   - **After:** `"reftarget": "[data-testid='save-rule']"` — matches only the alert-rule save button.
7. **Modal-aware copy.** _(Pathfinder workaround.)_ Steps that open a Grafana modal put instructional detail in a `noop` after the button click, because the modal covers the sidebar. Short, dropdown-name-first wording lets the learner read the step even with the modal open.
   - **Before:** one step that highlights **New folder**, tells the learner what to type in the modal's **Name** field, and to click **Create** — with the modal covering the sidebar the moment step 1 executes.
   - **After:** step 1 is a `button` click on **New folder**; step 2 is a `noop` that reads "In the **Name** field, enter a folder name, then click **Create**" — visible next to the open modal.
8. **`doIt: false` where the learner should own the outcome.** _(Pathfinder feature used intentionally.)_ Save, contact-point selection, and any destructive step leave the click to the user. `doIt: true` is used only for expand/collapse toggles and modal openers.
   - **`doIt: false`:** `save-rule` (creating an active alert rule), `select-contact-point` (picking which team gets paged).
   - **`doIt: true`:** `configure-handling` (expand the collapsed section so the learner can see the fields), `configure-labels-evaluation` (open the labels modal).
9. **Show me follows the ask.** _(Pathfinder workaround.)_ The **Show me** button always anchors to the bottom of a step's `content` field. Long reference material moves to a follow-up `noop` so **Show me** lands directly under the actionable sentence, not under a paragraph of optional UI detail.
   - **Before:** one `highlight` step whose `content` was "Set the **Duration** field to how long you want the silence to last. Valid units are years (y), months (M), weeks (w), days (d), hours (h), minutes (m), and seconds (s). The default `2h` works for a short deployment…" — **Show me** rendered under the units list, four sentences below the ask.
   - **After:** step 1 is a `highlight` with just "Set the **Duration** field to how long you want the silence to last, and Grafana calculates the end time for you"; step 2 is a `noop` with the units list. **Show me** now sits directly under the ask.

## Added

### `alerting-query-language-lj` — new learning path (`1e472aa`)

The learning-hub milestone `content/docs/learning-hub/basic-alerting/02-alert-with-query-language/` teaches the same first-rule flow with a PromQL/ratio query and adds one new concept (recovery threshold). There was no corresponding interactive LJ.

**Why a second LJ instead of extending the first one.** The first LJ (`alerting-first-rule-lj`) walks the learner through Builder mode, where Grafana composes the query from dropdowns. This second LJ exists so the learner can:

- **Practice code mode.** They write PromQL directly in the query editor instead of picking from dropdowns — the same rule idea, but authored differently. This is the payoff for the Builder-mode primer they got in the first LJ.
- **Build a second alert rule from scratch.** Repeating the full create-a-rule flow (name → query → condition → labels → evaluation → handling → contact point → notification → save) reinforces every step of the first LJ. By the end, the learner has built two rules and knows the flow well enough to build a third one on their own.

**Structure.** 12 milestones mirroring `alerting-first-rule-lj` so the learner recognizes every step from the first path — the only truly new material is code mode, the ratio query semantics, and recovery threshold.

**Where it deliberately differs from `alerting-first-rule-lj`:**

- `build-query` — writes PromQL directly instead of using Builder mode. Query is a ratio: `sum(rate(5xx)) / sum(rate(total))`.
- `set-condition` — threshold is `5` (percent). Section framing acknowledges the ratio's semantics (not "any errors").
- `configure-labels-evaluation` — intro reframed as review because the learner met these settings in the first rule. `severity=critical` rationale lives on the parent button step; modal-covered instruction is short and dropdown-first.
- `set-evaluation-behavior` — intro review-framed. Includes all three settings; recommends leaving **Keep firing for** at **None** because the recovery-threshold set two milestones later handles flapping for a ratio query.
- `configure-handling` — keeps the existing no-data / error defaults, plus a **skippable** `set-recovery-threshold` section that turns on Custom recovery threshold and sets the recovery value to `3`. Intro teaches recovery threshold as value-based dampening (fire above 5, recover below 3).
- `configure-notification` — **Summary** uses `{{ $value | printf "%.1f" }}%` to format the ratio as a percentage; **Description** names the ratio explicitly. Intro calls out the difference vs first-rule (count → percentage) so the reader understands why the templates differ.

### `alerting-first-rule-lj/install-datasources` — new milestone (`b1f322d`)

The pre-branch LJ told the learner to install QuickPizza as a prerequisite — outside the tutorial, before starting. The `business-value` milestone said: _"This path uses the QuickPizza tutorial data sources, which you install as a prerequisite before you begin."_ In practice that meant the learner had to leave the sidebar, install a Prometheus data source manually (add it, point it at the right URL, name it correctly), come back, and hope they set it up the way the rest of the LJ expected.

**What this milestone does.** The install step now runs inside the tutorial. The Pathfinder interaction installs the QuickPizza data source for the learner in one click, wired up exactly the way the rest of the LJ expects. The learner stays in the sidebar the whole time and doesn't have to context-switch to Grafana's data-source pages before they can start building the rule.

- Uses the shared `tutorial-datasources.json` template so this LJ installs QuickPizza the same way other tutorials do.
- Manifest rewired to run `business-value → install-datasources → navigate-to-form`, so the install happens before the learner is asked to pick a data source in `build-query`.
- The "install as a prerequisite" sentence in `business-value` is no longer needed and was removed.

### `alerting-first-rule-lj/configure-notification` — new milestone (`1090f17`)

Notification-message setup was previously bundled into `save-rule`, where it competed with save-and-activate for attention.

- Two `formfill` steps for **Summary** and **Description** with QuickPizza-specific values.
- Manifest updated to insert `configure-notification` between `select-contact-point` and `save-rule`.
- Recap bullets in `business-value` and `end-journey` split so the contact-point and annotation concepts aren't glued together.

### `alerting-first-rule-lj/set-evaluation-behavior/set-keep-firing-for` — new section (`0ce3ce8`)

The learning-hub milestone `01-first-alert-no-query-language/04-builder-evaluation/index.md` teaches three evaluation-behavior settings: evaluation group, pending period, and **Keep firing for**. The LJ had the first two but not the third.

- New section `set-keep-firing-for` added after `set-pending-period`.
- Highlights `#keep-firing-for-input` with `doIt: false` and recommends leaving it at **None** — the query is a raw count, not a hovering ratio, so there's no flapping to dampen.
- Parent milestone's intro markdown updated to name all three settings.

## Changed

### `alerting-first-rule-lj/business-value` (`6728fa5`, `1090f17`)

- Dense hook + list paragraph split into a one-sentence hook and a scannable bullet list of what the learner will build.
- Contact-point and annotation bullets separated so they don't read as a single concept.

### `alerting-first-rule-lj/navigate-to-form` and LJ intro (`9b3a886`, `60672a1`, `9cffeeb`)

- "Form" replaced with "new alert rule page" throughout learner-facing copy. Matches the Grafana docs, the button label (**+ New alert rule**), and the browser tab title.
- Alert-rule name pre-filled (`QuickPizza server errors`) via `formfill` so it aligns with the query built in `build-query`.
- Alert-name step collapsed from three blocks (intro + formfill + summary) into one interactive step with a transition `noop`.

### `alerting-first-rule-lj/build-query` (`3bba6b1`, `2feb7c2`, `5c85ce6`, `82609fd`)

- Query rewritten to `sum(increase(quickpizza_server_http_requests_total{status=~"5.."}[5m]))`, built in Builder mode with values pre-filled where the Grafana combobox allows.
- Intro simplified to a one-line lede, a plain-language bullet list, and a one-sentence payoff.
- Selectors verified against live Grafana: operator picker uses `[data-testid='data-testid Select match operator']`; explain toggle uses `[data-testid='data-testid prometheus explain switch wrapper']` and moved to run right after the data source pick where it's useful; value field switched to a stable data-testid because text-based `reftarget` on "Select value" matched multiple pickers.

### `alerting-first-rule-lj/set-condition` (`2b70e75`)

- Section titles rewritten around learner outcomes ("Choose when the alert fires", "Preview rule") instead of UI vocabulary ("Configure the threshold condition").
- Alert-condition area highlighted via the **WHEN QUERY** label instead of a fragile container selector; Is-above button scoped under `alert-rule step-2` to disambiguate.
- Threshold changed from `1` req/s to `0` (any errors) to match the new aggregation. "Traffic surge" framing dropped.
- Jargon ("comparison operator", "threshold") replaced with plain language; trailing wrap-up markdown folded into the final `noop`.

### `alerting-first-rule-lj/configure-labels-evaluation` (`fee7182`)

- Retitled "Create a folder and add labels" (learner outcome, not UI vocabulary).
- Intro rewritten as a plain routing summary; `annotations` and `template variables` references removed.
- Section 1 reduced to a single create-folder path (click **New folder**, `noop` for name + Create inside the modal — no more "if the picker is disabled" branch).
- Section 2: click **Add labels**, modal-aware `noop` with a concrete `severity=critical` example, brief transition. Reference-dump markdown table dropped.
- `service_name=quickpizza-public-api` references removed downstream because the new `sum()` aggregation drops labels.

### `alerting-first-rule-lj/set-evaluation-behavior` (`fb29d42`)

_(The new `set-keep-firing-for` section added to this milestone is under [Added](#alerting-first-rule-ljset-evaluation-behaviorset-keep-firing-for--new-section-0ce3ce8).)_

- Two reference tables (urgency vs interval, alert-type vs pending period) dropped. Learner doesn't need to decide these in a first rule.
- Section 1 retitled "Create an evaluation group" — no more "if you have an existing group, use it" branch.
- `highlight` on modal fields replaced with `button` click for the modal opener + `noop` for modal contents (which cover the sidebar).
- Concrete recommendations baked in: 1m interval, 1m pending period. No decision tree.

### `alerting-first-rule-lj/configure-handling` (`1090f17`)

- Plain-language intro. Auto-expand the collapse. Keep-defaults rationale explaining why defaults are safest for a first rule. `noop` transition.

### `alerting-first-rule-lj/select-contact-point` (`1090f17`)

- Reduced from picker + options table + decision paragraph to one `highlight` step on the picker with a concrete recommendation of `grafana-default-email`. Transition `noop`.

### `alerting-first-rule-lj/save-rule` (`1090f17`, `6728fa5`, `3bba6b1`)

- Slimmed to just save-and-activate; notification-message setup moved to the new `configure-notification` milestone. `doIt: false` — the learner presses **Save**.
- Selector switched from text-based `Save` (matched multiple buttons) to `[data-testid='save-rule']`; action switched to `highlight`.
- Summary annotation now uses `{{ $value }}` because `sum()` aggregates labels away.

### `alerting-first-rule-lj/end-journey` (`1090f17`, `6728fa5`)

- Recap bullets split so contact point and annotation aren't glued together.
- Trailing wrap-up markdown converted to a `noop` so it renders as a numbered step, not orphan text.

### `alerting-create-silence-lj/create-silence` (`a5920ae`)

The milestone was written against old UI vocabulary ("silence form"), had branching prose for optional time-range picking, mixed action + long reference material in single steps (so **Show me** landed under the reference paragraph instead of under the ask), and used a matcher example (`team=warning`) that wouldn't match anything the learner had built earlier.

**Vocabulary.** "Silence form" replaced with "the **Silences** page" throughout. Section 1 title changed to "Start a new silence"; click step is now "Click **Create silence** to start a new silence."

**Time-window section.**

- **Silence start and end** step split into a `highlight` with the concept (two timestamps, defaults to now + 2h) and a follow-up `noop` describing the optional **Absolute time range** menu. **Show me** now points at the field right after the concept.
- Same split applied to **Duration**: `highlight` with the ask, `noop` listing valid units. Units rendered as `years (y), months (M), …` instead of backtick-chip single letters (single-char copy chips look wrong in the sidebar).

**Matcher examples.**

- Concrete example switched from `team=warning` (would produce an empty preview) to `severity=critical`, which aligns with the labels the learner adds in `alerting-first-rule-lj/configure-labels-evaluation`.
- **Label** and **Value** steps use copy-chip framing ("copy `severity` and paste it into the **Label** field").
- Value step split so **Show me** appears immediately after the ask, with the operator-defaults explanation folded in as a single sentence.
- **Add matcher** step (`skippable: true`) uses a concrete `team=platform` alongside `severity=critical` example instead of abstract "add another matcher" prose.

**Verify-and-submit section.**

- **Affected alert instances** preview step now references "the alerts you created in the previous sections" and explains an empty preview is fine (the silence still catches future firings).
- **Comment** field step instructs the learner to **replace** the auto-populated timestamp text with a short reason (e.g. `Database upgrade in progress`). Grafana records creation time separately in metadata.

**Selectors.**

- New label-based selector `label:contains('Silence start and end')` for the time-range field, matching the `label:contains('WHEN QUERY')` pattern already used in `set-condition`.
- Other selectors (`#duration`, `#matcher-0-label`, `#matcher-0-value`, `#comment`, `a[href*='alerting/silence/new']`, `button:contains('Add matcher')`, `Save silence` button-text) are DOM-verified.

**Not touched.** Section IDs (`open-silence-form` still gates `set-time-window` even though the section title now says "Start a new silence"), requirement tokens, and manifest.

## Alignment with learning-hub docs

The two rule-building LJs align 1:1 with the conceptual content in `grafana/website` PR #30466:

| Concept | learning-hub location | `alerting-first-rule-lj` | `alerting-query-language-lj` |
|---|---|---|---|
| Evaluation group | milestone 01 `04-builder-evaluation` | ✅ `set-evaluation-behavior` | ✅ `set-evaluation-behavior` |
| Pending period | milestone 01 `04-builder-evaluation` | ✅ `set-evaluation-behavior` | ✅ `set-evaluation-behavior` |
| Keep firing for | milestone 01 `04-builder-evaluation` | ✅ `set-evaluation-behavior` (added in `0ce3ce8`) | ✅ `set-evaluation-behavior` |
| No-data / error handling | milestone 01 `04-builder-evaluation` | ✅ `configure-handling` | ✅ `configure-handling` |
| Recovery threshold | milestone 02 `04-code-complete-rule` | n/a (not taught in milestone 01) | ✅ `configure-handling / set-recovery-threshold` |

## Debugging note captured during the branch

Grafana's **New evaluation group** button in section 4 of the alert rule page is disabled (native 🚫 cursor) until a folder is selected in section 3. This looks like a Pathfinder overlay blocking clicks but it's Grafana's own form validation. Do not add Pathfinder workarounds — the click succeeds once the learner completes the folder step in `configure-labels-evaluation`.

## For JohnnyK — how to accept these changes and stay as the author

You own PR #377. This PR (#482) stacks a batch of edits on top of your branch so you don't have to redo any of it. When you land PR #377, everything here goes with it — and you stay as the author on `main`.

**Step 1: Merge PR #482 into your branch.**
PR #482 targets `docs/lp-basic-alerting` (your branch), not `main`. Review it like any other PR. When you're happy, click **Squash and merge** on PR #482. That collapses my commits into one commit on your branch — the attribution on that commit doesn't matter, because it won't survive step 2.

**Step 2: Squash-merge PR #377 to `main`.**
When PR #377 is ready to land, use **Squash and merge** on it. GitHub produces one commit on `main` — authored by you — that contains everything: your original learning-path work plus the additions from PR #482. That's the only commit that shows up in `git log` on `main`, and it's yours.

You don't need to touch any code on your side — just review and click merge.
