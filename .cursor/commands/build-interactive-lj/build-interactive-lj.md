# Build Interactive Learning Journey

This command automates the creation of interactive content (`content.json` files) for learning journeys in Grafana Pathfinder.

---

## AI Behavior Guidelines

When executing this command, you MUST follow these principles:

1. **Follow steps in order** — Do NOT skip or combine steps. Each step exists for a reason.

2. **Test ONE milestone at a time** — In Step 5, test only ONE milestone, report results, then STOP and ASK the user before testing the next milestone. Do NOT batch test all milestones at once.

3. **ASK before fixing issues** — When you find a broken selector, STOP, explain the problem, describe the proposed fix, and ASK the user for permission before making changes. Do NOT automatically attempt fixes.

4. **Test in Pathfinder, not just browser** — A selector that works in raw browser inspection may fail in Pathfinder's Block Editor. You MUST verify in the Block Editor.

6. **Try alternatives before giving up** — When a selector fails (after user approves fix):
   - Try 2 alternative selector approaches
   - If still failing, ask the user: "This selector isn't working after 2 attempts. Would you like me to file an issue at https://github.com/grafana/interactive-tutorials/issues?"
   - Only file the issue if the user approves

7. **Let the user handle git** — Do NOT run `git commit` or `git push`. Summarize changes and let the user decide when to commit.

8. **Ask when uncertain** — If a step is ambiguous or you're unsure how to proceed, ask the user rather than guessing.

9. **Re-read before critical steps** — Before Step 3 (Scaffolding), re-read the "JSON Schema Requirements" section. Before Step 4 (Selector Discovery), re-read the "Selector Priority" table.

10. **Reference the appendix** — Before scaffolding any LJ, consult "Appendix: Proven Patterns" for reusable JSON structures. Apply patterns that match your LJ's UI elements.

11. **ALWAYS use browser tools for selectors** — You MUST use Playwright to discover selectors by inspecting the actual DOM. NEVER guess selectors or copy them from the appendix without verifying they exist on the current page. The appendix shows patterns; browser inspection confirms reality.

---

## Do NOT (Anti-Patterns)

These are common mistakes. Avoid them:

- ❌ **Do NOT test all milestones at once** — Test ONE milestone, report results, then ASK the user before testing the next. This keeps the process manageable and easy to follow.
- ❌ **Do NOT automatically fix broken selectors** — When you find an issue, STOP, explain the problem, describe your proposed fix, and ASK for permission before making changes. The user needs visibility into what's happening.
- ❌ **Do NOT skip the welcome message** — It sets expectations for the session
- ❌ **Do NOT combine multiple steps** — Each step has verification built in
- ❌ **Do NOT create content.json without reading source markdown first** — You need context
- ❌ **Do NOT use placeholder selectors** — Never leave `"[selector]"` or `"TODO"` in files
- ❌ **Do NOT proceed to testing with empty selectors** — All selectors must be discovered first
- ❌ **Do NOT file GitHub issues without asking** — Always get user permission
- ❌ **Do NOT use `description` field** — The correct field is `content`
- ❌ **Do NOT use `formvalue` field** — The correct field is `targetvalue`
- ❌ **Do NOT guess at selectors** — ALWAYS use Playwright to inspect the actual DOM
- ❌ **Do NOT copy appendix selectors without verification** — Appendix patterns are templates; you MUST verify each selector exists on the actual page using browser tools
- ❌ **Do NOT skip browser inspection** — Even if a pattern looks familiar, always confirm with Playwright snapshot

---

## Lessons Learned

Patterns discovered from building interactive content:

### Selector Patterns

| Don't Use | Use Instead | Why |
|-----------|-------------|-----|
| `input[placeholder="..."]` | `[aria-label="..."]` | Placeholder text may change; aria-label is more stable |
| Generic classes (`.btn`) | `[data-testid="..."]` | Classes change frequently; test IDs are intentional |
| `:nth-child()` selectors | Specific attributes | Position-based selectors break when UI reorders |

