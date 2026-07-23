# Frontend selector PR (preflight Phase 5)

Walk an author through adding a stable `data-testid` upstream when Pathfinder needs one and the DOM has no good selector.

**Canonical example:** [grafana/grafana-cmab-app#1795](https://github.com/grafana/grafana-cmab-app/pull/1795) (Add `data-testid` selectors to Usage page components).

Use that PR as the model for:

- Small, uniform component changes (testids only)
- Plain kebab-case names matching the product area
- PR title/body that explains Pathfinder authoring needs stable selectors
- Friendly, low-ceremony tone

Do not paste the whole #1795 diff. Link it and mirror the pattern. No em dashes in drafted PR bodies.

---

## When to enter Phase 5

Trigger when Phase 2 shows a step needs a durable selector and:

- No `data-testid` / strong semantic attribute exists in the DOM, and
- Live Playwright or walk-me failed on that step (or the author wants a proactive testid anyway), and
- They reply **`frontend`** at Phase 3 or ask during Phase 4

At Phase 3, treat this as a **needs-frontend** finding: lead with **frontend**, not **fix N**. A package-only `reftarget` tweak is not the real fix. Only offer a temporary weak selector in the guide if the author explicitly asks, and label it as brittle.

If live passed with a justified `:contains()` and no stable selector exists, that stays Internal in review terms. Offer Phase 5 as an optional improvement, not a Fix-before-PR demand, unless Playwright/walk-me failed on that step.

---

## Walkthrough (checkpointed)

Announce **Phase 5 - frontend selector (step X of 5)** at each stop. One ask per message.

### 1. Confirm the element

From Playwright: URL, visible label, current weak selector, screenshot or DOM snippet if helpful.

Propose a `data-testid` (plain kebab-case, product-area prefix, matching existing testids in that app when present).

> **Phase 5  -  frontend selector (step 1 of 5)**
>
> **Element that failed live**
> - Page: {url or page name}
> - Control: {visible label}
> - Guide selector today: `{reftarget}`
>
> **Proposed `data-testid`:** `{proposed-name}`
>
> **Your turn:** Reply **yes** if that name is fine, or suggest a different kebab-case name.

**Wait for:** author OK on the name (or edits).

### 2. Locate owning source

- Default core UI: `grafana/grafana`
- Plugin app pages (`/a/grafana-*-app/...`): that plugin repo (as #1795 did for CMAB)

Use workspace clones or GitHub search. Do **not** invent file paths.

> **Phase 5  -  frontend selector (step 2 of 5)**
>
> Best guess for owning source: `{repo}` ({why}).
>
> Next I will confirm the exact file(s). I will not invent paths.
>
> **Your turn:** Reply **yes** if `{repo}` looks right, or name a different repo.

**Wait for:** confirm repo + file(s).

### 3. Draft the change

- Minimal diff: add `data-testid` (and wire through component props if needed)
- Match local naming conventions
- Draft PR title + body in the style of #1795 (Pathfinder needs stable selectors; keep scope tight)

Example body shape (adapt; do not copy blindly):

```markdown
Hey folks, I was building a Pathfinder guide and noticed some UI elements lacked stable selector IDs.

Adds `data-testid` attributes to {components} following the existing kebab-case naming on this page. These selectors are needed for interactive Pathfinder guides, which prefer `data-testid` over text or class-based targeting.

Example pattern: https://github.com/grafana/grafana-cmab-app/pull/1795
```

> **Phase 5  -  frontend selector (step 3 of 5)**
>
> Draft change: add `{testid}` on {component summary}. Testids only; no behavior change.
>
> **Title:** {title}
>
> **Body:** (show draft)
>
> **Your turn:** Reply **yes** to approve, or say what to change.

**Wait for:** author approval of the draft.

### 4. Open the PR

1. Confirm `gh` auth and write access
2. Create branch, commit, push (**ask before push**)
3. `gh pr create` with the approved title/body
4. Follow existing grafana org repo norms; do not change repo visibility

> **Phase 5  -  frontend selector (step 4 of 5)**
>
> Ready to open the PR in `{repo}` with the approved title/body.
>
> **Your turn:** Reply **yes** to push and create the PR, or **hold** to stop here.

Record `frontend_pr_url` in preflight state after create.

### 5. Update the guide selector

Update the milestone `reftarget` to the new testid **only after** the author confirms the frontend change is available on their test stack.

Until then: keep a temporary justified fallback if needed, and note the upstream PR URL in readiness / Open PR with notes.

> **Phase 5  -  frontend selector (step 5 of 5)**
>
> Frontend PR: {url}
>
> When `{testid}` is on your test stack, we can update `{milestone}` to `[data-testid="{testid}"]`. We should not change the guide before that lands.
>
> **Your turn:** Reply **update guide** when the testid is available, or **done** to leave the guide as-is for now.

---

## Anti-patterns

- Giant refactors or drive-by UI changes in the testid PR
- Inventing component paths
- Updating guide JSON to a testid that is not on the test stack yet without saying so
- Treating a missing upstream testid as something to "fix" only inside `interactive-tutorials` when the DOM has no stable hook
- Offering bare **fix N** at Phase 3 as if a guide edit adds the testid
