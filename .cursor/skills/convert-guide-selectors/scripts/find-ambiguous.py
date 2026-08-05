#!/usr/bin/env python3
"""
List every resolved selector value a guide references that maps to MORE THAN ONE path.

Those values are ambiguous: a value -> path lookup returns whichever path was walked first, which
may be semantically wrong for the step (e.g. `data-testid prometheus type` is both the config
page's Prometheus type dropdown and the query editor's Range/Instant/Both group).

Usage:
  find-ambiguous.py <guide>/content.json --map selmap.json

Pin each reported value with convert-reftargets.py --pin "VALUE=PATH".
"""
import argparse
import json
import re
import sys

# Any exact-match data-testid OR aria-label value, prefixed or not. Kept in step with
# convert-reftargets.py's ATTR so both scripts see the same set of reftargets — see the comment
# there for why both attributes and both spellings matter.
VALUE = re.compile(r"""\[(?:data-testid|aria-label)=['"]([^'"]+)['"]\]""")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('guide')
    ap.add_argument('--map', required=True, help='output of build-selector-map.ts')
    args = ap.parse_args()

    used = set(VALUE.findall(open(args.guide).read()))
    ambiguous = json.load(open(args.map)).get('ambiguous', {})

    hits = {v: sorted(set(ambiguous[v])) for v in sorted(used) if v in ambiguous}
    if not hits:
        print(f'No ambiguous values among the {len(used)} referenced by this guide.')
        return 0

    print(f'{len(hits)} ambiguous value(s) — pin each one explicitly:\n')
    for val, paths in hits.items():
        print(f'  {val!r}')
        for p in paths:
            print(f'      {p}')
        print(f'      --pin "{val}=<chosen path>"\n')
    # Non-zero so this can gate a pipeline until the values are pinned.
    return 1


if __name__ == '__main__':
    sys.exit(main())
