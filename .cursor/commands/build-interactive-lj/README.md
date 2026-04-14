# /build-interactive-lj

Add interactivity to an existing markdown learning path. Creates `content.json` and `manifest.json` files in the interactive-tutorials repo, and updates website markdown with `pathfinder_data` and `{{< pathfinder/json >}}`.

> **Creating a brand-new learning path?** Use `/create-learning-path` instead.

---

## Input

Ask the user for the **learning path slug** (the folder name from `website/content/docs/learning-paths/`).

---

## Workflow

Follow the steps in `.cursor/learning-path-workflows/workflows.md`. This is **Workflow A** (existing markdown).

The key difference from Workflow B: milestone markdown already exists. You update each `index.md` by adding `pathfinder_data` to the front matter and replacing the body with `{{< pathfinder/json >}}`.

---

## Critical rules

1. **Read all canonical feature docs before writing content.** Identify every Grafana product/feature referenced in the milestones. Read the docs pages in full from the local `website` repo first, then WebFetch. These docs are the authoritative source for all factual claims — never rely on training data.
2. **Scaffold ALL milestones.** Every milestone needs a `content.json`, including conceptual, intro, and conclusion pages. Pathfinder tracks progress through every milestone.
3. **Include supplementary content from frontmatter.** Extract `side_journeys`, `related_journeys`, and `cta.troubleshooting` from each `index.md` and add them as markdown blocks at the end of the `blocks` array.
4. **Use Playwright for selectors.** Never guess. Always inspect the actual DOM at `learn.grafana.net`.
5. **User handles all Pathfinder testing.** Tell the user which `content.json` to import into the Block Editor. Wait for their feedback. Never import JSON or click interactive buttons yourself.
6. **Ask before fixing.** When the user reports a broken selector, explain the problem and proposed fix, then wait for approval.
7. **3-attempt limit per selector.** If a selector fails after 3 tries, mark it `TODO:manual-review` and move on.
8. **Update CODEOWNERS.** Add the new `[slug]-lj/` directory to `.github/CODEOWNERS`.

---

## Anti-patterns

- Never use `description` — use `content`
- Never use `formvalue` — use `targetvalue`
- Never add `exists-reftarget` to requirements — it's auto-applied
- Never use position-based selectors (`:nth-child`, `:first-of-type`)
- Never use non-standard CSS (`:contains()`, `:has-text()`)
- Never use data-dependent selectors — use `^=` starts-with patterns
- Never leave placeholder selectors (`"[selector]"`, `"TODO"`)

---

## Reference

Consult these during the workflow:

| Document | When |
| --- | --- |
| `reference/json-schema.md` | Writing content.json (block types, action types, field reference) |
| `reference/selector-patterns.md` | Discovering selectors (priority, stability, anti-patterns) |
| `../create-learning-path/reference/frontmatter-schema.md` | Website front matter fields and CTA types |
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
