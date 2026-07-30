# Symbolic Selector Syntax Reference

How Pathfinder resolves `grafana:` reftargets, and the traps that come with them.

> **Provenance.** The behaviour below was established by reading the resolver in
> `grafana-pathfinder-app` **v2.15.0** (`/public/plugins/grafana-pathfinder-app/366.js`, webpack
> module `6845`) on a live Grafana Cloud instance, then verifying every path resolves against two
> Grafana versions. It is **not** described in the plugin's published docs. If resolution
> misbehaves, re-verify against the deployed plugin before trusting this file —
> see [Re-verifying the resolver](#re-verifying-the-resolver).

---

## The three forms

| Form | Use for | Example |
| --- | --- | --- |
| `grafana:<path>` | the whole reftarget is one selector | `grafana:components.TimePicker.openButton` |
| `grafana:<path>:<arg>` | parameterized (function) selectors | `grafana:components.Panels.Panel.title:Graph` |
| `{grafana:<path>}` | a selector **inside** a larger CSS expression | `{grafana:components.DataSource.Prometheus.queryEditor.options} button` |

`<path>` is a dotted path into `{ components, pages }` — i.e. the two exports of
`@grafana/e2e-selectors`. Both roots are valid: `components.Foo.bar` **and** `pages.Explore.toolbar.split`.

## What the resolver actually does

```js
// grafana-pathfinder-app, module 6845, simplified
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

### 3. Greedy parameterized selectors

Some function selectors have no distinguishing text — `QueryEditorRow.actionButton(t)` produces
just `data-testid ${t}`, which reverse-matches *any* value. The plugin's own heuristic ignores a
pattern whose significant part (after stripping `data-testid `) is under 3 characters, and
`scripts/build-selector-map.ts` mirrors that. Such paths are still perfectly usable — you just
have to supply them deliberately rather than infer them.

### 4. Localized values that look stable

A `data-testid` is only as stable as what produced it. Two live examples:

- `QueryOperationAction` falls back to `actionButton(props.title)` where `title` is `t()`-wrapped,
  so its test id changes with UI language unless the caller passes `dataTestId` explicitly.
- `RadioButtonGroup` options are distinguishable only by translated label/`title` unless the
  Grafana version has `RadioButton.option(value)`.

When a value traces back to a `t()` call, the selector is not i18n-safe — fix it in Grafana
rather than encoding the English string in the guide.

---

## Re-verifying the resolver

If symbolic reftargets stop resolving, confirm the contract against the deployed plugin:

```js
// In the browser console on a logged-in Grafana instance
const src = await (await fetch('/public/plugins/grafana-pathfinder-app/366.js')).text();
console.log(src.includes('Selector not found:'), src.includes(':is([data-testid='));
// both true => the resolver still behaves as documented here
```

Chunk numbering changes between plugin builds. To find the right chunk, fetch
`/public/plugins/grafana-pathfinder-app/module.js`, collect the numeric chunk ids, and search each
`<id>.js` for `Selector not found:`.
