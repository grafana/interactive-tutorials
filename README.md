# Interactive Tutorials

This repository contains interactive wizard experiences for Grafana, designed by
Developer Advocacy. It's designed to work with Cursor's AI assistant.

## First: Understand What We're Building!

1. Click "Open Grafana Pathfinder" button extreme upper right by Assistant button.
2. Make sure you're on the home screen, check the Recommendations tab.
3. Follow the _Interactive Tutorial: Drilldown apps 101_ by clicking the "View" button by that recommendation. We're going to build
an interactive tutorial like that!
4. Notice the structure: it's built in sections, of individual steps, with each step having a "Show Me" and "Do It" option.

## Quick Start: Let's Build a new Interactive Guide

0. **Make sure you have Cursor** (trust me it's worth it). [Download it](https://cursor.com/downloads).
1. If you don't have acess, request cursor access in `#it-help`. You'll need it so you
don't get rate limited
2. Sign in with your Grafana account after getting access
3. **Open in Cursor** - This repo is Cursor-enabled with AI guidance
4. **Create a tutorial** - Use the `/new` command to start a new tutorial, giving it a name.
5. **See an example** - Check out `first-dashboard/unstyled.html` for a complete working example
6. **Get help** - Use `/lint`, `/check`, and `/attack` commands to Cursor for validation and testing of what you're writing as you go.

## Authoring workflow / testing your tutorial in Pathfinder

There are several ways to be able to test your interactive tutorials before setting them live. Depending on your set-up it will alter your workflow or dictate what options are available to you.

1. Enable dev mode in Pathfinder. You do this by navigating to the configuration page in Pathfinder and appending the `dev=true` query parameter to your URL. In your Grafana instance the full path should be: `{instance}/plugins/grafana-pathfinder-app?page=configuration&dev=true`
2. This will show a Dev Mode checkbox in the configuration page. Ensure it is checked then save your settings. The page will automatically refresh.
3. This will enable the Dev Mode tools in Pathfinder which you can find under the 'Recommendations' tab.
4. One of the tools is the 'Tutorial Tester'. Here you will see two tabs where you can enter a URL to load up in Pathfinder. The main difference between the two is the 'GitHub' tab has additional validation steps to help guide you to the right path and doesn't expect the `unstyled.html` suffix, where the 'Other' tab is free-form and lets you enter any path which ends in `unstyled.html`.
5. For what URL to put in, you have two choices:
  - Either create a GitHub branch in this repo and push your changes as you make updates.
  - OR run a local server which is serving your interactive tutorials. VSCode / Cursor have an extension called [Live Server authored by Ritwick Dey](https://marketplace.cursorapi.com/items/?itemName=ritwickdey.LiveServer) which makes this exceptionally easy. Just open this repo in Cursor and in the bottom right you click 'Go Live'. Open the local server in your browser (it should open automatically) and you can navigate to any `unstyled.html` tutorial, copy the link and open it in your Pathfinder instance.
- In Pathfinder there is a refresh button, so as you make changes to your tutorial you don't have to refresh your Grafana Cloud window, just click the refresh button to see your changes immediately.
- Iterate on your Interactive Tutorial, and once it is complete commit the changes to the branch and open a Pull Request so it can be merged into `main` and set live in production!

## Ask Cursor Questions in Dev Loop

* Cursor has a bunch of docs on how these guides are structured and how this all works. (See `docs/` and `.cursor`)
you could read them all, or just ask Cursor to explain things as you go.
* DOM selectors for elements (`data-reftarget` in the guides) is usually the trickiest part. New tooling on the way
to help with that soon

## Ask Humans Questions in `#proj-grafana-pathfinder`

* Talk to Tom Glenn, David Allen, or Simon Prickett, all of whom have done this before. They will help.

## Getting Your Tutorial Into Pathfinder

1. Open a PR to this repo with your new guide! Ping Jay Clifford, Tom Glenn, or
David Allen in `#team-dev-advocacy` to get it merged.
2. We'll wire it into the recommender for you.
3. MAKE SURE TO INCLUDE IN YOUR PR:  When should users see your guide? What are they looking at in the UI when it appears as a recommendation? Who should see your guide? Admins only?  Commercial stacks?  Free stacks? "Everybody" is an acceptable answer.  This determines how it will appear.

## Full Reference Documentation

For complete AI reference documentation, see `.cursor/README.mdc`.  This contains
a full reference guide to all of the things that can be done, and how to use them.
