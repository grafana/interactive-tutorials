# Author testing (preflight)

Live-test helpers for [preflight-learning-path/SKILL.md](SKILL.md).

Aligns with the five-phase [review-learning-path](../review-learning-path/SKILL.md) live path, lighter for authors: Playwright DOM is required; Block Editor is opt-in. Fits the hard author flow: pause for login, then smoke choice; do not quiz between DOM milestones.

---

## Prerequisites

Confirm during identify (quietly unless blocked). Remind in the slash-command first message.

| Need | Required when | Why | How to verify / fix |
|---|---|---|---|
| `interactive-tutorials` checkout with `{slug}-lj/` | Always | Package under test | Path on disk / current branch |
| **Playwright MCP** enabled (`user-playwright`) | Live path (default for new/conversion interactive) | Agent DOM checks | Identify: list or call Playwright MCP tools. If missing or broken: follow [If Playwright MCP is missing or broken](#if-playwright-mcp-is-missing-or-broken) |
| Okta login in the **Playwright** browser to `{learn_host}` (default `learn.grafana.net`) | Before Playwright DOM loop | MCP cannot complete SAML alone | Login pause: author logs in, replies `ready` |
| Pathfinder Block Editor on learn | Only if author chooses `walk-me` | Optional smoke coaching | `{learn_host}/plugins/grafana-pathfinder-app?dev=true` → **?** → Debug → Block Editor → import local JSON |
| Pathfinder CLI (`grafana-pathfinder-app` built locally) | Nice-to-have | `validate --packages` | Note if missing; do not abort preflight |
| `gh` auth + write access to the UI repo | Frontend walkthrough only | Frontend testid PR | Check when entering frontend steps |
| `website` repo in workspace | Optional (conversion) | Read-only legacy compare | Never write |

Same Playwright + Okta role as [learning-path-workflows/workflows.md](../../learning-path-workflows/workflows.md) and `/create-learning-path`.

### If Playwright MCP is missing or broken

Stop before live DOM checks. Do **not** silently skip DOM checks on new/conversion interactive paths. `static-only: <reason>` only when [static-only rules](reference-checks.md#static-only-preflight) allow it.

Diagnose which case applies, then offer help (manual steps always; agent action when possible):

| Case | How you can tell | Offer |
|---|---|---|
| **Config missing** from `~/.cursor/mcp.json` (no `playwright` / `@playwright/mcp` entry) | Read `mcp.json`; server absent | Ask: **Want me to add the Playwright MCP config for you?** If yes, merge the standard block below into `mcp.json`. Then ask them to reload MCP and reply when ready so you recheck. |
| **Needs auth** (`needsAuth` / only `mcp_auth` tool) | `GetMcpTools` / server status | Ask: **Want me to start the Playwright MCP connect flow?** If yes, call `mcp_auth` for `user-playwright` (empty args), wait, recheck. |
| **Configured but toggled off** in Cursor Settings | Entry exists in `mcp.json`; tools still unavailable | Manual only: Settings → MCP → enable **Playwright**. Agent cannot flip that toggle. |
| **Configured but broken** | Entry exists; server shows error / tools fail / navigate fails. Common: custom CDP like `http://localhost:9222` with nothing listening | Explain the failure plainly. Offer to replace with the standard `npx @playwright/mcp@latest` block (reply **add playwright mcp** or **fix playwright mcp**). Warn that this overwrites a custom playwright entry; keep other servers. Then reload and recheck. |
| **Errored / won't start** | Tools missing; logs or STATUS show install/runtime errors | Diagnose (`npx`, Node, network). Offer the standard config; author confirms reload. |

Standard config to add or restore (do not overwrite unrelated servers; for **configured but broken**, replace only the `playwright` server entry after the author agrees):

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

**Blocked checkpoint shape (author-facing):**

> Playwright MCP isn't ready, so I can't run the live DOM checks on this path yet.
>
> **Manual setup:** Cursor Settings → MCP → enable **Playwright** (or fix / re-add it), then reload.
>
> If Playwright is listed but broken (for example a CDP URL like `localhost:9222` with no browser listening), reply **fix playwright mcp** and I'll switch it to the standard `npx @playwright/mcp@latest` config. You'll still need to reload MCP afterward.
>
> **Or:** reply **add playwright mcp** if it is missing entirely.
>
> Skipping live checks with `static-only` isn't a fit for new or conversion interactive paths.

Never edit `mcp.json` until the author agrees. Never claim MCP is ready until `GetMcpTools` for `user-playwright` shows usable browser tools (and a quick navigate smoke succeeds when diagnosing "broken").

---

## Two browsers (live path)

| Browser | Who | Purpose |
|---|---|---|
| **Playwright** (MCP) | Agent (+ author Okta login) | Required DOM existence checks |
| **Normal browser** | Author | Optional Block Editor (`walk-me` only) |

DOM exists ≠ Show me / Do it works. Reviewers still run full Block Editor smoke on the PR.

---

## Playwright DOM (required)

After author replies `ready` at the login pause:

For each interactive milestone in scope (path order):

1. Start URL: first `on-page:/path` in milestone blocks, else path manifest `startingLocation` (same as [review milestone start URL](../review-learning-path/reference-checks.md#milestone-start-url)).
2. Navigate on `{learn_host}`.
3. For each `reftarget`, record: `exists` / `missing` / `below-fold` / `state-dependent`.
4. Do **not** stop for author confirmation between milestones. One short progress line is enough; save the summary for the results menu.

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
> 1. Import the local `content.json`
> 2. Open `{derived_start_url}`
> 3. Run every **Show me** and **Do it**
>
> **While you run it, watch for:** wrong highlights, Do it that no-ops or errors, steps that never unlock, and fake step numbers (intro prose or "You'll…" lines counted as steps).
>
> **Your turn:** Reply **pass**, **fail step N -** *what happened*, or **N/A -** *reason*.

Do **not** give the fake-step-number glance its own numbered setup step. Keep it inside the short **While you run it, watch for** line.

Record in state `pathfinder.{milestone-slug}`.

---

## Milestone scope

| `path_type` | Scope |
|---|---|
| **new** / **conversion** | Every interactive milestone in path `milestones` |
| **update** | Touched interactive milestones first; full path on request |

Skip terminal-only / external-CLI milestones for DOM and walk-me unless the author asks.
