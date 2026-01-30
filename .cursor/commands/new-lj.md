## Command: /new-lj

This command scaffolds a new interactive Learning Journey (LJ) from existing content in the `website` repository. It supports two modes:

- **Tutorial Mode**: For first-time users - detailed explanations at each step with Y/N confirmations
- **Expert Mode**: For experienced users - quick checks with minimal pauses

---

## Step 0: Mode Selection

**Always start with project context, then ask about experience level:**

```
Welcome to the /new-lj workflow! 🚀

I'm excited to help you create interactive Learning Journeys! Let me tell you 
a bit about what we'll be doing together.

**Learning Journeys** are step-by-step guides that help Grafana users accomplish 
specific tasks - things like setting up alerting, creating dashboards, or 
configuring integrations. You may have already written some of these!

**Interactive LJs** take things a step further. When users click "Show me" or 
"Do it" buttons, Pathfinder (Grafana's in-app guide system) highlights UI 
elements, fills in forms, and walks users through tasks directly in the 
Grafana interface. Pretty cool, right?

**In this workflow**, we'll take an existing Learning Journey from the 
documentation website and create the JSON files that power the interactive 
experience. This involves:
- Reading the source content from the website repo
- Converting procedural steps into interactive blocks
- Recording UI selectors so Pathfinder knows what to highlight

Don't worry if any of this sounds new - I'll guide you through each step!

Is this your first time using this workflow? (Y/N): _
```

- **Y** → Tutorial Mode (detailed explanations, confirmations at each checkpoint)
- **N** → Expert Mode (quick checks, only pause on errors or before file creation)

---

## Step 1: Workspace & Repository Setup (Checkpoint 1/8)

This is the critical first checkpoint. We need to ensure the user has all three repositories available in their Cursor workspace.

### Tutorial Mode

```
📍 CHECKPOINT [1/8]: Workspace & Repository Setup
─────────────────────────────────────────────────

**What I'm about to do:**
Check that your Cursor workspace is set up correctly for this workflow.

This workflow requires access to three repositories:
- `interactive-tutorials` - where we create interactive JSON content
- `website` - contains the source Learning Journey markdown files
- `grafana-recommender` - contains the rules that map LJs to Grafana pages

**Why this matters:**
A "workspace" in Cursor lets me access multiple repositories at once. Without 
all three repos in your workspace, I can only see files in whichever repo you 
currently have open - and we need all three to complete this workflow!

Ready to proceed? (Y/N): _
```

**If N:** "No problem! What questions do you have about this step?"
- Answer their questions
- Re-prompt: "Ready to proceed now? (Y/N)"

**If Y:** Run the verification in this order:

#### Step A: Check current workspace

Read the Workspace Paths from user_info to see what repos are currently accessible.

**If all 3 repos are in workspace:**
```
✅ Workspace setup looks great!

All three repositories are in your workspace:
- `website` ✓
- `interactive-tutorials` ✓
- `grafana-recommender` ✓
```
→ Continue to Step 2

**If some repos are missing from workspace:**
```
⚠️ Your workspace is missing some repositories.

Currently in your workspace:
- `website` ✓
- `interactive-tutorials` ✗ (not in workspace)
- `grafana-recommender` ✗ (not in workspace)

Let me check if these repos exist on your machine...
```
→ Continue to Step B

#### Step B: Search for missing repos on disk

Check sibling folders of repos that ARE in the workspace.

```bash
# If website is at /Users/x/repos/website, check for siblings:
ls -d /Users/x/repos/interactive-tutorials 2>/dev/null
ls -d /Users/x/repos/grafana-recommender 2>/dev/null
```

**If repos found on disk but not in workspace:**
```
✅ Good news! I found the missing repos on your machine:
- `interactive-tutorials` → /Users/x/repos/interactive-tutorials
- `grafana-recommender` → /Users/x/repos/grafana-recommender

They're just not in your current Cursor workspace. I can create a workspace 
file that includes all three repos.

Would you like me to create a workspace file? (Y/N): _
```

**If Y:** Create workspace file (see Step D)

