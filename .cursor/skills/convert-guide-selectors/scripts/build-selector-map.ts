/**
 * Build a resolved-value -> dotted-path map for @grafana/e2e-selectors, plus a probe table for
 * parameterized selectors. Resolves the tree exactly as grafana-pathfinder-app does:
 * resolveSelectors({ components, pages }, version) — see
 * grafana-pathfinder-app/src/lib/dom/grafana-selector-core.ts (`getResolvedSelectors`).
 *
 * Run from THIS repo, with GRAFANA_REPO pointing at a grafana/grafana checkout:
 *   GRAFANA_REPO=~/Repos/grafana npx tsx build-selector-map.ts [version] > selmap.json
 *
 * `version` defaults to "latest". Pass the version of the Grafana you are targeting so that
 * version-gated selectors resolve to the value that instance actually renders.
 *
 * TWO DELIBERATE DIVERGENCES from the plugin's reverse index (`getReverseIndex`):
 *
 * 1. Ambiguous values. The plugin DROPS a value that several paths produce (`exact.delete(value)`)
 *    and emits no `grafana:` reference at all. This script keeps the first path and records every
 *    path under `ambiguous`, because a human with `--pin` can resolve what the picker cannot.
 *    Consequence: never trust `strMap` for a value listed in `ambiguous` — pin it.
 * 2. Probes are not filtered on `undefined`. The plugin rejects a template whose probe output
 *    `.includes('undefined')`; this script keeps them so the divergence is visible in the map
 *    rather than silent. They are marked `containsUndefined` and excluded from `fns`.
 */
import { loadSelectors } from './selectors-source';

const VERSION = process.argv[2] || 'latest';
const SENTINEL = 'PARAM';
/** The plugin ignores probe patterns whose significant part is shorter than this. */
const MIN_SIGNIFICANT = 3;


async function main() {
  const { versionedComponents, versionedPages, resolveSelectors } = await loadSelectors();
  const resolved: any = resolveSelectors(
    { components: versionedComponents, pages: versionedPages } as any,
    VERSION
  );

  // Null-prototype: a selector value of "constructor" / "toString" / "__proto__" would otherwise
  // collide with Object.prototype and either be dropped or crash the `??= []` below.
  /** value -> first path that produced it. Ambiguous values are reported separately. */
  const strMap: Record<string, string> = Object.create(null);
  /** every path that produced a given value, so callers can detect ambiguity */
  const allPaths: Record<string, string[]> = Object.create(null);
  /** single-argument function selectors, as reversible prefix/suffix probes */
  const fns: Array<{
    path: string;
    prefix: string;
    suffix: string;
    significant: number;
    containsUndefined: boolean;
  }> = [];

  function walk(node: any, path: string[]) {
    if (node == null) return;

    if (typeof node === 'string') {
      if (!(node in strMap)) strMap[node] = path.join('.');
      (allPaths[node] ??= []).push(path.join('.'));
      return;
    }

    if (typeof node === 'function') {
      let out: unknown;
      try {
        out = node(SENTINEL);
      } catch {
        return; // multi-arg or otherwise not probeable
      }
      if (typeof out !== 'string') return;
      const i = out.indexOf(SENTINEL);
      // Single-argument selectors only: the sentinel must appear exactly once.
      if (i === -1 || i !== out.lastIndexOf(SENTINEL)) return;

      const prefix = out.slice(0, i);
      const suffix = out.slice(i + SENTINEL.length);
      const significant = (prefix.replace(/^data-testid\s*/, '') + suffix).trim().length;
      fns.push({
        path: path.join('.'),
        prefix,
        suffix,
        significant,
        containsUndefined: out.includes('undefined'),
      });
      return;
    }

    if (typeof node === 'object') {
      for (const [k, v] of Object.entries(node)) walk(v, [...path, k]);
    }
  }

  walk(resolved, []);

  const ambiguous = Object.fromEntries(
    Object.entries(allPaths).filter(([, paths]) => new Set(paths).size > 1)
  );

  console.log(
    JSON.stringify({
      version: VERSION,
      minSignificant: MIN_SIGNIFICANT,
      strMap,
      ambiguous,
      // Most specific first so the best reverse-match wins.
      fns: fns
        .filter((f) => f.significant >= MIN_SIGNIFICANT && !f.containsUndefined)
        .sort((a, b) => b.significant - a.significant),
      // Kept for reporting: usable, but too greedy to infer automatically.
      greedyFns: fns.filter((f) => f.significant < MIN_SIGNIFICANT).map((f) => f.path),
      // The plugin rejects these outright; surfaced so a stale/misdeclared selector is visible.
      undefinedProbes: fns.filter((f) => f.containsUndefined).map((f) => f.path),
    })
  );
}

main().catch((e) => {
  console.error(String(e instanceof Error ? e.message : e));
  process.exit(1);
});
