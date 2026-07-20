# Author testing (preflight)

Live-test helpers for [preflight-learning-path/SKILL.md](SKILL.md) Phase 2.

Aligns with the five-phase [review-learning-path](../review-learning-path/SKILL.md) live path, lighter for authors: Playwright DOM is required; Block Editor is opt-in.

---

## Prerequisites

Confirm at Phase 0 / remind in the slash-command first message.

| Need | Required when | Why | How to verify / fix |
|---|---|---|---|
| `interactive-tutorials` checkout with `{slug}-lj/` | Always | Package under test | Path on disk / current branch |
| **Playwright MCP** enabled (`user-playwright`) | Live path (default for new/conversion interactive) | Agent DOM checks | Phase 0: list or call Playwright MCP tools. If missing: enable Playwright MCP in Cursor settings, then re-run |
| Okta login in the **Playwright** browser to `{learn_host}` (default `learn.grafana.net`) | Before Playwright DOM loop | MCP cannot complete SAML alone | Phase 2: author logs in, replies `ready` |
| Pathfinder Block Editor on learn | Only if author chooses `walk-me` | Optional smoke coaching | `{learn_host}/plugins/grafana-pathfinder-app?dev=true` → **?** → Debug → Block Editor → import local JSON |
| Pathfinder CLI (`grafana-pathfinder-app` built locally) | Nice-to-have | `validate --packages` | Note if missing; do not abort preflight |
| `gh` auth + write access to the UI repo | Phase 5 only | Frontend testid PR | Check when entering Phase 5 |
| `website` repo in workspace | Optional (conversion) | Read-only legacy compare | Never write |

Same Playwright + Okta role as [learning-path-workflows/workflows.md](../../learning-path-workflows/workflows.md) and `/create-learning-path`.

### If Playwright MCP is missing

Stop at Phase 0 (or before Phase 2) with friendly setup help. Do **not** silently skip DOM checks on new/conversion interactive paths. `static-only: <reason>` only when [static-only rules](reference-checks.md#static-only-preflight) allow it.

---

## Two browsers (live path)

| Browser | Who | Purpose |
|---|---|---|
| **Playwright** (MCP) | Agent (+ author Okta login) | Required DOM existence checks |
| **Normal browser** | Author | Optional Block Editor (`walk-me` only) |

DOM exists ≠ Show me / Do it works. Reviewers still run full Block Editor smoke on the PR.

---

## Playwright DOM (required)

After author replies `ready`:

For each interactive milestone in scope (path order):

1. Start URL: first `on-page:/path` in milestone blocks, else path manifest `startingLocation` (same as [review milestone start URL](../review-learning-path/reference-checks.md#milestone-start-url)).
2. Navigate on `{learn_host}`.
3. For each `reftarget`, record: `exists` / `missing` / `below-fold` / `state-dependent`.
4. One-line result in chat before moving on (or a short all-clear if clean).

Respect [live testing prerequisites](../review-learning-path/reference-checks.md#live-testing-prerequisites-phase-2) (stack state, credential-gated UI). Prefer documenting stack gaps over false "missing selector" on the wrong stack.

Apply [selector decision tree](../review-learning-path/reference-checks.md#selector-decision-tree) when promoting findings after live results.

---

## Block Editor (opt-in)

Authors are expected to dogfood while writing. Do **not** force a per-milestone interrogation by default.

### Prompt (once, after Playwright)

> Have you already smoke-tested this path in Block Editor (Show me / Do it)?
>
> Reply **`already-tested: <short notes>`** if yes (stack + anything flaky).
> Reply **`walk-me`** if you want a guided per-milestone check now.
> Reply **`skip-smoke`** to continue without recording Block Editor evidence.

### Local import (`walk-me` only)

No PR yet, so **do not** use the PR review tool.

1. Open `{learn_host}/plugins/grafana-pathfinder-app?dev=true` in the normal browser.
2. **?** → Debug → **Block Editor**.
3. Import `{path_dir}/{milestone}/content.json` from the local checkout.
4. Open the derived start URL; run every **Show me** and **Do it**.

### Guided loop prompts

For each scoped milestone:

> **Milestone {i} of {M}: `{milestone-id}`**
>
> Import the local `content.json`, open `{derived_start_url}`, run Show me / Do it.
>
> Also glance at the section step list for false step numbers (intro prose as step 1, or learner-action noops).
>
> **Your turn:** Reply **pass**, **fail step N  - ** *what happened*, or **N/A  - ** *reason*.

Record in state `pathfinder.{milestone-slug}`.

---

## Milestone scope

| `path_type` | Scope |
|---|---|
| **new** / **conversion** | Every interactive milestone in path `milestones` |
| **update** | Touched interactive milestones first; full path on request |

Skip terminal-only / external-CLI milestones for DOM and walk-me unless the author asks.
