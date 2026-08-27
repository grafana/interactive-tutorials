---
disclaimer: Auto-generated during guide update. Do not edit manually.
guide_id: get-started-see-dashboards
change_request: "Add interaction types that teach dashboard anatomy hands-on: guided hover for the panel menu, interactive time-range change. No quiz (user declined)."
---

# Change Log — 2026-08-27

Snapshot of the prior version: `assets/snapshots/content.json.before`.

## Live verification (play.grafana.org, anonymous, 2026-08-27 ~16:55 CT, Stats dashboard `/d/Zb3f4veGk`)

- All 11 panels are stat panels; no time series with hover tooltips, so the hover beat targets the **panel menu** instead.
- Panel menu button (`data-testid Panel menu The Basics`) is in the DOM but `visibility: hidden; opacity: 0` with class `show-on-hover` — CSS hover reveal, cannot be triggered programmatically → `guided` block (rule per docs/guided-interactions.md).
- Menu contents for anonymous visitors: View, Edit, Share, Inspect, Assistant, Extensions, More. Copy names View/Share/Inspect.
- Time picker: `button[data-testid='data-testid TimePicker Open Button']` opens overlay with options `[data-testid='data-testid TimePicker time range option now-5m to now']` etc. **Clicking the bare `li` does not apply the range; the `label` inside it must be clicked** — reftarget uses `... label`. Verified: click applies `?from=now-5m&to=now` and the button label updates. Read-only (URL params only).

## Edits

1. **Edit `blocks[0]` (intro)**: dropped the "**What you will learn:**" label (matches get-started-see-alerting style); "Play's" → "Grafana Play's"; promise now includes the hidden menu and changing the time window.
2. **Edit `blocks[4]`**: "Next, read the dashboard and try its controls:" (was "find the two parts every dashboard shares").
3. **Add `blocks[5].blocks[1]`**: `guided` block, single hover step on `[data-testid='data-testid Panel header The Basics']`, `stepTimeout: 45000`, `skippable: true` — learner physically hovers to reveal the panel menu (CSS `:hover`; automation cannot).
4. **Edit `blocks[5].blocks[2]`** (time picker): removed `doIt: false` — the learner now clicks to open the picker.
5. **Add `blocks[5].blocks[3]`**: highlight on the Last 5 minutes option (`... option now-5m to now'] label`) — every panel redraws; `exists-reftarget` is satisfied once the picker is open (sequential step gating).
6. **Edit `blocks[6]` (closer)**: adds the menu and "change it once and every panel follows".
7. **Edit `manifest.json` description**: mentions hover-to-reveal menu and the hands-on time-range change.
8. **Edit website slide `06-what-youre-looking-at/index.md`**: walk-through sentence mentions the hidden menu and the self-serve time-range change.

Quiz deliberately omitted (user declined).

## Addendum — dashboard switch (same session, user-directed)

User asked for a better dashboard than Stats. Switched to **Demo Wind Farm** (`/d/avzwehmz/demo-wind-farm`, Examples folder) — physically relatable (power, turbine RPM, wind) and has varied panel types (2 time series charts + stat/gauge panels) instead of all-stat.

Live verification (2026-08-27 ~17:15 CT, anonymous):

- 9 panels; headers include `Wind Farm - Total Average Power (Watts)` and `Current Power` (used as targets, both verified in DOM).
- Panel menu buttons present (9) and CSS-hidden until hover — guided hover beat unchanged, retargeted to **Current Power**.
- Default time range **Last 12 hours**. At **Last 1 hour**: all panels have data, 0 "No data". At **Last 5 minutes**: one panel shows "No data" and one chart drops out — so the range step now picks **Last 1 hour** (`now-1h to now`), not Last 5 minutes.
- Range option still requires clicking the inner `label` (not the `li`).

Edits: navigate reftarget/verify/objectives → `/d/avzwehmz`; section + step requirements → `on-page:/d/avzwehmz`; panel beat retargeted to the power chart; guided hover retargeted to Current Power; range option → `now-1h to now`; intro/step copy wind-farm flavored; `manifest.json` targeting `urlPrefix` → `/d/avzwehmz`, description updated. Website tracking docs updated (`getting-started-guide-outline.md`, `outline.md`, `doc-facts.md`).

## Addendum — panel menu fully automated (same session, user-directed)

User asked whether the panel-menu flow could run without any user action (highlight panel → highlight menu → menu opens). Replaced the `guided` hover-and-click block with a `multistep`.

Why it works (verified against engine source and live DOM, 2026-08-27 ~17:40 CT):

- The menu icon's reveal is **pure CSS `:hover`** — dispatching synthetic `mouseenter`/`mouseover`/`mousemove` on the panel leaves `visibility: hidden` (tested live via CDP). So no automation can show the fade-in itself.
- But Pathfinder's focus handler (`focus-handler.ts` `handleDoMode`) clicks invisible targets anyway ("Continue anyway (non-breaking)" then `element.click()`), and a JS click on the hidden menu button **does open the menu** (verified live earlier on the Stats dashboard).
- `interactive-multi-step.tsx` runs each step as show (highlight + tooltip) then do, with a delay — so one **Do it** plays: panel highlighted → corner highlighted → menu pops open.

Edits: `blocks[5].blocks[1]` guided → multistep; step 1 `hover` on the Current Power header (show highlights the panel; do dispatches harmless synthetic hover), step 2 `highlight` on the menu button (show boxes the corner where the icon lives; do clicks it and the menu opens with **View**, **Share**, **Inspect**). Copy reframed from "move your mouse and click" to "watch: the menu opens". Dropped `stepTimeout`/`skippable` (no user action to time out on); added `exists-reftarget` (menu button is always in the DOM, just hidden).

## Validation

Pathfinder CLI `validate --packages` (repo root): PASS (re-run after the multistep change).