**If repos NOT found on disk:**
```
❌ I couldn't find these repos on your machine:
- `interactive-tutorials`
- `grafana-recommender`

You'll need to clone them before we can continue. Here are the commands to run 
in your terminal (I recommend putting them in the same folder as your existing repos):

  cd /Users/x/repos
  git clone git@github.com:grafana/interactive-tutorials.git
  git clone git@github.com:grafana/grafana-recommender.git

💡 **Troubleshooting:** If cloning fails with a permission error, SSH may not be 
configured for GitHub. Run `ssh -T git@github.com` to check, or use HTTPS instead:

  git clone https://github.com/grafana/interactive-tutorials.git
  git clone https://github.com/grafana/grafana-recommender.git

Let me know when you've cloned them and we can continue! (Y when ready): _
```

→ After user confirms clone complete, continue to Step C

#### Step C: Verify cloned repos

After the user confirms they've cloned the repos, verify they exist:
```bash
ls -d [workspace-parent-folder]/interactive-tutorials 2>/dev/null
ls -d [workspace-parent-folder]/grafana-recommender 2>/dev/null
```

**If verification succeeds:** Continue to Step D
**If verification fails:** Ask the user to check the clone location and try again

#### Step D: Create workspace file (manual)

If repos exist but aren't all in the workspace, provide instructions to create a `.code-workspace` file:

```
📁 You need to create a Cursor workspace file to access all three repos at once.

**Here's how to create it:**

1. Create a new file called `interactive-lj-workspace.code-workspace` in your 
   repos folder (e.g., /Users/x/repos/)

2. Paste this content into the file:

{
  "folders": [
    { "path": "/Users/x/repos/website" },
    { "path": "/Users/x/repos/interactive-tutorials" },
    { "path": "/Users/x/repos/grafana-recommender" }
  ],
  "settings": {}
}

   ⚠️ Make sure to update the paths to match your actual folder locations!

3. Save the file

4. In Cursor, go to **File → Open Workspace from File...**

5. Select your new `interactive-lj-workspace.code-workspace` file

6. Cursor will reload with all three repos in the sidebar

7. Run `/new-lj` again once the workspace is open

Let me know when you're ready to continue! (Y when workspace is open): _
```

### Expert Mode

Run all checks silently. Only output on issues:
```
❌ Workspace incomplete. Missing: [repo names]
   Run /new-lj in tutorial mode (Y at first prompt) for setup help.
```

---

## Step 2: Get LJ Name

**Ask the user:**
```
What Learning Journey would you like to make interactive?

Please provide either:
- The LJ title (e.g., "Visualize metrics in a Grafana Cloud dashboard")
- The LJ folder name (e.g., "visualization-metrics")
```

Wait for response before proceeding.

---

## Step 3: Verify LJ Exists in Website Repo (Checkpoint 2/8)

### Tutorial Mode

```
📍 CHECKPOINT [2/8]: Learning Journey Verification
──────────────────────────────────────────────────

**What I'm about to do:**
Search for "[LJ name]" in the website repository to find:
- The LJ's `_index.md` file (journey overview)
- All milestone folders and their `index.md` files

**Why this matters:**
Interactive content must be based on existing, published Learning Journeys.
We need to read the source markdown to:
- Understand the milestone structure
- Extract step-by-step instructions
- Identify which milestones have interactive potential

Ready to proceed? (Y/N): _
```

**If Y:** Search for the LJ:
```bash
find content/docs/learning-journeys -type d -name "[lj-folder-name]"
```

Then read and display:
- LJ title and description from `_index.md`
- List of milestones with their titles and weights
- Identify which milestones have procedural steps (interactive candidates)

### Expert Mode

Run search, display summary:
```
✅ Found LJ: [title]
   Path: content/docs/learning-journeys/[folder]/
   Milestones: [count] total, [count] with procedural steps
```

---

## Step 4: Check Recommender Mapping (Checkpoint 3/8)

### Tutorial Mode

```
📍 CHECKPOINT [3/8]: Pathfinder Discovery Check
───────────────────────────────────────────────

**What I'm about to do:**
Check the `grafana-recommender` repository to see if this Learning Journey 
is mapped to any Grafana Cloud pages.

**Why this matters:**
Pathfinder (the in-app guide system) uses recommendation rules to know when 
to show a Learning Journey. Without a mapping, users won't discover this 
content while using Grafana.

If no mapping exists, we'll note it as a follow-up task - you can still 
create the interactive content, but someone will need to add the rule later.

Ready to proceed? (Y/N): _
```

**If Y:** Search recommender configs:
```bash
grep -r "[lj-path]" grafana-recommender/internal/configs/
```

**Result output:**
- If found: Show which pages/contexts trigger this LJ
- If not found: **Create the mapping** (see below)

