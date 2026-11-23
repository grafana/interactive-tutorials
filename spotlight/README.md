# Page spotlights

Create one JSON file per team in this folder. Each file contains an array.
Start with [the Alerting example](alerting.json). List standalone interactive
guide or learning path package IDs in sidebar order. A page can belong to one
spotlight across all files. A trailing slash is optional.

Use `additionalPaths` for other exact Grafana pages and an optional `schedule`
with inclusive UTC `startDate` and/or `endDate` in YYYY-MM-DD format. Removing
an object retires it after CDN publication and the next recommender reload.

PR validation checks package IDs and page ownership. The deploy job combines
the reviewed files into `packages/spotlights.json` beside `repository.json`.
Individual team JSON files are also published under `packages/spotlight/`.