### When Markdown Beats Interactive

Some UI patterns are better documented as markdown instructions rather than automated:

- **Conditional dialogs** — Buttons that only appear after user completes a real-world action (e.g., "Test connection" after installing software)
- **Multi-path flows** — When user must choose between options (create new vs use existing)
- **External actions** — Steps performed outside the browser (run CLI commands, install software)

### Integration-Specific Notes

For **integration setup flows** (Linux, Windows, macOS, MySQL, etc.):
- The "Run Grafana Alloy" expand button works: `[data-testid="agent-config-button"]`
- Token creation and "Test connection" buttons are conditional — use markdown
- "Install" button for dashboards/alerts works: `action: "button"` with `reftarget: "Install"`

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

> 💡 **Before scaffolding:** See "Appendix: Proven Patterns" for reusable JSON structures 
> that match common Grafana UI elements (navigation, forms, buttons, etc.).

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
// Highlight action (correct)
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "[data-testid=\"my-element\"]",
  "content": "Click **Button** to do the thing.",  // NOT "description"
  "requirements": ["exists-reftarget"]
}

// Button action (correct) - uses button text, not CSS selector
{
  "type": "interactive",
  "action": "button",
  "reftarget": "Install",  // The visible button text
  "content": "Click **Install** to add the dashboards.",
  "requirements": ["exists-reftarget"]
}

// Formfill action (correct)
{
  "type": "interactive",
  "action": "formfill",
  "reftarget": "[aria-label=\"Search connections by name\"]",
  "targetvalue": "value to enter",  // NOT "formvalue"
  "content": "Enter the value.",
  "requirements": ["exists-reftarget"]
}

// Hover action (correct) - for revealing hover-dependent UI
{
  "type": "interactive",
  "action": "hover",
  "reftarget": "[data-testid=\"hover-target\"]",
  "content": "Hover over this element to reveal options.",
  "requirements": ["exists-reftarget"]
}

// Multistep block (correct) - for navigation sequences
{
  "type": "multistep",
  "content": "Navigate to **X > Y > Z**.",
  "requirements": ["navmenu-open"],
  "steps": [
    { "action": "highlight", "reftarget": "[aria-label=\"Expand section: Connections\"]" },
    { "action": "highlight", "reftarget": "a[href=\"/connections/add-new-connection\"]" }
  ]
}