#### If Mapping Not Found: Create It

When no mapping exists, you MUST create one:

```
⚠️ No recommender mapping found for this Learning Journey.

Without a mapping, users won't discover this content in Pathfinder. 
I'll create the mapping now so the LJ appears in Grafana Cloud.

Here's what I'll do:
1. Create a branch in grafana-recommender: `add-lj-[lj-folder-name]`
2. Add a rule to the appropriate category JSON file
3. Ask you to verify the details before committing

Ready to proceed? (Y/N): _
```

**If Y:**

1. **Create branch in recommender repo:**
```bash
cd grafana-recommender
git checkout -b add-lj-[lj-folder-name]
```

2. **Determine the appropriate category file** based on the LJ's `journey.group` field:
   - `query-and-visualize` → `internal/configs/state_recommendations/dashboards.json`
   - `alerting` → `internal/configs/state_recommendations/alerting.json`
   - `get-started` → `internal/configs/state_recommendations/home.json`
   - etc.

3. **Add the mapping rule** to the category JSON:
```json
{
  "title": "[LJ Title from _index.md]",
  "url": "https://grafana.com/docs/learning-journeys/[lj-folder-name]/",
  "urlPrefix": "[Grafana page URL where this LJ should appear]",
  "learningJourney": true
}
```

4. **Ask the writer to verify:**
```
📝 Please verify the recommender mapping:

**Title:** [auto-populated from _index.md]
**Docs URL:** https://grafana.com/docs/learning-journeys/[lj-folder-name]/
**URL Prefix:** [best guess based on LJ content, e.g., "/dashboards" or "/explore"]

Are these correct? If not, please provide corrections:
- Title: _
- Docs URL: _
- URL Prefix (the Grafana page where this should appear): _

Confirm to proceed (Y/N): _
```

5. **Commit and note PR creation as follow-up:**
```bash
git add internal/configs/state_recommendations/[category].json
git commit -m "Add recommender mapping for [LJ name]"
```

```
✅ Recommender mapping created!

Branch: add-lj-[lj-folder-name]
File: internal/configs/state_recommendations/[category].json

**Follow-up task:** Create a PR in grafana-recommender when you're ready 
to publish the interactive content.
```

### Expert Mode

```
✅ Recommender mapping: Found in [file] (or "⚠️ Not found - creating...")
```

If not found, silently create the mapping and show:
```
✅ Recommender mapping created in grafana-recommender
   Branch: add-lj-[lj-folder-name]
   Please verify: title, docs URL, urlPrefix
```

---

## Step 5: Check for Existing Interactive Content (Checkpoint 4/8)

### Tutorial Mode

```
📍 CHECKPOINT [4/8]: Existing Content Check
───────────────────────────────────────────

**What I'm about to do:**
Check if interactive content already exists for this Learning Journey in 
the `interactive-tutorials` repository.

**Why this matters:**
If content already exists, we need to decide whether to:
- Update the existing content
- Start fresh (and potentially lose previous work)
- Abort and review what's there first

This prevents accidentally overwriting someone else's work.

Ready to proceed? (Y/N): _
```

**If Y:** Check for existing folder:
```bash
ls -la interactive-tutorials/[lj-folder-name]-lj/ 2>/dev/null
```

**If content exists:**
```
⚠️ Interactive content already exists!

Found: [folder-name]-lj/
  - [milestone-1]/content.json
  - [milestone-2]/content.json
  - ...

What would you like to do?
1. Review existing content first (abort)
2. Continue and update/overwrite
3. Create on a different branch

Choice (1/2/3): _
```

### Expert Mode

```
✅ No existing content (or "⚠️ Existing content found - will update")
```

---

## Step 6: Create Feature Branch (Checkpoint 5/8)

### Tutorial Mode

```
📍 CHECKPOINT [5/8]: Branch Creation
────────────────────────────────────

**What I'm about to do:**
Create a new Git branch for this work:
  `interactive-[lj-folder-name]`

**Why this matters:**
Working on a feature branch:
- Isolates your changes from the main branch
- Makes it easy to create a Pull Request for review
- Allows you to abandon changes without affecting others

Ready to proceed? (Y/N): _
```

**If Y:**
```bash
cd interactive-tutorials
git checkout -b interactive-[lj-folder-name]
```

### Expert Mode

```
✅ Created branch: interactive-[lj-folder-name]
```

---

