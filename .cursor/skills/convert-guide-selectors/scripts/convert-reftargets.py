#!/usr/bin/env python3
"""
Rewrite a guide's `reftarget` values to Pathfinder's symbolic selector syntax.

  grafana:<path>          whole reftarget
  grafana:<path>:<arg>    parameterized selector
  {grafana:<path>}        embedded inside a larger CSS expression

Usage:
  convert-reftargets.py <guide>/content.json --map selmap.json            # dry run (default)
  convert-reftargets.py <guide>/content.json --map selmap.json --write
  convert-reftargets.py ... --pin "data-testid prometheus type=components.DataSource.Prometheus.queryEditor.type"
  convert-reftargets.py ... --param "data-testid Duplicate query=components.QueryEditorRow.actionButton:Duplicate query"

Sources an exact `[data-testid='V']` or `[aria-label='V']` match, with or without the
`data-testid ` value prefix; `^=` / `*=` / `$=` are left alone. See the ATTR comment for why.

Edits raw text so the file's formatting is preserved, and asserts the parsed JSON is
structurally identical apart from reftargets.
"""
import argparse
import json
import re
import sys

# Nav menu items must stay literal: Pathfinder regex-matches this exact shape to auto-expand a
# collapsed menu section, and the resolved :is(...) form defeats that fix.
SKIP_VALUES = {'data-testid Nav menu item'}

# Matches an exact-match `[data-testid='<value>']` OR `[aria-label='<value>']`, with any value.
#
# Two deliberate widenings, both of which were blind spots:
#
# 1. Not only values carrying the `data-testid ` prefix. 105 of the 635 non-URL values in
#    @grafana/e2e-selectors have no prefix (`uplot-main-div`, `toggle-viz-picker` at 8.0.0,
#    `Explore Graph`, the TestData and time-range values). Whether a value is convertible is decided
#    by looking it up in the map, not by its spelling.
# 2. `aria-label`, not just `data-testid`. Unprefixed package values are the ones Grafana renders as
#    an `aria-label`, so that is where they show up in guides — and the resolver emits
#    `:is([data-testid=V], [aria-label=V])`, which covers both. A hand-written
#    `[data-testid='Explore Graph']` matches nothing at all; the reference matches.
#
# `^=` / `*=` / `$=` are deliberately excluded: a prefix match is an intentional pattern, not a
# snapshot of one resolved value, so there is nothing to reverse-map.
ATTR = re.compile(
    r"""(?P<tag>[a-zA-Z][\w-]*)?\[(?:data-testid|aria-label)=(?P<q>['"])(?P<val>[^'"]+)(?P=q)\]"""
)
REFTARGET = re.compile(r'("reftarget":\s*)"((?:[^"\\]|\\.)*)"')


class ReleaseGate:
    """
    Refuses to convert to a selector PATH that is not on the merged ref yet.

    Why paths and not resolved values: a parameterized selector's resolved value (e.g.
    `data-testid Panel header Graph`) never appears literally in the source, which is a template
    (`data-testid Panel header ${title}`). A substring check on the value therefore reports every
    function selector as missing. Comparing paths handles strings and functions alike.

    Why a gate is needed at all: version resolution cannot detect this. resolveSelectors falls back
    to the NEWEST version key when none is <= the target, so a 13.2.0-only selector still resolves
    to its 13.2.0 value when asked for 12.4.0.

    Feed this a second selector map built from a checkout at the merged ref (origin/main):

        git -C <grafana> worktree add /tmp/grafana-released origin/main
        GRAFANA_REPO=/tmp/grafana-released tsx build-selector-map.ts <min-version> > released.json

    MERGED IS NOT RELEASED. origin/main is a `-pre` version, so presence there only rules out
    "still on my branch". It does not prove the selector ships in any Grafana your guide runs
    against. Check the selector's version key against your minimum supported version by hand.

    This gate also only sees conversions the converter proposes — i.e. reftargets that already
    carry a literal data-testid. For the inverse case (a fragile aria-label/placeholder step whose
    replacement you just added), use find-unmerged-paths.py.
    """

    def __init__(self, merged_map_path):
        self.enabled = bool(merged_map_path)
        self.paths = set()
        if not self.enabled:
            return
        try:
            m = json.load(open(merged_map_path))
        except OSError as e:
            sys.exit(f'ABORT: could not read --merged-map: {e}')
        self.paths = set(m.get('strMap', {}).values())
        self.paths |= {f['path'] for f in m.get('fns', [])}
        self.paths |= set(m.get('greedyFns', []))
        self.paths |= set(m.get('undefinedProbes', []))
        for paths in m.get('ambiguous', {}).values():
            self.paths |= set(paths)

    def released(self, path):
        return (not self.enabled) or (path in self.paths)


