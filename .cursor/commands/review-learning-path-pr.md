## Command: /review-learning-path-pr

Review a learning path pull request in `grafana/interactive-tutorials`. Walk the reviewer through **one phase at a time** — narrate what you're doing, **stop at each checkpoint**, and **wait for their reply**. Never batch phases.

**This is not a full AI review.** The agent guides; the reviewer smoke-tests in Block Editor and decides what to post.

When invoked, read and follow **[review-learning-path/SKILL.md](../skills/review-learning-path/SKILL.md)** in order.

LP PRs are **single-repo** (`interactive-tutorials` only). Metadata lives in package `website.yaml`; the website repo is read-only for conversion ([PR #416](https://github.com/grafana/interactive-tutorials/pull/416)). Learning Hub criteria: [learning-hub-standards.md](../skills/review-learning-path/learning-hub-standards.md).

---

## First message to the reviewer

> I'll help you review this learning path PR **one phase at a time**. You will smoke-test each milestone in Block Editor; I'll run static checks and draft comments for you to approve before anything posts to GitHub.
>
> | Phase | What happens |
> |---|---|
> | 0 | Check out the PR |
> | 1 | Static pass (audit + path checks → internal workbook) |
> | 2 | Live test (required Playwright DOM check + Block Editor smoke test per milestone) |
> | 3 | Draft comments + summary in chat; you approve before posting |
> | 4 | Submit |
>
> **Phase 0:** Share the PR — a GitHub URL or number (like `#403`) from `grafana/interactive-tutorials`.

Do not start Phase 1 until the reviewer shares the PR and you have checked out the branch.
