# Shared Critical Rules

Rules 1–15 that apply to **all** generated guides (source-code and dashboard skills). Every rule is blocking. Skill-specific additions follow the extension point marker below.

---

## Critical Rules

1. **No markdown titles** -- the guide `title` renders in the app frame; a leading `## Title` duplicates it
2. **`exists-reftarget` is auto-applied** -- never add it manually to requirements
3. **`navmenu-open`** required for any step targeting navigation menu elements
4. **`on-page:/path`** required for page-specific interactive actions
5. **Tooltips** -- under 250 characters, one sentence, don't name the highlighted element
6. **`verify`** on all state-changing actions (Save, Create, Test)
7. **`doIt: false` for secrets** -- never automate filling passwords/tokens/keys
8. **Section bookends** -- 1-sentence "what you'll do" intro markdown, 1-sentence "what you learned" summary markdown
9. **Sections, not markdown headers** -- group steps with `section` blocks, each with a unique kebab-case `id`
10. **Connect sections** -- if section 1's objective creates a resource, section 2 should require it
11. **Action-focused content** -- "Save your configuration" not "The save button can be clicked"
12. **Bold only GUI names** -- "Click **Save & test**" not "Click the **Save & test** button"
13. **`skippable: true`** for conditional fields and permission-gated steps
14. **No multistep singletons** -- a `multistep` with one step must be a plain `interactive` block
15. **No focus-before-formfill** -- `highlight` on an input with `doIt: true` is a no-op; use `formfill` or set `doIt: false`

---

<!-- EXTENSION POINT: Skill-specific rules go here in the file that includes these shared rules -->
