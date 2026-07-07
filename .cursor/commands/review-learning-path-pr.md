## Command: /review-learning-path-pr

Review a learning path pull request in `grafana/interactive-tutorials`. Walk the reviewer through **one phase at a time** — narrate what you're doing, **stop at each checkpoint**, and **wait for their reply**. Never batch phases.

When invoked, read and follow **[review-learning-path/SKILL.md](../skills/review-learning-path/SKILL.md)** in order.

LP PRs are **single-repo** (`interactive-tutorials` only). Metadata lives in package `website.yaml`; the website repo is read-only for conversion ([PR #416](https://github.com/grafana/interactive-tutorials/pull/416)). Learning Hub criteria: [learning-hub-standards.md](../skills/review-learning-path/learning-hub-standards.md).

---

## First message to the reviewer

> I'll guide you through this learning path PR review **one phase at a time**. I'll pause after each phase for your input — please don't skip ahead.
>
> | Phase | What happens |
> |---|---|
> | 0 | Check out the PR |
> | 1–2 | Static audit + path checks |
> | 3 | Findings doc — choose live testing or **static-only** |
> | 4 | Draft GitHub review |
> | 5–6 | Live testing *(Playwright + Pathfinder)* |
> | 7–9 | Comments, your approval, submit |
>
> **Phase 0:** Share the PR — a GitHub URL or number (like `#403`) from `grafana/interactive-tutorials`.

Do not start Phase 1 until the reviewer shares the PR and you have checked out the branch.
