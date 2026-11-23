# Page spotlights

Create one JSON file per team in this folder. Each file contains an array.
List standalone interactive
guide or learning path package IDs in sidebar order. A page can belong to one
spotlight across all files. A trailing slash is optional.

For example, a team file could contain the following when ready to publish.

```json
[
  {
    "path": "/alerting/list",
    "heading": "Get started with alerting",
    "guides": ["alerting-101", "deploy-alert-terraform-lj"]
  }
]
```

Use `additionalPaths` for other exact Grafana pages and an optional `schedule`
with inclusive UTC `startDate` and/or `endDate` in YYYY-MM-DD format. Removing
an object retires it after CDN publication and the next recommender reload.

PR validation checks package IDs and page ownership. The deploy job combines
the reviewed files into `packages/spotlights.json` beside `repository.json`.
Individual team JSON files are also published under `packages/spotlight/`.
