## Command: /preflight-learning-path

Self-review a learning path package in `interactive-tutorials` **before** opening a PR. Walks you through **one phase at a time**. Same static and live checks as the five-phase [/review-learning-path-pr](review-learning-path-pr.md) coach, from the author side.

When invoked, read and follow **[preflight-learning-path/SKILL.md](../skills/preflight-learning-path/SKILL.md)** in order. Never batch phases.

LP packages are **single-repo** (`interactive-tutorials` only). Metadata lives in package `website.yaml`; the website repo is read-only for conversion ([PR #416](https://github.com/grafana/interactive-tutorials/pull/416)). Learning Hub criteria: [learning-hub-standards.md](../skills/review-learning-path/learning-hub-standards.md).

### Setup you need

- This repo checked out with your `{slug}-lj/` package
- **Playwright MCP** enabled in Cursor (for DOM checks)
- Access to `https://learn.grafana.net/` (Okta login in the Playwright browser when asked)
- Block Editor only if you choose a guided smoke walk later

---

## First message to the author

> I'll walk you through a preflight check on your learning path **one phase at a time**. I'll pause after each phase. Please don't skip ahead.
>
> | Phase | What happens |
> |---|---|
> | 0 | Identify your `{slug}-lj/` package + confirm Playwright MCP |
> | 1 | Static pass (audit + path / Learning Hub + claim-check). Only real review-level issues and contradicted/unsupported product facts |
> | 2 | Playwright DOM checks. Block Editor smoke is optional |
> | 3 | Readiness report + offer to fix |
> | 4 | Optional package fixes |
> | 5 | Optional frontend `data-testid` PR if a stable selector is missing |
>
> **Setup:** Playwright MCP should be on. If it isn't, I'll offer to add the config for you (or walk you through Settings). You'll Okta-login in the Playwright browser for DOM checks.
>
> **Phase 0:** Share the path package (`{slug}-lj/` directory), or tell me to infer it from your current branch.

Do not start Phase 1 until the author confirms the path directory.
