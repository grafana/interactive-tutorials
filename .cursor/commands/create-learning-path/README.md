# /create-learning-path

Create a complete interactive learning path from scratch. Produces `content.json`, `manifest.json`, and `website.yaml` files in the interactive-tutorials repo.

> **Adding interactivity to an existing learning path?** Use `/build-interactive-lj` instead.

---

## Input

The user provides:
- **Feature or product goal** — what the learning path should teach
- **Target audience** — who it's for (typically Grafana beginners)

---

## Workflow

Follow these phases in order:

1. **Validate environment.** Confirm the `interactive-tutorials` repo is writable and the `website` repo is readable in the workspace, and that Playwright MCP is available. The `website` repo is a read-only source — it's used only to read canonical docs and any existing source markdown. All generated files are written to interactive-tutorials.
2. **Read feature docs.** Identify the canonical Grafana docs pages for the feature. Read every doc page in full from the local `website` repo first, then WebFetch.
3. **Propose path options.** Review existing paths in `interactive-tutorials/[slug]-lj` for structural patterns. Propose 2-4 path options with milestones. Target 2-5 minutes per milestone, 6-8 milestones per path (max 10). Wait for user approval before proceeding.
4. **Scaffold content files.** Create `content.json` for every milestone — interactive blocks for UI steps, markdown blocks for conceptual content. While writing sections, keep bookends **outside** the `section` (critical rule 14). Never put "You'll…" / "To … complete the following steps" as the first block inside a `section`.
5. **Create website metadata files.** Create `website.yaml` for the path and each milestone. Refer to `docs/website-yaml-reference.md`.
6. **Generate manifests.** Create `manifest.json` for the path (`type: "path"`, milestones array, targeting) and each milestone (`type: "guide"`, depends/recommends chain). Refer to `docs/manifest-reference.md`. Where fields can't be derived, ask the user to provide values before generating.
7. **Scaffold self-check (required).** Before Playwright, run [reference/scaffold-self-check.md](reference/scaffold-self-check.md): section bookends, `button` vs CSS `reftarget` misuse, secrets `doIt`, and a light claim pass against the docs you already read. Fix findings (or ask the author) before continuing.
8. **Discover selectors.** Use Playwright at `learn.grafana.net` to find stable CSS selectors for each interactive element. The user must log in through the Playwright browser window (Okta SAML).
9. **Test in Pathfinder.** Tell the user which `content.json` to import into the Block Editor at `learn.grafana.net/?pathfinder-dev=true`. Wait for their feedback on each "Show me" / "Do it" button. Fix broken selectors based on their reports.
10. **Verify and wrap up.** Re-run the light claim pass if prose changed. Cross-check remaining factual claims against live docs. Update `.github/CODEOWNERS`. Provide a summary of all files created.

For background on how this command relates to `/build-interactive-lj`, refer to `.cursor/learning-path-workflows/workflows.md`.

---

## Critical rules

1. **Never modify the website repo.** The `website` repo is a read-only source. Read canonical docs and any existing source markdown from it, but never add `pathfinder_data`, insert the `{{< pathfinder/json >}}` shortcode, or otherwise write to it. All generated files — `content.json`, `manifest.json`, and `website.yaml` — live in the interactive-tutorials repo.
2. **Read all canonical feature docs before writing content.** Identify the canonical Grafana docs pages for the feature. Read every doc page in full from the local `website` repo first, then WebFetch. These docs are the authoritative source — never rely on training data.
3. **Scaffold ALL milestones.** Every milestone needs a `content.json`, including conceptual, intro, and conclusion pages.
4. **Use Playwright for selectors.** Never guess. Always inspect the actual DOM at `learn.grafana.net`.
5. **User handles all Pathfinder testing.** Tell the user which `content.json` to import. Wait for their feedback. Never import JSON or click interactive buttons yourself.
6. **Ask before fixing.** When the user reports a broken selector, explain and propose a fix, then wait for approval.
7. **3-attempt limit per selector.** If a selector fails after 3 tries, mark it `TODO:manual-review` and move on.
8. **Update CODEOWNERS.** Add the new `[slug]-lj/` directory to `.github/CODEOWNERS`.
9. **Verify docs accuracy.** After testing, cross-check all factual claims against live Grafana documentation.
10. **Do not skip the scaffold self-check.** Section bookends, `button`/CSS misuse, and unsupported product claims must be caught before selector discovery. See [reference/scaffold-self-check.md](reference/scaffold-self-check.md).

---

## Anti-patterns

- In `content.json` blocks, use `content` for instruction text — not `description`. The `description` field belongs in `website.yaml` (see `docs/website-yaml-reference.md`).
- Never use `formvalue` — use `targetvalue`
- Include `exists-reftarget` in requirements for steps with a `reftarget` (repo convention)
- Never use position-based selectors (`:nth-child`, `:first-of-type`)
- Never use non-standard CSS (`:contains()`, `:has-text()`)
- Never use data-dependent selectors — use `^=` starts-with patterns
- Never leave placeholder selectors (`"[selector]"`, `"TODO"`)
- All links in content.json must be absolute URLs (`https://grafana.com/docs/...`), not relative
- Never put section intro/summary markdown **inside** the `section` when it will number as a fake step (`You'll…`, `To … complete the following steps`)
- Never use `action: "button"` with a CSS selector `reftarget` (use `highlight` or `navigate`)

---

## Reference

Consult these during the workflow:

| Document | When |
| --- | --- |
| `docs/website-yaml-reference.md` | Creating website.yaml (field reference, CTA types, examples) |
| `../build-interactive-lj/reference/json-schema.md` | Writing content.json (block types, action types, field reference) |
| `../build-interactive-lj/reference/selector-patterns.md` | Discovering selectors (priority, stability, anti-patterns) |
| `reference/scaffold-self-check.md` | After scaffold, before Playwright (bookends, claims, action sanity) |
| `docs/manifest-reference.md` | Generating manifest.json files |
| `.cursor/proven-patterns.mdc` | Reusable patterns for common Grafana UI elements (auto-loaded) |

---

## Quick reference

### Block types

`markdown` · `interactive` · `multistep` · `section` · `guided`

### Action types

`highlight` · `button` · `formfill` · `hover` · `navigate` · `noop` · `popout`

### Selector priority

`data-testid` > `aria-label` > `href` > `id` > stable class

### Key properties

- `doIt: false` — hides "Do it" button, keeps "Show me"
- `targetvalue` — text to enter for `formfill` actions
- `content` — instruction text for interactive blocks
