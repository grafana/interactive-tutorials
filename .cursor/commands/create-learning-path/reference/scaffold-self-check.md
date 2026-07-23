# Scaffold self-check (create / convert learning paths)

Run this **after** all `content.json`, `manifest.json`, and `website.yaml` files exist, and **before** Playwright selector discovery. Goal: catch Pathfinder structure and unsupported product claims while scaffolding is still cheap to fix. Do not wait for preflight or PR review for these items.

Use for `/create-learning-path` and `/build-interactive-lj`.

---

## When to run

1. Scaffold + manifests + `website.yaml` are on disk.
2. Before asking the author to log in for Playwright.
3. Again during wrap-up if you edited prose after selectors.

If the self-check finds issues, fix them (or ask the author) before moving on. Do not treat this as optional polish.

---

## 1. Section bookends (critical rule 14)

For every `section` in every milestone `content.json`:

| Check | Fail if |
| --- | --- |
| Intro bookend | There is no one-sentence markdown block **immediately before** the `section` that states what the learner will do. Exception: a pre-section line already covers the goal (for example "To …, complete the following steps:"). |
| Summary bookend | There is no one-sentence markdown block **immediately after** the `section` that states what the learner learned or what comes next. |
| Intro inside section | The **first child** of the `section` is markdown that starts with `You'll `, `You will `, `In this section`, or `To … complete the following` (Pathfinder often numbers that as a fake step). |

**Fix:** Move goal/intro markdown **outside** (before) the `section`. Keep interactive/multistep/guided blocks inside. Prefer a short outside summary after the section. If a section would contain only markdown (no interactive UI steps), drop the `section` wrapper and keep top-level markdown.

---

## 2. Action / selector sanity (scaffold-time)

Scan interactive blocks before live DOM work:

| Check | Fail if |
| --- | --- |
| `button` vs CSS | `action` is `button` but `reftarget` looks like a CSS selector (`a[…]`, `[data-testid=…]`, contains `=` or starts with `/` for a path used as click text). Use `highlight` (or `navigate`) for CSS. Use `button` only for visible button **label** text. |
| Secrets | Any `formfill` / Do-it path fills passwords, tokens, or API keys with `doIt` not `false`. |
| `exists-reftarget` | A block or step has `reftarget` but `requirements` omits `exists-reftarget` (repo convention). |
| Multistep singleton | A `multistep` has exactly one step. Convert to a plain `interactive` block. |

---

## 3. Light claim pass (scaffold-time)

Do a **short** product-fact check now. Full adversarial claim-check can still run later (preflight / review). At scaffold time, flag and fix:

| Pattern | Why |
| --- | --- |
| Absolutes without a source (`only`, `never`, `always`, `must`, `live only in…`) | Easy to overstate. Soften or cite docs. |
| Exit codes, defaults, limits, token types, action names | Must match the docs you already read (local `website` + live grafana.com). |
| Archived or renamed tooling | Example: do not teach `grafana/k6-action` if docs/blog point to `setup-k6-action` / `run-k6-action`. |
| Invented UI labels or menu paths | Must match the product UI or docs. |

**Procedure:** For each milestone, list falsifiable product sentences. For each, point to a docs quote or URL from the feature-docs pass. No source → rewrite or remove before selectors. Do not invent behavior from training data.

---

## 4. Report to the author

After the self-check, tell the author in plain language:

- What you fixed automatically
- Anything that still needs their call
- That Playwright is next

Keep it short. No severity labels or rule-number dumps unless they ask.

---

## 5. Deploy preview is a wrap-up decision (not this self-check)

Do **not** block Playwright on a website preview. When you open (or are about to open) the PR, ask the author if they want the Learning Hub deploy preview (`deploy-preview` label). Default recommendation for new `*-lj` paths: yes.

Remember: the preview workflow builds only on `opened` / `synchronize` while the label is present. If you add the label after the PR exists, push a commit so CI actually runs.
