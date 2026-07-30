#!/usr/bin/env python3
"""
List selector paths that exist in your working tree but NOT at the merged ref.

Why this exists, and why the converter's gate is not enough:

    convert-reftargets.py can only gate conversions it actually proposes, and it only proposes
    conversions for reftargets that already contain a literal `data-testid`. The dangerous case is
    the opposite one — a step still on a fragile `aria-label` / `placeholder` / text selector whose
    replacement you just added on a branch. The converter never touches that step, so it lands in
    UNTOUCHED and the gate reports `pending=0`. Nothing warns you.

    This script closes that hole: it names exactly the selectors that are yours-and-unmerged, so
    you can check them against the UNTOUCHED list and resist adopting them.

Usage:
  find-unmerged-paths.py --map selmap.json --merged-map merged.json [--guide <guide>/content.json]

With --guide, also warns if any of those paths are already referenced by the guide.
Exit code 1 when unmerged paths exist, so it can gate a pipeline.
"""
import argparse
import json
import re
import sys


def paths_of(map_path):
    m = json.load(open(map_path))
    out = set(m.get('strMap', {}).values())
    out |= {f['path'] for f in m.get('fns', [])}
    out |= set(m.get('greedyFns', []))
    for ps in m.get('ambiguous', {}).values():
        out |= set(ps)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--map', required=True, help='selector map from your working tree')
    ap.add_argument('--merged-map', required=True, help='selector map built at the merged ref')
    ap.add_argument('--guide', help='also check whether the guide already references these')
    args = ap.parse_args()

    unmerged = sorted(paths_of(args.map) - paths_of(args.merged_map))

    if not unmerged:
        print('No unmerged selector paths — your working tree matches the merged ref.')
        return 0

    print(f'{len(unmerged)} selector path(s) exist locally but are NOT merged:\n')
    for p in unmerged:
        print(f'  {p}')

    print('\nDo NOT convert guide steps onto these — they resolve to nothing on any instance the')
    print('guide runs against today. Leave those steps as they are and record them as pending.')

    if args.guide:
        raw = open(args.guide).read()
        referenced = [p for p in unmerged if re.search(r'grafana:' + re.escape(p) + r'\b', raw)]
        if referenced:
            print('\n!!! The guide ALREADY references these unmerged paths — revert them:')
            for p in referenced:
                print(f'  {p}')
            return 2

    return 1


if __name__ == '__main__':
    sys.exit(main())
