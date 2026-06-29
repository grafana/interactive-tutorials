---
name: review-learning-path
description: >-
  Guide a reviewer through a full learning path PR review in interactive-tutorials —
  per-milestone audit, path consistency, Playwright, Pathfinder PR review tool, and
  GitHub submit. Use when the user runs /review-learning-path-pr.
---

# Review learning path PR

Interactive, phase-by-phase review of a `{slug}-lj/` pull request. The **agent narrates each step**, runs automated checks, and **prompts the reviewer for input** at checkpoints. Read-only on guide JSON.

**Entry command:** [/review-learning-path-pr](../../commands/review-learning-path-pr.md)

**Do NOT read external reference files upfront.** Each phase loads its own references on demand. Everything the orchestrator needs to start is inline below.

**Skill memory:** This skill does **not** use the per-guide `assets/manifest.yaml` convention ([skill-memory.md](../skill-memory.md)). PR-scoped state lives in `.cursor/pr-review-state/` so reviews survive across branches and do not write into author package directories.

**Severity:** [finding severity routing](reference-checks.md#finding-severity-routing) in this skill **supersedes** [audit-guide/severity-rubric.md](../audit-guide/severity-rubric.md) for Phase 3 bucketing and Phase 7 inline vs body decisions. audit-guide blocking/warning/info still applies during Phase 1; re-tag findings with this skill's routing before Phase 7.

**Checklists:** [reference-checks.md](reference-checks.md) · **GitHub API:** [github-review.md](github-review.md)

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
  ├─ Phase 3: Findings doc ──────── orchestrator → pr-{n}-findings.md
  │    Checkpoint: reviewer approves live testing
  │
  ├─ Phase 4: Pending GitHub review
  │
  ├─ Phase 5: Playwright DOM ────── orchestrator (reviewer logs in first)
  │
  ├─ Phase 6: Pathfinder PR tool ── reviewer reports pass/fail/N/A per milestone
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
- **Optional**: `website_slug` — companion path slug (`{path_dir}` minus `-lj`). Inferred when `website` repo is in workspace.
- **Optional**: `learn_host` — live test host (default `learn.grafana.net`).
- **Optional**: `waive_live_testing` — reviewer explicitly accepts static-only review; skip Phases 5–6.

If the user invokes `/review-learning-path-pr` with no arguments, start Phase 0 and ask for the PR.

---

## Safety invariants

These rules are **inviolable** during a review run:

1. **Never modify author `content.json` or `manifest.json`.** Read-only on guide JSON.
2. **Never post GitHub inline comments before Phase 7** (unless reviewer waives live testing and approves static-only inline at Phase 3).
3. **Never submit a review before Phase 8 approval** from the reviewer.
4. **Never commit `audit-guide` artifacts** (`{milestone}/assets/`) or `.cursor/pr-review-state/` to the author's branch.
5. **One pending GitHub review per PR review cycle** — workflow ends at Phase 9 submit.

---

## How this skill runs

1. Agent announces the current **phase**, what it is doing, and why.
2. Agent executes agent-side work (audit, `gh`, Playwright, draft files).
3. Agent stops at the **checkpoint** and prompts the reviewer for input or approval.
4. **Do not advance** until the checkpoint is satisfied.
5. **Do not post GitHub review comments** until Phase 7 (after Phases 1–6 unless reviewer waives live testing).

### Reviewer voice

Use short, direct prompts. One ask per checkpoint. Address the reviewer as **you**. Include the phase number. Say what you need and what happens next.

| Phase | Agent | You |
|---|---|---|
| 0 | Fetch PR, checkout branch | Share PR URL/number; confirm path |
| 1–2 | Audit + consistency checks | Skim summary; flag anything missed |
| 3 | Write findings doc | Approve live testing |
| 4 | Create pending GitHub review | — |
| 5 | Playwright DOM (after you log in) | Log in to Playwright browser; reply **ready** |
| 6 | Record Pathfinder results | Set up PR review tool; test each milestone; report pass/fail/N/A |
| 7 | Draft inline comments + body | — |
| 8 | — | Review draft; confirm verdict |
| 9 | Submit review | Reply **submit** |
| 10 | Optional follow-ups | — |

---

## Resume

If `.cursor/pr-review-state/pr-{n}.json` exists, read `phase` and `status`. Tell the reviewer:

> I found an in-progress review for PR #{n} (phase {phase}, status {status}). Would you like to **resume** from phase {phase + 1}, or **start fresh**?

---

## Phase 0: Get the PR and checkout branch

**Goal:** Identify the PR, check out its branch, infer the path package, initialize state.

### Tell the reviewer

> **Phase 0 — Get the PR**
>
> Share the GitHub PR for this learning path — a URL or number (for example `#403`) in `grafana/interactive-tutorials`. I'll fetch it and check out the branch.

**Wait for the PR** before continuing.

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

> **Phase 0 complete**
>
> - Branch: `{head_branch}` @ `{short_sha}`
> - Path: `{path_dir}` ({M} milestones)
> - Website slug: `{website_slug}` (or none in workspace)
>
> Does that look right? Reply **yes** to start the static audit, or tell me what to fix.

---

## Phase 1: Per-milestone audit

**Goal:** Run [audit-guide](../audit-guide/SKILL.md) on every milestone; apply [content checks](reference-checks.md#milestone-contentjson-checks).

### Tell the reviewer

> **Phase 1 — Static audit**
>
> I'm running audit-guide on each milestone under `{path_dir}`. This is read-only — nothing goes to GitHub yet.

### Agent steps

1. List milestones from path `manifest.json` `milestones` array **plus** any changed milestone dirs.
2. Dispatch [audit-guide](../audit-guide/SKILL.md) on each milestone directory (Explore sub-agent or Task, parallel OK). Skip framing-only packages not in path `milestones` unless PR changed them.
3. Apply every row in [reference-checks.md § content](reference-checks.md#milestone-contentjson-checks).
4. Tag each finding with severity from [finding severity routing](reference-checks.md#finding-severity-routing) (`inline` / `defer` / `body`).
5. Summarize per milestone: verdict, blocking count, top issues (file + rule + fix + severity).
6. **Do not** post to GitHub. **Do not** use `FROM AUDIT:` prefixes anywhere.
7. **audit-guide side effects:** audit-guide writes `{milestone}/assets/` (reports, manifest). Do not commit these files. Do not edit them. Optional: delete `{milestone}/assets/` after Phase 3 if the reviewer wants a clean working tree.

### Checkpoint

**Tell the reviewer:**

> **Phase 1 complete** — {X} milestones audited, {B} blocking patterns across {N} milestones.
>
> Top findings:
> [bullet list]
>
> Anything you already know is wrong or out of scope?

**Wait for:** acknowledgment or additions, then Phase 2.

---

## Phase 2: Path-level consistency

**Goal:** Validate path root `content.json`, manifests, `website.yaml`, depends chain, framing rules, targeting, website alignment, CODEOWNERS.

### Tell the reviewer

> **Phase 2 — Path consistency**
>
> I'm checking path root content, manifests, `website.yaml`, the dependency chain, framing rules, targeting, and companion website alignment.

### Agent steps

1. Run Pathfinder CLI if available: `validate --packages {path_dir}` (record pass/fail).
2. Walk [reference-checks.md](reference-checks.md): [path root content.json](reference-checks.md#path-root-contentjson), [website.yaml](reference-checks.md#websiteyaml), framing, valid manifests, depends chain, targeting, companion website, CODEOWNERS.
3. Compare path `milestones` to peer LPs (depends chain, no framing in array, first hands-on `depends: []`).
4. Tag each finding with [severity routing](reference-checks.md#finding-severity-routing).
5. Note companion website gaps separately (body later, not package blockers unless PR claims sync done).

### Checkpoint

**Tell the reviewer:**

> **Phase 2 complete**
>
> [pass/fail bullets — framing, depends chain, targeting, website.yaml, companion website]
>
> Ready for me to write the findings doc?

**Wait for:** yes.

---

## Phase 3: Internal findings document

**Goal:** Merge Phases 1–2 into one reviewer-facing doc. Still no GitHub comments.

### Tell the reviewer

> **Phase 3 — Findings doc**
>
> I'm merging the audit and consistency results into `.cursor/pr-review-state/pr-{n}-findings.md`.

### Agent steps

Write `pr-{n}-findings.md` using [finding severity routing](reference-checks.md#finding-severity-routing):

- **Merge blockers (always inline)** — dedupe by root cause; static + any Phase 5–6 failures if live testing already ran
- **Live-test candidates** — selectors and milestones for Playwright + Pathfinder
- **Defer until after Pathfinder** — findings in the **Defer** column only
- **Review body only** — companion website, CODEOWNERS, editorial, passed-milestone notes
- **Waived / N/A** — terminal milestones; fresh-stack retest notes e.g. install

Each listed finding includes severity tag and source phase (1, 2, 5, or 6).

Apply the [generated-file frontmatter](SKILL.md#generated-files) to `pr-{n}-findings.md`.

Update state: `"phase": 3`.

### Checkpoint

**Tell the reviewer:**

> **Phase 3 complete** — findings doc is ready.
>
> - Blockers before live test: [short list or none]
> - Milestones to live-test: [list]
> - Deferring until Pathfinder: [list]
>
> Open `pr-{n}-findings.md` for full detail. Reply **yes** to create the pending GitHub review and start live testing.

**Wait for:** yes. Offer to skip Phases 5–6 only if you explicitly accept a static-only review.

---

## Phase 4: Pending GitHub review

**Goal:** One pending review to hold all inline comments until submit.

### Tell the reviewer

> **Phase 4 — Pending GitHub review**
>
> I'm creating a pending review on PR #{n}. Inline comments stay hidden from the author until we submit at the end.

### Agent steps

1. GraphQL `addPullRequestReview` (no `event`), body: `Review in progress.`
2. Store `pending_review_id` and `pending_review_node_id` in state file.
3. **Do not** add inline comments yet (Phase 7).

See [github-review.md](github-review.md).

### Checkpoint

**Tell the reviewer:**

> **Phase 4 complete** — pending review is created.
>
> Next up is live testing on `{learn_host}`. Reply **yes** when you're ready for the Playwright pass.

**Wait for:** yes before starting Phase 5.

---

## Phase 5: Playwright DOM verification

**Goal:** Verify selectors exist on `learn.grafana.net` @ PR HEAD.

### Tell the reviewer

> **Phase 5 — Playwright DOM check**
>
> I'll verify selectors in the **Playwright browser** (separate from your normal browser — you'll need to log in with Okta).
>
> Reply **ready** when you're logged in to `{learn_host}` in Playwright.

**Wait for:** `ready`. **Do not navigate or run Playwright until the reviewer replies.**

### Agent steps

For each **interactive milestone** in path order:

1. Navigate to `startingLocation`.
2. Check each `reftarget`: exists / missing / below-fold.
3. Record results @ `{head_sha}`.

**Do not** post pass-only GitHub comments. **Do not** open Block Editor, load guides, or start Pathfinder testing — that is Phase 6 only.

### Checkpoint

**Tell the reviewer:**

> **Phase 5 complete**
>
> - Failures: [list or none]
> - Below fold (may still pass Pathfinder): [list or none]
>
> Next is Pathfinder testing with the PR review tool. Reply **yes** when you want setup instructions.

**Wait for:** yes before opening Phase 6. **Do not** preview, navigate to, or load any milestone in Block Builder yet.

---

## Phase 6: Pathfinder interactivity (PR review tool)

**Goal:** You exercise Show me / Do it for each milestone; the agent records results.

### Tell the reviewer (setup only — no milestone testing yet)

> **Phase 6 — Pathfinder (PR review tool)**
>
> Set this up in your browser (not Playwright):
> 1. Open `{learn_host}/plugins/grafana-pathfinder-app?dev=true`
> 2. Block Editor → dev tools → **PR review tool**
> 3. Point it at PR #{n} in `grafana/interactive-tutorials`
>
> Reply **ready** when the PR review tool is loaded. I won't ask you to test any milestone until you do.

**Wait for:** `ready`.

**Do not before `ready`:** navigate to a milestone `startingLocation`, load a guide in Block Builder, run Show me / Do it, or repeat setup instructions. **Do not** smoke-test the first milestone during Phase 5 or between phases.

### Per-milestone loop

Start only after setup **ready**. For each milestone in path `milestones` (skip terminal-only, e.g. external CLI):

**Prompt reviewer (one milestone at a time — never repeat a milestone already reported):**

> **Milestone {i} of {M}: `{milestone-id}`**
>
> Open `{startingLocation}` in learn, then run every **Show me** and **Do it** in the PR review tool.
>
> Reply when you're done:
> - **pass** — all steps worked
> - **fail step N —** what happened
> - **N/A —** reason (for example, resource already on your stack)

**Agent:** record in `pr-{n}.json` → `pathfinder.{milestone-slug}`. Advance to the next milestone only after the reviewer replies.

**Do not** post inline pass/N/A comments. N/A with stack caveat → note for review body (author fresh-stack retest).

### Checkpoint

**Tell the reviewer:**

> **Phase 6 complete**
>
> - Passed: [list]
> - Failed: [list]
> - N/A: [list]
>
> Next I'll draft GitHub comments (failures only). Reply **yes** to continue.

**Wait for:** yes.

---

## Phase 7: Consolidate GitHub comments

**Goal:** Add inline comments + draft review body. Apply [severity routing](reference-checks.md#finding-severity-routing) and [comment policy](reference-checks.md#github-comment-policy).

### Tell the reviewer

> **Phase 7 — Draft GitHub comments**
>
> I'm adding inline comments for blockers and writing the review body. Pass-only and deferred nits won't get inline comments.

### Agent steps

1. Re-fetch PR HEAD if author may have pushed; reconcile resolved threads.
2. From `pr-{n}-findings.md`, promote **Defer** items to inline only if Phase 5–6 failed; drop deferred items Pathfinder passed.
3. Dedupe to [one comment per root cause](reference-checks.md#one-comment-per-root-cause) before posting.
4. Add inline comments via GraphQL `addPullRequestReviewComment` — **Always inline** + runtime failures only.
5. Merge Playwright + Pathfinder evidence, and merge code fix + runtime symptom when they share a root cause (never two inline threads on the same file for the same bug).
6. Write `.cursor/pr-review-state/pr-{n}-review-body.md` with **Review body only** findings, passed milestones, and retest notes. List all merge blockers under one **Must fix before merge** section (no split "should fix" tier for **Always inline** items). Apply the [generated-file frontmatter](SKILL.md#generated-files).
7. Recommend a default [verdict](reference-checks.md#verdict-selection-phases-89) from findings (`REQUEST_CHANGES`, `COMMENT`, or `APPROVE`) with a one-sentence reason. Store in state: `"recommended_verdict"`.
8. Update state: `comment_count`, `"phase": 7`.

**Example inline tone:**

> **Blocker** — verified on `learn.grafana.net` @ `{sha}` (Playwright DOM + Pathfinder PR review tool). …

### Checkpoint

**Tell the reviewer:**

> **Phase 7 complete**
>
> - **{comment_count}** inline comments drafted
> - Review body saved to `pr-{n}-review-body.md`
> - Recommended verdict: **{recommended_verdict}** — {reason}
>
> GitHub won't show the pending body in the UI. Reply **show body** to read it here, or open the file. Then we'll confirm at Phase 8.

**Wait for:** body review, then Phase 8.

---

## Phase 8: Reviewer approval

**Goal:** Reviewer confirms or overrides the recommended [verdict](reference-checks.md#verdict-selection-phases-89) and final body text.

### Tell the reviewer

> **Phase 8 — Approve and submit**
>
> Recommended verdict: **{recommended_verdict}** — {reason}
>
> Please confirm:
> 1. Inline comments look right on GitHub **Files changed**
> 2. Review body text (here or in `pr-{n}-review-body.md`)
> 3. Verdict — keep **{recommended_verdict}** or choose `REQUEST_CHANGES` / `COMMENT` / `APPROVE`
>
> Reply **submit** with your final verdict when you're ready to publish.

### Agent steps

1. Apply [verdict selection](reference-checks.md#verdict-selection-phases-89) rules — do not recommend APPROVE if **Always inline** blockers were inlined in Phase 7.
2. Print full review body in chat if requested.
3. Apply reviewer edits to `-review-body.md`.
4. Store confirmed verdict in state: `"verdict"` (may differ from `recommended_verdict`).
5. **Do not submit** until reviewer says **submit** or **publish** with explicit verdict.

### Checkpoint

**Wait for:** explicit "submit" / "publish" with verdict.

---

## Phase 9: Submit (workflow ends)

**Goal:** Publish pending review + body.

### Tell the reviewer

> **Phase 9 — Submitting review**
>
> Publishing as **{verdict}**…

### Agent steps

1. GraphQL `submitPullRequestReview` with final body from `-review-body.md`.
2. Update state: `"status": "submitted"`, `verdict`, `submitted_at`, `review_url`.
3. Share review URL with reviewer.

### Tell the reviewer

> **Review submitted:** {url}
>
> This review cycle is complete. For follow-up after the author pushes, use Phase 10 or start a new review.

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

**Do not:** submit mid-process · `FROM AUDIT:` on GitHub · pass/N/A inline comments · cap comment count · assume Playwright = main browser · manual JSON paste when PR review tool works · UI submit without pasting body · continue after Phase 9 on same pending review · duplicate inline threads on the same file for the same root cause · navigate to or load Block Builder milestones before Phase 6 setup **ready** · smoke-test or repeat the first milestone before the formal Phase 6 loop · start Phase 6 milestone prompts before the reviewer confirms PR review tool setup.

**Do:** one pending review · defer authoring nits when Pathfinder passed · fresh-stack retest in body · GraphQL submit · save body locally for preview.

---

## Generated files

Deliverables for the reviewer. Write under `.cursor/pr-review-state/` — **never commit to the PR branch.**

| File | Phase | Purpose |
|---|---|---|
| `pr-{n}.json` | 0+ | Machine-readable review state ([schema](github-review.md#state-file-schema)) |
| `pr-{n}-findings.md` | 3 | Merged static + consistency findings |
| `pr-{n}-review-body.md` | 7 → 9 | Final review body (GitHub UI does not show pending body) |

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
| GitHub GraphQL | [github-review.md](github-review.md) |
| Manifest fields | [docs/manifest-reference.md](../../../docs/manifest-reference.md) |
| Recommendations | [how-to-write-recommendations.mdc](../../how-to-write-recommendations.mdc) |
| 21 critical rules | [AGENTS.md](../../../AGENTS.md) |
