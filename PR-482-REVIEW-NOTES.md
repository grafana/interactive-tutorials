# PR #482 review notes

Rationale for every commit stacked on top of `docs/lp-basic-alerting` (PR #377) for reviewers of PR #482. Read this before the file diff — it explains **why** each interaction was added, reworded, or reordered.

## Stack shape

- PR #377 (JohnnyK-Grafana): `main` ← `docs/lp-basic-alerting` — original first-rule learning path packages.
- PR #482 (Beverly): `docs/lp-basic-alerting` ← `docs/lp-basic-alerting-install-datasources` — everything below.

Merging PR #482 into `docs/lp-basic-alerting` folds all these commits into PR #377's changeset so they land on `main` together.

## Guiding principles applied across the branch

These principles drove most of the reworks. When you see a commit that changes an interaction, one or more of these is the reason.

1. **Concrete over generic.** Every step targets QuickPizza with real metric names, real threshold values, and real annotation copy — not `<service_name>` or "your metric here."
2. **Concept-first, plain language.** Section intros teach a concept in one paragraph. Jargon like "responders," "template variables," "rule-level labels ride along," "comparison operator," "signal," "annotations," "service_name" was removed and replaced with what the reader is doing and why.
3. **One numbered step per action.** Every `interactive` block has an action attached. Standalone `markdown` blocks between interactive steps caused lonely numbered lines when requirements gated the next block, so intros were folded into the interactive step's `content` field.
4. **Single path, no branching prose.** Sections that used to say "if the picker is enabled do X, otherwise do Y" were reduced to the one path the learner will actually see. Reference tables (Urgency/Interval, Alert type/Pending period) were dropped in favor of a single concrete recommendation.
5. **UI wording matches current Grafana docs (v11.1+).** The alerting UI is called the "new alert rule page," not "form" or "creation form" — this matches the Grafana docs and the button label (**+ New alert rule**).
6. **Stable selectors.** Where text-based `reftarget` was ambiguous or duplicated (e.g. multiple **Save** buttons), we switched to `[data-testid=...]` selectors verified against a live Grafana instance.
7. **Modal-aware copy.** Steps that open a Grafana modal put the instructional detail inside a `noop` after the button click, because the modal covers the sidebar. Short, dropdown-name-first wording lets the learner read the step even with the modal open.
8. **`doIt: false` where the learner should own the outcome.** Save, contact-point selection, and any step that opens a destructive dialog leave the click to the user. `doIt: true` is used only for expand/collapse toggles and modal openers.

## Commit-by-commit rationale (oldest → newest)

### `b1f322d` alerting-first-rule-lj: add install-datasources milestone

**Why.** The path assumed the QuickPizza data source was already installed. Learners hitting the LJ fresh had no way to get it. Added a Pathfinder-driven install step using the shared `tutorial-datasources.json` template so the LJ is self-sufficient.

**Interaction added.** `install-datasources` milestone using the shared install pattern; manifest rewired to run `business-value → install-datasources → navigate-to-form`.

### `9b3a886` alerting-first-rule-lj: replace "form" with "new alert rule page"

**Why.** Grafana's alerting docs (v11.1+) describe this UI by page name, not as a "form." Learner-facing copy that says "the form" doesn't match what the docs, the button label, or the browser tab title say. Wire-level IDs, folder names, section IDs, and requirement tokens were not touched — only the human-visible copy.

### `3bba6b1` alerting-first-rule-lj: rework query to watch QuickPizza 5xx errors

**Why.** The prior query was generic and abstracted. Learners built a rule without ever seeing what it detects. Rewritten to build `sum(increase(quickpizza_server_http_requests_total{status=~"5.."}[5m]))` in Builder mode, pre-filling values where the Grafana combobox allows.

**Downstream ripples.**
- `set-condition`: threshold changed from `1` (req/s) to `0` (any errors); "traffic surge" framing dropped.
- `configure-labels-evaluation`, `save-rule`: `service_name=quickpizza-public-api` references removed because the aggregation drops labels.
- `save-rule` summary annotation now uses `{{ $value }}` since `sum()` aggregates labels away.

### `2feb7c2` alerting-first-rule-lj: simplify build-query intro

**Why.** The opening paragraph was dense and mixed concept + steps. Split into a one-line lede, a plain-language bullet list of what the learner will do, and a one-sentence payoff.

### `60672a1` alerting-first-rule-lj: collapse section intros and pre-fill alert name

**Why.** Sections had a markdown intro block followed by an interactive step gated on `on-page:...`. When the requirement wasn't met, the intro rendered as a lonely numbered sentence with no action next to it. Folded every section's lede markdown into the immediately-following interactive step's `content` field.

Also pre-filled the alert rule name (`QuickPizza server errors`) via `formfill` on `navigate-to-form` so it matches the query the learner builds in the next milestone.

### `9cffeeb` alerting-first-rule-lj: tighten alert-name step copy

**Why.** The alert-name step still had a three-block intro + formfill + trailing summary. Collapsed into one interactive step (intro sentence, why-it-matters sentence, formfill instruction) with the next-milestone line as the transition noop.

### `5c85ce6` alerting-first-rule-lj: fix build-query selectors and step wording

**Why.** Preview against live Grafana revealed the selectors:
- Operator picker: needs `[data-testid='data-testid Select match operator']`; step reworded to "Show me only" with no skip option.
- Explain toggle: needs `[data-testid='data-testid prometheus explain switch wrapper']`; section moved to run immediately after the data source pick, where it's actually useful.
- Value: reworded to "In the **Select value** box, enter 5.." to match the visible field label.

### `82609fd` alerting-first-rule-lj: use stable Select value testid in build-query

**Why.** Text-based `reftarget` on "Select value" matched multiple pickers on the page. Switched to a stable data-testid to disambiguate.

### `2b70e75` alerting-first-rule-lj: rework set-condition milestone

**Why.** Sections were titled with jargon ("Configure the threshold condition"), the intros repeated the same idea twice, and there were redundant markdown blocks.

- Sections retitled to "Choose when the alert fires" and "Preview rule" (learner outcomes, not UI vocabulary).
- Alert-condition area highlighted via the **WHEN QUERY** label instead of a fragile container selector.
- Is-above button scoped under `alert-rule step-2` so it doesn't match the same button elsewhere.
- Dropped "comparison operator" and "threshold" jargon; used plain language.
- Removed the trailing markdown wrap-up; folded into the final noop.

### `fee7182` alerting-first-rule-lj: rework configure-labels-evaluation milestone

**Why.** The intro leaned on `service_name` and "Sum step" terms that no longer applied after the query rework in `3bba6b1`. The section for creating a folder branched on whether the picker was disabled.

- Retitled to "Create a folder and add labels."
- Intro rewritten as a plain routing summary (no `annotations`, no `template variables` mentions).
- Section 1 reduced to a single create-folder path: click **New folder**, then a `noop` for name + Create inside the modal.
- Section 2: click **Add labels**, then a modal-aware `noop` with a concrete `severity=critical` example, then a brief transition.
- Dropped the reference-dump markdown table and the orphan wrap-up.

### `fb29d42` alerting-first-rule-lj: rework set-evaluation-behavior milestone

**Why.** The milestone had two reference tables (urgency vs interval, and alert-type vs pending period) that made the reader decide something they don't need to decide in a first-rule tutorial. Removed both.

- Section 1 retitled to "Create an evaluation group" (single path — no more "if you have an existing group, use it" branch).
- Replaced `highlight` on modal fields with a `button` click for the modal opener + `noop` for the modal's contents (which cover the sidebar).
- Concrete recommendations: 1m interval, 1m pending period. No decision tree.
- Trailing wrap-up markdown converted to a noop transition.

### `1090f17` alerting-first-rule-lj: rework configure-handling, select-contact-point, save-rule; add configure-notification milestone

**Why.** The tail end of the LJ had four issues:
1. `configure-handling` explained no-data / error handling in dense reference-doc language.
2. `select-contact-point` mixed picker interaction, a table of options, and a decision paragraph.
3. `save-rule` bundled the notification-message setup with the actual save.
4. Notification-message setup wasn't its own milestone, so it competed with save-and-activate for attention.

- `configure-handling`: plain-language intro; auto-expand the collapse; keep-defaults rationale explaining why defaults are safest for a first rule; noop transition.
- `select-contact-point`: one `highlight` step on the picker with a concrete recommendation of `grafana-default-email`; transition noop.
- `configure-notification` (new milestone): two `formfill` steps for Summary and Description with QuickPizza-specific values.
- `save-rule` slimmed to just save-and-activate with `doIt: false` — the learner presses **Save**.
- Manifest updated to insert `configure-notification` between `select-contact-point` and `save-rule`.
- Business-value and end-journey recap bullets split so contact point and annotation aren't glued together.

### `6728fa5` alerting-first-rule-lj: fix save-rule selector and tighten business-value

**Why.**
- Save button text is just "Save" and matches multiple buttons on the page. Switched `save-rule` to a `highlight` action with `[data-testid='save-rule']`.
- Converted the trailing wrap-up markdown to a `noop` transition so it renders as a numbered step, not orphan text.
- Business-value copy had a dense hook + list paragraph. Split into a one-sentence hook and a scannable bullet list of what the learner will build.

### `0ce3ce8` alerting-first-rule-lj: add Keep firing for step to set-evaluation-behavior

**Why.** The learning-hub conceptual milestone `content/docs/learning-hub/basic-alerting/01-first-alert-no-query-language/04-builder-evaluation/index.md` teaches three evaluation-behavior settings: evaluation group, pending period, and **Keep firing for**. The LJ had the first two but not the third. This commit closes the gap so the LJ matches what the doc says the learner will encounter.

- New section `set-keep-firing-for` after `set-pending-period`.
- Highlights `#keep-firing-for-input` with `doIt: false` and recommends leaving the setting at **None** for this rule (the query is a raw count, not a hovering ratio — no flapping to dampen).
- Intro markdown updated to name all three evaluation-behavior settings.

### `1e472aa` alerting-query-language-lj: initial learning path

**Why.** The learning-hub milestone `content/docs/learning-hub/basic-alerting/02-alert-with-query-language/` teaches the same first-rule flow with a PromQL/ratio query and adds one new concept (recovery threshold). There was no corresponding interactive LJ.

**Structure.** Mirrors `alerting-first-rule-lj` with 12 milestones so the learner recognizes every step from the first path.

**Where it deliberately differs from first-rule-lj:**
- `build-query`: writes PromQL directly instead of using Builder mode. Query is a ratio (`sum(rate(5xx)) / sum(rate(total))`).
- `set-condition`: threshold is 5 (percent). Section framing acknowledges the ratio's semantics (not "any errors").
- `configure-labels-evaluation`: intro reframed as review, because the learner met these settings in the first rule. `severity=critical` rationale is on the parent button step; modal-covered instruction is short and dropdown-first.
- `set-evaluation-behavior`: intro is review-framed. Includes the same three settings including **Keep firing for**, but recommends leaving Keep firing for at **None** because the recovery-threshold set two milestones later handles flapping for a ratio query.
- `configure-handling`: keeps the existing no-data / error defaults. Adds a **skippable** `set-recovery-threshold` section that turns on Custom recovery threshold and sets the recovery value to 3. Intro markdown teaches recovery threshold as value-based dampening (fire above 5, recover below 3).
- `configure-notification`: **Summary** uses `{{ $value | printf "%.1f" }}%` to format the ratio as a percentage; **Description** names the ratio explicitly. Intro markdown calls out the difference vs first-rule (count → percentage) so the reader understands why the templates differ.

## Alignment with learning-hub docs

The two LJs align 1:1 with the conceptual content in `grafana/website` PR #30466:

| Concept | learning-hub location | alerting-first-rule-lj | alerting-query-language-lj |
|---|---|---|---|
| Evaluation group | milestone 01 `04-builder-evaluation` | ✅ `set-evaluation-behavior` | ✅ `set-evaluation-behavior` |
| Pending period | milestone 01 `04-builder-evaluation` | ✅ `set-evaluation-behavior` | ✅ `set-evaluation-behavior` |
| Keep firing for | milestone 01 `04-builder-evaluation` | ✅ `set-evaluation-behavior` (added in `0ce3ce8`) | ✅ `set-evaluation-behavior` |
| No-data / error handling | milestone 01 `04-builder-evaluation` | ✅ `configure-handling` | ✅ `configure-handling` |
| Recovery threshold | milestone 02 `04-code-complete-rule` | n/a (not taught in milestone 01) | ✅ `configure-handling / set-recovery-threshold` |

## Debugging note captured during the branch

Grafana's **New evaluation group** button in section 4 of the alert rule page is disabled (native 🚫 cursor) until a folder is selected in section 3. This looks like a Pathfinder overlay is blocking clicks but it's Grafana's own form validation. Do not add Pathfinder workarounds — the click succeeds once the learner completes the folder step in `configure-labels-evaluation`.

## Reviewer requests

- Merge strategy: squash-merge preferred so authorship consolidates on the merger. `Co-authored-by:` trailer is not required.
- These changes are intended to land as part of PR #377. If PR #482 merges into `docs/lp-basic-alerting` first, PR #377 carries everything to `main` when it merges.
