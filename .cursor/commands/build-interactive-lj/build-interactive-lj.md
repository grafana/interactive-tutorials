# Build Interactive Learning Journey

This command automates the creation of interactive content (`content.json` files) for learning journeys in Grafana Pathfinder.

---

## Workflow Overview

When a writer runs `/build-interactive-lj [slug]`, display this introduction:

```
👋 Welcome to the Interactive Learning Journey Builder!

I'll help you create interactive content that enables "Show me" and "Do it" 
functionality in Grafana Pathfinder.
```

### Here's what we'll do together

| Step | What I'm doing | What you'll see |
|------|----------------|-----------------|
| **1. ENVIRONMENT** | Checking repos, Playwright, and GitHub CLI | ✅/❌ checklist of your setup |
| **2. VALIDATE** | Finding the LJ, listing milestones, checking recommender | List of milestones found |
| **3. SCAFFOLD** | Creating content.json files with markdown from source | File creation progress |
| **4. DISCOVER** | Opening browser, navigating Grafana, finding selectors | Browser automation |
| **5. TEST** | Importing JSON into Pathfinder, clicking Show me | Highlights in real-time |
| **6. REPORT** | Summarizing results, identifying fixes needed | Pass/fail summary |

### What you'll need

- Grafana Cloud instance URL (e.g., `https://yourstack.grafana.net/`)
- ~30-60 minutes depending on milestone count
- Your attention during testing to verify highlights work

### What you'll gain

- Complete `content.json` files for each milestone
- Tested selectors that work in Pathfinder
- Ready-to-PR interactive content

---

Then ask:

```
Is this your first time using this command? (Y/n)
```

**If YES (tutorial mode):** Provide detailed explanations at each step.
**If NO (expert mode):** Move quickly with minimal explanation.

---

Then say:

```
First up is **Environment Validation** - I'll check that you have the required 
repositories, Playwright browser automation, and GitHub CLI configured.

This ensures we can discover selectors and file issues for any that don't work.

Ready to proceed with Step 1? (Y/n)
```

Wait for confirmation before proceeding.

---

## Step 1: Environment Validation

**CHECKPOINT 1** - This step is MANDATORY before proceeding.

Run these checks and display results:

### 1.1 Required Repositories

Check that these directories exist in the Cursor workspace:

```
✅ website repo: /Users/.../website
✅ interactive-tutorials repo: /Users/.../interactive-tutorials  
✅ grafana-recommender repo: /Users/.../grafana-recommender
```

On failure:
```
❌ [repo] not found in workspace

See setup instructions: SETUP.md#required-repositories
```

### 1.2 Playwright MCP

Test browser automation:

```
✅ Playwright MCP: Connected
```

On failure:
```
❌ Playwright MCP not available

See setup instructions: SETUP.md#playwright-mcp-setup
```

### 1.3 GitHub CLI

Check authentication:

```
✅ GitHub CLI: Authenticated as [username]
```

On failure:
```
❌ GitHub CLI not authenticated

See setup instructions: SETUP.md#github-cli-setup
```

### Checkpoint 1 Complete

Only proceed when ALL checks pass:

```
✅ Environment Validation Complete

All systems ready. Proceeding to Step 2...
```

---

## Step 2: Learning Journey Validation

**CHECKPOINT 2** - Validate the learning journey exists and is mapped.

### 2.1 Find Source Content

Locate the learning journey in the website repo:

```
website/content/docs/learning-journeys/[slug]/
```

List all milestones found:

```
Found learning journey: [title]

Milestones:
1. [milestone-1-title] (milestone-1-slug)
2. [milestone-2-title] (milestone-2-slug)
...
```

### 2.2 Check Recommender Mapping

Search `grafana-recommender` for rules that map this LJ:

```
✅ Recommender mapping found: [rule file]
   URL pattern: [urlPrefix value]
```

On failure:
```
❌ No recommender mapping found for this learning journey

The LJ won't appear in Pathfinder until mapped. 
Continue anyway? (Y/n)
```

### Checkpoint 2 Complete

```
✅ Learning Journey Validation Complete

Ready to scaffold [N] milestones. Proceed? (Y/n)
```

---

## Step 3: Scaffold Content Files

**CHECKPOINT 3** - Create content.json files for each milestone.

For each milestone:

1. Read the source markdown from `website/content/docs/learning-journeys/[slug]/[milestone]/index.md`
2. Create directory: `interactive-tutorials/[slug]-lj/[milestone]/`
3. Create `content.json` with:
   - `id`: Derived from slug
   - `title`: From frontmatter
   - `blocks`: Convert markdown steps to block structure

