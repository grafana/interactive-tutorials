---
name: review-learning-path
description: >-
  Guide a reviewer through a learning path PR in interactive-tutorials — nine phases
  from checkout through audit, live testing, and GitHub submit. Use when the user
  runs /review-learning-path-pr.
---

# Review learning path PR

Guide a reviewer through a `{slug}-lj/` pull request in **nine phases** — static audit, path checks, live testing, and GitHub submit. Narrate each step, run automated checks, and **pause at every checkpoint** for the reviewer's reply. Read-only on guide JSON.

**Terminology:** Say **learning path** or **path** in reviewer messages; use `{path_dir}` (package directory) in agent notes. A **draft review** is the GitHub pending review that holds comments until submit.

**Entry command:** [/review-learning-path-pr](../../commands/review-learning-path-pr.md)

**Do NOT read external reference files upfront.** Each phase loads its own references on demand. Everything the orchestrator needs to start is inline below.

**Skill memory:** Review-owned state lives in `.cursor/pr-review-state/` (gitignored). Phase 1 dispatches [audit-guide](../audit-guide/SKILL.md), which **writes** `{milestone}/assets/` inside package directories on the checked-out PR branch. Those files are not review-owned state — see [Commit safety](#commit-safety). Snapshot before audit, delete new audit files before leaving Phase 1, and verify `git status` stays clean.

**Severity:** [finding severity routing](reference-checks.md#finding-severity-routing) in this skill **supersedes** [audit-guide/severity-rubric.md](../audit-guide/severity-rubric.md) for Phase 3 bucketing and Phase 7 inline vs body decisions. audit-guide blocking/warning/info still applies during Phase 1; re-tag findings with this skill's routing before Phase 7.

**Checklists:** [reference-checks.md](reference-checks.md) · [learning-hub-standards.md](learning-hub-standards.md) · **GitHub API:** [github-review.md](github-review.md)

**Related:** [audit-guide](../audit-guide/SKILL.md) · [review-guide-pr.mdc](../../review-guide-pr.mdc)

**Example:** [PR #403](https://github.com/grafana/interactive-tutorials/pull/403) (`monitor-azure-resources-lj`)

---

## Workflow overview

```
Input (PR URL or number)
  │
  ├─ Phase 0: Get PR & checkout ── orchestrator (gh, infer path_dir)
  │
  ├─ Phase 1: Per-milestone audit ── dispatch audit-guide per milestone (parallel OK)
  │
  ├─ Phase 2: Path consistency ──── orchestrator (manifest, framing, website.yaml)
  │
  ├─ Phase 3: Findings doc ──────── merge static results; choose live test or static-only
  │
  ├─ Phase 4: Draft GitHub review ─ then Playwright login (or Phase 7 if static-only)
  │
  ├─ Phase 5: Playwright DOM ────── skipped when static-only
  │
  ├─ Phase 6: Pathfinder PR tool ── skipped when static-only
  │
  ├─ Phase 7: Consolidate comments ─ orchestrator → inline + review-body.md
  │
  ├─ Phase 8: Reviewer approval ─── orchestrator
  │
  └─ Phase 9: Submit ────────────── orchestrator (workflow ends)
       Phase 10: optional post-submit follow-ups
```

---

## Inputs

- **Required**: `pr_number` or GitHub PR URL for `grafana/interactive-tutorials` — supplied by the reviewer at Phase 0.
- **Optional**: `path_dir` — `{slug}-lj/` package directory. Inferred from changed files; confirm with reviewer if ambiguous.
- **Optional**: `website_slug` — `{path_dir}` minus `-lj`. When the `website` repo is in workspace, use only to **read** legacy markdown for conversion-review context ([PR #416](https://github.com/grafana/interactive-tutorials/pull/416)). Not a second PR target.
- **Optional**: `learn_host` — live test host (default `learn.grafana.net`).
- **Optional**: `waive_live_testing` — reviewer explicitly accepts static-only review; skip Phases 5–6.

If the user invokes `/review-learning-path-pr` with no arguments, start Phase 0 and ask for the PR.

---

## Safety invariants

These rules are **inviolable** during a review run:

1. **Never modify author `content.json` or `manifest.json`.** Read-only on guide JSON.
2. **Never post GitHub inline comments before Phase 7.**
3. **Never submit a review before Phase 8 approval** from the reviewer.
4. **Never commit review artifacts** — `.cursor/pr-review-state/` (gitignored) or audit-guide output under `{milestone}/assets/`. See [Commit safety](#commit-safety).
5. **One draft review per cycle** — after Phase 9 submit, start a new cycle for major follow-ups.

---

## Commit safety

This skill runs on the **author's checked-out branch** (`gh pr checkout`). Ask: *under what circumstances could a review artifact get committed?*

| Artifact | Where written | Risk | Mitigation |
|---|---|---|---|
| Findings, review body, state JSON | `.cursor/pr-review-state/` | Staged by mistake | `.gitignore` |
| audit-guide reports | `{milestone}/assets/` | Untracked `??` files staged with PR fixes | Snapshot + mandatory cleanup (Phase 1); gitignore audit filenames |
| Pre-existing package `assets/` | Author/migrate (e.g. `migration-notes.md`) | Deleted by careless cleanup | Snapshot — never delete files that existed before Phase 1 |

**Never commit:** audit-guide outputs, `.cursor/pr-review-state/`, or any file created only during this review run.

### Phase 1 snapshot (before audit-guide)

For each milestone directory to audit, record existing asset paths in state:

```bash
find {milestone}/assets -type f 2>/dev/null | sort
```

Store under `pre_review_assets` in `pr-{n}.json` — a map of milestone slug → file path list. See [github-review.md](github-review.md#state-file-schema).

### Phase 1 cleanup (mandatory — before Phase 1 checkpoint)

After extracting findings from each audit report:

1. Copy `audit-report.md` to `.cursor/pr-review-state/pr-{n}/audits/{milestone-slug}/` if you need a local audit trail (optional).
2. Under each audited `{milestone}/assets/`, **delete every file not listed** in that milestone's `pre_review_assets` snapshot (includes all audit-guide outputs: `audit-input.json`, `*-report.md`, `manifest.yaml` when new, `history/`).
3. Remove empty `assets/` directories only if the directory did not exist in the snapshot.

**Do not advance past Phase 1** until verification passes:

```bash
git status --porcelain -- {path_dir}
```

Must show **no untracked** (`??`) audit-guide paths under milestone `assets/`. Report remaining paths to the reviewer and clean up before continuing.

### Re-verify before Phase 4

Run the same `git status` check on `{path_dir}` after Phase 3. Live testing does not write into package dirs, but confirm no audit artifacts reappeared.

---

## How this skill runs

1. Announce the **phase** (number and name), what you're doing, and why — keep it to 2–3 sentences.
2. Do agent-side work (audit, `gh`, Playwright, draft files).
3. Stop at the **checkpoint** — one message, one ask. **Do not advance** until the reviewer replies.
4. Post nothing to GitHub until **Phase 7**.

**Never batch phases.** If the reviewer says "keep going," pause at the next checkpoint anyway and confirm before continuing.

---

## Checkpoint format

Every phase ends with the same shape. Keep messages short and scannable.

| Section | What to include |
|---|---|
| **Header** | `Phase {n} of 9 complete` + one-line outcome |
| **Summary** | Up to 5 bullets — counts, pass/fail, top issues. Point to `pr-{n}-findings.md` instead of pasting long lists |
| **Your turn** | Exactly **one** action — a reply keyword or a short answer |
| **Up next** | One sentence preview of the next phase |

**Reply keywords**

| Keyword | When |
|---|---|
| `yes` | Confirm and continue (Phases 0–3, 4 static-only, 5, 6 wrap-up) |
| `ready` | Playwright logged in (after Phase 4) or PR review tool loaded (Phase 6 setup) |
| `static-only` | Skip live testing at Phase 3 |
| `pass` / `fail step N — …` / `N/A — …` | Per-milestone result in Phase 6 |
| `show body` | Print review body in chat (Phases 7–8) |
| `submit` | Publish review with verdict (Phase 8) |
| `resume` / `start fresh` | Pick up saved state or restart |

**Tone:** Address the reviewer as **you**. Use plain language — no rule numbers in chat unless they ask. Say when a phase went cleanly (*no blockers found*, *all milestones passed*). Use **draft review** (not "pending review") in reviewer-facing messages.

---

## Resume

If `.cursor/pr-review-state/pr-{n}.json` exists, read `phase` and `status`. Tell the reviewer:

> **Resume?** I have an in-progress review for PR #{n} — stopped after phase {phase} ({status}).
>
> Reply **resume** to pick up from phase {next}, or **start fresh** to begin again.

---

## Phase 0: Get the PR and checkout branch

**Goal:** Identify the PR, check out its branch, infer the path package, initialize state.

### Tell the reviewer

> **Phase 0 of 9 — Get the PR**
>
> Share the PR for this learning path — a GitHub URL or number (like `#403`) from `grafana/interactive-tutorials`. I'll check out the branch and identify the package.

**Wait for the PR** before continuing.

### Agent steps

1. Parse PR number from URL or `#403` input.
2. Run `gh pr view {n} --repo grafana/interactive-tutorials --json number,title,headRefName,headRefOid,url,files,id`.
3. Tell the reviewer: PR title, number, branch, HEAD sha.
4. Check out: `gh pr checkout {n}` (or fetch + checkout).
5. Infer `{path_dir}` from changed files (directory ending in `-lj`). If ambiguous, **ask**.
6. Infer `website_slug` = `{path_dir}` minus `-lj` if `website` repo is in workspace.
7. Infer `pr_type` — `new`, `conversion`, or `update` per [reference-checks.md § PR type](reference-checks.md#pr-type-phase-0).
8. List milestones under `{path_dir}/` and path root files.
9. Write `.cursor/pr-review-state/pr-{n}.json` with `pull_request_node_id` from the `id` field (GraphQL node ID for Phase 4). See [github-review.md](github-review.md).

### Checkpoint

> **Phase 0 of 9 complete** — PR #{n} checked out on `{head_branch}` @ `{short_sha}`.
>
> - Path: `{path_dir}` ({M} milestones)
> - Type: `{pr_type}`
> - Legacy slug (read-only): `{website_slug}` *(or website repo not in workspace)*
>
> **Your turn:** Reply **yes** if this looks right, or tell me what to fix.
>
> **Up next:** Static audit of each milestone — read-only, nothing posted to GitHub.

---

## Phase 1: Per-milestone audit

**Goal:** Run [audit-guide](../audit-guide/SKILL.md) on every milestone; apply [content checks](reference-checks.md#milestone-contentjson-checks).

### Tell the reviewer

> **Phase 1 of 9 — Static audit**
>
> I'm running audit-guide on each milestone in `{path_dir}`. This only reads files — nothing goes to GitHub yet.

### Agent steps

1. List milestones from path `manifest.json` `milestones` array **plus** any changed milestone dirs.
2. **Snapshot** — for each milestone, record existing `assets/` file paths in state (`pre_review_assets`). See [Commit safety](#commit-safety).
3. Dispatch [audit-guide](../audit-guide/SKILL.md) on each milestone directory (Explore sub-agent or Task, parallel OK). Skip framing-only packages not in path `milestones` unless PR changed them.
4. Apply every row in [reference-checks.md § content](reference-checks.md#milestone-contentjson-checks). Scan milestone prose against [learning-hub-standards.md § common pitfalls](learning-hub-standards.md#common-pitfalls) and [§ task milestones](learning-hub-standards.md#task-milestones-hands-on-guides).
5. Tag each finding with [finding severity routing](reference-checks.md#finding-severity-routing) — **Always inline**, **Defer**, or **Review body only**.
6. Summarize per milestone: verdict, blocking count, top issues (file + rule + fix + severity).
7. **Mandatory cleanup** — remove audit-guide files not in the Phase 1 snapshot. Verify `git status` on `{path_dir}`. See [Commit safety](#commit-safety).
8. **Do not** post to GitHub. **Do not** use `FROM AUDIT:` prefixes anywhere.

### Checkpoint

> **Phase 1 of 9 complete** — audited {X} milestones.
>
> - {B} blocking patterns across {N} milestones *(or: No blocking patterns found)*
> - Top issues: [up to 5 bullets — file, issue, severity]
>
> **Your turn:** Reply **yes** to continue, or flag anything I missed or that's out of scope.
>
> **Up next:** Path-level checks — manifest, `website.yaml`, Learning Hub structure.

---

## Phase 2: Path-level consistency

**Goal:** Validate path root `content.json`, manifests, package `website.yaml`, depends chain, framing rules, targeting, Learning Hub structure, optional legacy website read, CODEOWNERS.

### Tell the reviewer

> **Phase 2 of 9 — Path consistency**
>
> I'm checking the path root, manifests, `website.yaml`, dependency chain, and Learning Hub standards. If this is a conversion PR and the website repo is available, I'll compare against legacy source too.

### Agent steps

1. Run Pathfinder CLI if available: `validate --packages {path_dir}` (record pass/fail).
2. Walk [reference-checks.md](reference-checks.md): [path root content.json](reference-checks.md#path-root-contentjson), [Learning Hub structure](reference-checks.md#learning-hub-structure-phase-2) (full detail in [learning-hub-standards.md](learning-hub-standards.md)), [`website.yaml`](reference-checks.md#websiteyaml), framing, valid manifests, depends chain, targeting, [supplementary content](reference-checks.md#supplementary-content), [CODEOWNERS](reference-checks.md#codeowners), [legacy website source](reference-checks.md#legacy-website-source-optional-read-only) (when `pr_type` is `conversion`), [PR type](reference-checks.md#pr-type-phase-0) checks.
3. Spot-check outbound links from `side_journeys`, `related_journeys`, and `cta.troubleshooting` per [learning-hub-standards.md § outbound links](learning-hub-standards.md#outbound-link-verification).
4. Compare path `milestones` to peer LPs (depends chain, no framing in array, first hands-on `depends: []`).
5. Tag each finding with [severity routing](reference-checks.md#finding-severity-routing).
6. Note `website.yaml` gaps and conversion mapping issues in findings (review body — not separate website PR blockers).

### Checkpoint

> **Phase 2 of 9 complete** — path consistency pass done.
>
> - [2–4 bullets: framing, depends chain, `website.yaml`, CLI validate, legacy source if checked]
>
> **Your turn:** Reply **yes** and I'll write the findings doc.
>
> **Up next:** Merge Phases 1–2 into `pr-{n}-findings.md`.

---

## Phase 3: Internal findings document

**Goal:** Merge Phases 1–2 into one reviewer-facing doc. Still no GitHub comments.

### Tell the reviewer

> **Phase 3 of 9 — Findings doc**
>
> I'm merging the audit and consistency results into `.cursor/pr-review-state/pr-{n}-findings.md`.

### Agent steps

Write `pr-{n}-findings.md` using [finding severity routing](reference-checks.md#finding-severity-routing):

- **Runtime blockers (always inline)** — dedupe by root cause; Phase 5–6 failures; manifest/depends/framing breaks; selector fails live
- **Selector notes** — audit rule 2 / `:contains()` findings; apply [selector decision tree](reference-checks.md#selector-decision-tree) — body-only when Pathfinder passed and fallback is justified
- **Live-test candidates** — selectors and milestones for Playwright + Pathfinder
- **Defer until after Pathfinder** — findings in the **Defer** column only
- **Review body only** — `website.yaml` metadata gaps, Learning Hub editorial (boilerplate, prerequisites, CTA type, troubleshooting), CODEOWNERS, editorial, passed-milestone notes
- **Waived / N/A** — terminal milestones; fresh-stack retest notes; stack-state caveats per [live testing prerequisites](reference-checks.md#live-testing-prerequisites-phases-56)

Each listed finding includes severity tag and source phase (1, 2, 5, or 6).

Apply the [generated-file frontmatter](SKILL.md#generated-files) to `pr-{n}-findings.md`.

Update state: `"phase": 3`.

**Re-verify commit safety** — `git status --porcelain -- {path_dir}` shows no untracked audit-guide files under milestone `assets/`. See [Commit safety](#commit-safety).

### Checkpoint

> **Phase 3 of 9 complete** — findings doc is ready.
>
> - Blockers before live test: [short list or *none*]
> - Milestones to live-test: [list]
> - Deferred until Pathfinder: [list or *none*]
>
> Full detail: `.cursor/pr-review-state/pr-{n}-findings.md`
>
> **Your turn:** Reply **yes** and tell me your test stack — for example `learn.grafana.net shared`, `fresh Cloud stack`, or `Azure credentialed`. Install and credential paths often need more than the default learn stack.
>
> Or reply **static-only** to skip live testing (Phases 5–6).
>
> **Up next:** Draft GitHub review — then Playwright and Pathfinder *(or straight to comments if static-only)*.

Record the reviewer's reply in state:
- **yes** + stack description → `stack_state`
- **static-only** → `waive_live_testing: true`

See [live testing prerequisites](reference-checks.md#live-testing-prerequisites-phases-56).

---

## Phase 4: Draft GitHub review

**Goal:** Create one GitHub draft review (pending until submit) to hold inline comments.

### Tell the reviewer

> **Phase 4 of 9 — Draft GitHub review**
>
> I'm creating a draft review on PR #{n}. Comments stay hidden from the author until we submit at the end.

### Agent steps

1. GraphQL `addPullRequestReview` (no `event`), body: `Review in progress.` Use `pullRequestId: {pull_request_node_id}` from state (set in Phase 0).
2. Store `pending_review_id` and `pending_review_node_id` from the mutation response in state file.
3. **Do not** add inline comments yet (Phase 7).

See [github-review.md](github-review.md).

### Checkpoint

Use one of these messages depending on state.

**Static-only** (`waive_live_testing: true`):

> **Phase 4 of 9 complete** — draft review created on PR #{n}.
>
> **Your turn:** Reply **yes** to draft GitHub comments from static findings.
>
> **Up next:** Phase 7 — inline comments and review body *(live testing skipped)*.

**Live testing** (default):

> **Phase 4 of 9 complete** — draft review created on PR #{n}.
>
> **Your turn:** Log into the **Playwright** browser with Okta *(separate from your everyday browser)* and open `{learn_host}`. Reply **ready** when you're logged in.
>
> Stack: `{stack_state}`
>
> **Up next:** Phase 5 — DOM check for selectors.

**Wait for:** `yes` (static-only → Phase 7) or `ready` (live testing → Phase 5). Do not run Playwright until the reviewer replies **ready**.

---

## Phase 5: Playwright DOM verification

**Goal:** Verify selectors exist on `{learn_host}` @ PR HEAD for the recorded stack state.

### Tell the reviewer

> **Phase 5 of 9 — Playwright DOM check**
>
> Checking selectors on `{learn_host}` for stack: `{stack_state}`.

The reviewer should already be logged in from Phase 4. If they reply **ready** before you send this, acknowledge and begin agent steps.

### Agent steps

For each **interactive milestone** in path order:

1. Derive start URL — first `on-page:/path` in milestone blocks, else path manifest `startingLocation` ([reference](reference-checks.md#milestone-start-url-phase-6)).
2. Navigate to that URL (or milestone-specific page from `on-page` requirements).
3. Check each `reftarget`: exists / missing / below-fold / **state-dependent** (present only after prior setup).
4. Record results @ `{head_sha}` and `stack_state`.
5. If a selector is missing, check whether [live testing prerequisites](reference-checks.md#live-testing-prerequisites-phases-56) explain it (pre-credential UI, fresh-stack install) before treating as blocker.

**Do not** post pass-only GitHub comments. **Do not** open Block Editor, load guides, or start Pathfinder — that is Phase 6 only.

### Checkpoint

> **Phase 5 of 9 complete** — DOM check done @ `{short_sha}`.
>
> - Failures: [list or *none*]
> - Below fold *(may still pass Pathfinder)*: [list or *none*]
>
> **Your turn:** Reply **yes** to continue to Pathfinder setup.
>
> **Up next:** Phase 6 — PR review tool setup, then Show me / Do it per milestone.

**Wait for:** `yes` before sending Phase 6 setup instructions.

---

## Phase 6: Pathfinder interactivity (PR review tool)

**Goal:** Reviewer exercises Show me / Do it for each milestone; agent records results.

### Tell the reviewer (setup only — no milestone testing yet)

> **Phase 6 of 9 — Pathfinder PR review tool**
>
> In your **normal browser** (not Playwright):
> 1. Open `{learn_host}/plugins/grafana-pathfinder-app?dev=true` *(Pathfinder 1.4.5+)*
> 2. **?** → Debug → Block Editor → dev tools → **PR review tool**
> 3. Point it at PR #{n} in `grafana/interactive-tutorials`
>
> Test milestones **in path order** on: `{stack_state}`. See [live testing prerequisites](reference-checks.md#live-testing-prerequisites-phases-56) if install or credential steps need a specific stack.
>
> Reply **ready** when the tool is loaded. I won't ask you to test a milestone until you do.

**Wait for:** `ready`.

**Do not before `ready`:** navigate to a milestone, load a guide in Block Editor, run Show me / Do it, or smoke-test the first milestone.

### Per-milestone loop

Start only after setup **ready**. For each milestone in path `milestones` (skip terminal-only, e.g. external CLI) **in order**:

**Prompt reviewer (one milestone at a time — never repeat a milestone already reported):**

> **Milestone {i} of {M}: `{milestone-id}`**
>
> Open `{derived_start_url}`, then run every **Show me** and **Do it** in the PR review tool.
>
> If earlier milestones used `doIt: false` on save or credential steps, run **Do it** on those before testing downstream UI — or note the stack was already configured.
>
> **Your turn:** Reply **pass**, **fail step N —** *what happened*, or **N/A —** *reason*.

**Agent:** record in `pr-{n}.json` → `pathfinder.{milestone-slug}`. Advance to the next milestone only after the reviewer replies.

**Do not** post inline pass/N/A comments. N/A with stack caveat → note for review body ([fresh-stack retest](reference-checks.md#live-testing-prerequisites-phases-56), credentialed retest).

### Checkpoint

> **Phase 6 of 9 complete** — Pathfinder testing done.
>
> - Passed: [list or *none*]
> - Failed: [list or *none*]
> - N/A: [list or *none*]
>
> **Your turn:** Reply **yes** and I'll draft GitHub comments *(failures and blockers only)*.
>
> **Up next:** Inline comments + review body.

---

## Phase 7: Consolidate GitHub comments

**Goal:** Add inline comments + draft review body. Apply [severity routing](reference-checks.md#finding-severity-routing) and [comment policy](reference-checks.md#github-comment-policy).

### Tell the reviewer

> **Phase 7 of 9 — Draft GitHub comments**
>
> I'm adding inline comments for blockers and writing the review body. Steps that passed won't get inline comments.

### Agent steps

1. Re-fetch PR HEAD if author may have pushed; reconcile resolved threads.
2. From `pr-{n}-findings.md`, promote **Defer** items to inline only if Phase 5–6 failed; drop deferred items Pathfinder passed.
3. Re-tag audit-only `:contains()` findings with the [selector decision tree](reference-checks.md#selector-decision-tree) — do **not** inline when Pathfinder passed and no stable selector exists in DOM.
4. Dedupe to [one comment per root cause](reference-checks.md#one-comment-per-root-cause) before posting.
5. Add inline comments via GraphQL `addPullRequestReviewComment` — **Always inline** + runtime failures only. **Ask the reviewer to confirm** before inlining any finding that is audit-only (no live failure).
6. Merge Playwright + Pathfinder evidence, and merge code fix + runtime symptom when they share a root cause (never two inline threads on the same file for the same bug).
7. Write `.cursor/pr-review-state/pr-{n}-review-body.md` with **Review body only** findings, passed milestones, and retest notes. List runtime merge blockers under **Must fix before merge**; put justified `:contains()` fallbacks and selector polish under **Optional follow-ups**. Apply the [generated-file frontmatter](SKILL.md#generated-files).
8. Recommend a default [verdict](reference-checks.md#verdict-selection-phases-89) from findings (`REQUEST_CHANGES`, `COMMENT`, or `APPROVE`) with a one-sentence reason. If all Pathfinder milestones passed and no runtime blockers remain, default to **COMMENT** or **APPROVE**, not REQUEST_CHANGES. Store in state: `"recommended_verdict"`.
9. Update state: `comment_count`, `"phase": 7`.

### Comment tone (required)

Write like a human reviewer talking to the author — not an audit report.

- Lead with what you tested and what happened.
- Reserve **Blocker** for runtime failures or broken manifest/depends/framing — not audit-only `:contains()` when Pathfinder passed.
- Selector polish: one plain sentence; link [selectors-and-testids.md](../../../docs/selectors-and-testids.md) when helpful; put in the **review body** when the step passed live.
- Mention host/sha once in the review body if useful — don't repeat on every inline comment.
- Acknowledge author context when you have it (for example, test IDs tried first and failed).

**Bad (canned):**

> **Blocker** — verified on `learn.grafana.net` @ `934a2c3` (Playwright DOM + Pathfinder PR review tool). Replace `h2:contains('Total Cost')`…

**Good (human):**

> This step passed on learn, but if you have a `data-testid` on this heading from Block Editor, prefer that over `:contains()` — otherwise the current selector matches our fallback order in the selectors doc.

### Checkpoint

> **Phase 7 of 9 complete** — comments drafted.
>
> - **{comment_count}** inline comment(s) on the PR
> - Review body: `.cursor/pr-review-state/pr-{n}-review-body.md`
> - Recommended verdict: **{recommended_verdict}** — {reason}
>
> GitHub won't show the draft review body in the UI. Reply **show body** to read it here, or open the file.
>
> **Your turn:** Skim inline comments on **Files changed**, then continue to Phase 8.
>
> **Up next:** Your approval before we submit.

---

## Phase 8: Reviewer approval

**Goal:** Reviewer confirms verdict and review body before submit.

### Checkpoint

> **Phase 8 of 9 — Approve and submit**
>
> Recommended verdict: **{recommended_verdict}** — {reason}
>
> Before we publish:
> 1. Inline comments on GitHub **Files changed**
> 2. Review body — reply **show body** or open `pr-{n}-review-body.md`
> 3. Verdict — keep **{recommended_verdict}** or override with `REQUEST_CHANGES`, `COMMENT`, or `APPROVE`
>
> **Your turn:** Reply **submit** with your final verdict *(for example `submit COMMENT`)*.

### Agent steps

1. Apply [verdict selection](reference-checks.md#verdict-selection-phases-89) — do not recommend **APPROVE** if **Always inline** blockers were posted in Phase 7.
2. Print the full review body in chat when the reviewer replies **show body**.
3. Apply reviewer edits to `pr-{n}-review-body.md`.
4. Store confirmed verdict in state as `verdict` (may differ from `recommended_verdict`).
5. **Do not submit** until the reviewer replies **submit** or **publish** with an explicit verdict.

---

## Phase 9: Submit (workflow ends)

**Goal:** Publish pending review + body.

### Tell the reviewer

> **Phase 9 of 9 — Submitting**
>
> Publishing as **{verdict}**…

### Agent steps

1. GraphQL `submitPullRequestReview` with final body from `-review-body.md`.
2. Update state: `"status": "submitted"`, `verdict`, `submitted_at`, `review_url`.
3. Share review URL with reviewer.

### Tell the reviewer

> **Review submitted:** {url}
>
> This cycle is complete. For follow-up after the author pushes, use Phase 10 or start a new review.

**Stop.** Do not add to the same pending review after submit.

---

## Phase 10: Post-submit (optional)

**Goal:** Ad-hoc comments after submit — new cycle if author rebases significantly.

### When to use

- Slack/colleague feedback (e.g. Pathfinder UX, stale `depends`)
- Product issues → **conversation** comment + follow-up issues
- Code fixes on new commits → new **inline** comment

**Prompt reviewer:**

> **Phase 10 — Post-submit follow-up**
>
> What would you like to add — an inline comment on a file, or a general PR comment?

---

## Anti-patterns

**Do not**

- Batch multiple phases in one message or skip checkpoints
- Post to GitHub before Phase 7, or submit before Phase 8 approval
- Use `FROM AUDIT:` prefixes or pass/N/A inline comments
- Assume Playwright is the reviewer's everyday browser
- Load Block Editor or test milestones before Phase 6 **ready**
- Smoke-test or repeat milestones outside the Phase 6 loop
- Leave Phase 1 without audit cleanup and a clean `git status`
- Delete pre-existing author `assets/` (for example `migration-notes.md`)
- Request website-repo changes (`pathfinder_data`, shortcodes) as merge blockers
- Treat Pathfinder pass on `doIt: false` save steps as proof of post-setup UI without a stack-state retest
- Submit from the GitHub UI without pasting the review body — it will be blank

**Do**

- One draft review per cycle; GraphQL submit with body from `pr-{n}-review-body.md`
- Defer authoring nits to the review body when Pathfinder passed
- Note fresh-stack retest caveats in the review body
- Dedupe inline comments to one thread per root cause

---

## Generated files

Deliverables for the reviewer. Write under `.cursor/pr-review-state/` — **never commit to the PR branch.**

| File | Phase | Purpose |
|---|---|---|
| `pr-{n}.json` | 0+ | Machine-readable review state ([schema](github-review.md#state-file-schema)) |
| `pr-{n}-findings.md` | 3 | Merged static + consistency findings |
| `pr-{n}-review-body.md` | 7 → 9 | Final review body (GitHub UI does not show draft review body) |
| `pr-{n}/audits/{milestone}/` | 1 (optional) | Copied audit reports before milestone cleanup |

Every generated markdown file in `.cursor/pr-review-state/` **must** start with:

```markdown
---
disclaimer: Auto-generated by review-learning-path skill. Do not edit manually.
notice: To regenerate, re-run the skill from the relevant phase.
pr_number: {n}
---
```

Do not add this frontmatter to `pr-{n}.json`.

---

## Deep references

| Topic | Doc |
|---|---|
| All checklists + severity routing + verdict selection | [reference-checks.md](reference-checks.md) |
| Learning Hub editorial + structure (internal course adapted) | [learning-hub-standards.md](learning-hub-standards.md) |
| GitHub GraphQL | [github-review.md](github-review.md) |
| Manifest fields | [docs/manifest-reference.md](../../../docs/manifest-reference.md) |
| `website.yaml` fields | [docs/website-yaml-reference.md](../../../docs/website-yaml-reference.md) |
| LP authoring workflow (single-repo model) | [learning-path-workflows/workflows.md](../../learning-path-workflows/workflows.md) |
| Legacy front matter → `website.yaml` (read-only) | [frontmatter-schema.md](../../commands/create-learning-path/reference/frontmatter-schema.md) |
| Recommendations | [how-to-write-recommendations.mdc](../../how-to-write-recommendations.mdc) |
| 21 critical rules | [AGENTS.md](../../../AGENTS.md) |
