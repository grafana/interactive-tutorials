# Step 7: Verify Website Markdown

Verify that every milestone has a corresponding website `index.md` and that the path overview `_index.md` is present and correct.

---

## Tutorial Mode Introduction

```
**Step 7: Verify Website Markdown**

I'll check that all website markdown files are in place and correct:
- welcome/content.json exists and _index.md points to it
- Every milestone content.json has a corresponding index.md
- Front matter fields are valid (pathfinder_data, layout, weight, step)

Ready to verify? (Y/N)
```

Wait for confirmation, then verify.

---

## Expert Mode

Verify immediately without introduction.

---

## Verification Steps

### 1. List All Files

Check that every milestone has both files:

```bash
# content.json files
ls interactive-tutorials/[slug]-lj/*/content.json

# website index.md files
ls website/content/docs/learning-paths/[slug]/*/index.md
```

Every content.json milestone should have a matching index.md. Flag any mismatches.

### 2. Verify Front Matter Fields

For each milestone `index.md`, confirm:

| Field | Check |
|-------|-------|
| `layout` | Must be `single-journey` |
| `pathfinder_data` | Must be `[slug]-lj/[milestone]` matching the content.json path |
| `weight` | Must be present and ordered correctly across milestones |
| `step` | Must be present and sequential |
| `title` | Should match the content.json `title` |
| `cta.type` | Must be one of: `start`, `continue`, `success`, `conclusion` |

### 3. Verify Welcome Page

Check that `welcome/content.json` exists:

```bash
ls interactive-tutorials/[slug]-lj/welcome/content.json
```

Check that `_index.md` exists and points to it:

```bash
ls website/content/docs/learning-paths/[slug]/_index.md
```

For `_index.md`, confirm:

| Field | Check |
|-------|-------|
| `pathfinder_data` | Must be `[slug]-lj/welcome` |
| `layout` | Must be `single-journey` |
| `cascade.layout` | Must be `single-journey` |
| `journey` | Must have `group`, `skill`, `source`, `logo` |
| `cta.type` | Must be `start` |

### 4. Verify Body Content

Every page (`_index.md` and all `index.md` files) should have only:

```
{{< pathfinder/json >}}
```

Flag any files with additional body content (the interactive content lives in content.json, not in the markdown).

---

## Common Issues

| Issue | Fix |
|-------|-----|
| Missing `welcome/content.json` | Create it following the welcome template in Step 3 |
| Missing `index.md` for a milestone | Create it following the template in Step 3 |
| `_index.md` missing `pathfinder_data` | Add `pathfinder_data: [slug]-lj/welcome` |
| `_index.md` has hand-written body | Replace body with `{{< pathfinder/json >}}` |
| `pathfinder_data` path doesn't match | Update to `[slug]-lj/[milestone]` |
| Missing `layout: single-journey` | Add it to front matter |
| Weight/step ordering gaps | Renumber to maintain consistent increments |
| Title mismatch between content.json and index.md | Sync from content.json `title` |

---

## Completion

Display a summary showing: verification status per milestone (content.json vs index.md alignment), issues found (if any), and announce Step 8.
