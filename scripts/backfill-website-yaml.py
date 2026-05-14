#!/usr/bin/env python3
"""Backfill website.yaml files in interactive-tutorials -lj directories from website markdown.

Writes two kinds of file:
  <lj-dir>/website.yaml            complete static frontmatter for the path cover page
  <lj-dir>/<milestone>/website.yaml  complete static frontmatter for each milestone page

Each file is designed to be concatenated verbatim into Hugo frontmatter; the build
script appends only the three derived fields (title, description, pathfinder_data).
"""

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML is required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


def usage():
    """Print usage information to stdout."""
    print("""\
Backfill website.yaml files in interactive-tutorials -lj directories from website markdown.

Usage:
  backfill-website-yaml.py [--force] <INTERACTIVE_TUTORIALS_PATH> <WEBSITE_PATH>

Arguments:
  INTERACTIVE_TUTORIALS_PATH  Path to the grafana/interactive-tutorials repository
  WEBSITE_PATH                Path to the grafana/website repository

Options:
  --force  Overwrite existing website.yaml files

Examples:
  backfill-website-yaml.py ../interactive-tutorials ../website
  backfill-website-yaml.py --force /path/to/interactive-tutorials /path/to/website\
""")


def parse_frontmatter(text):
    """Return parsed YAML frontmatter from a markdown string, or an empty dict."""
    match = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}


def read_frontmatter(path):
    """Return parsed frontmatter from a markdown file, or an empty dict on any error."""
    try:
        return parse_frontmatter(path.read_text(encoding='utf-8'))
    except OSError:
        return {}


def read_json(path):
    """Return parsed JSON from a file, or an empty dict on any error."""
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError):
        return {}


