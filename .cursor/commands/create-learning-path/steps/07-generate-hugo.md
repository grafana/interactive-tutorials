# Step 7: Generate Hugo Markdown

Run the generator script to produce Hugo-compatible `index.md` files from the enriched JSON.

---

## Tutorial Mode Introduction

```
**Step 7: Generate Hugo Markdown**

I'll run the generator script to produce the website markdown files:
- Reads the `website` key from each content.json
- Produces Hugo front matter + {{< pathfinder/json >}} shortcode
- Skips files without a `website` key (Hugo-only milestones)

Ready to generate? (Y/N)
```

Wait for confirmation, then generate.

---

## Expert Mode

Generate immediately without introduction.

---

## Generate

### 1. Dry Run First

Always dry-run before writing:

```bash
node scripts/generate-hugo.mjs [slug]-lj --dry-run
```

Review the output with the user. Confirm the front matter looks correct.

### 2. Generate for Real

```bash
node scripts/generate-hugo.mjs [slug]-lj
```

### 3. Verify Output

Check that generated files exist:

```bash
ls website/content/docs/learning-paths/[slug]/*/index.md
```

### 4. Diff Against Existing (If Applicable)

If this path already has hand-written markdown:

```bash
cd website && git diff content/docs/learning-paths/[slug]/
```

The diff should show only cosmetic YAML formatting differences (quote style, field ordering). Any content differences indicate the JSON `website` key or `title` needs updating.

---

## Files NOT Generated

These files are not produced by the generator and must be maintained manually:

| File | Reason |
|---|---|
| `_index.md` | Path overview with Hugo shortcodes |
| Milestones without `website` key | Hugo-only content with shortcodes |

Remind the user to verify these files are present and correct.

---

## Display

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Step 7 complete: Hugo Markdown Generated

Generated [N] index.md files:
├── website/.../[milestone-1]/index.md
├── website/.../[milestone-2]/index.md
└── ...

Skipped [N] (no website key):
├── [milestone-name] (Hugo-only)
└── ...

Manual files to verify:
├── website/.../[slug]/_index.md (path overview)
└── website/.../[hugo-only-milestone]/index.md

⏳ Next: Step 8 - Report and Next Steps
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
