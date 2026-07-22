---
name: preflight-learning-path
description: >-
  Guide a learning path author through pre-PR self-review in interactive-tutorials.
  Mirrors the five-phase /review-learning-path-pr coach from the author side: static
  pass (including adversarial claim-check), Playwright DOM checks, readiness report,
  optional package fixes, and optional frontend data-testid PR. Use when the user
  runs /preflight-learning-path.
---

# Preflight learning path (author self-review)

Walk through a `{slug}-lj/` package **before you open a PR**. Same checks as the five-phase [review-learning-path](../review-learning-path/SKILL.md) coach, from your side: static pass, Playwright DOM, readiness, then optional fixes.

**Terminology:** Say **learning path** or **path** in messages; use `{path_dir}` in agent notes.

**Entry command:** [/preflight-learning-path](../../commands/preflight-learning-path.md)

**Mirror skill:** [review-learning-path](../review-learning-path/SKILL.md) (five-phase coach on main only). Do **not** use any outdated review skill phases or Always-inline routing.

**Do NOT read external reference files upfront.** Each phase loads its own references on demand.

**Skill memory:** State lives in `.cursor/lp-preflight-state/` (gitignored). Phase 1 dispatches [audit-guide](../audit-guide/SKILL.md), which writes `{milestone}/assets/`. See [Commit safety](#commit-safety).

**Routing:** [reference-checks.md](reference-checks.md) · [claim-check.md](claim-check.md) · [author-testing.md](author-testing.md) · [frontend-selector-pr.md](frontend-selector-pr.md) · shared [learning-hub-standards.md](../review-learning-path/learning-hub-standards.md) · shared [review reference-checks](../review-learning-path/reference-checks.md)

**Related:** [audit-guide](../audit-guide/SKILL.md) · [update-guide](../update-guide/SKILL.md) · [review-learning-path](../review-learning-path/SKILL.md)

---

## Human-in-the-loop contract

| You (agent) | Author (human) |
|---|---|
| Confirm path, run audit + path/LH + claim-check | Confirm `{path_dir}`, reply at checkpoints |
| Surface **post-inline-only** findings in chat | Decide whether to fix now or open PR with notes |
| Required Playwright DOM check (live path) | Okta login in Playwright browser; reply `ready` |
| Optional Block Editor coaching | `already-tested` / `walk-me` / `skip-smoke` |
| Apply package fixes only when asked | Reply `fix all`, `fix N`, or a combo like `fix 1,3` |
| Walk frontend testid PR when needed | Approve push / PR create |

---

## Workflow overview

```
Input (path_dir or current branch)
  │
  ├─ Phase 0: Identify path ───── path_dir, path_type, Playwright MCP prereq
  │
  ├─ Phase 1: Static pass ─────── audit + path/LH + claim-check → author findings (post-inline only)
  │
  ├─ Phase 2: Live test ───────── Playwright DOM required; Block Editor opt-in
  │                              (skipped when static-only)
  │
  ├─ Phase 3: Readiness ───────── readiness report + offer to fix
  │
  ├─ Phase 4: Apply fixes ─────── optional package JSON / website.yaml edits
  │
  └─ Phase 5: Frontend testid ─── optional upstream data-testid PR (when needed)
```

---

## Inputs

- **Required**: `{path_dir}` ending in `-lj/` (for example `monitor-azure-resources-lj`). Infer from current branch if omitted; confirm if ambiguous.
- **Optional**: `website_slug` (`{path_dir}` minus `-lj`). Website repo is read-only for conversion ([PR #416](https://github.com/grafana/interactive-tutorials/pull/416)).
- **Optional**: `learn_host` (default `learn.grafana.net`).
- **Optional**: `waive_live_testing` via `static-only: <reason>` at Phase 1 end. See [static-only preflight](reference-checks.md#static-only-preflight).

---

## Prerequisites

See [author-testing.md § Prerequisites](author-testing.md#prerequisites). Phase 0 verifies Playwright MCP for the live path.

---

## Safety invariants

1. **Do not modify** `content.json`, `manifest.json`, or `website.yaml` until Phase 4 (and only when the author requests fixes).
2. **Never commit** preflight artifacts (`.cursor/lp-preflight-state/` or audit-guide files under `{milestone}/assets/`).
3. **Surface only post-inline** findings in chat and readiness (same bar as review [comment-style](../review-learning-path/comment-style.md)). Never dump Internal/Discard nits.
4. **No em dashes** in author-facing chat, readiness text, or drafted PR bodies. Use periods, commas, or parentheses.
5. **One preflight run per path slug** (resume from state; do not fork duplicate state files).
6. **Never** plan companion website / `pathfinder_data` / shortcode work as package blockers.

---

## Commit safety

Same snapshot/cleanup rules as [review-learning-path § Commit safety](../review-learning-path/SKILL.md#commit-safety).

| Artifact | Where | Mitigation |
|---|---|---|
| Findings, claim-check, readiness, state JSON | `.cursor/lp-preflight-state/` | `.gitignore` |
| audit-guide reports | `{milestone}/assets/` | Snapshot before Phase 1; delete new files before Phase 1 checkpoint |
| Pre-existing package `assets/` | Author/migrate notes | Never delete paths listed in `pre_review_assets` |

**Phase 1 snapshot:** `find {milestone}/assets -type f 2>/dev/null | sort` → store in state `pre_review_assets`.

**Phase 1 cleanup (mandatory before checkpoint):** remove audit files not in the snapshot; verify `git status --porcelain -- {path_dir}` shows no untracked audit paths.

Re-verify commit safety after Phase 1 before Phase 2.

---

## How this skill runs

1. Announce the phase (number and name), what you're doing, and why (2–3 sentences).
2. Do agent work (audit, CLI, Playwright, drafts).
3. Stop at the checkpoint: one message, one ask. **Do not advance** until the author replies.
4. **Never batch phases.** If they say "keep going," pause at the next checkpoint anyway.

---

## Checkpoint format

| Section | Content |
|---|---|
| **Header** | `Phase {n}` + short plain outcome (avoid jargon like "post-inline") |
| **What we checked** | Phase 3 (and readiness-style summaries): where findings came from, in plain language |
| **Findings** | Numbered list with enough context to act (what is wrong, why it matters, which file). No rule counts. |
| **Your turn** | Clear reply choices (including **fix all** / **fix N** when findings exist) |
| **Up next** | One sentence when useful |

Do **not** open Phase 3 with a "What this check is" primer. Lead with the outcome, then **What we checked**, then the numbered findings.

**Reply keywords:** `yes` · `ready` · `add playwright mcp` · `static-only: <reason>` · `already-tested: <notes>` · `walk-me` · `skip-smoke` · `pass` / `fail step N - …` / `N/A - …` · `show report` · `fix all` · `fix 1` / `fix 2` / `fix 3` · `fix 1,3` (package-fixable only) · `frontend` (needs-frontend / upstream testid) · `done` · `resume` / `start fresh`

**Tone:** Casual and friendly. Address the author as **you**. Celebrate clean passes. No rule numbers, no Blocker/nit labels, no em dashes. Prefer everyday words over skill jargon (say "copy fixes" not "post-inline"; say "product claims vs docs" not "claim-check MUST FIX").

---

## Resume

If `.cursor/lp-preflight-state/{slug}.json` exists:

> **Resume?** I have an in-progress preflight for `{path_dir}` (stopped after phase {phase}).
>
> Reply **resume** to pick up, or **start fresh** to begin again.

---

## Phase 0: Identify path

**Goal:** Confirm `{path_dir}`, `path_type`, milestones; verify Playwright MCP; init state.

### Tell the author

> **Phase 0  -  Identify path**
>
> Share the learning path package directory (for example `monitor-azure-resources-lj`), or tell me to infer it from your current branch.
>
> **Setup reminder:** For the live path I need **Playwright MCP** in Cursor. You'll Okta-login in the Playwright browser when we get to DOM checks. Block Editor is optional later.

### Agent steps

1. Infer or confirm `{path_dir}` (directory ending in `-lj`).
2. Record branch and HEAD sha.
3. Infer `website_slug` = `{path_dir}` minus `-lj` when website repo is in workspace (read-only).
4. Infer `path_type`: `new`, `conversion`, or `update` per [path type](reference-checks.md#path-type).
5. List milestones from path `manifest.json` `milestones` and dirs under `{path_dir}/`.
6. **Verify Playwright MCP** (`user-playwright`). If unavailable on a live path: stop per [If Playwright MCP is missing](author-testing.md#if-playwright-mcp-is-missing). Give manual setup steps **and** offer to help when possible (add `mcp.json` config on **add playwright mcp**, or `mcp_auth` if the server needs auth). Do not silently skip. Do not edit `mcp.json` until they agree.
7. Write `.cursor/lp-preflight-state/{slug}.json` ([state schema](reference-checks.md#state-file-schema)).

### Checkpoint (MCP ready)

> **Phase 0 complete** - `{path_dir}` on `{branch}` @ `{short_sha}`.
>
> - Path: `{path_dir}` ({M} milestones)
> - Type: `{path_type}`
> - Playwright MCP: ready
>
> **Your turn:** Reply **yes** if this looks right, or tell me what to change.
>
> **Up next:** Static pass (I won't edit your JSON unless you ask later).

### Checkpoint (MCP blocked)

Use the blocked shape in [author-testing.md](author-testing.md#if-playwright-mcp-is-missing). Still report path / type. **Your turn** must include the **add playwright mcp** offer (or auth offer) plus manual Settings steps. After they reload and MCP is ready, re-run the verify step and use the MCP-ready checkpoint.

---

## Phase 1: Static pass

**Goal:** Audit every milestone + path consistency + Learning Hub + adversarial claim-check. Surface **post-inline** findings only in chat.

Combines review Phase 1 checks plus [claim-check.md](claim-check.md). Author sees findings in chat (not a private workbook dump of nits).

### Tell the author

> **Phase 1  -  Static pass**
>
> I'm reading each milestone, checking manifests, `website.yaml`, and Learning Hub structure, then fact-checking product claims against live docs. I'll only call out things a reviewer would comment on (plus contradicted or unsupported product facts).

### Agent steps

1. Snapshot `pre_review_assets`; dispatch [audit-guide](../audit-guide/SKILL.md) per milestone (parallel OK).
2. Walk shared [review reference-checks](../review-learning-path/reference-checks.md) + [learning-hub-standards.md](../review-learning-path/learning-hub-standards.md).
3. **Always scan** for framing-in-milestones, [section intro markdown that may number as a step](../review-learning-path/reference-checks.md#section-intro-markdown-numbered-as-step), and [false noops](../review-learning-path/reference-checks.md#noop-and-non-interactive-steps).
4. Run Pathfinder CLI `validate --packages {path_dir}` if available.
5. Run the [claim-check](claim-check.md) pass across path root + all milestone prose. Write `{slug}-claim-check.md` under `.cursor/lp-preflight-state/`. Route Contradicted / Unsupported / Overstated as **Fix before PR**. Do not edit package JSON here.
6. Tag findings with review [finding routing](../review-learning-path/reference-checks.md#finding-routing) plus claim-check MUST FIX. Keep only **post inline** for author chat. Drop Internal/Discard entirely from chat.
7. Write `{slug}-findings.md` under `.cursor/lp-preflight-state/` (post-inline list + optional verify-live notes for Phase 2). Resume aid only; chat stays tiny.
8. Mandatory audit cleanup; verify `git status`.
9. Do not cite rule numbers or audit severity labels in chat.

### Checkpoint

> **Phase 1 complete**  -  static pass done.
>
> - {One plain sentence: clean, or a few things to fix}
> - **Fix before PR** (≤3 bullets, plain language; omit if none; include claim-check MUST FIX when present):
>   - {e.g. first hands-on still depends on business-value}
>   - {e.g. "You'll…" intros inside sections in create-dashboard}
>   - {e.g. claim check: contradicted alert count in business-value}
>
> **Your turn:** Reply **yes** and your test stack (for example `learn.grafana.net shared`, `fresh Cloud stack`).
>
> Or **`static-only: <reason>`** to skip live testing (not for **new** / **conversion** interactive paths). See [static-only preflight](reference-checks.md#static-only-preflight).
>
> **Up next:** Playwright DOM checks *(or readiness if static-only)*.

Record `stack_state`, or `waive_live_testing` + `static_only_reason`.

**Reject** bare `static-only` and static-only on **new** / **conversion** with interactive milestones.

---

## Phase 2: Live test

**Goal:** Required Playwright DOM checks. Block Editor smoke test is **not forced**.

Skipped when `waive_live_testing` is true → jump to Phase 3.

Details: [author-testing.md](author-testing.md).

### Setup (tell the author once)

> **Phase 2  -  Live test**
>
> I need the **Playwright** browser for DOM checks. Log into `{learn_host}` with Okta there, then reply **ready**.
>
> Stack: `{stack_state}`
>
> After DOM checks I'll ask whether you've already smoke-tested in Block Editor (optional).

**Wait for:** `ready`.

### Milestone scope

| `path_type` | Scope |
|---|---|
| **new** / **conversion** | Every interactive milestone in path `milestones` |
| **update** | Touched interactive milestones first; full path on request |

### Step A: Playwright DOM (required)

For each milestone in scope (path order; skip prose-only / terminal):

1. Derive start URL ([milestone start URL](../review-learning-path/reference-checks.md#milestone-start-url)).
2. Navigate; check each `reftarget`: exists / missing / below-fold / state-dependent.
3. Record in `playwright.{milestone-slug}`.
4. One-line DOM result in chat per milestone (or batch briefly if all clean).

### Step B: Block Editor (opt-in, once)

After Playwright:

> Have you already smoke-tested this path in Block Editor (Show me / Do it)?
>
> Reply **`already-tested: <short notes>`** if yes (stack + anything flaky).
> Reply **`walk-me`** for a guided per-milestone check now (local JSON import, not the PR review tool).
> Reply **`skip-smoke`** to continue without recording Block Editor evidence.

| Reply | Behavior | Readiness |
|---|---|---|
| `already-tested: …` | Store dogfood evidence; no per-milestone loop | Can still be **Ready for PR** if Playwright clean and no post-inline blockers |
| `walk-me` | Guided loop: local import, `pass` / `fail step N` / `N/A`; fold false-step checks into the short watch-for line | Same when scoped milestones pass or documented N/A |
| `skip-smoke` | Continue | Cap at **Open PR with notes**; say Block Editor was not recorded |

### Checkpoint

> **Phase 2 complete**  -  live checks done.
>
> - Playwright: [short summary]
> - Block Editor: already-tested / walked / skipped
>
> **Your turn:** Reply **yes** for the readiness report.
>
> **Up next:** Phase 3  -  readiness + whether to fix anything.

---

## Phase 3: Readiness

**Goal:** Merge static + live into a readiness outcome; offer the right next action per finding kind.

Author chat shape: [Author-facing findings](reference-checks.md#author-facing-findings) (package-fixable vs needs-frontend).

### Agent steps

1. Apply [selector decision tree](../review-learning-path/reference-checks.md#selector-decision-tree) and promote only post-inline items.
2. Apply [readiness gate](reference-checks.md#readiness-gate).
3. Write `{slug}-readiness.md` with outcome + [PR opener checklist](reference-checks.md#pr-opener-checklist).
4. In chat: follow the Phase 3 checkpoint template below. Number every open finding. Mark each as package-fixable or needs-frontend. Zero findings is first-class (skip the fix list and celebrate).
5. Map replies: `fix all` / `fix N` / combos → Phase 4 **only for package-fixable items**; `frontend` → Phase 5 for needs-frontend items; `show report` → readiness path; `done` → end with PR-opener notes. If the author says **fix N** on a needs-frontend item, clarify that a guide edit alone will not add a `data-testid` and re-offer **frontend** (or a clearly labeled temporary selector workaround if they insist).

### Checkpoint (when there are findings)

Use a friendly outcome line (examples: "almost ready, with N copy fixes first" for Fix then re-preflight; "ready for PR" or "open PR with notes" when that is the gate). Do **not** say only the raw gate label with no context.

> **Phase 3  -  {friendly outcome}**
>
> **What we checked**
> - {e.g. Written product claims against live docs}
> - {e.g. Whether UI selectors exist on learn.grafana.net (shared stack)}
> - {e.g. Block Editor smoke: skipped / already-tested / walked}
>
> **Please fix these {N}** ({short kind})
>
> 1. {Plain problem}. {Why / better wording}.  
>    (`{file or dirs}`)
> 2. …
>
> **Your turn** *(include only the lines that apply)*
> - **fix all** / **fix N** / **fix 1,3** — package edits for copy or guide JSON that we can fix here
> - **frontend** — upstream `data-testid` for item(s) {N} (live miss; no durable selector in the DOM)
> - **done** — open a PR and leave these for review
> - **show report** — longer write-up
>
> **Heads-up** *(optional, only when useful)*  
> {Stack or testing note}

When **every** open item needs-frontend, omit **fix all** / **fix N**. Lead **Your turn** with **frontend**.

When the list mixes kinds, say which numbers **fix** covers vs **frontend** (see [Author-facing findings](reference-checks.md#author-facing-findings)).

### Checkpoint (when clean)

> **Phase 3  -  {Ready for PR | Open PR with notes}**
>
> **What we checked**
> - …
>
> Nothing here that would draw a review comment on copy or selectors. Nice work.
>
> **Your turn:** Reply **done** if you're opening the PR, or **show report** for the write-up.
>
> *(If Open PR with notes: say why in one line, e.g. Block Editor smoke was skipped.)*
>
> *(Optional **frontend** only if you want a proactive testid improvement when live already passed with a weak-but-working selector.)*

---

## Phase 4: Apply package fixes (optional)

**Goal:** Author-requested surgical edits (`fix all` / `fix N` / numbered combos) for **package-fixable** findings only.

### Tell the author

> **Phase 4  -  Apply fixes**
>
> Working on {fix all | item N | items …}. I'll edit `content.json` / `manifest.json` / `website.yaml` only, same discipline as [update-guide](../update-guide/SKILL.md).

### Agent steps

1. Apply only the numbered **package-fixable** findings the author requested. Do not pretend a guide `reftarget` tweak solves a needs-frontend gap unless they explicitly asked for a temporary workaround.
2. Re-run Pathfinder CLI validate if content/manifests changed.
3. Suggest re-running Phase 2 Playwright for touched interactive milestones.
4. Do not commit unless the author explicitly asks.

### Checkpoint

> **Phase 4 complete**  -  applied {N} fix(es).
>
> **Your turn:** Reply **yes** to refresh readiness, **frontend** if you still need a testid upstream, or **done**.

---

## Phase 5: Frontend selector PR (optional)

**Goal:** When a stable selector is missing upstream, walk the author through a small `data-testid` PR.

Follow [frontend-selector-pr.md](frontend-selector-pr.md). Canonical example: [grafana/grafana-cmab-app#1795](https://github.com/grafana/grafana-cmab-app/pull/1795).

### Checkpoint

> **Phase 5 complete**  -  frontend PR {url} *(or deferred)*.
>
> **Your turn:** Reply **done** when you're ready to open the learning path PR (or wait on the testid merge).

---

## Anti-patterns

**Do not**

- Edit package JSON before Phase 4 / without an explicit ask
- Leave audit artifacts in milestone `assets/`
- Commit `.cursor/lp-preflight-state/`
- Surface Internal/Discard nits in chat or readiness
- Use em dashes, rule numbers, or Blocker labels with the author
- Force a full Block Editor loop when they already dogfooded
- Recommend **Ready for PR** with open post-inline items
- Recommend **Ready for PR** on **new** / **conversion** interactive paths when Playwright was skipped
- Request website-repo changes (`pathfinder_data`, shortcodes) as package blockers
- Use the PR review tool as a substitute for local import (no PR yet)

**Do**

- Mirror five-phase review checklists and Learning Hub standards
- Keep chat tiny and friendly
- Dedupe findings by root cause
- Run CLI validate when available
- Offer Phase 4 / 5 after readiness

---

## Generated files

Write under `.cursor/lp-preflight-state/` (never commit):

| File | Phase | Purpose |
|---|---|---|
| `{slug}.json` | 0+ | Machine state ([schema](reference-checks.md#state-file-schema)) |
| `{slug}-findings.md` | 1 | Post-inline findings + verify-live notes |
| `{slug}-readiness.md` | 3 | Readiness gate + PR opener checklist |
| `{slug}/audits/{milestone}/` | 1 (optional) | Copied audit reports before cleanup |

Generated markdown frontmatter:

```markdown
---
disclaimer: Auto-generated by preflight-learning-path skill. Do not edit manually.
notice: To regenerate, re-run the skill from the relevant phase.
path_dir: {path_dir}
---
```

---

## Deep references

| Topic | Doc |
|---|---|
| Author routing + readiness | [reference-checks.md](reference-checks.md) |
| Prereqs + Playwright + optional smoke | [author-testing.md](author-testing.md) |
| Frontend testid PR | [frontend-selector-pr.md](frontend-selector-pr.md) |
| Shared static checklists + finding routing | [../review-learning-path/reference-checks.md](../review-learning-path/reference-checks.md) |
| Learning Hub structure | [../review-learning-path/learning-hub-standards.md](../review-learning-path/learning-hub-standards.md) |
| Comment voice (post-inline bar) | [../review-learning-path/comment-style.md](../review-learning-path/comment-style.md) |
| Reviewer workflow (mirror) | [../review-learning-path/SKILL.md](../review-learning-path/SKILL.md) |
| `website.yaml` | [docs/website-yaml-reference.md](../../../docs/website-yaml-reference.md) |
| Single-repo LP workflows | [learning-path-workflows/workflows.md](../../learning-path-workflows/workflows.md) |
