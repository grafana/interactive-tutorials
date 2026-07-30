/**
 * Build a resolved-value -> dotted-path map for @grafana/e2e-selectors, plus a probe table for
 * parameterized selectors. Mirrors what grafana-pathfinder-app's resolver sees:
 * resolveSelectors({ components, pages }, version).
 *
 * Run from a grafana/grafana checkout:
 *   tsx build-selector-map.ts [version] > selmap.json
 *
 * `version` defaults to "latest". Pass the version of the Grafana you are targeting so that
 * version-gated selectors resolve to the value that instance actually renders.
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

  /** value -> first path that produced it. Ambiguous values are reported separately. */
  const strMap: Record<string, string> = {};
  /** every path that produced a given value, so callers can detect ambiguity */
  const allPaths: Record<string, string[]> = {};
  /** single-argument function selectors, as reversible prefix/suffix probes */
  const fns: Array<{ path: string; prefix: string; suffix: string; significant: number }> = [];

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
      fns.push({ path: path.join('.'), prefix, suffix, significant });
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
      fns: fns.filter((f) => f.significant >= MIN_SIGNIFICANT).sort((a, b) => b.significant - a.significant),
      // Kept for reporting: usable, but too greedy to infer automatically.
      greedyFns: fns.filter((f) => f.significant < MIN_SIGNIFICANT).map((f) => f.path),
    })
  );
}

main().catch((e) => {
  console.error(String(e instanceof Error ? e.message : e));
  process.exit(1);
});
