---
name: review-learning-path
description: >-
  Guide a human reviewer through a learning path PR in interactive-tutorials —
  five phases from checkout through Block Editor smoke testing and GitHub submit.
  AI assists; the reviewer tests and approves comments. Use when the user runs
  /review-learning-path-pr.
---

# Review learning path PR

Help a **human reviewer** work through a `{slug}-lj/` pull request in **five phases**. You run static checks and draft comments; **the reviewer** smoke-tests in Block Editor and approves what posts to GitHub.

**This is not a full AI review.** You are a review coach, not the reviewer.

**Terminology:** Say **learning path** or **path** in reviewer messages; use `{path_dir}` in agent notes. Call live testing **Block Editor smoke test** (load via PR review tool in Block Editor dev tools).

**Entry command:** [/review-learning-path-pr](../../commands/review-learning-path-pr.md)

**Do NOT read external reference files upfront.** Each phase loads its own references on demand.

**Skill memory:** State lives in `.cursor/pr-review-state/` (gitignored). Phase 1 dispatches [audit-guide](../audit-guide/SKILL.md), which writes `{milestone}/assets/` on the PR branch. See [Commit safety](#commit-safety).

**Routing:** [reference-checks.md](reference-checks.md) · [comment-style.md](comment-style.md) · [learning-hub-standards.md](learning-hub-standards.md) · [github-review.md](github-review.md)

**Related:** [audit-guide](../audit-guide/SKILL.md) · [review-guide-pr.mdc](../../review-guide-pr.mdc)

---

## Human-in-the-loop contract

| You (agent) | Reviewer (human) |
|---|---|
| Check out PR, run audit + path checks | Confirm path, choose test stack |
| Write internal workbook | Skim workbook if curious; do not paste to author |
| Required Playwright DOM check per milestone | Log into Playwright (Okta) |
| Record DOM + smoke test results | Run Show me / Do it in Block Editor per milestone |
| Draft inline comments + summary **in chat** | Approve, edit, or skip before GitHub post |
| Post approved comments, submit when told | Choose APPROVE / COMMENT / REQUEST_CHANGES |

---

## Workflow overview

```
Input (PR URL or number)
  │
  ├─ Phase 0: Setup ───────────── checkout PR, infer path_dir
  │
  ├─ Phase 1: Static pass ─────── audit + path/LH checks → workbook (internal)
  │
  ├─ Phase 2: Live test ───────── required Playwright DOM + Block Editor smoke test
  │                              (skipped when static-only)
  │
  ├─ Phase 3: Draft review ────── draft comments + summary in chat; reviewer approves;
  │                              then post to GitHub draft review
  │
  └─ Phase 4: Submit ──────────── reviewer confirms verdict; publish
```

---

## Inputs

- **Required**: `pr_number` or GitHub PR URL for `grafana/interactive-tutorials`.
- **Optional**: `path_dir`, `website_slug`, `learn_host` (default `learn.grafana.net`).
- **Optional**: `waive_live_testing` — skip Phase 2. Requires `static-only: <reason>` at Phase 1 end. See [static-only reviews](reference-checks.md#static-only-reviews).
- **Optional**: `reuse_live` — record prior Block Editor evidence and skip per-milestone re-test. Requires `reuse-live: <notes>`. See [reuse-live](reference-checks.md#reuse-live-prior-evidence).

---

## Safety invariants

1. **Never modify author `content.json` or `manifest.json`.**
2. **Never post to GitHub before Phase 3 approval** from the reviewer.
3. **Never submit before Phase 4** explicit `submit` from the reviewer.
4. **Never commit review artifacts** — `.cursor/pr-review-state/` or audit-guide output under `{milestone}/assets/`.
5. **Never paste the workbook to the author** — `pr-{n}-findings.md` is reviewer-private.

---

## Commit safety

Same rules as before. Snapshot `pre_review_assets` before audit-guide; mandatory cleanup before Phase 1 checkpoint; verify `git status --porcelain -- {path_dir}` shows no untracked audit files.

Re-verify commit safety after Phase 1 before Phase 2.

---

## How this skill runs

1. Announce phase, what you're doing, why (2–3 sentences).
2. Do agent work (audit, Playwright, draft text).
3. Stop at checkpoint — one ask. **Do not advance** until the reviewer replies.
4. **Never batch phases.**

---

## Checkpoint format

| Section | Content |
|---|---|
| **Header** | `Phase {n} complete` + one-line outcome |
| **Summary** | Up to 3 plain-language bullets. No rule counts, no "blocking patterns." |
| **Your turn** | Exactly one action |
| **Up next** | One sentence |

**Reply keywords:** `yes` · `ready` · `static-only: <reason>` · `reuse-live: <notes>` · `pass` / `fail step N — …` / `partial — …` / `N/A — …` · `post all` / `post 1,2` / `skip` · `show summary` · `submit COMMENT` · `resume` / `start fresh`

**Tone:** Plain language. No audit jargon in chat. Say when things went cleanly.

---

## Resume

If `.cursor/pr-review-state/pr-{n}.json` exists:

> **Resume?** In-progress review for PR #{n} — stopped after phase {phase}.
>
> Reply **resume** or **start fresh**.

---

## Phase 0: Setup

**Goal:** Checkout PR, infer path, init state.

### Tell the reviewer

> **Phase 0 — Setup**
>
> Share the PR (URL or `#403`) from `grafana/interactive-tutorials`.

### Agent steps

1. `gh pr view` + `gh pr checkout`
2. Infer `{path_dir}`, `website_slug`, `pr_type`
3. Write `pr-{n}.json` with `pull_request_node_id` ([github-review.md](github-review.md))

### Checkpoint

> **Phase 0 complete** — PR #{n} on `{head_branch}` @ `{short_sha}`, path `{path_dir}` ({M} milestones), type `{pr_type}`.
>
> **Your turn:** Reply **yes** to start the static pass.

---

## Phase 1: Static pass

**Goal:** Audit every milestone + path consistency + Learning Hub checks. Output: **internal workbook only**.

Combines the former Phases 1–2 and workbook write.

### Tell the reviewer

> **Phase 1 — Static pass**
>
> I'm reading each milestone and checking manifests, `website.yaml`, and Learning Hub structure. Nothing goes to GitHub. I'll save notes to your private workbook.

### Agent steps

1. Snapshot `pre_review_assets`; dispatch [audit-guide](../audit-guide/SKILL.md) per milestone (parallel OK).
2. Walk all [reference-checks.md](reference-checks.md) checklists + [learning-hub-standards.md](learning-hub-standards.md).
3. **Always scan** for [section intro markdown that may number as a step](reference-checks.md#section-intro-markdown-numbered-as-step) and [false noops](reference-checks.md#noop-and-non-interactive-steps). Put matches under **Verify in Block Editor**.
4. Run Pathfinder CLI validate if available.
5. Tag every finding with [finding routing](reference-checks.md#finding-routing): **post inline**, **internal**, or **discard**.
6. Write `pr-{n}-findings.md` — header: *"Reviewer workbook — internal only. Do not paste to PR."*
   - **Verify in Block Editor** — items that need live test to confirm (include section-intro markdown and false-noop candidates)
   - **Post inline if confirmed** — static compliance issues (broken depends, id mismatch, CLI fail)
   - **Internal** — nits, LH editorial, selector polish, `website.yaml` gaps
7. Mandatory audit cleanup; verify `git status`.
8. **Do not** cite rule numbers or blocking counts in chat.

### Checkpoint

> **Phase 1 complete** — static pass done.
>
> - {One plain sentence: e.g. "A few things to verify when you smoke-test" or "Looks clean statically."}
> - Workbook: `.cursor/pr-review-state/pr-{n}-findings.md` *(for you, not the author)*
>
> **Your turn:** Reply **yes** and your test stack (e.g. `learn.grafana.net shared`, `fresh Cloud stack`, `Azure credentialed`).
>
> Or **`static-only: <reason>`** to skip live testing (not on **new** / **conversion** interactive PRs).
>
> Or **`reuse-live: <notes>`** when Block Editor evidence already exists (author dogfood, earlier in-thread pass). See [reuse-live](reference-checks.md#reuse-live-prior-evidence).
>
> **Up next:** Block Editor smoke test with required Playwright DOM check per milestone *(or draft review if static-only / reuse-live)*.

Record: `stack_state`, or `waive_live_testing` + `static_only_reason`, or `reuse_live` + `reuse_live_notes` (+ `stack_state` when known).

**Reject** bare `static-only` and static-only on **new** / **conversion** with interactive milestones. **Reject** bare `reuse-live` (notes required).

---

## Phase 2: Live test (Block Editor smoke test)

**Goal:** Reviewer smoke-tests each milestone. **Required Playwright DOM check** runs before each milestone's Block Editor test.

Skipped when `waive_live_testing` is true → jump to Phase 3.

Skipped when `reuse_live` is true → record prior evidence, fill `pathfinder` from notes / workbook, jump to Phase 3. Do **not** re-prompt per milestone. See [reuse-live](reference-checks.md#reuse-live-prior-evidence).

### Setup (tell the reviewer once)

> **Phase 2 — Live test**
>
> Two browsers:
> - **Playwright** (Okta login): I use this for required DOM checks per milestone.
> - **Your normal browser**: Block Editor smoke test.
>
> **Playwright:** Log into `{learn_host}` with Okta. Reply **ready** when logged in.
>
> **Block Editor:** Open `{learn_host}/plugins/grafana-pathfinder-app?dev=true` → **?** → Debug → Block Editor → dev tools → **PR review tool** → point at PR #{n}.
>
> Stack: `{stack_state}`
>
> Reply **ready** when both are set up. I won't ask you to test a milestone until you do.
>
> Or **`reuse-live: <notes>`** if Block Editor was already run for this PR (dogfood / resume) and you have evidence to record.

**Wait for:** `ready` or `reuse-live: <notes>`.

### Milestone scope

| `pr_type` | Scope |
|---|---|
| **new** / **conversion** | Every interactive milestone in path `milestones` |
| **update** | PR-touched interactive milestones first; full path on request |

### Per-milestone loop

For each milestone in scope (path order; skip prose-only / terminal):

**Step A — Required Playwright DOM (agent):**

1. Derive start URL ([milestone start URL](reference-checks.md#milestone-start-url)).
2. Navigate; check each `reftarget`: exists / missing / below-fold / state-dependent.
3. Record in `playwright.{milestone-slug}`.
4. Briefly tell reviewer DOM result (one line) before Block Editor prompt.

**Step B — Block Editor smoke test (reviewer):**

> **Milestone {i} of {M}: `{milestone-id}`**
>
> Open `{derived_start_url}`, then run every **Show me** and **Do it** in Block Editor.
>
> If earlier milestones used `doIt: false` on save or credential steps, run **Do it** on those before testing downstream UI, or note the stack was already configured.
>
> Also scan the section step list for **false step numbers**: intro prose numbered as step 1 (for example "You'll …"), or learner-action `noop`s numbered as interactive steps. Say so in your reply if you see either.
>
> **Your turn:** Reply **pass**, **fail step N —** *what happened*, **partial —** *what failed / what passed*, or **N/A —** *reason*.

Record in `pathfinder.{milestone-slug}`. Advance only after reviewer replies.

**Do not** post GitHub comments during Phase 2.

### Checkpoint

> **Phase 2 complete** — smoke test done.
>
> - Passed: [short list or *all*]
> - Failed: [short list or *none*]
> - N/A: [short list or *none*]
>
> **Your turn:** Reply **yes** and I'll draft comments in chat for your approval.
>
> **Up next:** Draft review (nothing posts to GitHub until you approve).

---

## Phase 3: Draft review

**Goal:** Draft inline comments + summary **in chat**. Reviewer approves. Then post to GitHub.

### Tell the reviewer

> **Phase 3 — Draft review**
>
> I'll draft any inline comments and a short summary here in chat. Nothing posts to GitHub until you approve.

### Agent steps

1. From workbook + Phase 2 results, identify **post inline** items only ([finding routing](reference-checks.md#finding-routing)):
   - Runtime failures you or the reviewer hit in Block Editor
   - Playwright missing selector **when** Block Editor also failed (merge into one comment)
   - Static compliance: broken depends/framing, id mismatch, CLI validate fail, secrets auto-filled, confirmed 404, prose missing on conversion
2. **Drop all internal and discard tier items** unless reviewer explicitly says to post one.
3. Apply [selector decision tree](reference-checks.md#selector-decision-tree) — do not post selector nits when smoke test passed.
4. Draft numbered inline comments in chat using [comment-style.md](comment-style.md). **No em dashes.** Max 3 sentences each.
5. Draft summary in chat using [summary template](comment-style.md#summary-body-template). No bulleted blocker lists.
6. **Zero comments + APPROVE is first-class** — when static + live passed and nothing is post-inline, suggest APPROVE (complete clean review). Do not invent nits.
7. Offer [verdict guidance](comment-style.md#verdict-guidance-plain-language) in plain language.

### Checkpoint

> **Phase 3 — drafts for your approval**
>
> **Inline comments** *(post inline tier only):*
>
> 1. `{path}:{line}` — {draft text}
> 2. …
>
> *(or: No inline comments — smoke test passed, nothing blocking.)*
>
> **Summary:**
> {draft summary}
>
> **Verdict suggestion:** {plain language, e.g. "APPROVE looks right" or "COMMENT if you want to share notes without blocking"}
>
> **Your turn:** Reply **post all**, **post 1,2**, **skip** (summary only), or paste edits.

### After approval

1. Create GitHub draft review (GraphQL `addPullRequestReview`) if not already created.
2. Post **only approved** inline comments.
3. Save final summary to `pr-{n}-review-body.md`.
4. Update state: `comment_count`, `phase: 3`.

> **Phase 3 complete** — {N} comment(s) posted to draft review.
>
> **Your turn:** Reply **show summary** to re-read the summary, or continue to submit.
>
> **Up next:** Phase 4 — you pick the verdict and we publish.

---

## Phase 4: Submit

**Goal:** Reviewer confirms verdict; publish.

### Checkpoint

> **Phase 4 — Submit**
>
> Summary is in the draft review. {N} inline comment(s) on the diff.
>
> Suggested verdict: {plain language}.
>
> **Your turn:** Reply **submit APPROVE**, **submit COMMENT**, or **submit REQUEST_CHANGES**.

### Agent steps

1. Print summary when reviewer asks **show summary**.
2. Apply reviewer edits to `pr-{n}-review-body.md`.
3. GraphQL `submitPullRequestReview` with reviewer's verdict.
4. Update state: `status: submitted`, `verdict`, `review_url`.

> **Review submitted:** {url}
>
> This cycle is complete. For follow-up after the author pushes, start a new review.

---

## Post-submit (ad hoc)

Not a numbered phase. New review cycle for major author pushes. Use REST inline or conversation comments per [github-review.md](github-review.md).

---

## Anti-patterns

**Do not**

- Post to GitHub before Phase 3 approval
- Post nits, LH editorial, or selector polish when smoke test passed
- Use em dashes, rule numbers, or **Blocker** labels in GitHub text
- Paste workbook contents into summary or inline comments
- List blockers/nits in the summary body
- Cite blocking counts or audit severity in reviewer chat
- Recommend APPROVE when `waive_live_testing` is true
- Recommend APPROVE when `reuse_live` is true (prior evidence is not a fresh second-reviewer pass in this session)
- Skip required Playwright DOM check per milestone (unless static-only or reuse-live)
- Submit from GitHub UI without pasting summary (body will be blank)

**Do**

- Draft in chat first; reviewer approves before post
- Keep summary to 3–5 sentences
- Default to APPROVE or COMMENT; REQUEST_CHANGES only when reviewer wants to block
- Dedupe inline comments to one per root cause
- Let zero inline comments be a valid outcome

---

## Generated files

| File | Phase | Purpose |
|---|---|---|
| `pr-{n}.json` | 0+ | State ([schema](github-review.md#state-file-schema)) |
| `pr-{n}-findings.md` | 1 | **Internal workbook** — never paste to author |
| `pr-{n}-review-body.md` | 3 → 4 | Final summary for GitHub submit |

Workbook frontmatter:

```markdown
---
disclaimer: Reviewer workbook — internal only. Do not paste to PR or author.
notice: Auto-generated by review-learning-path skill.
pr_number: {n}
---
```

---

## Deep references

| Topic | Doc |
|---|---|
| Finding routing + checklists | [reference-checks.md](reference-checks.md) |
| Comment voice + summary | [comment-style.md](comment-style.md) |
| Learning Hub checks (workbook) | [learning-hub-standards.md](learning-hub-standards.md) |
| GitHub GraphQL | [github-review.md](github-review.md) |