### Block Conversion Rules

- Numbered steps → `interactive` blocks with `action: "highlight"` and empty `reftarget`
- Explanatory text → `markdown` blocks
- Navigation instructions → Individual `highlight` blocks (NOT multistep)

**IMPORTANT**: Do NOT use `multistep` blocks - Pathfinder Block Editor does not support them.

### Checkpoint 3 Complete

```
✅ Scaffold Complete

Created content.json files:
- [slug]-lj/milestone-1/content.json
- [slug]-lj/milestone-2/content.json
...

Ready for selector discovery. Provide your Grafana Cloud URL:
```

---

## Step 4: Selector Discovery

**CHECKPOINT 4** - Use Playwright to discover selectors for each interactive element.

### 4.1 Get Grafana URL

```
Enter your Grafana Cloud URL (e.g., https://yourstack.grafana.net/):
```

### 4.2 Navigate and Discover

For each milestone with empty `reftarget` fields:

1. Navigate to the appropriate Grafana page
2. Use Playwright to inspect the DOM
3. Find stable selectors in this priority order:
   - `data-testid` attributes (most stable)
   - `aria-label` attributes
   - `id` attributes
   - `placeholder` attributes
   - `href` for links
4. Update the `content.json` with discovered selectors

### Selector Discovery Patterns

```javascript
// Priority 1: data-testid
[data-testid='data-testid Data source settings page name input field']

// Priority 2: aria-label
button[aria-label='Expand section: Administration']

// Priority 3: Specific attributes
input[placeholder='Search Grafana plugins']
a[href='/plugins']
```

### Checkpoint 4 Complete

```
✅ Selector Discovery Complete

Discovered selectors for [N] interactive elements.
Ready to test in Pathfinder? (Y/n)
```

---

## Step 5: Test in Pathfinder (Rapid-Fire Mode)

**CHECKPOINT 5** - Test all selectors in Pathfinder Block Editor.

### 5.1 Enter Dev Mode

1. Navigate to Grafana
2. Open Pathfinder (Help button or `?` key)
3. Enter Block Editor / Dev Mode

### 5.2 Rapid-Fire Testing

For each milestone:

1. Import the `content.json` into Block Editor
2. Click through EVERY "Show me" button rapidly
3. Click "Do it" where applicable (skip if `doIt: false`)
4. **Only stop and screenshot if something FAILS**
5. Report one summary per milestone

### Testing Output Format

**On Success:**
```
✅ Milestone: [name]
   All [N] steps passed
```

**On Failure:**
```
❌ Milestone: [name]
   Step [N] failed: [step description]
   Selector: [reftarget value]
   Issue: [what went wrong]
   
   [Screenshot if failure]
```

### Handling Failures

When a selector fails:

1. **Try to fix**: Use Playwright to find the correct selector
2. **Update content.json**: Apply the fix
3. **Re-test**: Import and test again
4. **If unfixable**: Note for GitHub issue

### Checkpoint 5 Complete

```
✅ Testing Complete

Results:
- [N] milestones passed
- [N] milestones need fixes
- [N] selectors need GitHub issues
```

---

## Step 6: Report and Next Steps

**CHECKPOINT 6** - Final summary and recommended actions.

### Summary Report

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
[If any selectors consistently failed]

### Next Steps
1. Review the content.json files
2. Run: git add [slug]-lj/
3. Commit and create PR
```

### Filing GitHub Issues

For selectors that cannot be fixed, file an issue:

```
gh issue create \
  --repo grafana/interactive-tutorials \
  --title "[Selector] [element description] in [LJ name]" \
  --body "..."
```

---

## Error Recovery

If the workflow fails at any point:

1. Note which checkpoint failed
2. Fix the issue using SETUP.md guidance
3. Re-run: `/build-interactive-lj [slug]`
4. The workflow will resume from the failed checkpoint

---

## Quick Reference

### Commands
- `/build-interactive-lj [slug]` - Full workflow
- Restart: Re-run the command

### Key Files
- Source: `website/content/docs/learning-journeys/[slug]/`
- Output: `interactive-tutorials/[slug]-lj/`
- Mapping: `grafana-recommender/internal/configs/`

### Block Types (Supported)
- `markdown` - Explanatory text
- `interactive` - "Show me" / "Do it" actions
  - `action: "highlight"` - Click element
  - `action: "button"` - Click button by text
  - `action: "formfill"` - Enter text
  - `action: "navigate"` - Go to URL

### Block Types (NOT Supported)
- `multistep` - Do NOT use, Pathfinder Block Editor doesn't support it
