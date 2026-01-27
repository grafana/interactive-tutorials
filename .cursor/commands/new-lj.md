## Command: /new-lj

When an author tells you `/new-lj`, you will scaffold interactive content for an existing Learning Journey. This creates `content.json` files that add "Show me" / "Do it" interactivity to LJ milestones.

**Reference:** Read `@interactive-lj-guide.md` for the full workflow and JSON patterns.

---

### Step 1: Get the Learning Journey Name

Prompt the user for the Learning Journey name if not provided:

> What Learning Journey would you like to add interactivity to?
> (e.g., "drilldown-metrics", "linux-server-integration", "mysql-integration")

The name should match the folder name in `website/content/docs/learning-journeys/{lj-name}/`.

---

### Step 2: Verify the LJ Exists in the Website Repo

Check that the Learning Journey exists:

```
website/content/docs/learning-journeys/{lj-name}/
  _index.md           ← Main LJ page
  {milestone-1}/
    index.md          ← Milestone content
  {milestone-2}/
    index.md
  ...
```

If the LJ doesn't exist, inform the user and stop.

---

### Step 3: Check Recommender Mapping

Search the `grafana-recommender` repo for an existing mapping:

```bash
grep -r "{lj-name}" grafana-recommender/internal/configs/state_recommendations/
```

**If mapping exists:** Note the file and rule for the user.

**If no mapping exists:** Inform the user they'll need to create one:

> ⚠️ No recommender mapping found for this LJ. You'll need to add a rule to
> `grafana-recommender/internal/configs/state_recommendations/` before the
> interactive content will appear in Pathfinder.

---

### Step 4: Create the Branch (if not already on one)

Check the current branch:

```bash
git branch --show-current
```

If on `main`, create a new branch:

```bash
git checkout -b interactive-lj-{lj-name}
```

If already on an `interactive-lj-*` branch, confirm with the user before proceeding.

---

### Step 5: Create the Folder Structure

Create the LJ folder in `interactive-tutorials`:

```
interactive-tutorials/
  {lj-name}-lj/                    ← Add "-lj" suffix to distinguish from HTML tutorials
    {milestone-1}/
      content.json
    {milestone-2}/
      content.json
    ...
```

**Important:** Only create folders for milestones that have **Grafana UI interactions**. Skip milestones that are:
- Terminal/CLI only
- External configuration
- Pure reading/information

---

### Step 6: Read Each Milestone and Generate content.json

For each milestone with UI interactions:

1. **Read the `index.md`** from the website repo
2. **Extract the steps** the user needs to perform
3. **Check for existing selectors** in `interactive-tutorials/shared/snippets/` and other LJs
4. **Generate `content.json`** with this structure:

```json
{
  "id": "{lj-name}-{milestone-name}",
  "title": "Milestone Title from index.md",
  "blocks": [
    {
      "type": "markdown",
      "content": "Introductory text from the milestone."
    },
    {
      "type": "interactive",
      "action": "highlight",
      "reftarget": "TODO: find selector",
      "content": "Step description from markdown.",
      "requirements": ["exists-reftarget"]
    }
  ]
}
```

**Selector guidelines:**
- Use known-good selectors from `@selector-library.mdc` when available
- Use `TODO: find selector for {element description}` for unknown selectors
- Add `"doIt": false` for dropdowns, pickers, or context-dependent selections
- Use `"requirements": ["navmenu-open"]` for nav menu items

**Include images:** If the markdown has images, include them as image blocks:

```json
{
  "type": "image",
  "src": "/media/docs/learning-journey/{path}/image.png",
  "alt": "Description from markdown"
}
```

**Include videos:** If the markdown has YouTube videos (using `{{< docs/video >}}` shortcode), include them as video blocks:

```json
{
  "type": "video",
  "src": "https://www.youtube.com/embed/VIDEO_ID?start=0&end=57",
  "provider": "youtube",
  "title": "Video title based on context"
}
```

**Convert Hugo shortcodes:**
```markdown
{{< docs/video id="abc123" start="00" end="57" >}}
```
becomes:
```json
"src": "https://www.youtube.com/embed/abc123?start=0&end=57"
```

**Note:** The `start` and `end` attributes become URL query parameters. If only `start` is provided, omit `end` from the URL.

---

### Step 7: Output Summary

After scaffolding, provide a summary:

```
✅ Created interactive content for {LJ Name}

📁 Files created:
  - {lj-name}-lj/{milestone-1}/content.json
  - {lj-name}-lj/{milestone-2}/content.json
  - ...

⚠️ TODOs remaining:
  - {milestone-1}: 3 selectors need recording
  - {milestone-2}: 1 selector needs recording

📝 Next steps:
  1. Open Grafana Cloud with ?pathfinderDev=true
  2. Use the Block Editor to record missing selectors
  3. Test each milestone end-to-end
  4. Run /lint to validate the JSON
  5. Commit and push when ready
```

---

### Selector Patterns to Use

When generating content, prefer these known-good patterns:

**Navigation:**
```json
{
  "type": "multistep",
  "content": "Click **Section > Item**.",
  "steps": [
    { "action": "highlight", "reftarget": "button[aria-label='Expand section: SectionName']" },
    { "action": "highlight", "reftarget": "a[data-testid='data-testid Nav menu item'][href='/path']" }
  ]
}
```

**Buttons:**
```json
{
  "type": "interactive",
  "action": "button",
  "reftarget": "Button Text",
  "content": "Click **Button Text**."
}
```

**Form fields:**
```json
{
  "type": "interactive",
  "action": "formfill",
  "reftarget": "input[placeholder='Search']",
  "targetvalue": "example",
  "content": "Enter `example` in the search field."
}
```

**Dropdowns (Show me only):**
```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "label[data-testid*='Data source']",
  "content": "Select your data source.",
  "doIt": false
}
```

---

### What NOT to Include

- **No `tooltip` field** - Put all explanatory text in `content` or as markdown blocks
- **No dynamic selectors** - Avoid selectors with counts, timestamps, or user-specific values
- **No milestones without UI** - Skip terminal-only or config-file milestones

---

### After Scaffolding

Remind the user of the manual steps:

1. **Record selectors** using Pathfinder Block Editor (`?pathfinderDev=true`)
2. **Test interactivity** with "Show me" and "Do it" buttons
3. **Log issues** in `selector-issue-tracker/issues.md` for broken selectors
4. **Run `/lint`** to validate JSON structure
5. **Run `/check`** to review content quality
