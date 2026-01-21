# Interactive Learning Tutorials

This repository contains interactive learning tutorials for Grafana, designed by
Developer Advocacy. It includes JSON guide content and is designed to work with
the Block Editor; assisted by Cursor's AI assistant (if you use it).

## TL;DR for Grafana Employees

1. Go to [https://learn.grafana-ops.net/plugins/grafana-pathfinder-app?dev=true](https://learn.grafana-ops.net/plugins/grafana-pathfinder-app?dev=true)
2. Log in with Okta SAML. Find the "Dev Mode" checkbox; enable it ([it looks like this](docs/img/dev-mode.png)) and save
3. Click the `?` icon (help menu for Grafana) in the upper right → Debug icon ([it looks like this](docs/img/dev-tools.jpg)) → Block Editor ([looks like this](docs/img/block-editor.jpg))
4. Start building.

*Not a Grafana employee? [Run locally](#run-the-plugin-locally)*

## Stuck?

Ping Tom Glenn, David Allen, or Simon Prickett, all of whom have done this before on `#proj-grafana-pathfinder`

## If you can't access stack above: Run the Plugin Locally

If you don't have access to `learn.grafana-ops.net/login` (e.g., you're an open source community contributor, customer, or internal user who doesn't have the right permissions set up), you can still run the Pathfinder plugin locally:

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

**Need help with selectors?** The Block Editor captures them automatically via Record mode. For advanced patterns, see [Selectors Reference](docs/selectors-and-testids.md).

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

### Need Help? Ask Cursor

Cursor knows this repo well. Use Ask mode to query how interactive elements work—it reads the `docs/` folder automatically.

[Download Cursor](https://cursor.com/downloads) | [Interactive Types Reference](docs/interactive-types.md)

## Demo: Understand What We're Building!

1. Go to [Drilldown section of Grafana Play](https://play.grafana.org/drilldown)
2. Clicking the `?` help icon in the upper right hand corner of the screen, toggles the interactive learning plugin on/off.

<img src="docs/img/icon.png" alt="Interactive Learning Icon" width="40" style="height:auto;" />

3. Make sure you're on the Drilldown page, check the Recommendations tab.
4. Follow the _Interactive Guide: Explore Drilldowns 101_ by clicking the "View" button by that recommendation. We're going to build
an interactive guide like that!
5. Notice the structure: it's built in sections, of individual steps, with each step having a "Show Me" and "Do It" option.

## Getting Your Tutorial Into The Plugin

1. **Submit**: Open a PR to this repo, ping reviewers
2. **Include**: several sentences describing when/where/who should see
your guide, so we can include it in the recommender.

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