def write_yaml(path, data, force):
    """Write data as YAML to path, skipping if the file exists and force is false."""
    if path.exists() and not force:
        return False
    with path.open('w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    return True


def build_path_frontmatter(index_fm, manifest):
    """Return the complete static frontmatter dict for a learning-path cover page."""
    data = {}

    if 'menuTitle' in index_fm:
        data['menuTitle'] = index_fm['menuTitle']

    if 'weight' in index_fm:
        data['weight'] = index_fm['weight']

    wy_journey = index_fm.get('journey') or {}
    journey = {
        'group': manifest.get('category', 'general'),
        'skill': wy_journey.get('skill', 'Beginner'),
        'source': 'Docs & blog posts',
    }
    if 'logo' in wy_journey:
        journey['logo'] = dict(wy_journey['logo'])
    data['journey'] = journey

    data['step'] = 1
    data['layout'] = 'single-journey'
    data['cascade'] = {'layout': 'single-journey'}
    data['cta'] = {'type': 'start', 'title': 'Are you ready?', 'cta_text': "Let's go!"}

    if 'keywords' in index_fm:
        data['keywords'] = list(index_fm['keywords'])

    related = index_fm.get('related_journeys') or {}
    if related.get('items'):
        data['related_journeys'] = {
            'title': related.get('title', 'Related journeys'),
            'heading': related.get('heading', 'Consider taking the following journeys before you start this journey.'),
            'items': [
                {'title': i['title'], 'link': i['link']}
                for i in related['items']
                if 'title' in i and 'link' in i
            ],
        }

    return data


def build_milestone_frontmatter(milestone_fm):
    """Return the complete static frontmatter dict for a milestone page."""
    data = {}

    if 'menuTitle' in milestone_fm:
        data['menuTitle'] = milestone_fm['menuTitle']

    if 'weight' in milestone_fm:
        data['weight'] = milestone_fm['weight']

    if 'step' in milestone_fm:
        data['step'] = milestone_fm['step']

    data['layout'] = 'single-journey'

    cta_type = (milestone_fm.get('cta') or {}).get('type') or 'continue'
    data['cta'] = {'type': cta_type}

    if 'keywords' in milestone_fm:
        data['keywords'] = list(milestone_fm['keywords'])

    side = milestone_fm.get('side_journeys') or {}
    if side.get('items'):
        data['side_journeys'] = {
            'title': side.get('title', 'More to explore (optional)'),
            'heading': side.get('heading', 'At this point in your journey, you can explore the following paths:'),
            'items': [
                {'title': i['title'], 'link': i['link']}
                for i in side['items']
                if 'title' in i and 'link' in i
            ],
        }

    return data


def find_milestone_md(website_lp_dir, lj_name, milestone_name):
    """Return the frontmatter for a milestone by matching pathfinder_data or directory name."""
    for website_subdir in website_lp_dir.iterdir():
        if not website_subdir.is_dir():
            continue
        for fname in ('index.md', '_index.md'):
            md = website_subdir / fname
            if not md.exists():
                continue
            fm = read_frontmatter(md)
            pd = fm.get('pathfinder_data', '')
            if pd == f"{lj_name}/{milestone_name}":
                return fm
            if not pd and website_subdir.name == milestone_name:
                return fm
    return {}


def main():
    """Entry point."""
    args = sys.argv[1:]
    force = '--force' in args
    args = [a for a in args if a != '--force']

    if len(args) == 1 and args[0] in ('-h', '--help'):
        usage()
        sys.exit(0)

    if len(args) != 2:
        usage()
        sys.exit(2)

    it_root = Path(args[0]).resolve()
    website_root = Path(args[1]).resolve()

    for path, label in ((it_root, 'INTERACTIVE_TUTORIALS_PATH'), (website_root, 'WEBSITE_PATH')):
        if not path.is_dir():
            print(f"error: {label} {path} is not a directory", file=sys.stderr)
            sys.exit(1)

    learning_paths_dir = website_root / 'content' / 'docs' / 'learning-paths'
    lj_dirs = sorted(d for d in it_root.iterdir() if d.is_dir() and d.name.endswith('-lj'))

    written = skipped = 0

    for lj_dir in lj_dirs:
        slug = lj_dir.name[:-3]
        website_lp_dir = learning_paths_dir / slug

        if not website_lp_dir.is_dir():
            print(f"skip  {lj_dir.name}: no counterpart at learning-paths/{slug}/")
            skipped += 1
            continue

        index_md = website_lp_dir / '_index.md'
        if not index_md.exists():
            print(f"skip  {lj_dir.name}: no _index.md in learning-paths/{slug}/")
            skipped += 1
            continue

        manifest = read_json(lj_dir / 'manifest.json')
        index_fm = read_frontmatter(index_md)
        path_data = build_path_frontmatter(index_fm, manifest)

        if not path_data:
            print(f"skip  {lj_dir.name}: no usable frontmatter in learning-paths/{slug}/_index.md")
            skipped += 1
            continue

        if write_yaml(lj_dir / 'website.yaml', path_data, force):
            written += 1
            print(f"wrote {lj_dir.name}/website.yaml")
        else:
            skipped += 1
            print(f"skip  {lj_dir.name}/website.yaml: exists (use --force to overwrite)")

        for milestone_dir in sorted(d for d in lj_dir.iterdir() if d.is_dir()):
            if not (milestone_dir / 'content.json').exists():
                continue

            milestone_fm = find_milestone_md(website_lp_dir, lj_dir.name, milestone_dir.name)
            if not milestone_fm:
                continue

            milestone_data = build_milestone_frontmatter(milestone_fm)
            if not milestone_data:
                continue

            rel = f"{lj_dir.name}/{milestone_dir.name}/website.yaml"
            if write_yaml(milestone_dir / 'website.yaml', milestone_data, force):
                written += 1
                print(f"wrote {rel}")
            else:
                skipped += 1
                print(f"skip  {rel}: exists (use --force to overwrite)")

    print(f"\n{written} written, {skipped} skipped")


if __name__ == '__main__':
    main()