## Step 7: Create Folder Structure (Checkpoint 6/8)

### Tutorial Mode

```
📍 CHECKPOINT [6/8]: Folder Scaffolding
───────────────────────────────────────

**What I'm about to do:**
Create the folder structure for the interactive content:

[lj-folder-name]-lj/
├── [milestone-1]/
│   └── content.json
├── [milestone-2]/
│   └── content.json
└── ...

**Why this matters:**
Each milestone with procedural steps gets its own folder and `content.json` file.
This structure mirrors the website repo's milestone organization, making it 
easy to maintain and update.

**Why a separate repo?**
You might wonder: "Why don't these JSON files live in the website repo with 
the rest of the Learning Journey content?"

Great question! Here's why we use the `interactive-tutorials` repo:

- **Easier management** - Keeping interactive content separate makes it simpler 
  to track, review, and maintain
- **Leaderboard recognition** - Your contributions here show up on the team's 
  leaderboard dashboard, so you get credit for your work!
- **The JSON files become the milestone of record** - They contain ALL the 
  content (text, images, videos, tips) PLUS the interactive elements

**Important:** The content from these JSON files IS published to the website! 
Users visiting grafana.com will see the full milestone content. The interactivity 
(Show me / Do it buttons) only appears inside Grafana Cloud via Pathfinder.

Ready to proceed? (Y/N): _
```

**If Y:** Create folders:
```bash
mkdir -p [lj-folder-name]-lj/[milestone-1] [lj-folder-name]-lj/[milestone-2] ...
```

### Expert Mode

```
✅ Created [count] milestone folders
```

---

## Step 8: Generate Content Files (Checkpoint 7/8)

### Tutorial Mode

```
📍 CHECKPOINT [7/8]: Content Generation
───────────────────────────────────────

**What I'm about to do:**
Generate `content.json` files for each milestone by:

1. Reading the source markdown from the website repo
2. Converting procedural steps to interactive blocks
3. Adding TODO placeholders for selectors that need recording
4. Including all content (text, images, videos, tips) from the source

**Why this matters:**
The JSON files define what Pathfinder displays:
- `markdown` blocks for explanatory text
- `interactive` blocks for UI actions (highlight, click, formfill)
- `multistep` blocks for sequences of actions

I'll include TODOs where you need to record selectors using Pathfinder's 
dev mode (?pathfinderDev=true).

Ready to proceed? (Y/N): _
```

**If Y:** For each milestone with procedural steps:

1. Read the source `index.md`
2. Extract all content (intro, steps, tips, images, videos)
3. Generate `content.json` with:
   - All markdown content preserved
   - Interactive blocks with TODO selectors
   - Proper block structure
4. **Automatically run /lint** to validate JSON and selectors
5. **Automatically run /check** for quality review

Report any issues found by lint/check and fix them before proceeding.

### Expert Mode

Generate files, run lint/check, show summary:
```
✅ Generated content.json files:
   - [milestone-1]: 5 blocks (2 interactive, 1 TODO)
   - [milestone-2]: 8 blocks (4 interactive, 3 TODOs)
   ...

✅ Lint passed (or ⚠️ [count] issues found - fixing...)
✅ Check passed (or ⚠️ [count] suggestions - see below)
```

---

## Step 9: Summary & Next Steps (Checkpoint 8/8)

### Tutorial Mode

```
📍 CHECKPOINT [8/8]: Summary & Next Steps
─────────────────────────────────────────

🎉 Scaffolding Complete!
────────────────────────

**What was created:**
- Branch: interactive-[lj-folder-name]
- Folder: [lj-folder-name]-lj/
- Files: [count] content.json files

**TODOs remaining:**
- [ ] Record [count] selectors using ?pathfinderDev=true
- [ ] Test each milestone end-to-end

Would you like a step-by-step guide for recording selectors? (Y/N): _
```

**If Y:** Provide the detailed selector recording guide:

