# Step 6: Test in Pathfinder (Collaborative Testing)

Collaboratively test each milestone in Pathfinder's Block Editor.

---

## ⛔ CRITICAL: User Does ALL Importing and Testing

> **THE AI MUST NEVER IMPORT JSON OR CLICK INTERACTIVE BUTTONS IN PATHFINDER.**
> 
> The user handles ALL Pathfinder interactions: importing JSON, clicking "Show me", "Do it", and testing.

Testing is a **collaborative process** where AI and user work together:

- **AI's job:** Tell the user which content.json file to import, then **STOP AND WAIT**
- **User's job:** Import the JSON, click "Show me" / "Do it" buttons, and report results
- **User reports:** "This doesn't work" if a selector fails
- **AI fixes:** Inspect DOM, find correct selector, update the content.json file

**Why this rule exists:** Users can import and test faster and catch visual/UX problems that automated interaction misses. The AI interacting with Pathfinder wastes time and is error-prone.

**You MUST follow this pattern:**
1. Tell the user which content.json file to import next
2. **WAIT** for user to report results (pass or "this doesn't work")
3. If user reports a failure, help fix the selector in the content.json file
4. After milestone passes, move on to the next milestone

---

## Access the Block Editor

Testing happens in **Pathfinder Dev Mode** at: `https://learn.grafana-ops.net/?pathfinder-dev=true`

> ⚠️ **Important:** This is different from selector discovery (Step 5), which uses 
> `https://learn.grafana-ops.net/` to walk through the actual UI.

Dev mode must be enabled before you can access the Block Editor. If this is the user's first time, direct them to SETUP.md section 4.

**Display:**
```
Have you enabled Dev Mode before? (If not, see SETUP.md section 4 for first-time setup)

To test, open Pathfinder in dev mode:
https://learn.grafana-ops.net/?pathfinder-dev=true

Once the page loads, the Pathfinder sidebar should open automatically with Dev Tools visible.
Click on "Interactive guide editor" to open the Block Editor.

Let me know when you're in the Block Editor. (Y/N)
```

> ⚠️ **First-time users:** Must enable dev mode first at:
> `https://learn.grafana-ops.net/plugins/grafana-pathfinder-app?dev=true`
> See SETUP.md section 4 for full instructions.

---

## Tutorial Mode Introduction

```
**Step 6: Test in Pathfinder**

We'll test collaboratively ONE MILESTONE AT A TIME:
- I'll identify which milestones have interactive steps (skipping markdown-only ones)
- I'll tell you which content.json file to import into the Block Editor
- YOU import the JSON, click through "Show me" / "Do it" buttons
- Tell me if anything doesn't work
- I'll fix the content.json and you can re-import

Note: We only test milestones with interactive steps. Markdown-only milestones 
(like introductions or conceptual content) don't need testing.

Ready to test the first interactive milestone? (Y/N)
```

Wait for confirmation, then tell the user which file to import.

---

## Expert Mode

Same behavior — tell user which file to import, user tests, fix issues as reported.

---

## Which Milestones to Test

**CRITICAL: Only test milestones that contain interactive steps.**

Before loading any JSON, check the milestone's content.json:

- ✅ **Test if:** Contains `interactive`, `multistep`, or `guided` blocks with `reftarget` values
- ❌ **Skip if:** Contains ONLY `markdown` blocks (purely conceptual content)

**Why skip markdown-only milestones?**
- No interactive steps = nothing to test
- Markdown content renders correctly by default
- Testing wastes time on non-interactive content

**Example:**
```json
// ❌ SKIP - No interactive steps to test
{
  "schemaVersion": "1.0.0",
  "id": "billing-usage-business-value",
  "title": "Understand the business value",
  "blocks": [
    {
      "type": "markdown",
      "content": "Understanding your Grafana Cloud billing..."
    }
  ]
}

// ✅ TEST - Has interactive steps
{
  "schemaVersion": "1.0.0",
  "id": "billing-usage-navigate-to-billing-dashboard",
  "title": "Navigate to the billing dashboard",
  "blocks": [
    {
      "type": "markdown",
      "content": "The Grafana Cloud billing dashboard..."
    },
    {
      "type": "interactive",
      "action": "button",
      "reftarget": "GrafanaCloud",
      "content": "Open the **GrafanaCloud** folder."
    }
  ]
}
```

---

## Test Procedure (Per Interactive Milestone)

**For EACH milestone with interactive steps (one at a time):**

1. **First, check if milestone has interactive steps** (see "Which Milestones to Test" above)
2. If no interactive steps, **skip to next milestone** and inform user
3. **Tell the user which file to import:**
   - Provide the full path to the content.json file
   - Example: "Please import `mongodb-integration-lj/select-platform/content.json` into the Block Editor"
4. **STOP. WAIT. Do nothing until the user responds.**
5. If user reports "this doesn't work": help fix the selector in the content.json file
6. After user confirms milestone passes, move on to the next milestone

> ⚠️ **Reminder:** The AI must NOT interact with Pathfinder. The user handles all importing and testing. After telling the user which file to import, wait for their feedback.

---

## When a Selector Fails

**CRITICAL: Do NOT automatically attempt fixes.** When the user reports a broken selector:

1. **STOP immediately**
2. **Report the problem clearly:**
   ```
   ❌ SELECTOR ISSUE FOUND
   
   Block: [description of the interactive step]
   Current selector: [the reftarget value]
   Problem: [why it failed - element not found, wrong element, etc.]
   
   Proposed fix:
   - I will use Playwright to inspect the DOM and find the correct selector
   - Once found, I will update the content.json with the new selector
   - You can then re-import and re-test
   
   Proceed with fix? (Y/N)
   ```
3. **Wait for user approval** before making any changes
4. After user approves, update the content.json file and tell the user to re-import
5. If fix doesn't work after 2 attempts, ask user for guidance (see "Handling Persistent Failures")

---

## Display Per Milestone

**When skipping a markdown-only milestone:**
```
⏭️ Skipping: [milestone-name] (markdown-only, no interactive steps)
```

**When telling user to test an interactive milestone:**

Use this exact format:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Testing: [milestone-name] ([N] of [total interactive])
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please import: [slug]-lj/[milestone-name]/content.json

Interactive blocks in this milestone:
├── Block 1: [description]
├── Block 2: [description]
└── Block 3: [description]

Let me know how it goes!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Wait for user feedback before proceeding to the next milestone.**

---

## Handling Persistent Failures

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

---

## Final Summary (After ALL Interactive Milestones Tested)

Only after all interactive milestones have been tested and user has confirmed each one:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Step 6 Complete: All Interactive Milestones Tested
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total milestones: [N]
├── Interactive milestones tested: [N]
└── Markdown-only milestones skipped: [N]

Test Results:
├── [milestone-1]: ⏭️ Skipped (markdown-only)
├── [milestone-2]: ✅ All blocks passed
├── [milestone-3]: 🟡 [N] blocks needed fixes
├── [milestone-4]: ✅ All blocks passed
├── [milestone-5]: ⏭️ Skipped (markdown-only)
└── [milestone-6]: ✅ All blocks passed

Proceeding to Step 7: Final Summary...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
