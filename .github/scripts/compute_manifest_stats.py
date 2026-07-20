#!/usr/bin/env python3
"""
Manifest rollup-stats computation for the GitHub Actions build pipeline.

SPIKE (RFC grafana/pathfinder-rfcs#14 — "Step-level progression tracking for
learning paths"). Computes per-guide content statistics and embeds them into
each package manifest.json as a `stats` object, then rolls those stats up onto
each learning path / journey manifest. Runs on the *staged* package tree just
before the pathfinder-app CLI's `build-repository` step.

Ordering: every `guide` manifest is measured first, building an id -> stats
map, and only then are `path`/`journey` manifests rolled up from that map.
This guarantees a path's milestone stats are available before its rollup.

Output shape
------------
guide manifest:
    "stats": { "version": 1, "steps": N, "blocks": N, "sections": N }

path / journey manifest (sums over its `milestones`, keyed by milestone id):
    "stats": {
      "version": 1,
      "guides": N,            # number of milestones listed on the path
      "steps": N,             # sum of milestone steps
      "blocks": N,            # sum of milestone blocks
      "sections": N,          # sum of milestone sections
      "perMilestone": {       # keyed by milestone *id*, not position
        "<milestone-id>": { "steps": N, "blocks": N, "sections": N },
        ...
      }
    }

Counting semantics
------------------
`steps` is an exact port of the authoritative runtime helper
`count-guide-steps.ts` (grafana-pathfinder-app, branch feat/journey-step-weights,
src/docs-retrieval/count-guide-steps.ts; originally requested as
backup/1370-step-weights, which has since been renamed). A block counts as one
step iff its `type` is in STEP_COUNTING_BLOCK_TYPES. The traversal recurses
ONLY into `section` blocks. Consequently, and matching the runtime:
  * `conditional` branches (whenTrue/whenFalse) count 0 — not recursed.
  * `snippet-ref` counts 0 — unresolved, not a step type.
  * an `assistantEnabled` step *inside a section* counts 0 (the render wrapper
    hides it from section extraction); the same step at top level counts 1.
  * `multistep` / `guided` count 1 each regardless of their inner `steps` array.

DOCUMENTED APPROXIMATIONS (acceptable for this spike; see PR body):
  1. `blocks` and `sections` use a DIFFERENT, fuller traversal than `steps`:
     they descend through every array that holds content blocks — `blocks`
     (sections) AND `conditional` branches `whenTrue` / `whenFalse`. This is a
     deliberate choice: `steps` mirrors the runtime exactly, while `blocks`/
     `sections` describe total authored content (so conditional content is not
     invisible). It means a section or step nested inside a conditional is
     included in `blocks`/`sections` but NOT in `steps`. `multistep`/`guided`
     inner `steps` are action descriptors, not content blocks, so they are
     never counted as blocks (each such block counts as exactly one block).
  2. `blocks` counts EVERY block node, container blocks included: a `section`
     or `conditional` counts as one block in addition to its descendants.
  3. `sections` counts every block whose `type` is `section`, anywhere in the
     tree (nested sections included), via the same fuller traversal as (1).
  4. Rollup linkage is by milestone `id` (a guide manifest whose `id` equals
     the milestone string), NOT by directory name or position. A milestone that
     resolves to no measured guide is skipped from `perMilestone` and the sums,
     and a warning is emitted; `guides` still reflects the full milestone count.
  5. A path/journey's own sibling content.json (if any) is NOT counted — a path
     is defined purely as the rollup of its milestones.

Determinism: `stats` is written with a fixed key order and no timestamps.
Re-running on unchanged content is a byte-for-byte no-op: an existing `stats`
member is excised (JSON-structure-aware) and re-inserted identically, and all
other bytes of the manifest are preserved exactly (no whole-file reformat).

Usage:
    python3 compute_manifest_stats.py <package-root> [--exclude DIR ...] [--check]

    <package-root>  Directory to scan for package manifest.json files.
    --exclude DIR   Additional top-level directory name to skip (repeatable).
    --check         Do not write; exit non-zero if any manifest would change.
"""