def parse_kv(pairs, split_on='='):
    out = {}
    for p in pairs or []:
        if split_on not in p:
            sys.exit(f'--pin/--param expects key{split_on}value, got: {p}')
        k, v = p.split(split_on, 1)
        out[k] = v
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('guide')
    ap.add_argument('--map', required=True, help='output of build-selector-map.ts')
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--pin', action='append',
                    help='VALUE=PATH, to disambiguate a value with several paths')
    ap.add_argument('--param', action='append',
                    help='VALUE=PATH:ARG, for parameterized selectors too greedy to infer')
    ap.add_argument('--merged-map',
                    help='selector map built from a checkout at the merged ref (origin/main); omitting it '
                         'disables the release gate (NOT recommended)')
    args = ap.parse_args()

    gate = ReleaseGate(args.merged_map)
    if not gate.enabled:
        print('WARNING: release gate DISABLED — you may convert to selectors that do not exist '
              'in any shipped Grafana, which breaks the guide today.\n', file=sys.stderr)

    m = json.load(open(args.map))
    str_map = dict(m['strMap'])
    str_map.update(parse_kv(args.pin))

    param_overrides = {}
    for val, spec in parse_kv(args.param).items():
        # Split on the FIRST colon: a selector path never contains one, but an argument can
        # (e.g. a panel titled "Latency: p99").
        path, sep, arg = spec.partition(':')
        if not sep or not path:
            sys.exit(f'--param value must be PATH:ARG, got: {spec}')
        param_overrides[val] = (path, arg)

    fn_patterns = [
        (f['path'],
         re.compile('^' + re.escape(f['prefix']) + '(.+)' + re.escape(f['suffix']) + '$'))
        for f in m.get('fns', [])
    ]

    ambiguous = m.get('ambiguous', {})
    # 'pending' entries are (ref, would_become, path, ref_was_partially_converted). The last field
    # matters: a compound reftarget can have one part converted and another gated, in which case the
    # file WAS modified and reporting it as "left unchanged" would be false.
    report = {'bare': [], 'param': [], 'embedded': [], 'partial': [], 'unmapped': [],
              'untouched': [], 'warn': [], 'pending': []}

    def match_fn(val):
        if val in param_overrides:
            return param_overrides[val]
        for path, rx in fn_patterns:
            mo = rx.match(val)
            if mo:
                return path, mo.group(1)
        return None, None

    def note_ambiguity(val, chosen):
        if val in ambiguous and val not in str_map_pins:
            report['warn'].append(
                f'{val!r} maps to {sorted(set(ambiguous[val]))}; used {chosen!r} — pin it with --pin'
            )

    str_map_pins = set(parse_kv(args.pin))

    def convert(ref):
        if ref.startswith(('grafana:', 'panel:')) or '{grafana:' in ref:
            report['untouched'].append((ref, 'already symbolic'))
            return ref

        matches = list(ATTR.finditer(ref))
        if not matches:
            report['untouched'].append((ref, 'no exact data-testid/aria-label match'))
            return ref
        if any(mo.group('val') in SKIP_VALUES for mo in matches):
            report['untouched'].append((ref, 'nav menu: relies on Pathfinder auto-fix'))
            return ref

        # Whole reftarget is a single (optionally tag-qualified) data-testid selector.
        only = matches[0]
        if len(matches) == 1 and only.group(0) == ref:
            val = only.group('val')
            if val in str_map:
                if not gate.released(str_map[val]):
                    report['pending'].append((ref, f'grafana:{str_map[val]}', str_map[val], False))
                    return ref
                note_ambiguity(val, str_map[val])
                new = f'grafana:{str_map[val]}'
                report['bare'].append((ref, new))
                return new
            path, arg = match_fn(val)
            if path:
                if not gate.released(path):
                    report['pending'].append((ref, f'grafana:{path}:{arg}', path, False))
                    return ref
                new = f'grafana:{path}:{arg}'
                report['param'].append((ref, new))
                return new
            report['unmapped'].append(val)
            return ref

        # Scoped / compound: embed each mappable part as a {grafana:...} token. Parts are gated
        # individually, so some may convert while others stay literal.
        changed = False
        gated = []

        def repl(mo):
            nonlocal changed
            val, tag = mo.group('val'), (mo.group('tag') or '')
            if val in str_map:
                if not gate.released(str_map[val]):
                    gated.append((f'{{grafana:{str_map[val]}}}', str_map[val]))
                    return mo.group(0)
                note_ambiguity(val, str_map[val])
                changed = True
                return f'{tag}{{grafana:{str_map[val]}}}'
            path, arg = match_fn(val)
            if path:
                if not gate.released(path):
                    gated.append((f'{{grafana:{path}:{arg}}}', path))
                    return mo.group(0)
                changed = True
                return f'{tag}{{grafana:{path}:{arg}}}'
            report['unmapped'].append(val)
            return mo.group(0)

        new = ATTR.sub(repl, ref)
        for target, path in gated:
            report['pending'].append((ref, target, path, changed))
        if changed:
            report['partial' if gated else 'embedded'].append((ref, new))
            return new
        if not gated:
            report['untouched'].append((ref, 'no mappable attributes'))
        return ref

    raw = open(args.guide).read()

    def sub(mo):
        old = json.loads('"' + mo.group(2) + '"')
        return f'{mo.group(1)}"{json.dumps(convert(old), ensure_ascii=False)[1:-1]}"'

    new_raw = REFTARGET.sub(sub, raw)

    # Structural guard: nothing but reftargets may change.
    def strip_refs(n):
        if isinstance(n, dict):
            return {k: ('<REF>' if k == 'reftarget' else strip_refs(v)) for k, v in n.items()}
        if isinstance(n, list):
            return [strip_refs(v) for v in n]
        return n

    if strip_refs(json.loads(raw)) != strip_refs(json.loads(new_raw)):
        sys.exit('ABORT: structure changed beyond reftargets')

    if args.write:
        open(args.guide, 'w').write(new_raw)

    for title, key in [('BARE -> grafana:<path>', 'bare'),
                       ('PARAMETERIZED -> grafana:<path>:<arg>', 'param'),
                       ('EMBEDDED -> {grafana:<path>}', 'embedded'),
                       ('PARTIALLY CONVERTED — some parts gated, see PENDING', 'partial')]:
        print(f'\n=== {title} ===')
        for a, b in report[key]:
            print(f'  {a}\n    -> {b}')

    if report['pending']:
        print('\n=== PENDING RELEASE — not converted (path absent from --merged-map) ===')
        print('   Record these in the guide PR; swap them once the selector ships.')
        for label, partial in [('reftarget left entirely unchanged', False),
                               ('reftarget WAS rewritten; only this part left literal', True)]:
            rows = [r for r in report['pending'] if r[3] is partial]
            if rows:
                print(f'   -- {label}:')
                for ref, target, path, _ in rows:
                    print(f'  {ref}\n    would become: {target}   [{path}]')

    print('\n=== UNMAPPED (no package selector) ===')
    for v in sorted(set(report['unmapped'])):
        print(f'  {v}')
    print('\n=== UNTOUCHED ===')
    for a, why in report['untouched']:
        print(f'  [{why}] {a}')
    if report['warn']:
        print('\n=== WARNINGS ===')
        for w in report['warn']:
            print(f'  {w}')

    pending_refs = {r[0] for r in report['pending']}
    print(f"\nreftargets: bare={len(report['bare'])} param={len(report['param'])} "
          f"embedded={len(report['embedded'])} partial={len(report['partial'])} "
          f"untouched={len(report['untouched'])}")
    print(f"values: unmapped={len(set(report['unmapped']))}")
    print(f"pending: {len(report['pending'])} path(s) across {len(pending_refs)} reftarget(s)"
          f"{'  (dry run — pass --write to apply)' if not args.write else ''}")


if __name__ == '__main__':
    main()
