# /create-learning-path

Create a complete interactive learning path from scratch. Produces `content.json` and `manifest.json` files in the interactive-tutorials repo, and creates website markdown with `pathfinder_data` and `{{< pathfinder/json >}}`.

> **Adding interactivity to an existing learning path?** Use `/build-interactive-lj` instead.

---

## Input

The user provides:
- **Feature or product goal** — what the learning path should teach
- **Target audience** — who it's for (typically Grafana beginners)

---

## Workflow

Follow the steps in `.cursor/learning-path-workflows/workflows.md`. This is **Workflow B** (new from scratch).

The key difference from Workflow A: no milestone markdown exists. You create the `_index.md` and every `[milestone]/index.md` from scratch with full Hugo front matter, `pathfinder_data`, and `{{< pathfinder/json >}}`. Refer to `reference/frontmatter-schema.md` for the complete front matter templates.

### Planning (unique to this workflow)

Before writing files, propose 2-4 path options with milestones. Get user approval before proceeding. Follow these scope guidelines:
- Target 2-5 minutes per milestone, 6-8 milestones per path (max 10)
- Read all canonical feature docs before proposing (same rule as Workflow A)

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
