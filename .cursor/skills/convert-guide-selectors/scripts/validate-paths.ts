/**
 * Verify every selector path a guide references actually resolves — at each Grafana version you
 * support. Mirrors grafana-pathfinder-app's `toGrafanaSelectorForVersion`
 * (src/lib/dom/grafana-selector-core.ts): walk the dotted path over
 * resolveSelectors({ components, pages }, version), then require string | function.
 *
 * Run from THIS repo, with GRAFANA_REPO pointing at a grafana/grafana checkout:
 *   GRAFANA_REPO=~/Repos/grafana npx tsx validate-paths.ts \
 *     '["components.TimePicker.openButton", ...]' "12.4.0,13.2.0"
 *
 * Exits non-zero if any path fails at any version. Validating the MINIMUM supported version as
 * well as current is what catches selectors whose older form matched aria-label rather than
 * data-testid.
 *
 * A resolved value is NOT proof the selector exists at that version. `resolveSelector` falls back to
 * the NEWEST version key when none is <= the requested version, so a path introduced above your
 * floor resolves cleanly there to a value that Grafana's DOM never carried. This script therefore
 * also reads each path's lowest version key straight from the versioned tree and flags any path
 * whose floor is above a requested version (reported as BELOW-FLOOR / WARN). Those are warnings, not
 * failures — targeting a newer-only selector is legitimate if your guide targets newer instances —
 * but they are never silently green.
 */
import { loadSelectors } from './selectors-source';

const paths: string[] = JSON.parse(process.argv[2] ?? '[]');
const versions = (process.argv[3] ?? 'latest').split(',').map((v) => v.trim());

if (paths.length === 0) {
  console.error('usage: tsx validate-paths.ts \'["components.X.y"]\' "12.4.0,13.2.0"');
  process.exit(2);
}

const SEMVER = /^\d+\.\d+\.\d+$/;
const cmpVersion = (a: string, b: string): number => {
  const [x, y] = [a, b].map((v) => v.split('.').map(Number));
  return x[0] - y[0] || x[1] - y[1] || x[2] - y[2];
};

async function main() {
  const { versionedComponents, versionedPages, resolveSelectors } = await loadSelectors();

  // Walk the RAW versioned tree — not the resolved one — to recover the version keys the resolver
  // consumes. The lowest key is the version the selector was introduced at.
  function introducedAt(path: string): string | undefined {
    let cur: any = { components: versionedComponents, pages: versionedPages };
    for (const part of path.split('.')) {
      if (!cur || typeof cur !== 'object') return undefined;
      cur = cur[part];
      if (cur === undefined) return undefined;
    }
    if (!cur || typeof cur !== 'object') return undefined;
    const keys = Object.keys(cur).filter((k) => SEMVER.test(k));
    return keys.length ? keys.sort(cmpVersion)[0] : undefined;
  }

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
  const belowFloor: Array<{ path: string; version: string; floor: string }> = [];
  const floors = new Map(paths.map((p) => [p, introducedAt(p)]));

  for (const v of versions) {
    console.log(`\n===== Grafana ${v} =====`);
    for (const p of paths) {
      const r = resolveOne(p, v);
      if (!r.ok) {
        failures++;
        console.log(`  FAIL  ${p}  ->  ${r.err}`);
        continue;
      }

      (seen.get(p) ?? seen.set(p, new Set()).get(p)!).add(r.value);

      const floor = floors.get(p);
      const below = floor && SEMVER.test(v) && cmpVersion(v, floor) < 0;
      if (below) {
        belowFloor.push({ path: p, version: v, floor });
        console.log(`  WARN  ${p}  ->  ${r.value}   (defined only from ${floor})`);
      } else {
        console.log(`  OK    ${p}  ->  ${r.value}`);
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

  // The resolver's below-floor fallback returns the newest value, so these resolved "fine" above.
  // They are the one class of problem a green run cannot rule out — and because such a path usually
  // has a single version key, it also looks maximally stable in the divergence section.
  if (belowFloor.length) {
    console.log('\n===== BELOW FLOOR: resolves, but did not exist at that version =====');
    for (const { path: p, version, floor } of belowFloor) {
      console.log(`  ${p}\n    asked for ${version}, defined only from ${floor} — matches nothing on ${version}`);
    }
    console.log('\n  Either raise your minimum supported version, or keep these steps on a');
    console.log('  working selector until the floor is within range.');
  }

  const unknownFloor = paths.filter((p) => seen.has(p) && !floors.get(p));
  if (unknownFloor.length) {
    console.log('\n===== Version keys not found (floor unchecked) =====');
    for (const p of unknownFloor) {
      console.log(`  ${p}`);
    }
  }

  console.log(`\nTOTAL FAILURES: ${failures}    BELOW-FLOOR WARNINGS: ${belowFloor.length}`);
  process.exit(failures === 0 ? 0 : 1);
}

main().catch((e) => {
  console.error(String(e instanceof Error ? e.message : e));
  process.exit(1);
});
