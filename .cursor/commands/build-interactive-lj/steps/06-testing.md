# Step 6: Test in Pathfinder (Collaborative Testing)

Collaboratively test each milestone in Pathfinder's Block Editor.

---

## ⛔ CRITICAL: AI Must NOT Test

> **THE AI MUST NEVER CLICK "Show me", "Do it", OR ANY INTERACTIVE BUTTONS.**
> 
> The user does ALL testing. The AI only imports JSON and waits for feedback.

Testing is a **collaborative process** where AI and user work together:

- **AI's job:** Load JSON into Pathfinder, switch to Preview mode, then **STOP AND WAIT**
- **User's job:** Click "Show me" / "Do it" buttons (user is faster and catches visual issues)
- **User reports:** "This doesn't work" if a selector fails
- **AI fixes:** Inspect DOM, find correct selector, update JSON, reload

**Why this rule exists:** Users can test faster and catch visual/UX problems that automated clicking misses. The AI clicking buttons wastes time and prevents the user from seeing the actual behavior.

**You MUST follow this pattern:**
1. Load ONE milestone's JSON into Pathfinder
2. Switch to Preview mode
3. **Tell the user it's ready for testing**
4. **WAIT** for user to report results (pass or "this doesn't work")
5. If user reports a failure, help fix it
6. After milestone passes, **ASK** before loading the next milestone

---

## Access the Block Editor

Testing happens in **Pathfinder Dev Mode** at: `https://learn.grafana-ops.net/?pathfinder-dev=true`

> ⚠️ **Important:** This is different from selector discovery (Step 5), which uses 
> `https://learn.grafana-ops.net/` to walk through the actual UI.

Dev mode must be enabled before you can access the Block Editor. If this is the user's first time, direct them to SETUP.md section 4.

**Display:**
```
Have you enabled Dev Mode before? (If not, see SETUP.md section 4 for first-time setup)

I'll navigate to Pathfinder in dev mode for testing.

Opening: https://learn.grafana-ops.net/?pathfinder-dev=true

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
- I'll load each interactive milestone's content.json and switch to Preview mode
- YOU click through "Show me" / "Do it" buttons (you're quicker!)
- Tell me if anything doesn't work
- I'll help fix any issues

Note: We only test milestones with interactive steps. Markdown-only milestones 
(like introductions or conceptual content) don't need testing.

Ready to test the first interactive milestone? (Y/N)
```

Wait for confirmation, then load the first milestone with interactive steps.

---

## Expert Mode

Same behavior — load milestone, user tests, fix issues as reported.

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
3. Navigate to `https://learn.grafana-ops.net/?pathfinder-dev=true` (if not already there)
4. Open the Block Editor from the Pathfinder sidebar (Dev tools → Interactive guide editor)
5. **Load the JSON using "Edit JSON" method:**
   - Click "Start new guide" to clear the editor (if needed)
   - Click "Edit JSON" button
   - Read the content.json file for this milestone
   - Use browser automation to paste the JSON into the editor
   - Save/apply the JSON
6. Switch to Preview mode
7. **Tell user: "Ready for testing! Please click through the Show me / Do it buttons and let me know what works and what doesn't."**
8. **STOP. WAIT. Do nothing until the user responds.** — The AI must NOT click any buttons.
9. If user reports "this doesn't work": help fix the selector (see below)
10. After user confirms milestone passes, **ASK** before loading next milestone

> ⚠️ **Reminder:** After step 7, the AI's job is done until the user provides feedback. Do not proceed, do not click buttons, do not test. Just wait.

> 💡 **Technical note:** Use "Edit JSON" button instead of "Import JSON guide" to avoid file upload dialogs. The Edit JSON approach allows direct text input via browser automation.

---

## When a Selector Fails

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
   
   Proceed with fix? (Y/N)
   ```
3. **Wait for user approval** before making any changes
4. After user approves, attempt the fix and report results
5. If fix doesn't work after 2 attempts, ask user for guidance (see "Handling Persistent Failures")

---

## Display Per Milestone

**When skipping a markdown-only milestone:**
```
⏭️ Skipping: [milestone-name] (markdown-only, no interactive steps)
```

**When testing an interactive milestone:**

Use this exact format:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Testing: [milestone-name] ([N] of [total interactive])
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

Ready to test the next interactive milestone: "[next-name]"? (Y/N)
```

**Wait for user confirmation before proceeding to the next milestone.**

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