import argparse
import json
import os
import sys

# Authoritative step-counting block types. Mirrors STEP_COUNTING_BLOCK_TYPES in
# grafana-pathfinder-app src/types/json-guide.types.ts (feat/journey-step-weights).
STEP_COUNTING_BLOCK_TYPES = frozenset({
    'interactive',
    'multistep',
    'guided',
    'quiz',
    'terminal',
    'terminal-connect',
    'challenge',
    'code-block',
})

# Directory names never treated as packages (mirrors the deploy.yml EXCLUDE set
# plus VCS/editor/dependency dirs). Pruned at every depth during the walk.
DEFAULT_EXCLUDES = frozenset({
    '.git',
    '.github',
    '.cursor',
    'docs',
    'shared',
    'courses',
    'pathfinder-app',
    'packages',
    'guides',
    'kiosk',
    'node_modules',
})

STATS_VERSION = 1


def count_steps(blocks, in_section=False):
    """Exact port of count-guide-steps.ts: section-only recursion, membership
    in STEP_COUNTING_BLOCK_TYPES, assistant-in-section counts 0."""
    total = 0
    for block in blocks:
        if not isinstance(block, dict):
            continue
        btype = block.get('type')
        if btype == 'section':
            total += count_steps(block.get('blocks', []), True)
            continue
        if btype not in STEP_COUNTING_BLOCK_TYPES:
            continue
        assistant_wrapped = block.get('assistantEnabled') is True
        total += 0 if (in_section and assistant_wrapped) else 1
    return total


def count_blocks_and_sections(blocks):
    """Fuller traversal for `blocks` and `sections` totals. Descends through
    every content-block-bearing array (section `blocks`, conditional
    `whenTrue`/`whenFalse`). Container blocks are themselves counted."""
    n_blocks = 0
    n_sections = 0
    for block in blocks:
        if not isinstance(block, dict):
            continue
        n_blocks += 1
        btype = block.get('type')
        if btype == 'section':
            n_sections += 1
        for child_key in ('blocks', 'whenTrue', 'whenFalse'):
            child = block.get(child_key)
            if isinstance(child, list):
                cb, cs = count_blocks_and_sections(child)
                n_blocks += cb
                n_sections += cs
    return n_blocks, n_sections


def compute_guide_stats(content):
    """Compute the stats object for a single guide from its content.json data."""
    blocks = content.get('blocks', []) if isinstance(content, dict) else []
    if not isinstance(blocks, list):
        blocks = []
    steps = count_steps(blocks)
    n_blocks, n_sections = count_blocks_and_sections(blocks)
    return {
        'version': STATS_VERSION,
        'steps': steps,
        'blocks': n_blocks,
        'sections': n_sections,
    }


def build_path_stats(milestones, guide_stats_by_id, manifest_path):
    """Roll up a path/journey's milestone stats. Linkage is by milestone id."""
    per_milestone = {}
    total_steps = total_blocks = total_sections = 0
    for milestone_id in milestones:
        gs = guide_stats_by_id.get(milestone_id)
        if gs is None:
            sys.stderr.write(
                f"⚠️  {manifest_path}: milestone '{milestone_id}' has no "
                f"measured guide manifest; skipped from rollup\n"
            )
            continue
        per_milestone[milestone_id] = {
            'steps': gs['steps'],
            'blocks': gs['blocks'],
            'sections': gs['sections'],
        }
        total_steps += gs['steps']
        total_blocks += gs['blocks']
        total_sections += gs['sections']
    return {
        'version': STATS_VERSION,
        'guides': len(milestones),
        'steps': total_steps,
        'blocks': total_blocks,
        'sections': total_sections,
        'perMilestone': per_milestone,
    }


