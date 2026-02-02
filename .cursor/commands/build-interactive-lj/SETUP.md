# Setup Guide for /build-interactive-lj

This guide covers everything you need to run the `/build-interactive-lj` command successfully.

---

## Quick AI Shortcuts

| Task | Prompt to Use |
|------|---------------|
| Clone all repos | `Clone the website, interactive-tutorials, and grafana-recommender repos for me` |
| Check workspace | `Verify my Cursor workspace has all required repos for /build-interactive-lj` |
| Install GitHub CLI | `Install GitHub CLI on my machine` |
| Authenticate GitHub CLI | `Help me authenticate GitHub CLI` |
| Setup Playwright MCP | `Walk me through setting up Playwright MCP in Cursor` |
| Full setup | `Help me complete the full setup for /build-interactive-lj` |

---

## 1. Cursor Configuration

For the AI to fully assist you with browser automation and file operations, ensure Cursor is running in **Agent mode** and using the **Claude Opus 4.5** model.

### Switch to Agent Mode

1. In Cursor, look for the mode selector (often in the chat interface header)
2. Select **Agent** mode (not "Ask" or "Edit")
3. Agent mode enables the AI to run terminal commands and use browser automation

### Select Claude Opus 4.5

1. In the chat interface, click the model selector dropdown
2. Select **Claude Opus 4.5** (or the most capable Claude model available)

> **🤖 AI Shortcut:** Ask the AI:
> ```
> Walk me through setting up Cursor in Agent mode with Claude Opus 4.5
> ```

---

## 2. Required Repositories

The workflow requires three repositories in your Cursor workspace:

| Repository | Purpose | Clone URL |
|------------|---------|-----------|
| `website` | Source markdown for learning journeys | `git@github.com:grafana/website.git` |
| `interactive-tutorials` | Where content.json files are created | `git@github.com:grafana/interactive-tutorials.git` |
| `grafana-recommender` | Validates LJ is mapped to Grafana UI | `git@github.com:grafana/grafana-recommender.git` |

### Clone Repositories

```bash
# Navigate to your repositories folder
cd ~/Documents/repositories

# Clone each repo
git clone git@github.com:grafana/website.git
git clone git@github.com:grafana/interactive-tutorials.git
git clone git@github.com:grafana/grafana-recommender.git
```

> **🤖 AI Shortcut:** Ask the AI:
> ```
> Clone the website, interactive-tutorials, and grafana-recommender repos to my repositories folder
> ```

### Add to Cursor Workspace

1. In Cursor, go to **File → Add Folder to Workspace**
2. Add all three repository folders
3. Save the workspace configuration

---

## 3. Playwright MCP Setup

Playwright MCP enables browser automation for selector discovery and testing.

### Enable Playwright MCP

1. Open Cursor Settings (`Cmd + ,` on Mac, `Ctrl + ,` on Windows)
2. Go to **Features → MCP Servers**
3. Find and enable **Playwright** (may also be called **cursor-ide-browser**)
4. **Restart Cursor completely** (Quit and reopen)

> **🤖 AI Shortcut:** Ask the AI:
> ```
> Walk me through setting up Playwright MCP in Cursor
> ```

### Verify Playwright Works

After restart, the AI should be able to:
- Navigate to URLs
- Take snapshots of pages
- Click elements
- Fill form fields

If you see errors about "browser not installed", ask the AI:
```
Install the Playwright browser for me
```

### Troubleshooting Playwright

**"Failed to launch browser"**
- Close any existing Chrome instances
- Restart Cursor completely

**"MCP server not found"**
- Check Cursor Settings → Features → MCP Servers
- Ensure Playwright is enabled
- Restart Cursor

**Browser opens but automation fails**
- The AI may need to use `mcp_Playwright_browser_install` first
- Try: "Install the Playwright browser"

---

## 4. GitHub CLI Setup

GitHub CLI (`gh`) is used to file issues for broken selectors.

### Why We File Issues

It's important to understand that some Grafana UI elements may not have stable or easily targetable selectors, and that's perfectly okay! When you encounter a selector that consistently fails, we file an issue.

👉 **https://github.com/grafana/interactive-tutorials/issues**

This is the preferred method for communicating with **Robby Milo** about which selectors don't work. The Pathfinder team tracks these issues and can:
- Request `data-testid` additions from the Grafana UI team
- Document known limitations
- Suggest workarounds

**It's totally acceptable to find selectors that don't work.** That's part of the discovery process!

### Install

**macOS (Homebrew):**
```bash
brew install gh
```

**Windows (winget):**
```bash
winget install --id GitHub.cli
```

**Linux:**
```bash
# Debian/Ubuntu
sudo apt install gh

# Fedora
sudo dnf install gh
```

> **🤖 AI Shortcut:** Ask the AI:
> ```
> Install GitHub CLI on my machine
> ```

### Authenticate

```bash
gh auth login
```

Follow the prompts:
1. Select **GitHub.com**
2. Select **HTTPS** (recommended)
3. Authenticate with browser or token

> **🤖 AI Shortcut:** Ask the AI:
> ```
> Help me authenticate GitHub CLI
> ```

### Verify Authentication

```bash
gh auth status
```

Should show:
```
✓ Logged in to github.com as [your-username]
```

---

## 5. Verifying Your Setup

Run this checklist before using `/build-interactive-lj`:

### Manual Verification

```bash
# Check repos exist
ls ~/Documents/repositories/website
ls ~/Documents/repositories/interactive-tutorials
ls ~/Documents/repositories/grafana-recommender

# Check GitHub CLI
gh auth status

# Check Cursor workspace (in Cursor)
# File → Open Workspace → verify all 3 repos visible
```

### AI-Assisted Verification

> **🤖 AI Shortcut:** Ask the AI:
> ```
> Verify my setup for /build-interactive-lj - check repos, Playwright, and GitHub CLI
> ```

---

## 6. Common Issues

### "Repository not found in workspace"

**Cause:** The repo isn't added to your Cursor workspace.

**Fix:**
1. File → Add Folder to Workspace
2. Navigate to the missing repo
3. Click Add

### "Playwright MCP not available"

**Cause:** Playwright MCP isn't enabled or Cursor needs restart.

**Fix:**
1. Cursor Settings → Features → MCP Servers
2. Enable Playwright
3. Completely quit and restart Cursor

### "GitHub CLI not authenticated"

**Cause:** You haven't logged in with `gh auth login`.

**Fix:**
```bash
gh auth login
# Follow the prompts
```

### "Browser automation fails silently"

**Cause:** Usually an existing Chrome process blocking Playwright.

**Fix:**
1. Close all Chrome windows
2. Restart Cursor
3. Try again

### "Selector works in browser but fails in Pathfinder"

**Cause:** Pathfinder's Block Editor has different context than raw browser.

**Fix:**
1. Test selectors IN Pathfinder Block Editor, not just the browser
2. Some selectors need adjustment for the Pathfinder context
3. File an issue if consistently broken

---

## 7. Getting Help

- **Slack:** `#proj-grafana-pathfinder`
- **Issues:** https://github.com/grafana/interactive-tutorials/issues
- **Contact:** Robby Milo for selector issues

---

## Ready to Build!

Once all checks pass, you're ready to run:

```
/build-interactive-lj [learning-journey-slug]
```

Example:
```
/build-interactive-lj prometheus
/build-interactive-lj github-data-source
/build-interactive-lj mysql-data-source
```
