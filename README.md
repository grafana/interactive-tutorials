# Interactive Tutorials

This repository contains interactive wizard experiences for Grafana, designed by
Developer Advocacy. It's designed to work with Cursor's AI assistant.

## First: Understand What We're Building!

1. Click "Open Grafana Pathfinder" button extreme upper right by Assistant button.
2. Make sure you're on the home screen, check the Recommendations tab.
3. Follow the _Interactive Tutorial: Explore Drilldowns 101_ by clicking the "View" button by that recommendation. We're going to build
an interactive tutorial like that!
4. Notice the structure: it's built in sections, of individual steps, with each step having a "Show Me" and "Do It" option.

## Quick Start: Let's Build a new Interactive Guide

0. **Make sure you have Cursor** (trust me it's worth it). [Download it](https://cursor.com/downloads).
1. If you don't have acess, request cursor access in `#it-help`. You'll need it so you
don't get rate limited
2. Sign in with your Grafana account after getting access
3. **Open in Cursor** - This repo is Cursor-enabled with AI guidance
4. **Create a tutorial** - Use the `/write My First Tutorial` command to start a new tutorial, giving it a name.
5. **See an example** - Check out `first-dashboard/unstyled.html` for a complete working example
6. **Get help** - Use `/lint`, `/check`, and `/attack` commands to Cursor for validation and testing of what you're writing as you go.

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
