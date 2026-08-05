# Symbolic Selector Syntax Reference

How Pathfinder resolves `grafana:` reftargets, and the traps that come with them.

> **Sources.** Everything below is checked against `grafana-pathfinder-app`, which
> [CLAUDE.md](../../../CLAUDE.md#pathfinder-source) names as the source of truth:
>
> | What | Where |
> | --- | --- |
> | The resolver itself | `src/lib/dom/grafana-selector-core.ts` — `toGrafanaSelectorForVersion`, `getReverseIndex` |
> | Prefix dispatch (`grafana:`, `{grafana:}`, `panel:`) | `src/lib/dom/selector-resolver-core.ts` |
> | Nav-menu auto-fix (trap 1) | `src/lib/dom/dom-utils.ts`, `src/interactive-engine/action-handlers/guided-handler.ts` |
> | Upstream author docs | `docs/developer/interactive-examples/selectors-reference.md` |
>
> Read the source, not a deployed bundle. What this file adds on top of the upstream doc: the
> `{grafana:…}` embedded form (upstream documents only the bare and parameterized forms, though the
> embedded form is covered by the plugin's own tests in `src/lib/dom/selector-generator.test.ts`),
> the four traps below, and the conversion workflow.

---

## The three forms

| Form | Use for | Example |
| --- | --- | --- |
| `grafana:<path>` | the whole reftarget is one selector | `grafana:components.TimePicker.openButton` |
| `grafana:<path>:<arg>` | parameterized (function) selectors | `grafana:components.Panels.Panel.title:Graph` |
| `{grafana:<path>}` | a selector **inside** a larger CSS expression | `{grafana:components.DataSource.Prometheus.queryEditor.options} button` |

`<path>` is a dotted path into `{ components, pages }` — i.e. the two exports of
`@grafana/e2e-selectors`. Both roots are valid: `components.Foo.bar` **and** `pages.Explore.toolbar.split`.

The `:<arg>` split is on the **first** colon (`splitGrafanaPathParam`), and a path never contains
one, so an argument may: `grafana:components.Panels.Panel.title:Latency: p99` passes
`"Latency: p99"`.

## What the resolver actually does

```js
// src/lib/dom/grafana-selector-core.ts — toGrafanaSelectorForVersion, simplified
function resolve(path, version, arg) {
  let cur = resolveSelectors({ components, pages }, version);   // version-aware!
  for (const part of path.split('.')) {
    cur = cur[part];
    if (cur === undefined) throw new Error(`Selector not found: ${path}`);
  }
  const value = typeof cur === 'function' ? cur(arg) : cur;     // arg = the :<arg> suffix
  return `:is([data-testid=${q(value)}], [aria-label=${q(value)}])`;
}
```

Three consequences worth internalising:

1. **It is version-aware.** The tree is resolved with `config.buildInfo.version` of the *running*
   Grafana. This is the entire reason to prefer symbolic form over a literal.
2. **It matches `data-testid` OR `aria-label`.** Older selector versions often predate the
   `data-testid ` prefix convention and are matched by `aria-label` instead. The emitted `:is()`
   covers both spellings; a hand-written `[data-testid=...]` covers only one.
3. **A bad path throws.** `Selector not found: <path>` — so paths must be verified, not guessed.

### Why version-awareness matters — a concrete case

`components.QueryEditorRows.rows` resolves to:

| Grafana | Resolved value | A literal `[data-testid='data-testid Query editor row']` |
| --- | --- | --- |
| 13.1.0+ | `data-testid Query editor row` | matches |
| < 13.1.0 | `Query editor row` (an `aria-label`) | **silently fails** |

The symbolic form matches on both. This class of bug is invisible in review and only shows up on
older instances.

## Related shorthand: `panel:`

The resolver also accepts `panel:<title>` and `panel:<title> > <rest>`, expanding to:

```
[data-viz-panel-key]:has([data-testid*="Panel header <title>"])
```

Prefer `grafana:components.Panels.Panel.title:<title>` when you want the panel header element
itself; `panel:` is for scoping *into* a panel.

Two things about `<rest>` that read wrong (`resolvePanelSelector`):

- The separator must be exactly `" > "`, spaces included. Without it the entire remainder is taken
  as the **panel title** — so `panel:My panel button` looks for a panel titled `My panel button`.
- Despite that `>`, `<rest>` is joined with a **descendant** combinator, not a child one:
  `panel:CPU > .legend` becomes `[data-viz-panel-key]:has(…) .legend`.

---

## Traps

### 1. Nav menu items must stay literal

Pathfinder has an auto-fix that expands a collapsed menu section. It finds the target href by
regex-matching the **literal** selector shape:

```js
r.match(/a\[data-testid=['"]data-testid Nav menu item['"]\]\[href=['"]([^'"]+)['"]\]/)
```

The resolved `:is(...)` form still passes the preceding `.includes('data-testid Nav menu item')`
check but **fails this regex**, so `fixType: 'expand-parent-navigation'` never fires and the step
dead-ends whenever the section happens to be collapsed.

That regex appears twice — `src/lib/dom/dom-utils.ts` (the `exists-reftarget` check) and
`src/interactive-engine/action-handlers/guided-handler.ts` (guided blocks) — so converting a nav
item breaks both paths. A symbolic form also cannot express the `[href='…']` part at all, since the
href is not in the selector package; the whole point of the nav selector is the href discriminator.

**Leave nav menu reftargets exactly as they are:**

```json
"reftarget": "a[data-testid='data-testid Nav menu item'][href='/explore']"
```

### 2. One value, several paths

Some resolved values are shared by more than one path, so a value→path lookup is ambiguous and
whichever path you find first may be semantically wrong. Known cases:

| Value | Paths | Pick |
| --- | --- | --- |
| `data-testid prometheus type` | `configPage.prometheusType`, `queryEditor.type` | whichever the step means — the query editor's Range/Instant/Both group is `queryEditor.type` |
| `data-testid Select a data source` | `components.DataSourcePicker.inputV2` + 3 dashboard-variable aliases | `components.DataSourcePicker.inputV2` |
| `data-testid Data source picker select container` | `components.DataSourcePicker.container` + variable alias | `components.DataSourcePicker.container` |
| `data-testid radio-button` | `components.RadioButton.container` + a pages alias | `components.RadioButton.container` |
| `data-testid viz-layout-legend` | `VizLayout.legend`, `VizLegend.legend` | either resolves identically; prefer `VizLegend.legend` for a legend |

`scripts/find-ambiguous.py` lists every ambiguous value a guide touches. Pin each one explicitly.

**The plugin handles this by giving up.** `getReverseIndex` deletes a value the moment a second path
produces it (`exact.delete(value)`), so its element picker emits no `grafana:` reference for an
ambiguous value and falls back to a CSS strategy. `build-selector-map.ts` deliberately diverges — it
keeps the first path and records all of them — because you can pin what the picker cannot. That is
why **`strMap` is untrustworthy for any value listed in `ambiguous`**: resolve it with `--pin`.

### 3. Greedy parameterized selectors

Some function selectors have no distinguishing text — `QueryEditorRow.actionButton(t)` produces
just `data-testid ${t}`, which reverse-matches *any* value. The plugin's `buildTemplate` ignores a
pattern whose significant part (after stripping `data-testid `) is under 3 characters, and
`scripts/build-selector-map.ts` mirrors that (`MIN_SIGNIFICANT = 3`, reported as `greedyFns`). Such
paths are still perfectly usable — you just have to supply them deliberately, with `--param`, rather
than infer them.

`buildTemplate` also rejects a probe whose output contains the literal text `undefined`, which
indicates a selector template referencing something the resolved tree does not carry.
`build-selector-map.ts` reports those under `undefinedProbes` and excludes them from `fns`.

### 4. Localized values that look stable

A `data-testid` is only as stable as what produced it. Two live examples:

- `QueryOperationAction` falls back to `actionButton(props.title)` where `title` is `t()`-wrapped,
  so its test id changes with UI language unless the caller passes `dataTestId` explicitly.
- `RadioButtonGroup` options are distinguishable only by translated label/`title` unless the
  Grafana version has `RadioButton.option(value)`.

When a value traces back to a `t()` call, the selector is not i18n-safe — fix it in Grafana
rather than encoding the English string in the guide.

### 5. One bad token voids the whole reftarget

`resolveEmbeddedGrafanaTokens` is all-or-nothing: if **any** `{grafana:…}` token in a reftarget
fails to resolve, it returns the reftarget *untouched* — braces and all. The step then queries the
literal string `div{grafana:components.Foo.bar} button`, which matches nothing, and the only signal
is an `onError` callback.

So in a compound reftarget, a single typo'd or unreleased path also disables the tokens that were
correct. Two consequences:

- Validate **every** path in a reftarget, not a sample — `scripts/validate-paths.ts` over the whole
  extracted set.
- A partially converted reftarget (some parts symbolic, some still literal, which is what the
  release gate produces) is fine: the literal parts are plain CSS and are not tokens. It is only
  *failing tokens* that void the reftarget.

The bare `grafana:<path>` form degrades differently — on error it returns the reftarget, so the step
queries the literal text `grafana:components.Foo.bar`. Also nothing, but easier to spot.

---

## Re-verifying the resolver

If symbolic reftargets stop resolving, read the resolver in a `grafana-pathfinder-app` checkout:

```bash
sed -n '/toGrafanaSelectorForVersion/,/^}/p' src/lib/dom/grafana-selector-core.ts
grep -n "grafana:\|panel:" src/lib/dom/selector-resolver-core.ts
npx jest src/lib/dom/grafana-selector          # the resolver's own tests, incl. versioned cases
```

Check the plugin version you are targeting: `git log --oneline -- src/lib/dom/grafana-selector-core.ts`.

Do **not** reverse-engineer the shipped bundle. It was how this file started, and it produced a
false claim (that the syntax was undocumented) which then propagated into this repo's reference
docs. The source and the upstream author docs are both public.
