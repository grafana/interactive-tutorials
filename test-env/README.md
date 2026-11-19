# Local test environment for interactive learning paths

A Docker Compose stack that serves this repository's packages from an external
repository and launches them in a local Grafana OSS instance, so a writer can
test an unpublished path, including a multi-milestone path, before it ships.
It needs no Grafana Cloud and no CDN.

This is a draft harness, wired as a worked example for `drilldown-metrics-lj`.

## What it does

- Runs Grafana OSS with the Metrics Drilldown and Pathfinder plugins.
- Serves the repo's own package directory from Grafana's own origin under
  `/public/pathfinder-ext/`, with a generated `repository.json` index.
- Points Pathfinder at that local repository instead of the production CDN.
- Runs Prometheus plus node_exporter so the Metrics Drilldown path has live
  metrics to browse, including a synthetic `asserts:resource:threshold` series.

## Dependencies: two grafana-pathfinder-app PRs

This harness does not work against a released Pathfinder plugin yet. It needs a
local build of `grafana/grafana-pathfinder-app` that includes both:

- grafana/grafana-pathfinder-app#2284 — a configurable dev repository source, so
  the plugin resolves guides from a local repository instead of the hardcoded
  CDN. Read from `/etc/grafana/pathfinder-dev-repository-url` here.
- grafana/grafana-pathfinder-app#2285 — a provisioned dev-mode opt-in honoured as
  the instance default, so `devMode` can be turned on from provisioning. Dev mode
  is what makes the plugin trust the `http://localhost` content this harness
  serves.

Build that checkout (`npm run build` and `mage build:linuxARM64`, or your
platform target) and point `PATHFINDER_PLUGIN_DIST` in `.env` at its `dist/`.

## Run it

```
export PATH="$HOME/.docker/bin:$PATH"   # if docker is not already on PATH
cd test-env

# 1. Build the external repository from this repo's packages. --cli points at
#    the grafana-pathfinder-app CLI (dist/cli/cli/index.js).
scripts/build-external-repo.bash --cli ../../grafana-pathfinder-app/dist/cli/cli/index.js

# 2. Start the stack.
docker compose up -d
```

Then open `http://localhost:3000`, log in as `admin` / `grafana`, open
`/a/grafana-metricsdrilldown-app/drilldown`, open the Interactive Learning panel,
and start "Explore data using Metrics Drilldown". It loads from the local
repository.

Tear down with `docker compose down -v`.

## How it fits together

- `scripts/build-external-repo.bash` copies the package into `generated/`
  (gitignored), builds `repository.json`, and rewrites the entry's targeting to
  supported predicates on `targetPlatform: oss` so it is recommended on OSS.
- `compose.yaml` mounts `generated/` at `/public/pathfinder-ext`, the local
  plugin build into the plugins directory, and `dev-repository-url` so the
  backend resolves the local repository.
- `grafana/provisioning/plugins/pathfinder.yaml` enables dev mode from
  provisioning (needs #2285).

## Known limitations

- Requires a local patched plugin build until the two PRs land in a release.
- Logged-in user only. A purely anonymous stack cannot enable dev mode, because
  the opt-in has no user identity to key on.
- The Prometheus seeding is specific to `drilldown-metrics-lj`. Other paths need
  their own data.
- The served index's targeting is rewritten to OSS for local recommendation; it
  does not reflect the path's real production targeting.
- `generated/` is rebuilt from scratch each run; re-run the script after editing
  a package.
