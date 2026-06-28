## Command: /review-learning-path-pr

Review a learning path pull request in `grafana/interactive-tutorials`. **Guide the reviewer phase by phase** — explain what you are doing, prompt for input at checkpoints, and wait for approval before advancing.

When invoked, read and follow **[review-learning-path/SKILL.md](../skills/review-learning-path/SKILL.md)** in order. Do not skip phases or checkpoints.

---

## First message to the reviewer

> I'll walk you through a full learning path PR review in phases: checkout → static audit → path consistency → live testing (Playwright + Pathfinder) → GitHub comments → submit.
>
> **Phase 0:** Share the GitHub PR for this learning path (URL or PR number for `grafana/interactive-tutorials`).

Do not start Phase 1 until the reviewer shares the PR and you have checked out the branch.

---

## What you do vs what the reviewer does

| Phase | You (agent) | Reviewer |
|---|---|---|
| 0 | `gh pr view`, checkout, infer `path_dir` | Share PR; confirm path |
| 1–2 | audit-guide, manifest/consistency checks | Acknowledge summary |
| 3 | Write `pr-{n}-findings.md` | Approve live testing |
| 4 | Create pending GitHub review | — |
| 5 | Playwright DOM | Log in to Playwright browser; say **ready** |
| 6 | Record results | PR review tool: report pass/fail/N/A per milestone |
| 7 | Inline comments + body draft | — |
| 8 | Apply edits | Read body; **approve** verdict |
| 9 | `submitPullRequestReview` | Say **submit** |

---

## Reference material (read on demand)

- [reference-checks.md](../skills/review-learning-path/reference-checks.md) — severity routing, manifest, framing, noop, comment policy
- [github-review.md](../skills/review-learning-path/github-review.md) — GraphQL pending review
- [audit-guide](../skills/audit-guide/SKILL.md) — Phase 1 per milestone
- [review-guide-pr.mdc](../review-guide-pr.mdc) — single-guide blocking rules

---

## Rules

- Read-only on guide JSON — do not edit `content.json` / `manifest.json` during review
- No GitHub inline comments until Phase 7
- Failures only on inline comments — no pass/N/A threads
- Workflow **ends at Phase 9 submit**
- Companion website PR and Pathfinder app UX → review body or conversation, not fake JSON fixes

---

## Example

[PR #403](https://github.com/grafana/interactive-tutorials/pull/403) (`monitor-azure-resources-lj`) — reference run documented in the skill.