// Guided block (correct) - user performs action manually, no "Do it" button
{
  "type": "guided",
  "content": "Copy the installation command and run it on your server.",
  "requirements": []
}
```

**Common mistakes to avoid:**
- ❌ `description` → ✅ `content`
- ❌ `formvalue` → ✅ `targetvalue`
- ❌ `title` on interactive blocks (not needed)

### When to Use Markdown Instead of Interactive

Some steps are better as plain `markdown` blocks rather than `interactive`:

| Scenario | Why Markdown is Better |
|----------|------------------------|
| Steps inside dialogs that require prior user actions | Dialog may not exist yet; automation will fail |
| External actions (run command on another machine) | Can't automate outside the browser |
| Conditional UI (create new vs use existing) | Multiple paths; can't predict user's choice |
| Complex multi-option flows | Better to explain options than force one path |
| Steps after external verification | User must complete real-world action first |

**Example from Windows integration:**
The "Test Alloy connection" button only appears after the user has actually installed Alloy on their Windows machine. Since automation can't do that, the step is markdown:

```json
{
  "type": "markdown",
  "content": "After installing Alloy, click **Test Alloy connection** to verify the installation."
}
```

### Requirements Reference

| Requirement | When to Use |
|-------------|-------------|
| `exists-reftarget` | Any DOM interaction (highlight, formfill, button, hover) |
| `navmenu-open` | Navigation menu elements (ensures menu is expanded) |
| `on-page:/path` | Page-specific actions (checks current URL) |
| `section-completed:id` | Sequential dependencies between sections |
| `is-admin` | Admin-only features |
| `has-datasource:type` | When a specific data source is needed |
| `has-plugin:id` | When a specific plugin must be installed |

### Verification Checklist (REQUIRED)

Before proceeding to Step 4, verify EACH content.json file:

- [ ] Every block has a `"type"` field
- [ ] Instruction text uses `"content"` (NOT `"description"`)
- [ ] Formfill actions use `"targetvalue"` (NOT `"formvalue"`)
- [ ] Navigation steps use `"multistep"` blocks
- [ ] Interactive blocks have `"requirements": ["exists-reftarget"]`
- [ ] No placeholder text like `"[selector]"` or `"TODO"` exists

**If any check fails, fix before continuing.**

**Display (use this exact format):**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Step 3 complete: Scaffold

Created [N] content.json files:
├── [slug]-lj/milestone-1/content.json ([N] blocks)
├── [slug]-lj/milestone-2/content.json ([N] blocks)
└── ...

Verification: All checks passed ✓

⏳ Next: Step 4 - Selector Discovery
   What's your Grafana Cloud URL?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Step 4: Selector Discovery

### Re-Read Before Starting

Before discovering selectors, re-read the "Selector Priority" table in Quick Reference.
You MUST try selectors in this order: data-testid → aria-label → href → id → class

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

### Selector Decision Tree

When you find an element, choose selector in this order:

1. Has `data-testid`? → Use `[data-testid="..."]` 🟢
2. Has `aria-label`? → Use `[aria-label="..."]` 🟢
3. Is a link with href? → Use `a[href="..."]` 🟢
4. Is a button with stable text? → Use `action: "button"` 🟡
5. Has unique id? → Use `#id` 🟡
6. None of above? → Try class-based, then ask user 🔴

**Display progress (use this exact format):**
```
Discovering selectors for [milestone-name]...
├── [element description] → [selector] 🟢
├── [element description] → [selector] 🟡
└── [element description] → FAILED ❌
    Attempt 1: [selector tried] - [why it failed]
    Attempt 2: [selector tried] - [why it failed]
```

### Verification Checklist (REQUIRED)

Before proceeding to Step 5, verify:

- [ ] All interactive blocks have real selectors (no placeholders)
- [ ] No `"[selector]"` or `"TODO"` strings remain
- [ ] Selectors follow priority order (data-testid preferred)
- [ ] Failed selectors are noted for user decision

**Display (use this exact format):**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Step 4 complete: Selector Discovery

Results by milestone:
├── [milestone-1]: [N] selectors found
├── [milestone-2]: [N] selectors found
└── ...

Selector quality:
├── 🟢 High confidence: [N]
├── 🟡 Medium confidence: [N]
└── 🔴 Failed/needs review: [N]

⏳ Next: Step 5 - Test in Pathfinder
   Ready to test? (Y/n)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Step 5: Test in Pathfinder (One Milestone at a Time)

### IMPORTANT: Test ONE milestone, then STOP and ASK

Do NOT test all milestones in rapid succession. This is confusing and hard to follow.

**You MUST follow this pattern:**
1. Test ONE milestone completely
2. Report results for that milestone
3. **ASK the user** before proceeding to the next milestone
4. Repeat until all milestones are tested

### Tutorial Mode Introduction

```
**Step 5: Test in Pathfinder**

I'll test selectors ONE MILESTONE AT A TIME:
- Import the content.json for a single milestone
- Click through all "Show me" buttons in that milestone
- Report results
- ASK YOU before moving to the next milestone

This way you can follow along and verify each milestone works.

Ready to test the first milestone? (Y/n)
```

Wait for confirmation, then test ONLY the first milestone.

### Expert Mode

Same behavior — test one milestone, ask before proceeding.

### Test Procedure (Per Milestone)

