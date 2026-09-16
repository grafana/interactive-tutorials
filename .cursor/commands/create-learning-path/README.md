# /create-learning-path

Create a complete interactive learning path — either from an approved plan (a docs-ai Grafana Learn journey already defined its scope and milestones) or from scratch (just a feature goal and audience). Produces `content.json` and `manifest.json` files in the interactive-tutorials repo, and creates website markdown with `pathfinder_data` and `{{< pathfinder/json >}}`.

> **Adding interactivity to an existing learning path?** Use `/build-interactive-lj` instead.

---

## Input

Two ways this command gets started. Detect which one you're in before doing anything else.

**A. From an approved plan (preferred when one exists).** The prompt names a source journey, a package slug, a scope described as coming from "the approved journey outline" or "the approved journey plan," and/or points at an `outline.md` file in the docs-ai repo (typically `journeys/<slug>/outline/outline.md`). This is what `docs-ai`'s journey workflow generates and pastes in — a plan a human already reviewed and signed off on. Treat every field the prompt supplies (scope, milestones, package slug, source journey) as **decided, not proposed**. Do not re-derive them from the docs. If the prompt names a jargon-inventory file (`outline/reference/jargon-inventory.md`, `## UI elements` section), read it and use those exact names for buttons and pages — a slide and a path must never call the same UI element two different names.

**B. From scratch.** No plan is supplied — just a feature or product goal and a target audience. Propose the path yourself (phase 3 below runs in full).

If you're unsure which one you're in, ask. Don't guess: building from a stale or partial reading of "approved" input is worse than asking once.

---

## Workflow

Follow these phases in order:

1. **Validate environment.** Confirm both the `website` and `interactive-tutorials` repos are accessible in the workspace and Playwright MCP is available.
2. **Read feature docs.** Identify the canonical Grafana docs pages for the feature. Read every doc page in full from the local `website` repo first, then WebFetch. Track which pages you read — these go into the path `_index.md` front matter as `source_docs`. Do this regardless of Input mode: an approved plan supplies scope and milestone names, never the milestone content itself.
3. **Decide the path options.**
   - **Mode A (approved plan):** skip proposing options. Use the supplied scope, milestones, and package slug as given. If the outline file is reachable, read it (and the source journey's outline) to confirm the milestones still make sense against the current docs — flag it to the user and stop if something has clearly drifted (a milestone's procedure no longer exists, for example), but otherwise proceed without asking for re-approval of a plan that was already approved.
   - **Mode B (from scratch):** review existing paths in `website/content/docs/learning-paths/` for structural patterns. Propose 2-4 path options with milestones. Target 2-5 minutes per milestone, 6-8 milestones per path (max 10). Wait for user approval before proceeding.
4. **Scaffold content files.** Create `content.json` for every milestone — interactive blocks for UI steps, markdown blocks for conceptual content.
5. **Create website markdown.** Create `_index.md` and every `[milestone]/index.md` from scratch with full Hugo front matter, `pathfinder_data`, and `{{< pathfinder/json >}}` body. Refer to `reference/frontmatter-schema.md` for the complete front matter templates.
6. **Generate manifests.** Create `manifest.json` for the path (`type: "path"`, milestones array, targeting) and each milestone (`type: "guide"`, depends/recommends chain). Refer to `docs/manifest-reference.md`.
7. **Discover selectors.** Use Playwright at `learn.grafana.net` to find stable CSS selectors for each interactive element. The user must log in through the Playwright browser window (Okta SAML).
8. **Test in Pathfinder.** Tell the user which `content.json` to import into the Block Editor at `learn.grafana.net/?pathfinder-dev=true`. Wait for their feedback on each "Show me" / "Do it" button. Fix broken selectors based on their reports.
9. **Verify and wrap up.** Cross-check all factual claims against live docs. Update `.github/CODEOWNERS`. Provide a summary of all files created.

For background on how this command relates to `/build-interactive-lj`, refer to `.cursor/learning-path-workflows/workflows.md`.

---

## Critical rules

1. **Read all canonical feature docs before writing content.** Identify the canonical Grafana docs pages for the feature. Read every doc page in full from the local `website` repo first, then WebFetch. These docs are the authoritative source — never rely on training data.
2. **Scaffold ALL milestones.** Every milestone needs a `content.json`, including conceptual, intro, and conclusion pages.
3. **Use Playwright for selectors.** Never guess. Always inspect the actual DOM at `learn.grafana.net`.
4. **User handles all Pathfinder testing.** Tell the user which `content.json` to import. Wait for their feedback. Never import JSON or click interactive buttons yourself.
5. **Ask before fixing.** When the user reports a broken selector, explain and propose a fix, then wait for approval.
6. **3-attempt limit per selector.** If a selector fails after 3 tries, mark it `TODO:manual-review` and move on.
7. **Update CODEOWNERS.** Add the new `[slug]-lj/` directory to `.github/CODEOWNERS`.
8. **Verify docs accuracy.** After testing, cross-check all factual claims against live Grafana documentation.

---

## Anti-patterns

- Never use `description` — use `content`
- Never use `formvalue` — use `targetvalue`
- Never add `exists-reftarget` to requirements — it's auto-applied
- Never use position-based selectors (`:nth-child`, `:first-of-type`)
- Never use non-standard CSS (`:contains()`, `:has-text()`)
- Never use data-dependent selectors — use `^=` starts-with patterns
- Never leave placeholder selectors (`"[selector]"`, `"TODO"`)
- All links in content.json must be absolute URLs (`https://grafana.com/docs/...`), not relative

---

## Reference

Consult these during the workflow:

| Document | When |
| --- | --- |
| `reference/frontmatter-schema.md` | Creating website front matter (field reference, CTA types, templates) |
| `../build-interactive-lj/reference/json-schema.md` | Writing content.json (block types, action types, field reference) |
| `../build-interactive-lj/reference/selector-patterns.md` | Discovering selectors (priority, stability, anti-patterns) |
| `docs/manifest-reference.md` | Generating manifest.json files |
| `.cursor/proven-patterns.mdc` | Reusable patterns for common Grafana UI elements (auto-loaded) |

---

## Quick reference

### Block types

`markdown` · `interactive` · `multistep` · `section` · `guided`

### Action types

`highlight` · `button` · `formfill` · `hover` · `navigate` · `noop`

### Selector priority

`data-testid` > `aria-label` > `href` > `id` > stable class

### Key properties

- `doIt: false` — hides "Do it" button, keeps "Show me"
- `targetvalue` — text to enter for `formfill` actions
- `content` — instruction text for interactive blocks
