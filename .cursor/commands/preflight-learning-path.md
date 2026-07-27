## Command: /preflight-learning-path

Self-review a learning path package in `interactive-tutorials` **before** opening a PR. Same checks as [/review-learning-path-pr](review-learning-path-pr.md), from the author side, with fewer stop-and-type moments: the agent runs what it can, then pauses only when it needs you (login, smoke choice, results / fixes).

When invoked, read and follow **[preflight-learning-path/SKILL.md](../skills/preflight-learning-path/SKILL.md)** in order.

LP packages are **single-repo** (`interactive-tutorials` only). Metadata lives in package `website.yaml`; the website repo is read-only for conversion ([PR #416](https://github.com/grafana/interactive-tutorials/pull/416)). Learning Hub criteria: [learning-hub-standards.md](../skills/review-learning-path/learning-hub-standards.md).

### Setup you need

- This repo checked out with your `{slug}-lj/` package
- **Playwright MCP** enabled in Cursor (for DOM checks)
- Access to `https://learn.grafana.net/` (Okta login in the Playwright browser when asked)
- Block Editor only if you choose a guided smoke walk later

---

## First message to the author

> I'll preflight your learning path with as few interruptions as possible. I'll run the static checks on my own, then pause when I need you logged into Playwright, again for an optional Block Editor smoke choice, then once for results and fix options.
>
> | When I pause | Why |
> |---|---|
> | Path unclear | Confirm which `{slug}-lj/` package |
> | Playwright not ready | Fix or add MCP |
> | Before live DOM | Okta login + which stack |
> | After DOM | Smoke: already-tested / walk-me / skip |
> | Results | What to fix (if anything) |
>
> **Setup:** Playwright MCP should be on. If it is missing or broken, I'll help fix it. You'll Okta-login in the Playwright browser for DOM checks.
>
> Preflight reports stay under `.cursor/lp-preflight-state/` (gitignored). Don't force-add them to your PR.
>
> **To start:** Share the path package (`{slug}-lj/` directory), or tell me to infer it from your current branch. If you already named the path, I'll begin the static checks now.

If the path is already clear from the user message, skip asking and start identify + static immediately.