```
📖 STEP-BY-STEP: Recording Selectors
────────────────────────────────────

**Step 1: Open the Pathfinder Dev Environment**

Go to: https://learn.grafana-ops.net/?pathfinderDev=true

This is our dedicated learning environment with Pathfinder developer mode 
enabled. The `?pathfinderDev=true` parameter activates the Block Editor, 
which lets you record and test selectors.

**Step 2: Enable Dev Mode (First Time Only)**

If this is your first time using Dev Mode, you need to enable it:

1. The Pathfinder panel should already be open on the right side
2. Click the **more options menu** (⋮) in the top-right of the panel
3. Click **Settings**
4. Scroll down to the **Dev mode** section
5. Check the **Dev mode checkbox** to enable it

   ⚠️ Note: You'll see a warning that Dev mode "disables security protections."
   This is safe in learn.grafana-ops.net since it's an isolated learning environment.

6. The panel will refresh and you'll now see "Dev Mode" highlighted in red

───────────────────────────────────────────────────────────────────────────────

✋ **Quick Check:** Can you confirm you see "Dev Mode" in red at the top of the 
Pathfinder panel? (Y/N): _

**If N:** What do you see? Let me help troubleshoot.
**If Y:** Great! Let's continue...

───────────────────────────────────────────────────────────────────────────────

**Step 3: Import the First Milestone JSON**

Here are the milestones for this Learning Journey, in order:

[AI will list the specific milestones here, e.g.:]
```
1. add-visualization/content.json    ← Start here
2. write-query/content.json
3. time-range-refresh/content.json
4. save-dashboard/content.json
```

To import the first milestone:

1. In the **Interactive guide editor** panel, look at the toolbar with icons
2. Find the **Import JSON guide** button (upload icon ⬆️) - hover over icons to see tooltips
3. Click **Import JSON guide**
4. A file picker dialog will open
5. Navigate to your `interactive-tutorials` folder
6. Go to `[lj-folder-name]-lj/add-visualization/` (or whichever milestone is first)
7. Select `content.json` and click **Open**
8. The blocks from your JSON file will appear in the Interactive guide editor

You should now see your content blocks listed (Markdown, Multistep, Interactive, etc.)

**Step 4: Navigate to the Context Page**

For this Learning Journey, navigate to the page where users will start:
- Go to **Dashboards** in the left navigation menu
- This is where the first interactive step takes place

**Step 5: Record a Selector**

[Additional steps to be added for recording selectors]

**Step 6: Copy the Selector to Your JSON**

[Additional steps to be added for copying selectors]

**Step 7: Repeat for All TODOs**

Work through each TODO selector in order:

[List of TODOs for this specific LJ will be shown here]

**Tips for Good Selectors:**
- ✅ Prefer `data-testid` attributes (most stable)
- ✅ Use `aria-label` as a backup
- ⚠️ Avoid class names that might change
- ⚠️ Avoid dynamic IDs or indices

**Need help?**
- Recording selectors: See .cursor/ai-guide-reference.mdc
- JSON format: See docs/json-guide-format.md
- Common issues: See .cursor/edge-cases-and-troubleshooting.mdc

Ready to start recording? Open: https://learn.grafana-ops.net/?pathfinderDev=true
```

**If N:**
```
No problem! Here's a quick summary:

1. Go to: https://learn.grafana-ops.net/?pathfinderDev=true
2. Open Pathfinder (Help button) → Block Editor tab
3. Record selectors for each TODO in your content.json files
4. Test each milestone end-to-end
5. Commit and push when ready

Run /help-selectors anytime if you need the detailed guide later.
```

### Expert Mode

```
✅ Scaffolding complete for [lj-name]

Files created: [count]
TODOs: [count] selectors to record

Next steps:
1. Go to: https://learn.grafana-ops.net/?pathfinderDev=true
2. Open Block Editor (Help → Block Editor tab)
3. Record selectors for TODOs
4. Commit and push when ready
```

---

## Content Generation Guidelines

When generating `content.json` files:

### Content Checklist
- [ ] All introductory paragraphs from source markdown
- [ ] All numbered steps converted to interactive blocks
- [ ] All images (`{{< figure >}}` or `![]()`} converted to image blocks
- [ ] All videos (`{{< docs/video >}}`) converted to video blocks
- [ ] All admonitions (tips, notes, "did you know") preserved
- [ ] All tables preserved as markdown
- [ ] Transition sentences to next milestone

### Selector Priority
1. Use known `data-testid` selectors where documented
2. Add `TODO: find selector for [element]` for unknowns

### Block Types
- Explanatory text → `markdown` block
- Single UI action → `interactive` block
- Multi-step sequence → `multistep` block
- Images → `image` block
- Videos → `video` block

### Requirements
- DOM interactions need `["exists-reftarget"]`
- Nav menu items need `["navmenu-open"]` or `["exists-reftarget"]` depending on context
- "Show me" only steps need `doIt: false`
