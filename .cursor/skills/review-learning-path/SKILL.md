---
name: review-learning-path-pr
description: >-
  Guide a reviewer through a full learning path PR review in interactive-tutorials —
  per-milestone audit, path consistency, Playwright, Pathfinder PR review tool, and
  GitHub submit. Use when the user runs /review-learning-path-pr.
---

# Review learning path PR

Interactive, phase-by-phase review of a `{slug}-lj/` pull request. The **agent narrates each step**, runs automated checks, and **prompts the reviewer for input** at checkpoints. Read-only on guide JSON.

**Entry command:** [/review-learning-path-pr](../../commands/review-learning-path-pr.md)

**Checklists:** [reference-checks.md](reference-checks.md) · **GitHub API:** [github-review.md](github-review.md)

**Related:** [audit-guide](../audit-guide/SKILL.md) · [review-guide-pr.mdc](../../review-guide-pr.mdc)

**Example:** [PR #403](https://github.com/grafana/interactive-tutorials/pull/403) (`monitor-azure-resources-lj`)

---

## How this skill runs

1. Agent announces the current **phase**, what it is doing, and why.
2. Agent executes agent-side work (audit, `gh`, Playwright, draft files).
3. Agent stops at the **checkpoint** and prompts the reviewer for input or approval.
4. **Do not advance** until the checkpoint is satisfied.
5. **Do not post GitHub review comments** until Phase 7 (after Phases 1–6 unless reviewer waives live testing).

| Phase | Agent | Reviewer |
|---|---|---|
| 0 | Fetch PR, checkout branch | Share PR URL/number; confirm `path_dir` |
| 1–2 | Audit + consistency checks | Skim summary; flag anything missed |
| 3 | Write internal findings doc | Approve moving to live testing |
| 4 | Create pending GitHub review | — |
| 5 | Playwright DOM | Log in to Playwright browser |
| 6 | Record results | PR review tool: Show me / Do it per milestone |
| 7 | Draft inline + body | — |
| 8 | — | Read body; approve verdict + edits |
| 9 | Submit review | Confirm submit |
| 10 | Optional follow-ups | — |

---

## Resume

If `.cursor/pr-review-state/pr-{n}.json` exists, read `phase` and `status`. Tell the reviewer:

> Found an in-progress review for PR #{n} (phase {phase}, status {status}). Resume from phase {phase + 1}, or start fresh?

---

## Phase 0: Get the PR and checkout branch

**Goal:** Identify the PR, check out its branch, infer the path package, initialize state.

### Tell the reviewer

> Starting Phase 0. Share the GitHub PR for this learning path — URL or PR number for `grafana/interactive-tutorials`. I'll fetch it and check out the branch.

**Wait for PR** before continuing.

### Agent steps

1. Parse PR number from URL or `#403` input.
2. Run `gh pr view {n} --repo grafana/interactive-tutorials --json number,title,headRefName,headRefOid,url,files`.
3. Tell the reviewer: PR title, number, branch, HEAD sha.
4. Check out: `gh pr checkout {n}` (or fetch + checkout).
5. Infer `{path_dir}` from changed files (directory ending in `-lj`). If ambiguous, **ask**.
6. Infer `website_slug` = `{path_dir}` minus `-lj` if `website` repo is in workspace.
7. List milestones under `{path_dir}/` and path root files.
8. Write `.cursor/pr-review-state/pr-{n}.json` (see [github-review.md](github-review.md)).

### Checkpoint

**Confirm with reviewer:**

> Checked out `{head_branch}` @ `{short_sha}`. Reviewing `{path_dir}` ({M} milestones). Website companion slug: `{website_slug}` (or none). Proceed to static audit?

**Wait for:** yes / corrections to `path_dir` or slug.

---

## Phase 1: Per-milestone audit

**Goal:** Run [audit-guide](../audit-guide/SKILL.md) on every milestone; apply [content checks](reference-checks.md#milestone-contentjson-checks).

### Tell the reviewer

> Phase 1 — static audit. I'm running audit-guide on each milestone under `{path_dir}`. This is read-only; nothing goes to GitHub yet.

### Agent steps

1. List milestones from path `manifest.json` `milestones` array **plus** any changed milestone dirs.
2. Run audit-guide on each milestone directory (parallel OK). Skip framing-only packages not in path `milestones` unless PR changed them.
3. Apply every row in [reference-checks.md § content](reference-checks.md#milestone-contentjson-checks).
4. Tag each finding with severity from [finding severity routing](reference-checks.md#finding-severity-routing) (`inline` / `defer` / `body`).
5. Summarize per milestone: verdict, blocking count, top issues (file + rule + fix + severity).
6. **Do not** post to GitHub. **Do not** use `FROM AUDIT:` prefixes anywhere.
7. **audit-guide side effects:** audit-guide writes `{milestone}/assets/` (reports, manifest). Do not commit these files. Do not edit them. Optional: delete `{milestone}/assets/` after Phase 3 if the reviewer wants a clean working tree.

### Checkpoint

**Tell the reviewer:**

> Phase 1 complete. {X} milestones audited — {B} blocking patterns across {N} milestones. Summary: [bullet list]. Anything you already know is wrong or out of scope?

**Wait for:** acknowledgment or additions, then Phase 2.

---

## Phase 2: Path-level consistency

**Goal:** Validate path root `content.json`, manifests, `website.yaml`, depends chain, framing rules, targeting, website alignment, CODEOWNERS.

### Tell the reviewer

> Phase 2 — path-level consistency. I'm validating path root content, manifests, website.yaml, the milestone dependency chain, framing-milestone rules, targeting, and companion website alignment.

### Agent steps

1. Run Pathfinder CLI if available: `validate --packages {path_dir}` (record pass/fail).
2. Walk [reference-checks.md](reference-checks.md): [path root content.json](reference-checks.md#path-root-contentjson), [website.yaml](reference-checks.md#websiteyaml), framing, valid manifests, depends chain, targeting, companion website, CODEOWNERS.
3. Compare path `milestones` to peer LPs (depends chain, no framing in array, first hands-on `depends: []`).
4. Tag each finding with [severity routing](reference-checks.md#finding-severity-routing).
5. Note companion website gaps separately (body later, not package blockers unless PR claims sync done).

### Checkpoint

**Tell the reviewer:**

> Phase 2 complete. Path consistency: [pass/fail bullets — e.g. framing in milestones, stale depends, broad targeting, website.yaml present, companion website drift]. Ready for me to write the internal findings doc?

**Wait for:** yes.

---

## Phase 3: Internal findings document

**Goal:** Merge Phases 1–2 into one reviewer-facing doc. Still no GitHub comments.

### Tell the reviewer

> Phase 3 — I'm merging audit and consistency results into `.cursor/pr-review-state/pr-{n}-findings.md`.

### Agent steps

Write `pr-{n}-findings.md` using [finding severity routing](reference-checks.md#finding-severity-routing):

- **Merge blockers (always inline)** — dedupe by root cause; static + any Phase 5–6 failures if live testing already ran
- **Live-test candidates** — selectors and milestones for Playwright + Pathfinder
- **Defer until after Pathfinder** — findings in the **Defer** column only
- **Review body only** — companion website, CODEOWNERS, editorial, passed-milestone notes
- **Waived / N/A** — terminal milestones; fresh-stack retest notes e.g. install

Each listed finding includes severity tag and source phase (1, 2, 5, or 6).

Update state: `"phase": 3`.

### Checkpoint

**Tell the reviewer:**

> Findings doc ready. Blockers before live test: [short list]. Live-test milestones: [list]. Deferring until Pathfinder: [list]. Open `pr-{n}-findings.md` if you want detail. Proceed to create the pending GitHub review and live testing?

**Wait for:** yes. Offer skip/waive of Phases 5–6 only if reviewer explicitly accepts static-only review.

---

## Phase 4: Pending GitHub review

**Goal:** One pending review to hold all inline comments until submit.

### Tell the reviewer

> Phase 4 — creating a pending GitHub review on PR #{n}. Comments stay hidden from the author until we submit at the end.

### Agent steps

1. GraphQL `addPullRequestReview` (no `event`), body: `Review in progress.`
2. Store `pending_review_id` and `pending_review_node_id` in state file.
3. **Do not** add inline comments yet (Phase 7).

See [github-review.md](github-review.md).

### Checkpoint

**Tell the reviewer:**

> Pending review created. Next: Playwright DOM checks, then you'll test interactivity in the PR review tool. Ready for Playwright?

**Wait for:** yes.

---

## Phase 5: Playwright DOM verification

**Goal:** Verify selectors exist on `learn.grafana.net` @ PR HEAD.

### Tell the reviewer

> Phase 5 — Playwright DOM pass on `{learn_host}`. Please log in to the **Playwright browser** (separate from your normal browser — Okta SAML). Reply **ready** when logged in.

**Wait for:** `ready`.

### Agent steps

For each **interactive milestone** in path order:

1. Navigate to `startingLocation`.
2. Check each `reftarget`: exists / missing / below-fold.
3. Record results @ `{head_sha}`.

**Do not** post pass-only GitHub comments.

### Checkpoint

**Tell the reviewer:**

> Playwright complete. Failures: [list or none]. Below-fold (may still pass Pathfinder): [list]. Next I'll guide you through Pathfinder milestone by milestone.

**Wait for:** ready for Phase 6.

---

## Phase 6: Pathfinder interactivity (PR review tool)

**Goal:** Reviewer exercises Show me / Do it for each milestone; agent records failures only.

### Tell the reviewer

> Phase 6 — Pathfinder testing with the **PR review tool** (not manual JSON paste).
>
> 1. Open `{learn_host}/plugins/grafana-pathfinder-app?dev=true`
> 2. Block Editor → dev tools → **PR review tool**
> 3. Point it at PR #{n} in `grafana/interactive-tutorials`
>
> We'll do **one milestone at a time** in path order. For each, navigate to its `startingLocation`, then click every Show me and Do it.

**Setup wait:** confirm reviewer has PR review tool pointed at this PR.

### Per-milestone loop

For each milestone in path `milestones` (skip terminal-only e.g. external CLI):

**Prompt reviewer:**

> **Milestone:** `{milestone-id}` — starting page `{startingLocation}`. Run all steps in the PR review tool. Reply with:
> - `pass` — all steps OK
> - `fail step N — {what happened}`
> - `N/A — {reason}` (e.g. already installed on stack)

**Agent:** record in `pr-{n}.json` → `pathfinder.{milestone-slug}`.

**Do not** post inline pass/N/A comments. N/A with stack caveat → note for review body (author fresh-stack retest).

### Checkpoint

**Tell the reviewer:**

> Pathfinder complete. Passed: [list]. Failed: [list]. N/A: [list]. I'll consolidate GitHub comments next — failures and code discrepancies only, no pass comments.

**Wait for:** yes.

---

## Phase 7: Consolidate GitHub comments

**Goal:** Add inline comments + draft review body. Apply [severity routing](reference-checks.md#finding-severity-routing) and [comment policy](reference-checks.md#github-comment-policy).

### Tell the reviewer

> Phase 7 — consolidating findings into pending inline comments and a review body draft. Only **Always inline** findings and live-test failures — no pass comments, no deferred items Pathfinder passed.

### Agent steps

1. Re-fetch PR HEAD if author may have pushed; reconcile resolved threads.
2. From `pr-{n}-findings.md`, promote **Defer** items to inline only if Phase 5–6 failed; drop deferred items Pathfinder passed.
3. Dedupe to [one comment per root cause](reference-checks.md#one-comment-per-root-cause) before posting.
4. Add inline comments via GraphQL `addPullRequestReviewComment` — **Always inline** + runtime failures only.
5. Merge Playwright + Pathfinder evidence, and merge code fix + runtime symptom when they share a root cause (never two inline threads on the same file for the same bug).
6. Write `.cursor/pr-review-state/pr-{n}-review-body.md` with **Review body only** findings, passed milestones, and retest notes. List all merge blockers under one **Must fix before merge** section (no split "should fix" tier for **Always inline** items).
7. Update state: `comment_count`, `"phase": 7`.

**Example inline tone:**

> **Blocker** — verified on `learn.grafana.net` @ `{sha}` (Playwright DOM + Pathfinder PR review tool). …

### Checkpoint

**Tell the reviewer:**

> Draft ready: **{comment_count}** inline comments + review body saved to `pr-{n}-review-body.md`. GitHub won't show the pending body in the UI — I'll paste it here if you want to read it. Reply **show body** or open the file, then tell me edits or **approve** with verdict (`REQUEST_CHANGES` / `COMMENT` / `APPROVE`).

**Wait for:** body review + explicit approval (Phase 8).

---

## Phase 8: Reviewer approval

**Goal:** Reviewer approves verdict and final body text.

### Tell the reviewer

> Phase 8 — approval checkpoint. Confirm:
> 1. Inline comments look correct on GitHub **Files changed**
> 2. Review body text (chat or `pr-{n}-review-body.md`)
> 3. Verdict: REQUEST_CHANGES / COMMENT / APPROVE

### Agent steps

1. Print full review body in chat if requested.
2. Apply reviewer edits to `-review-body.md`.
3. **Do not submit** until reviewer says **submit** or **publish**.

### Checkpoint

**Wait for:** explicit "submit" / "publish" with verdict.

---

## Phase 9: Submit (workflow ends)

**Goal:** Publish pending review + body.

### Tell the reviewer

> Phase 9 — submitting your review as **{verdict}**.

### Agent steps

1. GraphQL `submitPullRequestReview` with final body from `-review-body.md`.
2. Update state: `"status": "submitted"`, `verdict`, `submitted_at`, `review_url`.
3. Share review URL with reviewer.

### Tell the reviewer

> Review submitted: {url}. Workflow complete. For follow-up comments after author pushes, start Phase 10 or a new review cycle.

**Stop.** Do not add to the same pending review after submit.

---

## Phase 10: Post-submit (optional)

**Goal:** Ad-hoc comments after submit — new cycle if author rebases significantly.

### When to use

- Slack/colleague feedback (e.g. Pathfinder UX, stale `depends`)
- Product issues → **conversation** comment + follow-up issues
- Code fixes on new commits → new **inline** comment

**Prompt reviewer:**

> Post-submit follow-up. What should we add — inline on a file, or a general PR comment?

---

## Anti-patterns

**Do not:** submit mid-process · `FROM AUDIT:` on GitHub · pass/N/A inline comments · cap comment count · assume Playwright = main browser · manual JSON paste when PR review tool works · UI submit without pasting body · continue after Phase 9 on same pending review · duplicate inline threads on the same file for the same root cause (e.g. `depends` fix + "steps paused" symptom).

**Do:** one pending review · defer authoring nits when Pathfinder passed · fresh-stack retest in body · GraphQL submit · save body locally for preview.

---

## Artifacts

| File | Phase |
|---|---|
| `.cursor/pr-review-state/pr-{n}.json` | 0+ |
| `.cursor/pr-review-state/pr-{n}-findings.md` | 3 |
| `.cursor/pr-review-state/pr-{n}-review-body.md` | 7 → 9 |

---

## Deep references

| Topic | Doc |
|---|---|
| All checklists + severity routing | [reference-checks.md](reference-checks.md) |
| GitHub GraphQL | [github-review.md](github-review.md) |
| Manifest fields | [docs/manifest-reference.md](../../../docs/manifest-reference.md) |
| Recommendations | [how-to-write-recommendations.mdc](../../how-to-write-recommendations.mdc) |
| 21 critical rules | [AGENTS.md](../../../AGENTS.md) |