**For EACH milestone (one at a time):**

1. Navigate to Grafana (if not already there)
2. Open Pathfinder (Help button or `?` key)
3. Enter Block Editor / Dev Mode
4. Import the content.json for THIS milestone only
5. Switch to Preview mode
6. Click each "Show me" button to verify selectors
7. **If a selector fails:** STOP and report the issue (see "When a Selector Fails" below)
8. Report results for THIS milestone
9. **STOP and ASK user to proceed to next milestone**

---

### When a Selector Fails

**CRITICAL: Do NOT automatically attempt fixes.** When you find a broken selector:

1. **STOP immediately**
2. **Report the problem clearly:**
   ```
   ❌ SELECTOR ISSUE FOUND
   
   Block: [description of the interactive step]
   Current selector: [the reftarget value]
   Problem: [why it failed - element not found, wrong element, etc.]
   
   Proposed fix:
   - I will use Playwright to inspect the DOM and find the correct selector
   - Once found, I will update the content.json with: [new selector]
   - Then re-import and re-test this specific block
   
   Proceed with fix? (Y/n)
   ```
3. **Wait for user approval** before making any changes
4. After user approves, attempt the fix and report results
5. If fix doesn't work after 2 attempts, ask user for guidance (see "Handling Persistent Failures")

---

**Display per milestone (use this exact format):**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Testing: [milestone-name] ([N] of [total])
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

├── Block 1: [description] ✅
├── Block 2: [description] ✅
├── Block 3: [description] ❌ FAILED (awaiting approval to fix)
└── Block 4: [description] (not yet tested)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**After EACH milestone (if all blocks pass), ALWAYS ask:**
```
✅ Milestone "[name]" complete.

Ready to test the next milestone: "[next-name]"? (Y/n)
```

**Wait for user confirmation before proceeding to the next milestone.**

---

### Handling Persistent Failures

When a step fails after 2 fix attempts, ask user:
   ```
   Block [N] failed after 2 attempts.
   Selector tried: [list selectors]
   
   Options:
   1. Convert to markdown (remove interactivity)
   2. File issue at https://github.com/grafana/interactive-tutorials/issues
   3. Skip and continue
   
   Which would you prefer? (1/2/3)
   ```

### Final Summary (After ALL Milestones Tested)

Only after all milestones have been tested and user has confirmed each one:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Step 5 Complete: All Milestones Tested
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Milestones tested: [N]/[N]
├── [milestone-1]: ✅ All blocks passed
├── [milestone-2]: ✅ All blocks passed
├── [milestone-3]: 🟡 [N] blocks needed fixes
└── [milestone-4]: ✅ All blocks passed

Proceeding to Step 6: Final Summary...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Step 6: Report and Next Steps

### Summary (use this exact format)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎉 BUILD COMPLETE: [slug] Interactive LJ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RESULTS
├── Total milestones: [N]
├── Fully interactive: [N] ✅
├── Partial (some markdown): [N] 🟡
└── Issues filed: [N] 📝

FILES CREATED
├── [slug]-lj/milestone-1/content.json ✅
├── [slug]-lj/milestone-2/content.json ✅
└── ...

ISSUES FILED (if any)
├── #[N]: [element] - [brief description]
└── ...

NEXT STEPS
1. Review the content.json files in your editor
2. Stage files: git add [slug]-lj/
3. Commit with message: "Add interactive content for [slug] LJ"
4. Push and create PR

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Slack-Ready Summary

Offer to provide a copy-paste summary for Slack:

```
Would you like a Slack-ready summary? (Y/n)
```

If yes, display:
```
🎯 Interactive LJ complete: [slug]
✅ [N]/[N] milestones interactive
📝 [N] issues filed for broken selectors
🔗 Ready for PR
```

### Filing GitHub Issues

For broken selectors that need Pathfinder team attention, file at:
https://github.com/grafana/interactive-tutorials/issues