def _find_top_level_key_span(text, key):
    """Return (start, end) byte span of a top-level `"key": <value>` member in a
    JSON object string, value included, or None. String/escape aware; assumes a
    single top-level object (true for manifest.json)."""
    target = f'"{key}"'
    i = 0
    depth = 0
    in_string = False
    escape = False
    n = len(text)
    while i < n:
        ch = text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == '\\':
                escape = True
            elif ch == '"':
                in_string = False
            i += 1
            continue
        if ch == '"':
            # Candidate key only at object depth 1.
            if depth == 1 and text[i:i + len(target)] == target:
                key_start = i
                j = i + len(target)
                # skip whitespace then ':'
                while j < n and text[j] in ' \t\r\n':
                    j += 1
                if j < n and text[j] == ':':
                    j += 1
                    while j < n and text[j] in ' \t\r\n':
                        j += 1
                    value_end = _scan_value_end(text, j)
                    return key_start, value_end
            # not our key: skip this string
            in_string = True
            i += 1
            continue
        if ch in '{[':
            depth += 1
        elif ch in '}]':
            depth -= 1
        i += 1
    return None


def _scan_value_end(text, start):
    """Return index just past the JSON value beginning at `start`."""
    ch = text[start]
    if ch in '{[':
        depth = 0
        in_string = False
        escape = False
        i = start
        n = len(text)
        while i < n:
            c = text[i]
            if in_string:
                if escape:
                    escape = False
                elif c == '\\':
                    escape = True
                elif c == '"':
                    in_string = False
            elif c == '"':
                in_string = True
            elif c in '{[':
                depth += 1
            elif c in '}]':
                depth -= 1
                if depth == 0:
                    return i + 1
            i += 1
        return n
    # scalar: string, number, true/false/null — read until , or } or ] at depth 0
    if ch == '"':
        i = start + 1
        escape = False
        n = len(text)
        while i < n:
            c = text[i]
            if escape:
                escape = False
            elif c == '\\':
                escape = True
            elif c == '"':
                return i + 1
            i += 1
        return n
    i = start
    n = len(text)
    while i < n and text[i] not in ',}]':
        i += 1
    return i


def _excise_stats(text):
    """Remove an existing top-level `stats` member (and one adjacent comma),
    returning text as if stats had never been inserted. Idempotent inverse of
    the insertion below."""
    span = _find_top_level_key_span(text, 'stats')
    if span is None:
        return text
    start, end = span
    # Absorb a preceding comma (our insertion form: `<prev>,\n  "stats": ...`).
    pre = start
    k = start - 1
    while k >= 0 and text[k] in ' \t\r\n':
        k -= 1
    if k >= 0 and text[k] == ',':
        pre = k
    else:
        # No leading comma (stats was first/only member): absorb a trailing comma.
        m = end
        while m < len(text) and text[m] in ' \t\r\n':
            m += 1
        if m < len(text) and text[m] == ',':
            end = m + 1
    return text[:pre] + text[end:]


def _format_stats_member(stats):
    """Serialize the stats member at object indent level 1 (2-space base)."""
    body = json.dumps(stats, indent=2, ensure_ascii=False)
    indented = '\n'.join(
        ('  ' + line) if line else line for line in body.split('\n')
    )
    return '  "stats": ' + indented.lstrip()


def render_manifest_with_stats(text, stats):
    """Return manifest text with `stats` as the last member, preserving all
    other formatting. Deterministic and idempotent."""
    base = _excise_stats(text)
    trailing = base[len(base.rstrip()):]  # usually "\n"
    stripped = base.rstrip()
    if not stripped.endswith('}'):
        raise ValueError('manifest does not end with a closing object brace')
    inner = stripped[:-1].rstrip()
    member = _format_stats_member(stats)
    # Guard the (non-existent for manifests) empty-object case.
    sep = ',\n' if not inner.endswith('{') else '\n'
    return inner + sep + member + '\n}' + (trailing or '\n')


