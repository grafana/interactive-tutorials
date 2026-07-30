/**
 * Verify every selector path a guide references actually resolves — at each Grafana version you
 * support. Mirrors grafana-pathfinder-app's resolver: walk the dotted path over
 * resolveSelectors({ components, pages }, version), then require string | function.
 *
 * Run from a grafana/grafana checkout:
 *   tsx validate-paths.ts '["components.TimePicker.openButton", ...]' "12.4.0,13.2.0"
 *
 * Exits non-zero if any path fails at any version. Validating the MINIMUM supported version as
 * well as current is what catches selectors whose older form matched aria-label rather than
 * data-testid.
 */
import { loadSelectors } from './selectors-source';

const paths: string[] = JSON.parse(process.argv[2] ?? '[]');
const versions = (process.argv[3] ?? 'latest').split(',').map((v) => v.trim());

if (paths.length === 0) {
  console.error('usage: tsx validate-paths.ts \'["components.X.y"]\' "12.4.0,13.2.0"');
  process.exit(2);
}

async function main() {
  const { versionedComponents, versionedPages, resolveSelectors } = await loadSelectors();

  type Result = { ok: true; value: string } | { ok: false; err: string };

  function resolveOne(path: string, version: string): Result {
    let cur: any = resolveSelectors(
      { components: versionedComponents, pages: versionedPages } as any,
      version
    );
    for (const part of path.split('.')) {
      if (!cur || typeof cur !== 'object') return { ok: false, err: `failed at "${part}"` };
      cur = cur[part];
      if (cur === undefined) return { ok: false, err: `"${part}" is undefined` };
    }
    if (typeof cur === 'function') {
      const out = cur('ARG');
      return typeof out === 'string'
        ? { ok: true, value: out }
        : { ok: false, err: 'function returned non-string' };
    }
    return typeof cur === 'string' ? { ok: true, value: cur } : { ok: false, err: `type ${typeof cur}` };
  }

  let failures = 0;
  const seen = new Map<string, Set<string>>();

  for (const v of versions) {
    console.log(`\n===== Grafana ${v} =====`);
    for (const p of paths) {
      const r = resolveOne(p, v);
      if (r.ok) {
        console.log(`  OK    ${p}  ->  ${r.value}`);
        (seen.get(p) ?? seen.set(p, new Set()).get(p)!).add(r.value);
      } else {
        failures++;
        console.log(`  FAIL  ${p}  ->  ${r.err}`);
      }
    }
  }

  // Values that differ across versions are exactly why the symbolic form is required; surface them
  // so nobody "simplifies" them back into a literal.
  const varying = [...seen.entries()].filter(([, vals]) => vals.size > 1);
  if (varying.length) {
    console.log('\n===== Resolves differently per version (do NOT hardcode these) =====');
    for (const [p, vals] of varying) {
      console.log(`  ${p}\n    ${[...vals].map((v) => JSON.stringify(v)).join('  |  ')}`);
    }
  }

  console.log(`\nTOTAL FAILURES: ${failures}`);
  process.exit(failures === 0 ? 0 : 1);
}

main().catch((e) => {
  console.error(String(e instanceof Error ? e.message : e));
  process.exit(1);
});
