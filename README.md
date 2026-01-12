# Interactive Learning Tutorials

This repository contains interactive learning tutorials for Grafana, designed by
Developer Advocacy. It includes JSON guide content and is designed to work with
the Block Editor and Cursor's AI assistant.

## First: Understand What We're Building!

0. Go to [Drilldown section of Grafana Play](https://play.grafana.org/drilldown)
1. Click the `?` help icon in the upper right hand corner of the screen, to open the interactive learning plugin

<img src="docs/img/icon.png" alt="Interactive Learning Icon" width="80" style="height:auto;" />

2. Make sure you're on the Drilldown page, check the Recommendations tab.
3. Follow the _Interactive Guide: Explore Drilldowns 101_ by clicking the "View" button by that recommendation. We're going to build
an interactive guide like that!
4. Notice the structure: it's built in sections, of individual steps, with each step having a "Show Me" and "Do It" option.

## Quick Start: Let's Build a new Interactive Guide

Big picture, here's what you need to do: run a stack with the plugin, enable dev mode, and then
go use the Block Editor under dev tools to create your new content. Sections below step you through how to do each of those things.

### For Grafana Employees

The fastest way to get started:

1. Go to [pathfinder.grafana-dev.net](https://pathfinder.grafana-dev.net)
2. Log in with your Grafana credentials
3. Navigate to the plugin configuration with `?dev=true`:
   [https://pathfinder.grafana-dev.net/plugins/grafana-pathfinder-app?dev=true](https://pathfinder.grafana-dev.net/plugins/grafana-pathfinder-app?dev=true)
4. Enable "Dev Mode" checkbox and save.  **This must be done or the editor will not appear**.

![Dev Mode Checkbox](docs/img/dev-mode.png)

5. Click the `?` help icon to open the Pathfinder sidebar
6. Click the "Debug" icon at the top of the sidebar to access dev tools.

![Dev Tools](docs/img/dev-tools.jpg)

6. Use the **Block Editor** (in the dev tools section) to create your guide

![Block Editor](docs/img/block-editor.jpg)

*The Block Editor is the main way to write new guides, it provides a visual interface for composing guides from blocks.*

### If you can't access stack above: Run the Plugin Locally

If you don't have access to pathfinder.grafana-dev.net (e.g., you're an open source community contributor, customer, or internal user who doesn't have the right permissions set up), you can run the Pathfinder plugin locally:

* **Cursor is recommended but not required** (but we think it's worth it). [Download it](https://cursor.com/downloads).
* Clone this repo to your machine. Also clone the [interactive learning plugin](https://github.com/grafana/grafana-pathfinder-app)
* Start the plugin repo. [Full instructions are here](https://github.com/grafana/grafana-pathfinder-app/blob/main/docs/developer/LOCAL_DEV.md) but the short version is: `npm install` then `npm run build && npm run server` and go to http://localhost:3000/
* Now follow the same instructions as above: go to the Interactive Learning Plugin settings page, and set the
end of the URL to include `?dev=true`. The full URL should be roughly `{instance}/plugins/grafana-pathfinder-app?dev=true`
* All other instructions are the same.

### Writing Your Guide with the Block Editor

Interactive guides are JSON documents. See [explore-drilldowns-101/content.json](explore-drilldowns-101/content.json) for a complete example.

The **Block Editor** is the recommended way to create guides:

1. Open the Block Editor from the Pathfinder sidebar (dev mode must be enabled)
2. Click "Add Block" to add content blocks (markdown, interactive, section, etc.)
3. Use the **Record** feature on sections to capture your interactions automatically
4. Preview your guide with the Preview toggle
5. Export via "Copy JSON" or create a GitHub PR directly from the editor

**Alternative: Cursor-assisted authoring**

This repository includes Cursor AI prompts and commands for guide authoring.
In Cursor, you can use `/new My Guide Name` to scaffold a new guide directory.
See the `.cursor/` folder for available commands and prompts.

### Iterate & Develop

The Block Editor auto-saves your work to localStorage, so you can iterate without losing progress.

To test your guide:

1. Use the **Preview** mode in the Block Editor to see how it renders
2. Alternatively, export the JSON and use the **Tutorial Tester** to load it by URL

The Tutorial Tester accepts:
- A local file URL (if using [Live Server extension](https://marketplace.cursorapi.com/items/?itemName=ritwickdey.LiveServer))
- A GitHub raw URL (push to a branch first)
- Pasted JSON content

![Test Tutorial](docs/img/test-tutorial.png)

**NOTE**: Tutorial Tester and Block Editor only appear when dev mode is enabled.

### DOM Selectors

Interactive guides target UI elements using CSS selectors stored in the `reftarget` field. The Block Editor provides two ways to capture these selectors automatically:

**Record Mode** (for sections)

1. Click the **Record** button (red circle icon) on any section block
2. Navigate and interact with Grafana normally - clicks, inputs, and form fills are captured
3. A red banner appears showing your step count; hover over elements to see the DOM path
4. Press **Stop** or **Escape** when finished
5. Recorded steps are automatically added as interactive blocks with selectors filled in

**Element Picker** (for individual blocks)

1. When editing an interactive, multistep, or guided block, click the **Pick Element** button (crosshair icon)
2. Click any element on the page to capture its selector
3. The selector is automatically inserted into the form

Both methods use intelligent selector generation that prefers stable `data-testid` attributes, falls back to semantic attributes (`href`, `aria-label`, `id`), and warns about fragile selectors.

For advanced selector patterns and manual writing, see [docs/selectors-and-testids.md](docs/selectors-and-testids.md).

### Interactive Action Types: Asking Cursor for Help

What kinds of interactive steps can you make? See [docs/interactive-types.md](docs/interactive-types.md) for a full list, or
just ask Cursor. A good way to get started is to read one of the existing guides, highlight bits and
add it to the model context, and ask Cursor "How does this part work?"

Cursor knows quite a lot about what's in this repo! Use `Ask` mode and ask it
questions about how different interactive elements work. Cursor will use the `docs`
folder in this repo to answer your questions.

Here's an example of Cursor in Ask mode, explaining a feature:

![Cursor Explain](docs/img/cursor-explain.png)

## Ask Us Questions!

* Talk to Tom Glenn, David Allen, or Simon Prickett, all of whom have done this before. They will help.
* They can be reached by email (if they have shared with you) or internal on Grafana's slack in `#proj-grafana-pathfinder`

## Getting Your Tutorial Into The Plugin

Once you're finished with a draft, we need to add it to the recommender. This will
ensure that the right users get the content recommended to them when using Grafana.

1. Open a PR to this repo with your new guide! Ping Jay Clifford, Tom Glenn, or
David Allen to get it merged.
2. We'll wire it into the recommender for you.
3. MAKE SURE TO INCLUDE IN YOUR PR: When should users see your guide? What are they looking at in the UI when it appears as a recommendation? Who should see your guide? Admins only? Commercial stacks? Free stacks? "Everybody" is an acceptable answer. This determines how it will appear.

## Full Reference Documentation

For complete reference documentation:

- **This repo**: See [.cursor/ai-guide-reference.mdc](.cursor/ai-guide-reference.mdc) for AI-assisted authoring
- **Pathfinder Plugin Docs**: See [interactive learning plugin docs](https://grafana.com/docs/plugins/grafana-pathfinder-app/latest/)

Primary documentation files in this repo:

| Topic | File |
|-------|------|
| Guide Format | [docs/json-guide-format.md](docs/json-guide-format.md) |
| Block Types | [docs/interactive-types.md](docs/interactive-types.md) |
| Properties | [docs/json-block-properties.md](docs/json-block-properties.md) |
| Requirements | [docs/requirements-reference.md](docs/requirements-reference.md) |
| Selectors | [docs/selectors-and-testids.md](docs/selectors-and-testids.md) |
