# Build Interactive Learning Journey

This command automates the creation of interactive content (`content.json` files) for learning journeys in Grafana Pathfinder.

---

## Welcome

When a writer runs `/build-interactive-lj`, display this welcome:

```
👋 Welcome to the Interactive Learning Journey Builder!

I'm here to help you create interactive content that powers the "Show me" and 
"Do it" buttons in Grafana Pathfinder. By the end of our session, you'll have 
fully functional content.json files ready for a PR.

Here's what our session will look like:

1. **Environment check** — I'll verify your setup is ready (repos, browser 
   automation, GitHub CLI). Takes about 30 seconds.

2. **Find your learning journey** — I'll locate the source content and list 
   all the milestones we'll be making interactive.

3. **Scaffold the files** — I'll create the content.json structure for each 
   milestone, converting your markdown steps into interactive blocks.

4. **Discover selectors** — This is where the magic happens! I'll open a 
   browser, navigate through Grafana, and find the CSS selectors that target 
   each UI element you want to highlight.

5. **Test in Pathfinder** — We'll import each file into Pathfinder's Block 
   Editor and click through every "Show me" button to verify the highlights 
   work. You'll see the highlights in real-time.

6. **Wrap up** — I'll summarize what we built and give you the next steps 
   for committing and creating a PR.

Expect this to take 30-60 minutes depending on how many milestones your 
learning journey has. I'll need your attention during testing so you can 
verify the highlights look right.
```

---

## Ask: First Time?

```
Is this your first time using /build-interactive-lj? (Y/n)
```

---

## If YES (Tutorial Mode)

```
Great! I'll walk you through the process step by step.

Before each step, I'll explain what I'm about to do and ask for your 
confirmation before proceeding. This way you'll understand exactly what's 
happening and can ask questions along the way.

Ready to get started? (Y/n)
```

Wait for confirmation.

---

## If NO (Expert Mode)

```
Welcome back! I'll move quickly through the steps.

Ready to get started? (Y/n)
```

Wait for confirmation.

---

## Ask: Which Learning Journey?

```
Which learning journey would you like to make interactive?

Provide the slug (the folder name) from:
website/content/docs/learning-journeys/

Examples: prometheus, github-data-source, mysql-data-source
```

Wait for the user to provide the LJ slug, then proceed to Step 1.

---

## Step 1: Environment Validation

### Tutorial Mode Introduction

```
**Step 1: Environment Validation**

I'll check that your setup is ready:
- Three repositories in your workspace (website, interactive-tutorials, grafana-recommender)
- Playwright browser automation working
- GitHub CLI authenticated (for filing selector issues if needed)

If anything fails, I'll point you to SETUP.md for instructions.

Ready to proceed? (Y/n)
```

Wait for confirmation, then run checks.

### Expert Mode

Run checks immediately without introduction.

### Run Checks

Check these and display results:

- ✅/❌ `website` repo in workspace
- ✅/❌ `interactive-tutorials` repo in workspace
- ✅/❌ `grafana-recommender` repo in workspace
- ✅/❌ Playwright MCP available
- ✅/❌ GitHub CLI authenticated

**On any failure:** Direct user to `SETUP.md` for that specific section.

**On all pass:**
```
✅ Environment ready. Proceeding to Step 2...
```

---

## Step 2: Learning Journey Validation

### Tutorial Mode Introduction

```
**Step 2: Learning Journey Validation**

I'll locate the "[slug]" learning journey and:
- Find all milestones (the steps users complete)
- Check if it's mapped in the recommender (so it appears in Pathfinder)

Ready to proceed? (Y/n)
```

Wait for confirmation, then validate.

### Expert Mode

Validate immediately without introduction.

### Validate

1. Find source: `website/content/docs/learning-journeys/[slug]/`
2. List all milestones found
3. Search `grafana-recommender` for mapping rules

**Display:**
```
Found learning journey: [title]

Milestones:
1. [milestone-1-title] (milestone-1-slug)
2. [milestone-2-title] (milestone-2-slug)
...

Recommender mapping: ✅ Found / ❌ Not found
```

**On success:**
```
✅ Learning journey validated. Ready to scaffold [N] milestones.
```

---

## Step 3: Scaffold Content Files

### Tutorial Mode Introduction

```
**Step 3: Scaffold Content Files**

I'll create the content.json structure for each milestone:
- Read the source markdown from the website repo
- Create directories in interactive-tutorials/[slug]-lj/
- Convert steps to interactive blocks (with empty selectors for now)

Ready to proceed? (Y/n)
```

Wait for confirmation, then scaffold.

### Expert Mode

Scaffold immediately without introduction.

### Scaffold

For each milestone:
1. Read `website/content/docs/learning-journeys/[slug]/[milestone]/index.md`
2. Create `interactive-tutorials/[slug]-lj/[milestone]/content.json`
3. Convert content using these rules:
   - Numbered steps → `interactive` blocks with `action: "highlight"` and empty `reftarget`
   - Explanatory text → `markdown` blocks
   - Sequential navigation steps (e.g., "Navigate to X > Y > Z") → `multistep` blocks