def discover_manifests(root, excludes):
    """Yield manifest.json paths under root, pruning excluded directory names."""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in excludes)
        if 'manifest.json' in filenames:
            yield os.path.join(dirpath, 'manifest.json')


def main():
    parser = argparse.ArgumentParser(
        description='Compute and embed rollup stats into package manifest.json files.'
    )
    parser.add_argument('root', help='Directory to scan for package manifests')
    parser.add_argument(
        '--exclude', action='append', default=[],
        help='Additional top-level directory name to skip (repeatable)',
    )
    parser.add_argument(
        '--check', action='store_true',
        help='Do not write; exit non-zero if any manifest would change',
    )
    args = parser.parse_args()

    if not os.path.isdir(args.root):
        print(f'❌ Error: {args.root} is not a directory')
        sys.exit(1)

    excludes = DEFAULT_EXCLUDES | set(args.exclude)

    # Load every manifest once, classify, and cache raw text.
    manifests = []  # list of (path, data, raw_text)
    for path in discover_manifests(args.root, excludes):
        try:
            with open(path, encoding='utf-8') as f:
                raw = f.read()
            data = json.loads(raw)
        except (OSError, json.JSONDecodeError) as exc:
            print(f'❌ Error reading {path}: {exc}')
            sys.exit(1)
        manifests.append((path, data, raw))

    # ---- Phase 1: measure every guide, keyed by manifest id. ----
    guide_stats_by_id = {}
    guide_stats_by_path = {}
    for path, data, _raw in manifests:
        if data.get('type') != 'guide':
            continue
        content_path = os.path.join(os.path.dirname(path), 'content.json')
        if not os.path.isfile(content_path):
            # A guide with no content.json cannot be measured; record zeros.
            stats = {'version': STATS_VERSION, 'steps': 0, 'blocks': 0, 'sections': 0}
            sys.stderr.write(f"⚠️  {path}: no sibling content.json; stats are zero\n")
        else:
            try:
                with open(content_path, encoding='utf-8') as f:
                    content = json.load(f)
            except (OSError, json.JSONDecodeError) as exc:
                print(f'❌ Error reading {content_path}: {exc}')
                sys.exit(1)
            stats = compute_guide_stats(content)
        guide_stats_by_path[path] = stats
        manifest_id = data.get('id')
        if manifest_id:
            guide_stats_by_id[manifest_id] = stats

    # ---- Phase 2: roll up paths / journeys from the guide map. ----
    path_stats_by_path = {}
    for path, data, _raw in manifests:
        if data.get('type') not in ('path', 'journey'):
            continue
        milestones = data.get('milestones', [])
        if not isinstance(milestones, list):
            milestones = []
        path_stats_by_path[path] = build_path_stats(
            milestones, guide_stats_by_id, path
        )

    # ---- Write phase (deterministic, idempotent). ----
    changed = 0
    guides_n = paths_n = 0
    for path, data, raw in manifests:
        if path in guide_stats_by_path:
            stats = guide_stats_by_path[path]
            guides_n += 1
        elif path in path_stats_by_path:
            stats = path_stats_by_path[path]
            paths_n += 1
        else:
            continue  # not a package type we compute stats for
        new_text = render_manifest_with_stats(raw, stats)
        if new_text != raw:
            changed += 1
            if not args.check:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_text)

    print(f'📊 Manifests processed: {len(manifests)} '
          f'({guides_n} guides, {paths_n} paths/journeys)')
    if args.check:
        if changed:
            print(f'❌ {changed} manifest(s) would change (stale stats)')
            sys.exit(1)
        print('✅ All manifest stats are up to date')
        sys.exit(0)
    print(f'✅ Updated {changed} manifest(s); '
          f'{len(manifests) - changed} already current')
    sys.exit(0)


if __name__ == '__main__':
    main()
