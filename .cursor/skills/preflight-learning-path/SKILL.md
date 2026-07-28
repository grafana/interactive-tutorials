---
name: preflight-learning-path
description: >-
  Guide a learning path author through pre-PR self-review in interactive-tutorials.
  Mirrors /review-learning-path-pr (shared static checklists, shared claim-check,
  Playwright DOM, readiness) from the author side, then optional package fixes and
  optional frontend data-testid PR. Use when the user runs /preflight-learning-path.
---

# Preflight learning path (author self-review)

Walk through a `{slug}-lj/` package **before you open a PR**. Mirrors [review-learning-path](../review-learning-path/SKILL.md): shared static checklists, shared [claim-check](../review-learning-path/claim-check.md), Playwright DOM, then readiness and optional fixes. Author flow batches agent work and pauses only at real human gates (not a five-stop quiz).

**Terminology:** Say **learning path** or **path** in author messages; use `{path_dir}` in agent notes.

**Entry command:** [/preflight-learning-path](../../commands/preflight-learning-path.md)

**Mirror skill:** [review-learning-path](../review-learning-path/SKILL.md). Shared claim policy lives under the review skill so both callers cannot drift.

**Do NOT read external reference files upfront.** Each step loads its own references on demand.

**Skill memory:** State lives in `.cursor/lp-preflight-state/` (gitignored; never commit). Static pass dispatches [audit-guide](../audit-guide/SKILL.md), which writes `{milestone}/assets/`. See [Commit safety](#commit-safety).

**Routing:** [reference-checks.md](reference-checks.md) · [claim-check.md](claim-check.md) (pointer) · [author-testing.md](author-testing.md) · [frontend-selector-pr.md](frontend-selector-pr.md) · shared [claim-check](../review-learning-path/claim-check.md) · shared [learning-hub-standards.md](../review-learning-path/learning-hub-standards.md) · shared [review reference-checks](../review-learning-path/reference-checks.md)

**Related:** [audit-guide](../audit-guide/SKILL.md) · [update-guide](../update-guide/SKILL.md) · [review-learning-path](../review-learning-path/SKILL.md)

---

## Voice (author-facing)

Write like a calm teammate helping someone ship, not like a linter report.

| Do | Don't |
|---|---|
| Short sentences; plain words | Jargon in chat (`post-inline`, `MUST FIX`, "refresh readiness", rule numbers) |
| Say what is wrong, why it matters, which file | Dump severity labels or audit counts |
| Offer only actions that can resolve the item | Offer **fix N** when the real fix is upstream |
| Celebrate clean passes briefly | Hedge with "seems fine" / "maybe" |
| Pause only when you truly need the author | Quiz them with "reply yes" between agent-only steps |

No em dashes in author chat, readiness text, or drafted PR bodies. Use periods, commas, or parentheses.

Address the author as **you**. Prefer "copy fixes," "product claims vs docs," "UI selectors," "smoke test," "ready / not-ready summary."

---

## Author experience (hard flow)

Do as much as you can without stopping. Authors should not confirm every internal phase.

**Pause only for:**

1. Path unclear (ambiguous / missing `{path_dir}`)
2. Playwright MCP blocked or broken (setup)
3. Okta / browser ready before DOM checks (and stack choice, unless already known)
4. Block Editor smoke choice (and walk-me replies if they choose guided smoke)
5. Results + fix menu (and later fix / frontend / done)

**Do not** pause for "Phase 0 complete, reply yes" or "Phase 1 complete, reply yes" when the path is known and MCP is healthy. Run identify → static → then ask for login in one beat.

Internal **checkpoint** names (see [state schema](reference-checks.md#state-file-schema)) stay in state and agent notes. Author chat can say "checking your path," "live checks," "results" instead of a quiz board.

---

## Human-in-the-loop contract

| You (agent) | Author (human) |
|---|---|
| Infer path when clear; confirm only if ambiguous | Share `{path_dir}` when asked |
| Run static + claim-check without a mid-stop | Wait or do other work |
| Open Playwright; ask when logged in | Okta in Playwright browser; reply when ready |
| Run DOM checks; then ask about smoke | `already-tested` / `walk-me` / `skip-smoke` |
| One results + fix menu | `fix all` / `fix N` / `frontend` / `done` / `show report` |
| Apply package or frontend fixes only when asked | Approve edits / push |

---

## Workflow overview

```
Input (path_dir or current branch)
  │
  ├─ Identify + MCP check ─────── quiet unless path/MCP needs the author
  │
  ├─ Static pass ─────────────── audit + path/LH + claim-check (no author yes)
  │
  ├─ PAUSE: login + stack ────── Playwright Okta; stack (or static-only if allowed)
  │
  ├─ Playwright DOM ──────────── required (unless static-only)
  │
  ├─ PAUSE: smoke choice ─────── already-tested / walk-me / skip-smoke
  │
  ├─ Results + fix menu ──────── one readiness summary (former Phase 3)
  │
  ├─ Optional package fixes ──── fix all / fix N
  │
  └─ Optional frontend testid ── when needs-frontend
```

---

## Inputs

- **Required**: `{path_dir}` ending in `-lj/` (for example `monitor-azure-resources-lj`). Infer from current branch if omitted; confirm if ambiguous.
- **Optional**: `website_slug` (`{path_dir}` minus `-lj`). Website repo is read-only for conversion ([PR #416](https://github.com/grafana/interactive-tutorials/pull/416)).
- **Optional**: `learn_host` (default `learn.grafana.net`).
- **Optional**: `waive_live_testing` via `static-only: <reason>` at the login/stack pause. See [static-only preflight](reference-checks.md#static-only-preflight).

---

## Prerequisites

See [author-testing.md § Prerequisites](author-testing.md#prerequisites). Identify verifies Playwright MCP before live checks.

---

## Safety invariants

1. **Do not modify** `content.json`, `manifest.json`, or `website.yaml` until the author requests package-fixable fixes.
2. **Never commit** preflight artifacts (`.cursor/lp-preflight-state/` or audit-guide files under `{milestone}/assets/`). Remind the author once that reports are local and gitignored.
3. **Surface only review-level** findings in chat and readiness (same bar as review [comment-style](../review-learning-path/comment-style.md)). Never dump Internal/Discard nits.
4. **No em dashes** in author-facing chat, readiness text, or drafted PR bodies.
5. **One preflight run per path slug** (resume from state; do not fork duplicate state files).
6. **Never** plan companion website / `pathfinder_data` / shortcode work as package blockers.

---

## Commit safety

Same snapshot/cleanup rules as [review-learning-path § Commit safety](../review-learning-path/SKILL.md#commit-safety).

| Artifact | Where | Mitigation |
|---|---|---|
| Findings, claim-check, readiness, state JSON | `.cursor/lp-preflight-state/` | `.gitignore` (must ship with this skill) |
| audit-guide reports | `{milestone}/assets/` | Snapshot before static; delete new files before login pause |
| Pre-existing package `assets/` | Author/migrate notes | Never delete paths listed in `pre_review_assets` |

**Static snapshot:** `find {milestone}/assets -type f 2>/dev/null | sort` → store in state `pre_review_assets`.

**Static cleanup (mandatory before login pause):** remove audit files not in the snapshot; verify `git status --porcelain -- {path_dir}` shows no untracked audit paths.

---

## How this skill runs

1. Tell the author briefly what you are starting (path name when known). Do not lecture.
2. Run every agent-only step you can before the next real pause.
3. At a pause: one message, one clear ask. Plain language. **Do not advance** until they reply.
4. Do **not** invent extra "reply yes if this looks right" stops between agent-only work.
5. If they say "keep going" during a real pause (login / smoke / results), still honor that pause's need (e.g. you cannot DOM-check without login).

---

## Results menu format (after live)

| Section | Content |
|---|---|
| **Header** | Friendly outcome (e.g. almost ready, with N copy fixes first) |
| **What we checked** | Plain bullets: claims vs docs, UI selectors, smoke choice |
| **Findings** | Numbered: what is wrong, why it matters, which file |
| **Your turn** | Only actions that can resolve open items |
| **Heads-up** | Optional stack note; gitignore reminder if useful |

Do **not** open with a "What this check is" primer.

**Useful replies:** `ready` · `add playwright mcp` · `fix playwright mcp` · `static-only: <reason>` · `already-tested: <notes>` · `walk-me` · `skip-smoke` · `pass` / `fail step N - …` / `N/A - …` · `show report` · `fix all` · `fix 1` / `fix 2` / `fix 3` · `fix 1,3` · `frontend` · `done` · `resume` / `start fresh`

After package fixes, ask: **Want an updated ready / not-ready summary?** (not "refresh readiness").

---

## Resume

If `.cursor/lp-preflight-state/{slug}.json` exists:

> **Resume?** I have an in-progress preflight for `{path_dir}` (stopped at **`{checkpoint}`**).
>
> Reply **resume** to pick up, or **start fresh** to begin again.

On resume, read `checkpoint` + `status` from state and continue from that gate. Do not invent a numeric phase.

---

## Identify path + MCP (quiet unless blocked)

**Goal:** Confirm `{path_dir}`, `path_type`, milestones; verify Playwright MCP; init state.

**Persist:** After init (or when blocked on MCP), set `checkpoint` to `identify` (still blocked) or `login` (ready for login pause). Set `status: in_progress`.

### Author chat

If `{path_dir}` is missing or ambiguous:

> Which learning path package should I preflight? Share the `{slug}-lj/` directory, or tell me to infer it from your current branch.

If path is clear, say one short line (e.g. "Preflighting `{path_dir}`. Running the static checks now.") and continue. Do **not** ask them to confirm the path/type/MCP table when everything looks fine.

Mention once (early, not every pause): reports land under `.cursor/lp-preflight-state/` and are gitignored; do not force-add them to a PR.

### Agent steps

1. Infer or confirm `{path_dir}` (directory ending in `-lj`).
2. Record branch and HEAD sha.
3. Infer `website_slug` = `{path_dir}` minus `-lj` when website repo is in workspace (read-only).
4. Infer `path_type`: `new`, `conversion`, or `update` per [path type](reference-checks.md#path-type).
5. List milestones from path `manifest.json` `milestones` and dirs under `{path_dir}/`.
6. **Verify Playwright MCP** (`user-playwright`). Cover missing, needs-auth, toggled-off, **and configured-but-broken** per [If Playwright MCP is missing or broken](author-testing.md#if-playwright-mcp-is-missing-or-broken). Do not silently skip. Do not edit `mcp.json` until they agree.
7. Write `.cursor/lp-preflight-state/{slug}.json` ([state schema](reference-checks.md#state-file-schema)).

If MCP is blocked, stop with the blocked shape in author-testing.md (`checkpoint: identify`). Do not run live later until tools work.

---

## Static pass (no author yes)

**Goal:** Audit every milestone + path consistency + Learning Hub + claim-check. Keep findings for the final results menu.

**Persist:** Keep `checkpoint: login` while static runs (next human gate). Do not invent a separate author-facing "static done" pause.

### Agent steps

1. Snapshot `pre_review_assets`; dispatch [audit-guide](../audit-guide/SKILL.md) per milestone (parallel OK).
2. Walk shared [review reference-checks](../review-learning-path/reference-checks.md) + [learning-hub-standards.md](../review-learning-path/learning-hub-standards.md).
3. **Always scan** for framing-in-milestones, [section intro markdown that may number as a step](../review-learning-path/reference-checks.md#section-intro-markdown-numbered-as-a-step), and [false noops](../review-learning-path/reference-checks.md#noop-and-non-interactive-steps).
4. Run Pathfinder CLI `validate --packages {path_dir}` if available.
5. Run the shared [claim-check](../review-learning-path/claim-check.md) pass (preflight pointer: [claim-check.md](claim-check.md)). Write `{slug}-claim-check.md`. Route Contradicted / Unsupported / Overstated as Fix before PR. Do not edit package JSON here.
6. Tag findings with review [finding routing](../review-learning-path/reference-checks.md#finding-routing). Keep only review-level items for later author chat.
7. Write `{slug}-findings.md` (findings + verify-live notes).
8. Mandatory audit cleanup; verify `git status`.
9. Do not cite rule numbers or audit severity labels in chat.

Then go straight to the login pause (unless `static-only` was already set).

---

## PAUSE: Login + stack

**Goal:** Author is logged into Playwright on `{learn_host}`; record stack (or allow static-only when rules permit).

**Persist:** Before asking, `checkpoint: login`. After `ready`, set `checkpoint: dom`. After allowed `static-only`, set `checkpoint: results` and `waive_live_testing`.

> **Live checks next**
>
> I need you logged into `{learn_host}` in the **Playwright** browser (Okta there). I can open it for you if it is not open yet.
>
> Also tell me which stack you are using (for example `learn.grafana.net shared`, `fresh Cloud stack`).
>
> Reply **ready** when the Playwright browser is logged in (include the stack in the same reply if you have not already).
>
> Or **`static-only: <reason>`** to skip live testing (not for **new** / **conversion** interactive paths).

**Wait for:** `ready` (+ stack), or allowed `static-only: <reason>`.

Record `stack_state`, or `waive_live_testing` + `static_only_reason`.

**Reject** bare `static-only` and static-only on **new** / **conversion** with interactive milestones. Precedence: [static-only preflight](reference-checks.md#static-only-preflight).

If static-only: skip Playwright + smoke; jump to results menu with **Not live-tested** notes.

---

## Playwright DOM (no author yes between milestones)

Details: [author-testing.md](author-testing.md).

**Persist:** `checkpoint: dom` while sweeping; set `checkpoint: smoke` when DOM is done (before the smoke ask).

| `path_type` | Scope |
|---|---|
| **new** / **conversion** | Every interactive milestone in path `milestones` |
| **update** | Touched interactive milestones first; full path on request |

For each milestone in scope (path order; skip prose-only / terminal):

1. Derive start URL ([milestone start URL](../review-learning-path/reference-checks.md#milestone-start-url)).
2. Navigate; check each `reftarget`: exists / missing / below-fold / state-dependent.
3. Record in `playwright.{milestone-slug}`.

Keep chat quiet during the sweep (or a short progress line). Prefer documenting stack gaps over false "missing" on the wrong stack.

Then go to the smoke pause.

---

## PAUSE: Block Editor smoke

**Persist:** Before asking, `checkpoint: smoke`. After the author replies, set `checkpoint: results` (or stay on `smoke` during walk-me until scoped milestones finish).

> Have you already smoke-tested this path in Block Editor (Show me / Do it)?
>
> - **`already-tested: <short notes>`** if yes (stack + anything flaky)
> - **`walk-me`** for a guided per-milestone check now (local JSON import)
> - **`skip-smoke`** to continue without recording Block Editor evidence

| Reply | Behavior | Readiness |
|---|---|---|
| `already-tested: …` | Store dogfood evidence | Can still be **Ready for PR** if Playwright clean and no open blockers |
| `walk-me` | Guided loop per [author-testing.md](author-testing.md) | Same when scoped milestones pass or documented N/A |
| `skip-smoke` | Continue | Cap at **Open PR with notes** |

After smoke (or walk-me finishes), build readiness and show the **results menu** once.

---

## Results + fix menu

**Goal:** One readiness outcome; right next actions. Author chat shape: [Author-facing findings](reference-checks.md#author-facing-findings).

**Persist:** `checkpoint: results` when showing the menu. On `fix all` / `fix N` → `checkpoint: package_fixes`. On `frontend` → `checkpoint: frontend`. On `done` → `status: complete`, keep `checkpoint: results` (or `frontend` if that was last).

### Agent steps

1. Apply [selector decision tree](../review-learning-path/reference-checks.md#selector-decision-tree); promote only review-level items.
2. Apply [readiness gate](reference-checks.md#readiness-gate).
3. Write `{slug}-readiness.md` with outcome + [PR opener checklist](reference-checks.md#pr-opener-checklist).
4. Show the results menu below. Mark each finding package-fixable or needs-frontend.
5. Map replies: `fix all` / `fix N` → package fixes; `frontend` → frontend walkthrough; `show report` → readiness path; `done` → wrap with PR-opener notes.

### When there are findings

> **{Friendly outcome}**
>
> **What we checked**
> - {Product claims vs live docs}
> - {UI selectors on {stack}}
> - {Block Editor smoke: skipped / already-tested / walked}
>
> **Please fix these {N}** ({short kind})
>
> 1. {Plain problem}. {Why / better wording}.  
>    (`{file or dirs}`)
> 2. …
>
> **Your turn** *(include only lines that apply)*
> - **fix all** / **fix N** / **fix 1,3** — package edits we can make here
> - **frontend** — upstream `data-testid` for item(s) {N}
> - **done** — open a PR and leave these for review
> - **show report** — longer write-up
>
> **Heads-up** *(optional)*  
> {Stack note. Remind once if needed: preflight reports are gitignored under `.cursor/lp-preflight-state/`.}

When every open item needs-frontend, omit **fix all** / **fix N**. Lead with **frontend**.

### When clean

> **{Ready for PR | Open PR with notes}**
>
> **What we checked**
> - …
>
> Nothing here that would draw a review comment on copy or selectors. Nice work.
>
> **Your turn:** Reply **done** if you are opening the PR, or **show report** for the write-up.
>
> *(If Open PR with notes: say why in one line, e.g. Block Editor smoke was skipped.)*

---

## Package fixes (optional)

**Goal:** Surgical edits for **package-fixable** findings only (`fix all` / `fix N`).

**Persist:** `checkpoint: package_fixes` while editing; return to `checkpoint: results` after offering an updated summary.

> Working on {fix all | item N | items …}. I will edit `content.json` / `manifest.json` / `website.yaml` only, same discipline as [update-guide](../update-guide/SKILL.md).

1. Apply only requested package-fixable findings.
2. Re-run Pathfinder CLI validate if content/manifests changed.
3. Suggest re-running Playwright for touched interactive milestones when relevant.
4. Do not commit unless the author explicitly asks.

> Applied {N} fix(es).
>
> **Your turn:** Want an **updated ready / not-ready summary**? Or reply **frontend** / **done**.

---

## Frontend selector PR (optional)

When a stable selector is missing upstream, follow [frontend-selector-pr.md](frontend-selector-pr.md). Canonical example: [grafana/grafana-cmab-app#1795](https://github.com/grafana/grafana-cmab-app/pull/1795).

**Persist:** `checkpoint: frontend` for the whole walkthrough.

> Frontend PR {url} *(or deferred)*.
>
> **Your turn:** Reply **done** when you are ready to open the learning path PR (or wait on the testid merge).

---

## Anti-patterns

**Do not**

- Quiz the author between agent-only steps ("Phase N complete, reply yes")
- Edit package JSON without an explicit ask
- Leave audit artifacts in milestone `assets/`
- Commit `.cursor/lp-preflight-state/`
- Surface Internal/Discard nits in chat or readiness
- Use em dashes, rule numbers, Blocker labels, or "refresh readiness"
- Force a full Block Editor loop when they already dogfooded
- Offer **fix N** as the main path for a needs-frontend finding
- Recommend **Ready for PR** with open review-level items
- Recommend **Ready for PR** on **new** / **conversion** interactive paths when Playwright was skipped
- Request website-repo changes as package blockers
- Use the PR review tool instead of local import (no PR yet)
- Leave `checkpoint` stale across gates (resume depends on it)

**Do**

- Batch agent work; pause only for real human gates
- Persist named `checkpoint` after each gate
- Keep chat short, clear, and friendly
- Dedupe findings by root cause
- Run CLI validate when available
- Offer package vs frontend actions correctly after the results menu
- Run the shared claim-check (same policy as review)

---

## Generated files

Write under `.cursor/lp-preflight-state/` (never commit; gitignored):

| File | Purpose |
|---|---|
| `{slug}.json` | Machine state ([schema](reference-checks.md#state-file-schema)) |
| `{slug}-findings.md` | Findings + verify-live notes |
| `{slug}-claim-check.md` | Claim-check report |
| `{slug}-readiness.md` | Ready / not-ready summary + PR opener checklist |
| `{slug}/audits/{milestone}/` | Optional copied audit reports before cleanup |

```markdown
---
disclaimer: Auto-generated by preflight-learning-path skill. Do not edit manually.
notice: To regenerate, re-run the skill from the relevant pause.
path_dir: {path_dir}
---
```

---

## Deep references

| Topic | Doc |
|---|---|
| Author routing + readiness | [reference-checks.md](reference-checks.md) |
| Claim-check (product facts) | [../review-learning-path/claim-check.md](../review-learning-path/claim-check.md) (pointer: [claim-check.md](claim-check.md)) |
| Prereqs + Playwright + optional smoke | [author-testing.md](author-testing.md) |
| Frontend testid PR | [frontend-selector-pr.md](frontend-selector-pr.md) |
| Shared static checklists + finding routing | [../review-learning-path/reference-checks.md](../review-learning-path/reference-checks.md) |
| Learning Hub structure | [../review-learning-path/learning-hub-standards.md](../review-learning-path/learning-hub-standards.md) |
| Comment voice (review-level bar) | [../review-learning-path/comment-style.md](../review-learning-path/comment-style.md) |
| Reviewer workflow (mirror) | [../review-learning-path/SKILL.md](../review-learning-path/SKILL.md) |
| `website.yaml` | [docs/website-yaml-reference.md](../../../docs/website-yaml-reference.md) |
| Single-repo LP workflows | [learning-path-workflows/workflows.md](../../learning-path-workflows/workflows.md) |
