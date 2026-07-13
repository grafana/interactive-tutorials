# Reference checks

Checklists for [review-learning-path/SKILL.md](SKILL.md) Phase 1 (static pass). Findings land in `pr-{n}-findings.md` — **reviewer workbook only**, never pasted to the author.

**Comment voice:** [comment-style.md](comment-style.md)

**Selector authority:** [docs/selectors-and-testids.md](../../../docs/selectors-and-testids.md). Do not apply build-interactive-lj autogen "never `:contains()`" rules to hand-authored guides.

**Publishing model (PR [#416](https://github.com/grafana/interactive-tutorials/pull/416)):** LP PRs are single-repo. Package `website.yaml` is authoritative; website repo is read-only for conversion.

**Learning Hub:** [learning-hub-standards.md](learning-hub-standards.md) — checks run in Phase 1; default tier is **internal** (workbook only).

---

## Finding routing

Tag every finding when writing the workbook. **Author-facing change requests always go on the GitHub diff as short inline comments** (path-wide OK) after Phase 3 approval. The workbook is reviewer-private scratch — never the channel for telling the author what to fix.

| Post inline (author must change) | Internal (workbook only) | Discard |
|---|---|---|
| Block Editor / Playwright runtime fail (reviewer-reported) | Section bookends missing when live passed | Audit noise with no runtime impact |
| Framing in path `milestones` / broken depends | `website.yaml` metadata gaps | CODEOWNERS reminder |
| In-section intro markdown confirmed numbered as a step | In-section intro (static detect only; not yet live-confirmed) | Passed-milestone notes |
| False `noop` (learner action, no `reftarget`) | `:contains()` fallback when live passed | Pathfinder shell UX |
| Missing `exists-reftarget`, `navmenu-open` **when live fails** | LH editorial (boilerplate, prerequisites, CTA) | Fresh-stack retest notes (unless live failed) |
| Outdated `data-testid` when live fails | Selector polish when live passed | Suspected bad link (unverified) |
| `:contains()` when stable `data-testid` in DOM and live fails | Vague copy when live passed | |
| Path root / manifest `id` mismatch | `related_journeys` wording | |
| Pathfinder CLI validate failure | Editorial / tooltip / vocabulary | |
| `index.json` modified, invalid `testEnvironment.tier` | Conversion `website.yaml` mapping gaps | |
| Secrets auto-filled (`doIt: true`) | Missing troubleshooting on verification (when live passed) | |
| Hard cross-path artifact dependency in step copy | Landing screenshot / milestone count notes | |
| Confirmed 404 in `website.yaml` supplementary fields | Framing snippet alignment | |
| Prose only in legacy markdown (conversion PR) | | |

**After live test:** promote **internal** items to **post inline** only when Block Editor or Playwright failed, or the issue is clearly wrong regardless of runtime (e.g. `id` mismatch, broken depends, framing, false noop).

**Never:** paste the workbook (or agent paraphrases of it) to the author; leave an author fix only in the workbook; invent nits so the review “has comments.”

**Never post:** anything still in **internal** or **discard** unless the reviewer explicitly promotes it at Phase 3.

### Selector decision tree

Apply after Phase 2 when deciding post inline vs internal:

```
Selector finding
  │
  ├─ Block Editor or Playwright fail on this step? → post inline
  │
  ├─ Stable data-testid in DOM but author used :contains()? → post inline
  │
  ├─ :contains() fallback per selectors doc, live passed, no stable selector? → internal (do not post)
  │
  └─ CSS class / nth-only, live passed? → discard
```

---

## Milestone `content.json` checks

Run via [audit-guide](../audit-guide/SKILL.md) plus confirm every row:

| Check | Route when |
|---|---|
| `schemaVersion` not `"1.1.0"` when present | post inline |
| Markdown `##` / `###` for grouping | internal |
| Section bookends missing (rule 14) — no intro/summary **around** the section | internal until live fails |
| In-section intro markdown that may number as a step | **internal** until Block Editor confirms; then **post inline** (see [section intro markdown](#section-intro-markdown-numbered-as-step)). Prefer bookends **outside** the section per rule 14. |
| Missing `exists-reftarget`, `navmenu-open` | internal until live fails |
| Missing `on-page` | internal until live fails |
| `lazyRender` missing on virtualized targets | internal until live fails |
| Multistep singleton, focus-before-formfill, `noop` misuse | post inline if compliance; else internal |
| Secrets `doIt: true` | post inline |
| Missing `verify` on save | internal until live fails |

LH prose checks: [learning-hub-standards.md](learning-hub-standards.md) — default **internal**.

---

## Section intro markdown numbered as a step

Recurring Pathfinder UX issue (seen across multiple LP PRs, including interactive dashboards and Infinity JSON): a one-sentence "what you'll do" markdown block as the **first child inside a `section`** shows up in Block Editor as a numbered step (for example "1. You'll open a dashboard…") instead of unnumbered prose.

Docs sometimes say in-section `markdown` is unnumbered. **Treat Block Editor as source of truth.** If the reviewer sees a number on that block, flag it.

### Phase 1 — static detect (workbook)

For every interactive `section`, check the first block:

| Detect when first in-section block is `markdown` and… | Example |
|---|---|
| Content starts with `You'll ` / `You will ` | `You'll customize how a variable appears…` |
| Content is a one-sentence action preview before the first interactive | `In this section, open Edit and add a variable.` |
| Content restates the section goal without teaching a concept | Same pattern under different wording |

Write under **Verify in Block Editor** in `pr-{n}-findings.md`. Note every milestone that matches (path-wide pattern is common). Do **not** post from static detect alone.

Missing bookends (no intro/summary **around** the section at all) stay a separate **internal** finding. Correct placement is **outside** the `section` (intro immediately before, summary immediately after). This check is the opposite problem: intro exists **inside** the section and Pathfinder treats it like a step.

### Phase 2 — confirm

On **every** interactive milestone Block Editor prompt, ask the reviewer to scan the section step list for false step numbers — not only when Phase 1 flagged the milestone:

- Intro prose numbered as step 1 (for example "You'll …")
- Learner-action `noop`s numbered as interactive steps

| Live result | Route |
|---|---|
| Numbered as a step (intro or false noop) | **Post inline** |
| Unnumbered prose / accepted noop only | Discard this finding for that milestone |

Same scan applies to [false noops](#noop-and-non-interactive-steps) even when static detect missed a wording variant.

### Phase 3 — comment shape

- **One path-wide inline** when the same pattern appears in multiple milestones. Anchor on the first clear example; list the other milestone slugs in the comment body.
- Fix: move the intro markdown **outside** (before) the `section` block, or drop it if the section title is enough. Keep a one-sentence summary bookend (outside or after the section) so rule 14 intent is preserved without a fake step 1.

---

## Framing milestones

Framing packages may live in the path directory for the website Learning Path, but must **not** appear in path `manifest.json` `milestones`. First hands-on `depends` must not reference framing IDs.

Framing in path `milestones` or broken depends → **post inline**.

### Framing vs not framing

Framing is about **role**, not “markdown-only.”

| Kind | Examples | In path `milestones`? |
|---|---|---|
| **Framing** (value / why intro) | `business-value`, `value-*`, `advantages-*`, `welcome` | No — keep the package + `website.yaml` if the website needs it; omit from Pathfinder `milestones` |
| **Not framing** (path destination) | `end-journey`, `end-<topic>` | Yes |
| **Case-by-case** | Prose conceptual packages such as `understanding-*` | Only if they are a Pathfinder path step learners must complete. If they are website-only conceptual framing, treat as framing (omit from `milestones`, first hands-on `depends: []`) |

Do **not** auto-flag every markdown-only `milestones` entry. `end-journey` is normally prose-only and correctly listed.

When a prose milestone is ambiguous, note it under **Internal** as “is this framing?” for the reviewer. Promote to **post inline** only after the reviewer confirms it is framing (or it matches a known framing name above).

---

## Path root `content.json`

| Check | Route when |
|---|---|
| `id` mismatch with manifest | post inline |
| Prose only in legacy `index.md` (conversion) | post inline |
| Before you begin gaps | internal |
| Editorial intro prose | internal |

LH detail: [learning-hub-standards.md § path landing](learning-hub-standards.md#path-landing-page).

---

## Learning Hub structure (Phase 1)

Walk [learning-hub-standards.md](learning-hub-standards.md) after manifest/depends checks. **Default tier: internal.** Only promote to post inline when live test fails or compliance issue (e.g. hard cross-path dependency in step copy).

---

## `website.yaml`

Package `website.yaml` is authoritative ([docs/website-yaml-reference.md](../../../docs/website-yaml-reference.md)).

Missing fields vs peers → **internal**. Broken required fields that break publish → **post inline**. Confirmed 404 on supplementary links → **post inline**. Suspected bad links → **internal** until confirmed.

---

## Valid manifests

```bash
node {pathfinder-app}/dist/cli/cli/index.js validate --packages {path_dir}
```

CLI failure → **post inline**. Dependency chain: first hands-on `depends: []`.

---

## Targeting / recommender

Overly broad `targeting.match` → **internal**. No separate recommender PR.

---

## Legacy website source (optional, read-only)

Never flag missing website writes, `pathfinder_data`, or legacy markdown drift.

Prose not captured in package on conversion → **post inline**. Front matter mapping gaps → **internal**.

---

## PR type (Phase 0)

| Type | Signals | Phase 1 emphasis | Phase 2 scope |
|---|---|---|---|
| **new** | New `{slug}-lj/` | `website.yaml`, path root | All interactive milestones |
| **conversion** | Prose-heavy blocks, `/build-interactive-lj` | Legacy source compare | All interactive milestones |
| **update** | Existing package changes only | Touched milestones | Touched interactive first |

---

## Static-only reviews

`static-only: <reason>` at end of Phase 1 skips Phase 2.

| Situation | Allowed? |
|---|---|
| **new** / **conversion** with interactive milestones | **No** |
| **update** with only markdown / `website.yaml` | Yes, with reason |
| Practice / archaeology on merged PR | Yes, with reason |

Record `waive_live_testing: true` and `static_only_reason`. Never suggest APPROVE when waived. Summary mentions live test was skipped (one sentence).

---

## Reuse-live (prior evidence)

`reuse-live: <notes>` records Block Editor evidence that already exists so Phase 2 does not re-test every milestone. **Not** the same as static-only: you are claiming live evidence, not skipping it.

### When to use

| Situation | Use `reuse-live`? |
|---|---|
| Author dogfooding the skill as reviewer after already smoke-testing while authoring | Yes |
| Resume mid-review; Block Editor results already in the workbook / chat | Yes |
| Cold second-reviewer pass with no prior live test this PR | **No** — run Phase 2 normally |
| Want to skip live testing with no prior evidence | **No** — that is `static-only` (and forbidden on new/conversion interactive) |

### Rules

1. **Notes required.** Reject bare `reuse-live`. Notes must say what was tested, where (stack), and by whom when (e.g. `reuse-live: author smoke-tested all interactive milestones on learn.grafana.net during authoring 2026-07-10`).
2. **Allowed on new/conversion.** Unlike static-only, reuse-live is valid on interactive new/conversion PRs when prior evidence exists.
3. **Accepted at** Phase 1 checkpoint or Phase 2 setup (instead of `ready`).
4. **Agent steps when accepted:**
   - Set `reuse_live: true`, `reuse_live_notes: "<notes>"`, and `stack_state` if mentioned.
   - Fill `pathfinder.{milestone}` for interactive milestones in scope as `pass (reused — <short notes>)` unless notes call out a fail/partial; copy any known fails into the workbook.
   - Skip Playwright DOM loop and per-milestone Block Editor prompts.
   - Jump to Phase 3. Do not invent Show me / Do it results beyond what notes claim.
5. **Verdict:** never suggest **APPROVE** when `reuse_live` is true. Cap at **COMMENT**. A fresh second-reviewer Phase 2 can still APPROVE later.
6. **Summary:** one sentence that live results were reused from prior evidence (do not pretend this session re-ran Block Editor).

---

## Live testing prerequisites (Phase 2)

### Stack state

| Path pattern | Minimum stack | False-pass risk |
|---|---|---|
| Install / bootstrap | Fresh Cloud stack | Install vs Uninstall button |
| Connect + credentials | Real credential saved | Pre-setup UI missing |
| Permission-gated | Required RBAC | `exists-reftarget` fails |
| learn.grafana.net shared | Demo stack | May not match fresh/credentialed flows |

Record `stack_state` in state.

### Pathfinder pass ≠ resource created

`doIt: false` on save steps can pass without mutating stack. Note in workbook if downstream UI assumes post-setup state.

### Milestone start URL

1. First `on-page:/path` in milestone blocks
2. Path manifest `startingLocation`
3. Ask reviewer if ambiguous

---

## Supplementary content

Duplicated `side_journeys` in `website.yaml` and `content.json` → **internal**. Recap referencing framing not in path `milestones` → **internal**.

---

## CODEOWNERS

New path not in CODEOWNERS → **discard** (mention in workbook only if reviewer asks).

---

## noop and non-interactive steps

`noop` creates a **numbered** step with no automation. It is not a fallback for missing selectors.

### Reject (false noop) → prefer `markdown` or a real interactive step

| Pattern | Use instead |
|---|---|
| Learner action with no `reftarget` (open, click, type, fill, select, hover, save) | `markdown`, or restore `highlight` / `button` / `formfill` / `guided` if you have a stable selector |
| Flaky-selector workaround (“Pathfinder can’t highlight this, so noop”) | `markdown` (or `highlight` + `doIt: false` when a selector exists) |
| Observation / confirmation / pure explanation that should not be numbered | `markdown` |
| Outside a `section` | `markdown` |

Examples of false noops: “Open a dashboard…”, “In the **Label** field, enter…”, “Hover the panel menu, then click **Edit**.”

When obvious from JSON or confirmed in Block Editor → **post inline**. Deduplicate path-wide (one comment listing milestones).

### Accept `noop` only when

| Pattern | Notes |
|---|---|
| Intentional numbered pause that is **not** a click/type instruction | e.g. “Wait for the query to finish”, “Confirm the preview looks right before you continue” |
| Optional `reftarget` to draw attention without requiring a click | Look-at context only; copy must not say “click / enter / select …” |

Route: accepted `noop` → no finding. False noop → **post inline**.

Phase 2 always asks the reviewer to scan for numbered learner-action noops (see [section intro Phase 2](#phase-2--confirm)), even when static detect missed them.

---

## GitHub posting (Phase 3)

Apply [finding routing](#finding-routing) and [comment-style.md](comment-style.md).

1. Every **author-facing** fix is a short inline on the file (path-wide OK). Draft those in chat first.
2. Reviewer approves (`post all`, `post 1,2`, `skip`, or edits).
3. Post only approved comments to draft review.
4. Summary is short acknowledgment only. No bulleted lists. No workbook content.

### Dedupe

- Same root cause, same file → one inline comment.
- Same root cause, multiple files → one per file, second references first.
- Playwright DOM + Block Editor fail on same step → one merged comment.

**Never post:** pass-only, N/A-only, internal tier, discard tier, em dashes, rule numbers. Never substitute a workbook dump for inline comments the author needs to act on.

---

## Verdict guidance (Phase 4)

The **reviewer** chooses the GitHub event. The agent suggests in plain language ([comment-style.md](comment-style.md#verdict-guidance-plain-language)):

| Situation | Suggest |
|---|---|
| Live-tested, zero inline comments posted | APPROVE or COMMENT |
| Live-tested, posted inline on real issues | COMMENT; REQUEST_CHANGES only if reviewer wants to block |
| Static-only | COMMENT only |
| Reuse-live | COMMENT only (never APPROVE) |
| Unsure | COMMENT |

REQUEST_CHANGES is rare. Do not run a decision tree. Do not list blockers in the summary to justify a verdict.