Use this template:
```
gh issue create \
  --repo grafana/interactive-tutorials \
  --title "[Selector] [element] in [LJ name]" \
  --body "## Element
[Description of the UI element]

## Selectors Tried
1. \`[selector-1]\` - [why it failed]
2. \`[selector-2]\` - [why it failed]

## Page URL
[Grafana page where element appears]

## Suggested Fix
[If you have ideas, otherwise: Needs data-testid added]"
```

---

## Quick Reference

### Key Files
- Source: `website/content/docs/learning-journeys/[slug]/`
- Output: `interactive-tutorials/[slug]-lj/`
- Mapping: `grafana-recommender/internal/configs/`

### Block Types

| Type | Purpose | Has "Do it"? |
|------|---------|--------------|
| `markdown` | Explanatory text, instructions | No |
| `interactive` | Automated actions with "Show me" / "Do it" | Yes |
| `multistep` | Sequential navigation (shows "▶ Run N steps") | Yes |
| `guided` | User performs manually, no automation | No |

### Interactive Action Types

| Action | Use Case | `reftarget` Value |
|--------|----------|-------------------|
| `highlight` | Click element by CSS selector | CSS selector |
| `button` | Click button by visible text | Button text |
| `formfill` | Enter text in field | CSS selector (+ `targetvalue`) |
| `hover` | Reveal hover-dependent UI | CSS selector |
| `navigate` | Change pages | URL path |

### Selector Priority (Most to Least Stable)

| Priority | Selector Type | Example |
|----------|---------------|---------|
| 1 | `data-testid` | `[data-testid="agent-config-button"]` |
| 2 | `aria-label` | `[aria-label="Search connections by name"]` |
| 3 | `href` (for links) | `a[href="/connections/add-new-connection"]` |
| 4 | `id` | `#my-element` |
| 5 | Stable class | `.specific-component-class` |

**Avoid:** Generic classes (`.btn`, `.input`), positional selectors (`:nth-child`), text content

---

## Appendix: Proven Patterns

Reusable JSON structures for common Grafana UI elements. These were validated through real testing.

> ⚠️ **IMPORTANT:** These are **templates**, not copy-paste solutions. You MUST use Playwright 
> browser tools to verify each selector exists on the actual page before using it. Selectors 
> can change between Grafana versions.

---

### Navigation Patterns

#### Multi-Level Menu Navigation

Use `multistep` for any navigation through nested menus:

```json
{
  "type": "multistep",
  "content": "Navigate to **[Section] > [Subsection] > [Page]**.",
  "requirements": ["navmenu-open"],
  "steps": [
    { "action": "highlight", "reftarget": "[aria-label=\"Expand section: [Section]\"]" },
    { "action": "highlight", "reftarget": "[aria-label=\"Expand section: [Subsection]\"]" },
    { "action": "highlight", "reftarget": "a[href=\"/[path]\"]" }
  ]
}
```

**Common navigation selectors:**

| Destination | Selector |
|-------------|----------|
| Connections | `[aria-label="Expand section: Connections"]` |
| Alerts & IRM | `[aria-label="Expand section: Alerts & IRM"]` |
| Alerting | `[aria-label="Expand section: Alerting"]` |
| Dashboards | `[aria-label="Expand section: Dashboards"]` |
| Explore | `a[href="/explore"]` |
| Alert rules | `a[href="/alerting/list"]` |
| Add new connection | `a[href="/connections/add-new-connection"]` |

---

### Form Patterns

#### Search/Filter Input

ALWAYS use `aria-label` for search inputs, NOT `placeholder`:

```json
{
  "type": "interactive",
  "action": "formfill",
  "reftarget": "[aria-label=\"Search [description]\"]",
  "targetvalue": "[search term]",
  "content": "In the search box, type **[term]** to filter the results.",
  "requirements": ["exists-reftarget"]
}
```

