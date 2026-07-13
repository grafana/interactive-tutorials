# Comment style (learning path PR reviews)

Voice and formatting for GitHub inline comments and the review summary. The agent drafts in **chat** at Phase 3; the reviewer approves before anything posts.

**This is not a full AI review.** You smoke-tested in Block Editor. The agent helps you phrase what you found.

---

## Rules

1. **Human voice** — write like you are talking to the author, not filing an audit report.
2. **No em dashes** — do not use `—` in any GitHub comment or summary body. Use periods, commas, or parentheses.
3. **No rule numbers** — never cite "rule 14", "critical rule 8", or audit-guide labels in GitHub text.
4. **No Blocker / nit labels in GitHub** — nits stay in the workbook and are not posted. Inline comments are for real issues only.
5. **Short** — max 3 sentences per inline comment. One issue per comment.
6. **Lead with what you tested** — start with what you did in Block Editor, not what the linter found.
7. **No host/sha spam** — mention stack once in the summary if useful, not on every inline comment.

---

## What posts to GitHub

| Tier | Post? |
|---|---|
| **Post inline** — anything the author should change (runtime fail, framing/depends, false noop, numbered “You'll…” intro, secrets, CLI validate, confirmed 404, conversion prose gap) | Yes — short comment on the file (path-wide OK) |
| **Internal** — LH editorial, `website.yaml` polish, selector fallback when live passed, bookends when live passed | No — workbook only |
| **Discard** — passed-milestone notes, shell UX, CODEOWNERS reminder, audit noise | No |

**Authors act on the diff.** If they should change a file, put a short inline on that file. Do not leave author fixes only in the reviewer workbook, and do not ask the reviewer to paste audit volume to the PR.

**Phase 1 chat stays tiny:** one outcome sentence + at most 3 “verify live” bullets. The workbook absorbs the rest.

**Zero inline comments + APPROVE is a first-class outcome** for a clean path: static pass + Block Editor live test passed, and nothing in the post-inline tier. That is a complete review, not a skipped or incomplete one. Prefer APPROVE (or COMMENT with a short “looks good” summary). Do not invent nits to post.

---

## Inline comment examples

**Bad (robotic, dense):**

> **Blocker** — verified on `learn.grafana.net` @ `934a2c3` (Playwright DOM + Pathfinder PR review tool). Replace `h2:contains('Tab Services')` with `data-testid` per selectors-and-testids.md priority order. Rule 2 violation.

**Good (human):**

> I couldn't find the Services tab when I ran this step in Block Editor after saving the credential. The guide paused here. Worth checking whether the selector still matches the UI on a stack with Azure configured.

**Bad (nit that should stay internal):**

> Section bookends missing. Add a one-sentence intro and summary markdown inside the section block.

**Good (compliance, still human):**

> The first hands-on milestone depends on `business-value`, which isn't in the path milestones array. That will break the depends chain for learners. Should be `"depends": []`.

**Good (section intro numbered as a step, path-wide):**

> The "You'll …" markdown inside the section shows as a numbered step in Pathfinder. Same pattern in create-custom, use-variables-queries, and chain-variables. Move those intros outside the section (or drop them if the section title is enough).

**Good (false noop):**

> These steps tell the learner to open the variable and fill Label / Display / Multi-value, but they use `noop` with no selector, so Pathfinder still numbers them as interactive steps. Prefer markdown (or restore highlight if you have a stable selector). Same pattern on the open-dashboard and panel-menu Edit noops in the earlier milestones.

---

## Summary body template

Short acknowledgment only. No bulleted blocker or nit lists.

```markdown
Thanks for the PR. I smoke-tested this on {stack_state} in Block Editor.

{One sentence: what the path does and whether the flow worked for you.}

{If inline comments: "I left a few notes on the diff." — do not list them.}

{If no issues: "Looks good to merge from my testing."}

{If static-only: one sentence that interactive milestones were not live-tested.}

{If reuse-live: one sentence that Block Editor results were reused from prior evidence, not re-run in this session.}
```

**Target length:** 3–5 sentences. Never paste the workbook into the summary.

---

## Verdict guidance (plain language)

The agent offers a suggestion; **you** choose the GitHub event at Phase 4.

| Situation | Suggest |
|---|---|
| Live-tested, no inline comments (clean path) | **APPROVE** (first-class). COMMENT also fine if you want a short acknowledgment only |
| Live-tested, posted inline comments on real issues | COMMENT, or REQUEST_CHANGES if you want to block merge |
| Static-only review | COMMENT only (never APPROVE) |
| Reuse-live (prior evidence, not a fresh pass this session) | COMMENT only (never APPROVE) |
| Unsure | COMMENT is always safe |

Do not use REQUEST_CHANGES unless you intend to block merge. Most LP reviews end as APPROVE or COMMENT.
