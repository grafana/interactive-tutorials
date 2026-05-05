---
disclaimer: Authored by hand for an internal presentation; not auto-generated.
notice: Update this file if the slide order, asset paths, or demo policy change.
---

# Authoring notes — pathfinder-roadmap-2026-lj

This package is a Pathfinder learning path that doubles as a slide deck for an internal talk on the Pathfinder roadmap. It is **not** intended for public discovery.

## Audience and scope

- **Recommended only on `learn.grafana.net`** via `targeting.match.source`.
- **Not added to** `index.json` / public recommender flows.
- **Eight milestones**, one per slide.

## Demo policy

- **No live multistep demos** during the talk — Pathfinder runs in full-screen mode and stage selectors are fragile.
- **One live interactive section** in milestone 05 (`05-killing-issues-at-the-root`) tours the Grafana Assistant. The Assistant lives in the sidebar, so it's safe alongside full-screen mode. Selectors come from a snippet Jay verified.
- All other slides use static `markdown`, `image`, and `video` blocks.

## Asset checklist (before the talk)

All `image` blocks reference paths under `/media/docs/learning-journey/pathfinder-roadmap-2026/` (the standard Grafana docs CDN convention). Assets live on `~/Desktop/` and need to be uploaded to the static site under that prefix before the talk.

Staged on Desktop:
- `era-timeline.svg` → slide 01
- `experiment-analytics-flow-v2.svg` → slide 03 *(replaces the earlier `openfeature-faro-flow.svg`; we don't run Faro, the diagram now reflects the real RudderStack event flow)*
- `recovery-ladder.svg` → slide 05
- `coda-architecture.svg` → slide 07
- `pathfinder-logo-v2.svg` → cover + slide 08 *(replaces the bare `pathfinder-logo.svg`; v2 is a presentation-grade lockup with icon + GRAFANA/PATHFINDER wordmark + path-trace motif)*
- `pathfinder-banner.svg` → header on slide 01 + slide 08 *(wide banner version of the logo for milestone bookends)*
- `grot-discouraged.svg` → slide 06 (pulled from `grafana-pathfinder-app/src/img/Grot-Emotions-Discouraged.svg`)
- `coda-logo.png` → slide 07 (pulled from `grafana-coda-app/img/logo.png`)

Captures still to take:
- `kiosk-mode.png` (slide 02) — fresh capture of Pathfinder running in kiosk mode with the GrafanaCON 2026 banner
- `selector-health.png` (slide 04) — capture of the Selector Health Badge in the block editor

If any image src 404s on stage, the surrounding markdown blocks summarise the slide so the talk continues.

## Headline metric placeholder

Slide 03 has a `> Headline metric:` callout reserved for the Maria experiment number. Edit that block before the talk.

## Why this manifest shape

- `category: general` — internal deck, doesn't fit a product category.
- `targeting.match.source: learn.grafana.net` — verified against `drilldown-metrics-lj/manifest.json` and `knowledge-graph-guide/manifest.json`.
- `startingLocation: /a/grafana-pathfinder-app` — the deck launches from the Pathfinder app home.
- Each step `depends` on the previous and `recommends` the next — gives Pathfinder a clean linear walk.

## Verification

1. Run `/lint` against `pathfinder-roadmap-2026-lj/` to validate JSON shape.
2. Run `/check` for best-practice violations.
3. Load locally in Pathfinder dev mode and walk all eight milestones in full-screen mode.
4. Confirm slide 05's Assistant section: open extension → form-fill works → assistant response highlights.
5. Stage rehearsal with internet + projector before the talk.