**Why:** `placeholder` text can change; `aria-label` is more stable.

#### Text Input Fields

For labeled form fields:

```json
{
  "type": "interactive",
  "action": "formfill",
  "reftarget": "[aria-label=\"[Field label]\"]",
  "targetvalue": "[value]",
  "content": "Enter **[value]** in the [field name] field.",
  "requirements": ["exists-reftarget"]
}
```

---

### Button Patterns

#### Button by Text (Stable Text)

When a button has consistent, visible text:

```json
{
  "type": "interactive",
  "action": "button",
  "reftarget": "[Button Text]",
  "content": "Click **[Button Text]** to [action].",
  "requirements": ["exists-reftarget"]
}
```

**Examples:** "Install", "Save", "Create", "Add", "Apply"

#### Button by data-testid (Preferred)

When a button has a `data-testid` attribute:

```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "[data-testid=\"[testid-value]\"]",
  "content": "Click **[Button name]** to [action].",
  "requirements": ["exists-reftarget"]
}
```

#### Icon-Only Button

For buttons with only an icon (no text), use `aria-label`:

```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "[aria-label=\"[Action description]\"]",
  "content": "Click the **[icon name]** icon to [action].",
  "requirements": ["exists-reftarget"]
}
```

---

### Link/Tile Patterns

#### Card or Tile Selection

For clickable cards/tiles with href:

```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "a[href=\"/[path]\"]",
  "content": "Click the **[Tile name]** tile to select it.",
  "requirements": ["exists-reftarget"]
}
```

---

### When to Use Markdown

Some UI elements cannot be reliably automated. Use `markdown` blocks instead:

#### Conditional UI (Multiple Paths)

When user must choose between options:

```json
{
  "type": "markdown",
  "content": "**Choose your option:**\n\n- **Option A**: [description]\n- **Option B**: [description]"
}
```

**Why:** Can't predict user's choice.

#### External Actions

When user must do something outside the browser:

```json
{
  "type": "markdown",
  "content": "**On your machine:**\n\n1. [Step 1]\n2. [Step 2]\n3. [Step 3]"
}
```

**Why:** Can't automate outside the browser.

#### Conditional Buttons

When a button only appears after user completes a prior action:

```json
{
  "type": "markdown",
  "content": "After [completing the action], click **[Button]** to continue."
}
```

**Why:** Button may not exist when automation runs.

#### Verification/Confirmation Steps

When user needs to verify something worked:

```json
{
  "type": "markdown",
  "content": "If successful, you'll see: **[success message]**"
}
```

---

### Integration Setup Patterns

These patterns are specific to integration/data source setup LJs (Linux, Windows, macOS, MySQL, etc.):

#### Alloy Installation Expand Button

```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "[data-testid=\"agent-config-button\"]",
  "content": "Click **Run Grafana Alloy** to expand the installation options.",
  "requirements": ["exists-reftarget"]
}
```

#### Token Creation → Use Markdown

Token dialogs have multiple paths (create new vs use existing):

```json
{
  "type": "markdown",
  "content": "**Create or select a token:**\n\n- **Create new token**: Click \"Create new token\", enter a name, then click \"Create token\".\n- **Use existing token**: Click \"Use an existing token\" and enter your token."
}
```

#### Test Connection → Use Markdown

Conditional on real-world installation:

```json
{
  "type": "markdown",
  "content": "After installation completes, click **Test connection** to verify."
}
```

---

### Quick Decision Guide

| UI Element | Pattern to Use |
|------------|----------------|
| Navigate through menus | `multistep` with `navmenu-open` |
| Search/filter input | `formfill` with `aria-label` |
| Button with stable text | `button` action |
| Button with data-testid | `highlight` with data-testid |
| Clickable card/tile | `highlight` with `a[href="..."]` |
| User chooses between options | `markdown` |
| Action outside browser | `markdown` |
| Button that may not exist yet | `markdown` |
