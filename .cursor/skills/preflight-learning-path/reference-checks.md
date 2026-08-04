# Reference checks (preflight-learning-path)

Author-side routing and readiness for [preflight-learning-path/SKILL.md](SKILL.md).

**Shared checklists (source of truth):** [../review-learning-path/reference-checks.md](../review-learning-path/reference-checks.md) and [../review-learning-path/learning-hub-standards.md](../review-learning-path/learning-hub-standards.md). Run every checklist the five-phase review coach runs in Phase 1.

**Publishing model (PR [#416](https://github.com/grafana/interactive-tutorials/pull/416)):** Single-repo packages in `interactive-tutorials`. Metadata in package `website.yaml`; prose in `content.json`. Website repo is read-only for conversion. Never plan companion website / `pathfinder_data` / shortcode work.

**Voice bar:** Same severity bar as review [comment-style.md](../review-learning-path/comment-style.md) (review-level only in chat). No em dashes. Prefer everyday words in chat (see [Author-facing findings](#author-facing-findings) and [Voice](SKILL.md#voice-author-facing)).

---

## Author-facing findings

Use this shape for the **one results menu** after live (or after allowed static-only). Do **not** open with a "What this check is" primer. Match [Voice](SKILL.md#voice-author-facing).

1. **Friendly outcome line** (e.g. "almost ready, with 3 copy fixes first"). Keep gate labels in the readiness file; chat can stay plainer.
2. **What we checked** — short bullets in plain language (product claims vs docs, UI selectors on `{stack}`, Block Editor smoke choice).
3. **Numbered findings** — each item: plain problem, why it matters or better wording, then the file/dir in parentheses. Enough context that the author can decide without opening the skill. Treat each item as **package-fixable** or **needs-frontend** (see below).
4. **Your turn** — offer only actions that can resolve the open items:
   - **fix all** / **fix N** / combos — only for **package-fixable** items (prose, manifest, `website.yaml`, guide `reftarget` when a better selector already exists in the DOM)
   - **frontend** — when any open item **needs-frontend** (live failed; no durable `data-testid` / strong semantic selector in the DOM). Do **not** offer **fix N** for that item as if a guide edit alone is the real fix
   - **done** — open PR / leave for review
   - **show report**
5. **Heads-up** — optional stack/testing notes (already-installed plugins, read-only provisioned sources, etc.).

### Package-fixable vs needs-frontend

| Kind | Examples | Results menu offer |
|---|---|---|
| **Package-fixable** | Claim-check copy, framing/`depends`, fake in-section steps, false noops, wrong `reftarget` when a stable testid already exists in the DOM | **fix N** / **fix all** |
| **Needs-frontend** | Playwright or walk-me failed; element has no durable selector in the DOM | **frontend** (primary). Optional: clearly labeled **try temporary selector** only if the author asks for a brittle package workaround. Never present bare **fix N** as the main path for this kind |

When the list mixes both kinds, number everything, but in **Your turn** say which numbers **fix** covers and that **frontend** covers the selector gap (e.g. "fix 2,3 for copy; **frontend** for item 1").

Keep the identify + static work quiet when the path is known. Put the full numbered + fix-choice treatment in the **one results menu** after live (or after allowed static-only).

### Framing finding wording

When a framing ID is in path `milestones`, use wording like:

> `{slug}` is framing (value / why). Omit it from Pathfinder path `milestones` so the in-app path stays action-oriented. Keep the package and `website.yaml` — the website Learning Path still shows it. First hands-on `depends` must be `[]`.

Never say “remove this milestone” without the Pathfinder-only / website-kept distinction.

---

## Finding severity (author)

Map review [finding routing](../review-learning-path/reference-checks.md#finding-routing) 1:1:

| Review tier | Author action |
|---|---|
| **Post inline** | **Fix before PR** (surface in chat + readiness) |
| **Internal** | Hide (do not mention in chat or readiness) |
| **Discard** | Hide |

Do not invent an author-only softer bar. Do not surface "Polish / follow-up" lists.

### Must surface (post-inline examples)

Apply the same five-phase coach rules (cite shared reference-checks; do not soften):

- Playwright / Block Editor runtime fail (when live failed or `walk-me` failed)
- **Framing milestones** listed in path `milestones`, or first hands-on `depends` on a framing ID (must be `depends: []`). When surfacing: say this is **Pathfinder-only** (omit from `milestones` so Pathfinder stays action-oriented); keep the framing package + `website.yaml` for the website Learning Path. Do not imply the milestone is removed from the website.
- **Fake steps in sections:** missing bookends outside the section; in-section intro markdown that numbers as a step (e.g. first child "You'll …")
- **False noops:** learner-action copy with `noop` and no `reftarget`
- Missing / broken required `website.yaml` identity; Learning Hub structure the author must change
- Path root / manifest `id` mismatch; Pathfinder CLI validate failure
- Secrets `doIt: true`; confirmed 404s; conversion prose only in legacy markdown
- Fragile / wrong selectors when live fails, or stable `data-testid` exists in DOM and the guide uses a weak selector
- **Claim-check MUST FIX:** Contradicted, Unsupported, or Overstated product facts per shared [claim-check.md](../review-learning-path/claim-check.md) (made-up counts, invented names, docs contradictions)

### Never surface

Wording polish, justified `:contains()` when live passed, CODEOWNERS reminders, audit noise, selector polish when live passed, landing screenshot notes, milestone-count guidelines.

---

## Checklists to run (Phase 1)

Apply every section from [../review-learning-path/reference-checks.md](../review-learning-path/reference-checks.md):

- Milestone `content.json` checks
- Section intro markdown numbered as a step
- Framing milestones / framing vs not framing
- Path root `content.json`
- Learning Hub structure + [learning-hub-standards.md](../review-learning-path/learning-hub-standards.md)
- `website.yaml`
- Valid manifests (CLI)
- Targeting / recommender
- Supplementary content
- Legacy website source (conversion, read-only)
- noop and non-interactive steps
- CODEOWNERS (discard for author chat)

Then run shared [claim-check.md](../review-learning-path/claim-check.md) across path root + milestone prose. Route Contradicted / Unsupported / Overstated as Fix before PR. Hide Supported from chat. Author-decides items may appear in readiness as open questions.

Tag each finding; keep only post-inline for author-facing output.

---

## Path type

Infer from branch diff, directory age, and legacy website source. Record in `{slug}.json` → `path_type`.

| Type | Signals | Live emphasis |
|---|---|---|
| **new** | New `{slug}-lj/`; no legacy website folder | Full Playwright; `website.yaml` + path root completeness |
| **conversion** | Built via `/build-interactive-lj`; prose-heavy | Legacy prose captured in package; Playwright full path |
| **update** | Changes existing package only | Touched interactive milestones first |

---

## Static-only preflight

`static-only: <reason>` at the **login / stack pause** skips Playwright and smoke (jump to the results menu).

**Precedence (evaluate in order; first match wins):**

1. **Bare `static-only` (no reason)** → always **reject**.
2. **`path_type` is `new` or `conversion` and the path has interactive milestones** → always **reject**, even if the author cites "no stack access" or "practice run." Playwright is mandatory here.
3. **`path_type` is `update` and the change touches only markdown / `website.yaml` (no interactive selector work)** → **allow** with a non-empty reason. Cap readiness (never **Ready for PR** if interactive milestones exist and were not live-tested).
4. **Practice run / no stack access on `update` only** → **allow** with a non-empty reason. Cap readiness the same way.
5. Anything else → **reject** and ask for a clearer reason or proceed with live checks.

| Situation | Allowed? |
|---|---|
| Bare `static-only` | **No** |
| **new** / **conversion** with interactive milestones (any reason, including no stack) | **No** |
| **update** touching only markdown / `website.yaml` | Yes, with reason |
| **update** practice / no stack access | Yes, with reason (caps readiness) |

Record `waive_live_testing` + `static_only_reason` only when allowed.

When live was skipped or incomplete, readiness must include **Not live-tested** (interactive path `milestones` minus recorded Playwright results). Never recommend **Ready for PR** for new/conversion interactive when Playwright was waived.

---

## Readiness gate

Recommend **Ready for PR** only when all are true:

1. Zero open **Fix before PR** (post-inline) items
2. Pathfinder CLI validate passed, or CLI unavailable was noted and no other blockers
3. Playwright: no unexplained **missing** selectors on claimed-tested milestones (or documented stack prerequisite)
4. Block Editor: `already-tested` or successful `walk-me` (not `skip-smoke`) for new/conversion interactive, **or** author accepts **Open PR with notes**
5. `git status` clean of audit-guide artifacts under `{path_dir}`
6. Not `waive_live_testing` on new/conversion interactive (or outcome is **Open PR with notes**)

| Outcome | When |
|---|---|
| **Ready for PR** | Gate conditions met |
| **Fix then re-preflight** | Open post-inline items or Playwright/walk-me failures |
| **Open PR with notes** | Package mergeable but smoke skipped, or fresh-stack retest notes for the reviewer |

---

## PR opener checklist

Include in `{slug}-readiness.md`:

- [ ] Path `{path_dir}` validates with Pathfinder CLI (or CLI unavailable noted)
- [ ] First hands-on milestone `depends: []`
- [ ] No framing IDs in path `manifest.json` `milestones` (Pathfinder-only omission; framing packages remain for the website)
- [ ] `schemaVersion: "1.1.0"` or omitted on milestone `content.json`
- [ ] Playwright DOM checked for scoped interactive milestones
- [ ] Block Editor: already-tested notes, walk-me results, or skip noted for reviewer
- [ ] Path and milestone `website.yaml` complete
- [ ] **Not live-tested** section in PR description if any interactive milestone skipped Playwright
- [ ] Single PR in `interactive-tutorials` only (no companion website PR)

---

## State file schema

Path: `.cursor/lp-preflight-state/{slug}.json`

```json
{
  "path_dir": "monitor-azure-resources-lj",
  "slug": "monitor-azure-resources-lj",
  "website_slug": "monitor-azure-resources",
  "path_type": "conversion",
  "branch": "docs/my-path",
  "head_commit": "abc123",
  "learn_host": "learn.grafana.net",
  "stack_state": "learn.grafana.net shared",
  "waive_live_testing": false,
  "static_only_reason": null,
  "smoke_mode": null,
  "smoke_notes": null,
  "pre_review_assets": {},
  "checkpoint": "login",
  "status": "in_progress",
  "readiness": null,
  "playwright": {},
  "pathfinder": {},
  "frontend_pr_url": null
}
```

| Field | Notes |
|---|---|
| `smoke_mode` | `already-tested` \| `walk-me` \| `skip-smoke` \| null |
| `smoke_notes` | Author notes for already-tested / skip |
| `pathfinder` | Only when `walk-me`; keys = milestone slug |
| `playwright` | DOM results per milestone |
| `checkpoint` | Named gate (required). One of: `identify` \| `login` \| `dom` \| `smoke` \| `results` \| `package_fixes` \| `frontend`. Persist at every gate per [SKILL.md](SKILL.md). Do **not** use integer phase 0–5. |
| `status` | `in_progress` \| `blocked` \| `complete` |
| `readiness` | `Ready for PR` \| `Fix then re-preflight` \| `Open PR with notes` |

Legacy state files with numeric `phase` are invalid for resume: ask **start fresh**, or map once (`0`→`identify`, `1`→`login`, `2`→`dom`, `3`→`results`, `4`→`package_fixes`, `5`→`frontend`) then rewrite `checkpoint` and drop `phase`.

---

## Pathfinder CLI validate

```bash
node {pathfinder-app}/dist/cli/cli/index.js validate --packages {path_dir}
```

CLI failure → Fix before PR. CLI missing → note in readiness; do not abort the whole preflight.
