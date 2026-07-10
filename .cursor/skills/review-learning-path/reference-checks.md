# Reference checks

Checklists for [review-learning-path/SKILL.md](SKILL.md) Phase 1 (static pass). Findings land in `pr-{n}-findings.md` — **reviewer workbook only**, never pasted to the author.

**Comment voice:** [comment-style.md](comment-style.md)

**Selector authority:** [docs/selectors-and-testids.md](../../../docs/selectors-and-testids.md). Do not apply build-interactive-lj autogen "never `:contains()`" rules to hand-authored guides.

**Publishing model (PR [#416](https://github.com/grafana/interactive-tutorials/pull/416)):** LP PRs are single-repo. Package `website.yaml` is authoritative; website repo is read-only for conversion.

**Learning Hub:** [learning-hub-standards.md](learning-hub-standards.md) — checks run in Phase 1; default tier is **internal** (workbook only).

---

## Finding routing

Tag every finding when writing the workbook. Only **post inline** items may become GitHub comments (after reviewer approval at Phase 3).

| Post inline | Internal (workbook only) | Discard |
|---|---|---|
| Block Editor / Playwright runtime fail (reviewer-reported) | Section bookends missing when live passed | Audit noise with no runtime impact |
| In-section intro markdown confirmed numbered as a step in Block Editor | In-section intro markdown (static detect only; not yet live-confirmed) | |
| Broken `depends` chain or framing in path `milestones` | `website.yaml` metadata gaps | CODEOWNERS reminder |
| Missing `exists-reftarget`, `navmenu-open` **when live fails** | `:contains()` fallback when live passed | Pathfinder shell UX |
| Outdated `data-testid` when live fails | LH editorial (boilerplate, prerequisites, CTA) | Passed-milestone notes |
| `:contains()` when stable `data-testid` in DOM and live fails | Selector polish when live passed | Fresh-stack retest notes (unless live failed) |
| Path root / manifest `id` mismatch | Vague copy when live passed | Suspected bad link (unverified) |
| Pathfinder CLI validate failure | `related_journeys` wording | |
| `index.json` modified, invalid `testEnvironment.tier` | Editorial / tooltip / vocabulary | |
| Secrets auto-filled (`doIt: true`) | Conversion `website.yaml` mapping gaps | |
| Hard cross-path artifact dependency in step copy | Missing troubleshooting on verification (when live passed) | |
| Confirmed 404 in `website.yaml` supplementary fields | Landing screenshot / milestone count notes | |
| Prose only in legacy markdown (conversion PR) | Framing snippet alignment | |

**After live test:** promote **internal** items to **post inline** only when Block Editor or required Playwright DOM failed, or the issue is clearly wrong regardless of runtime (e.g. `id` mismatch, broken depends).

**Never post:** anything in **internal** or **discard** unless the reviewer explicitly promotes it at Phase 3.

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
| Section bookends missing (rule 14) | internal until live fails |
| In-section intro markdown that may number as a step | **internal** until Block Editor confirms; then **post inline** (see [section intro markdown](#section-intro-markdown-numbered-as-step)) |
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

Missing bookends (no intro/summary at all) stay a separate **internal** finding. This check is the opposite problem: intro exists but Pathfinder treats it like a step.

### Phase 2 — confirm

When prompting Block Editor for a flagged milestone, ask the reviewer to notice whether the section's first "You'll…" (or similar) line is numbered.

| Live result | Route |
|---|---|
| Numbered as a step | **Post inline** |
| Unnumbered prose | Discard this finding for that milestone |

### Phase 3 — comment shape

- **One path-wide inline** when the same pattern appears in multiple milestones. Anchor on the first clear example; list the other milestone slugs in the comment body.
- Fix: move the intro markdown **outside** (before) the `section` block, or drop it if the section title is enough. Keep a one-sentence summary bookend (outside or after the section) so rule 14 intent is preserved without a fake step 1.

---

## Framing milestones

Framing packages must **not** appear in path `manifest.json` `milestones`. First hands-on `depends` must not reference framing IDs.

Framing in path `milestones` or broken depends → **post inline**.

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

`noop` misuse → **post inline** if it breaks interactivity; else **internal**.

**False noops (learner actions without `reftarget`):** steps that tell the learner to click, type, or open UI but use `action: "noop"` with no selector. Prefer `markdown` (or a real highlight). When confirmed in Block Editor or obvious from JSON → **post inline**. Deduplicate path-wide like section-intro markdown.

---

## GitHub posting (Phase 3)

Apply [finding routing](#finding-routing) and [comment-style.md](comment-style.md).

1. Draft all inline comment text **in chat** first.
2. Reviewer approves (`post all`, `post 1,2`, `skip`, or edits).
3. Post only approved comments to draft review.
4. Summary is short acknowledgment only. No bulleted lists.

### Dedupe

- Same root cause, same file → one inline comment.
- Same root cause, multiple files → one per file, second references first.
- Playwright DOM + Block Editor fail on same step → one merged comment.

**Never post:** pass-only, N/A-only, internal tier, discard tier, em dashes, rule numbers.

---

## Verdict guidance (Phase 4)

The **reviewer** chooses the GitHub event. The agent suggests in plain language ([comment-style.md](comment-style.md#verdict-guidance-plain-language)):

| Situation | Suggest |
|---|---|
| Live-tested, zero inline comments posted | APPROVE or COMMENT |
| Live-tested, posted inline on real issues | COMMENT; REQUEST_CHANGES only if reviewer wants to block |
| Static-only | COMMENT only |
| Unsure | COMMENT |

REQUEST_CHANGES is rare. Do not run a decision tree. Do not list blockers in the summary to justify a verdict.