### JSON Schema Requirements

**IMPORTANT:** Use these exact field names or validation will fail:

```json
// Interactive block (correct)
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "[selector]",
  "content": "Click **Button** to do the thing.",  // NOT "description"
  "requirements": ["exists-reftarget"]
}

// Formfill block (correct)
{
  "type": "interactive",
  "action": "formfill",
  "reftarget": "[selector]",
  "targetvalue": "value to enter",  // NOT "formvalue"
  "content": "Enter the value.",
  "requirements": ["exists-reftarget"]
}

// Multistep block (correct)
{
  "type": "multistep",
  "content": "Navigate to **X > Y > Z**.",
  "requirements": ["navmenu-open"],
  "steps": [
    { "action": "highlight", "reftarget": "[selector-1]" },
    { "action": "highlight", "reftarget": "[selector-2]" },
    { "action": "highlight", "reftarget": "[selector-3]" }
  ]
}
```

**Common mistakes to avoid:**
- ❌ `description` → ✅ `content`
- ❌ `formvalue` → ✅ `targetvalue`
- ❌ `title` on interactive blocks (not needed)

**Display:**
```
✅ Scaffold complete

Created:
- [slug]-lj/milestone-1/content.json
- [slug]-lj/milestone-2/content.json
...

Next: selector discovery. What's your Grafana Cloud URL?
```

---

## Step 4: Selector Discovery

### Tutorial Mode Introduction

```
**Step 4: Selector Discovery**

I'll use browser automation to find selectors for each interactive element:
- Navigate to the relevant Grafana pages
- Inspect the DOM to find stable selectors
- Update the content.json files with discovered selectors

Selector priority: data-testid > aria-label > id > placeholder > href

Ready to proceed? (Y/n)
```

Wait for confirmation, then discover.

### Expert Mode

Discover immediately without introduction.

### Discover

1. Navigate to the starting page for the LJ
2. For each interactive block with empty `reftarget`:
   - Navigate to the relevant page
   - Find the element using Playwright snapshot
   - Extract the best available selector
   - Update the content.json

**Display progress:**
```
Discovering selectors for [milestone-name]...
- [element description]: [selector found]
- [element description]: [selector found]
...
```

**On complete:**
```
✅ Selector discovery complete

Found selectors for [N] interactive elements.
Ready to test in Pathfinder?
```

---

## Step 5: Test in Pathfinder (Rapid-Fire Mode)

### Tutorial Mode Introduction

```
**Step 5: Test in Pathfinder**

I'll test every selector in Pathfinder's Block Editor:
- Import each content.json
- Click through all "Show me" buttons rapidly
- Click "Do it" where applicable
- Only stop and screenshot if something FAILS

You'll see highlights in real-time. Watch for any that don't work.

Ready to proceed? (Y/n)
```

Wait for confirmation, then test.

### Expert Mode

Test immediately without introduction.

### Test

1. Navigate to Grafana
2. Open Pathfinder (Help button or `?` key)
3. Enter Block Editor / Dev Mode
4. For each milestone:
   - Import the content.json
   - Rapid-fire through all "Show me" clicks
   - Report one summary per milestone

**On success:**
```
✅ Milestone: [name] - All [N] steps passed
```

**On failure:**
```
❌ Milestone: [name]
   Step [N] failed: [description]
   Selector: [reftarget]
   [Screenshot]
```

**Handling failures:**
1. Try to find correct selector with Playwright
2. Update content.json
3. Re-test
4. If unfixable, note for GitHub issue

---

## Step 6: Report and Next Steps

### Summary

```
## Build Interactive LJ: [slug]

### Results
- Total milestones: [N]
- Passed: [N]
- Failed: [N]

### Files Created
- [slug]-lj/milestone-1/content.json ✅
- [slug]-lj/milestone-2/content.json ✅
...

### Issues to File
[List any selectors that couldn't be fixed]

### Next Steps
1. Review the content.json files
2. git add [slug]-lj/
3. Commit and create PR
```

### Filing GitHub Issues

For broken selectors, file an issue at https://github.com/grafana/interactive-tutorials/issues

```
gh issue create \
  --repo grafana/interactive-tutorials \
  --title "[Selector] [element] in [LJ name]" \
  --body "..."
```

---

## Quick Reference

### Key Files
- Source: `website/content/docs/learning-journeys/[slug]/`
- Output: `interactive-tutorials/[slug]-lj/`
- Mapping: `grafana-recommender/internal/configs/`

### Block Types
- `markdown` - Explanatory text
- `interactive` - "Show me" / "Do it" actions
  - `action: "highlight"` - Click element by selector
  - `action: "button"` - Click button by text
  - `action: "formfill"` - Enter text in field (use `targetvalue` for the value)
  - `action: "navigate"` - Go to URL
- `multistep` - Groups sequential navigation steps (shows "▶ Run N steps" button)
