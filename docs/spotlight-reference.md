# Page spotlights

Teams propose one file per team under `spotlight/`. Agree page ownership with
the product team. Add a file-specific CODEOWNERS entry when onboarding a team.
Spotlight maintainers review new teams and must sign off on shared pages such
as `/`. An expired entry still reserves its pages. Remove or update it before
another team claims them. Validation warns about expired entries.

A team file is an array of spotlight objects. The heading is 1–80 characters,
trimmed, with no control characters. Supply one primary path and up to 11
additional paths. Paths must start with a slash, be normalized, fit in 2048
UTF-8 bytes, and contain no query, fragment, backslash, whitespace, control
character or double slash. A trailing slash represents the same page.

List 1–12 distinct package IDs in sidebar order. Choose standalone interactive
guides or learning paths. Milestones, track members, nested chapters and test
packages are excluded. At request time the recommender also applies guide
health and source/platform targeting. Optional startDate and endDate fields
under schedule use inclusive UTC dates in YYYY-MM-DD format.

Rebuild the package index from the checkout before validating team files:

```sh
node pathfinder-app/dist/cli/cli/index.js build-repository . --exclude pathfinder-app --exclude shared -o repository.json
python3 .github/scripts/build_spotlights.py spotlight repository.json spotlights.json
```

The [v1 JSON Schema](spotlight-index-v1.schema.json) describes the wire format. Editors can associate team files with its `#/$defs/teamFile` definition.
The CDN document is an object with integer `schemaVersion: 1` and a required
`spotlights` array. An empty array clears all published pages. Consumers ignore
new optional fields within version 1. Coordinate breaking changes and update
the matching fixture in both repositories before publishing another major
version. The producer fixture is in `.github/scripts/testdata/spotlights-v1.json`
and the reader fixture is in `cmd/recommender/testdata/spotlights-v1.json`.
A spotlight build failure leaves the last published index in place and guide
publication proceeds.
