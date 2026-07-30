#!/usr/bin/env python3
"""
Hermetic regression tests for convert-reftargets.py and find-ambiguous.py.

No grafana/grafana checkout, no tsx, no network — selector maps are hand-written fixtures, which is
the whole point: every case below reproduces from a few lines of JSON.

  python3 .cursor/skills/convert-guide-selectors/tests/test-convert-reftargets.py
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / 'scripts'
CONVERT = SCRIPTS / 'convert-reftargets.py'
AMBIGUOUS = SCRIPTS / 'find-ambiguous.py'

MAP = {
    'version': '13.2.0',
    'minSignificant': 3,
    'strMap': {
        'data-testid Query editor row': 'components.QueryEditorRows.rows',
        'uplot-main-div': 'components.UPlotChart.container',
        'toggle-viz-picker': 'components.PanelEditor.toggleVizPicker',
        'Explore Graph': 'pages.Explore.General.graph',
        'data-testid Nav menu item': 'components.NavMenu.item',
        'data-testid Panel header CPU': 'components.Panels.Panel.headerCPU',
        'data-testid Brand new sel': 'components.MyBrandNew.thing',
        'data-testid prometheus type': 'components.DataSource.Prometheus.configPage.type',
    },
    'ambiguous': {
        'data-testid prometheus type': [
            'components.DataSource.Prometheus.configPage.type',
            'components.DataSource.Prometheus.queryEditor.type',
        ],
    },
    'fns': [{'path': 'components.Panels.Panel.title', 'prefix': 'data-testid Panel header ',
             'suffix': '', 'significant': 14}],
    'greedyFns': ['components.QueryEditorRow.actionButton'],
}

# Everything except the two selectors that are meant to look unreleased.
MERGED = {
    'strMap': {k: v for k, v in MAP['strMap'].items()
               if k not in ('data-testid Brand new sel',)},
    'ambiguous': MAP['ambiguous'],
    'fns': MAP['fns'],
    'greedyFns': MAP['greedyFns'],
}

failures = []


def run(refs, *extra, gated=True, guide=None, write=False):
    """Convert a guide made of `refs` and return (exit_code, stdout, resulting_file_text)."""
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / 'map.json').write_text(json.dumps(MAP))
        (d / 'merged.json').write_text(json.dumps(MERGED))
        content = guide if guide is not None else json.dumps(
            {'blocks': [{'type': 'interactive', 'reftarget': r} for r in refs]}, indent=2)
        (d / 'content.json').write_text(content)

        cmd = [sys.executable, str(CONVERT), str(d / 'content.json'), '--map', str(d / 'map.json')]
        if gated:
            cmd += ['--merged-map', str(d / 'merged.json')]
        if write:
            cmd.append('--write')
        cmd += list(extra)
        p = subprocess.run(cmd, capture_output=True, text=True)
        return p.returncode, p.stdout + p.stderr, (d / 'content.json').read_text()


def check(name, cond, detail=''):
    if cond:
        print(f'  ok    {name}')
    else:
        print(f'  FAIL  {name}{"  " + detail if detail else ""}')
        failures.append(name)


def section(title):
    print(f'\n== {title} ==')


section('values without the `data-testid ` prefix are still conversions')
code, out, _ = run(["div[data-testid='uplot-main-div']"])
check('bare non-prefixed value converts',
      'grafana:components.UPlotChart.container' in out, out)
check('non-prefixed value is not reported as "no data-testid attribute"',
      'no data-testid attribute' not in out, out)

code, out, _ = run(['div[data-testid="uplot-main-div"]:nth-match(3)'])
check('non-prefixed value inside a compound converts',
      '{grafana:components.UPlotChart.container}' in out and ':nth-match(3)' in out,
      out)

code, out, _ = run(["button[data-testid='toggle-viz-picker']"])
check('8.0.0-era unprefixed value converts',
      'grafana:components.PanelEditor.toggleVizPicker' in out, out)

section('aria-label is a conversion source too')
# Unprefixed package values are what Grafana renders as an aria-label, so that is where they appear
# in guides. The resolved :is(...) covers both attributes.
code, out, _ = run(["div[aria-label='Explore Graph']"])
check('bare aria-label value converts',
      'grafana:pages.Explore.General.graph' in out, out)
code, out, _ = run(["div[aria-label='Explore Graph'] button[data-testid='toggle-viz-picker']"])
check('mixed aria-label + data-testid compound converts',
      '{grafana:pages.Explore.General.graph}' in out
      and '{grafana:components.PanelEditor.toggleVizPicker}' in out, out)

section('prefix-match selectors are left alone')
code, out, _ = run(["div[data-testid^='data-testid Panel header ']"])
check('^= is not treated as a resolved value',
      'no exact data-testid/aria-label match' in out, out)
code, out, _ = run(["div[aria-label*='section: Alerts']"])
check('*= aria-label is not treated as a resolved value',
      'no exact data-testid/aria-label match' in out, out)

section('nav menu stays literal (trap 1)')
code, out, res = run(["a[data-testid='data-testid Nav menu item'][href='/explore']"], write=True)
check('nav item untouched', 'relies on Pathfinder auto-fix' in out, out)
check('nav item unchanged on disk', "[href='/explore']" in res and 'grafana:' not in res, res)

section('release gate: fully gated compound')
ref = ("section[data-testid='data-testid Brand new sel']"
       " button[data-testid='data-testid Brand new sel']")
code, out, res = run([ref], write=True)
check('reported as pending', 'PENDING RELEASE' in out, out)
check('reported as entirely unchanged', 'reftarget left entirely unchanged' in out, out)
check('NOT mislabelled "no mappable attributes"', 'no mappable attributes' not in out, out)
check('file untouched', 'grafana:' not in res, res)

section('release gate: partially gated compound')
ref = ("section[data-testid='data-testid Panel header CPU']"
       " button[data-testid='data-testid Brand new sel']")
code, out, res = run([ref], write=True)
check('shown under PARTIALLY CONVERTED', 'PARTIALLY CONVERTED' in out, out)
check('pending row says the reftarget WAS rewritten',
      'reftarget WAS rewritten' in out, out)
check('does NOT claim "left entirely unchanged"',
      'reftarget left entirely unchanged' not in out, out)
check('released part converted on disk',
      '{grafana:components.Panels.Panel.headerCPU}' in res, res)
check('gated part still literal on disk',
      "data-testid Brand new sel" in res, res)

section('count units are explicit')
check('summary separates reftargets from paths',
      'pending: 1 path(s) across 1 reftarget(s)' in out, out)

section('ambiguity')
code, out, _ = run(["div[data-testid='data-testid prometheus type']"])
check('ambiguous value warns', 'pin it with --pin' in out, out)
code, out, _ = run(
    ["div[data-testid='data-testid prometheus type']"],
    '--pin', 'data-testid prometheus type=components.DataSource.Prometheus.queryEditor.type')
check('--pin silences the warning and wins',
      'pin it with --pin' not in out
      and 'grafana:components.DataSource.Prometheus.queryEditor.type' in out, out)

section('--param splits on the first colon, like the plugin')
code, out, _ = run(
    ["div[data-testid='data-testid Latency: p99']"],
    '--param', 'data-testid Latency: p99=components.Panels.Panel.title:Latency: p99')
check('argument may contain a colon',
      'grafana:components.Panels.Panel.title:Latency: p99' in out, out)

section('parameterized reverse-match')
code, out, _ = run(["section[data-testid='data-testid Panel header Requests']"])
check('fn probe reverse-matches',
      'grafana:components.Panels.Panel.title:Requests' in out, out)

section('idempotence')
code, out, res = run(['grafana:components.QueryEditorRows.rows',
                      'div{grafana:components.Panels.Panel.headerCPU} button'], write=True)
check('already-symbolic left alone', out.count('already symbolic') == 2, out)
check('no double-wrapping', '{grafana:{grafana:' not in res, res)

section('prose that documents a reftarget is not rewritten')
# The key regex cannot match inside a string value: JSON escapes the inner quotes, so a markdown
# block reads `\"reftarget\": ...` and never looks like the `"reftarget":` key. The structural guard
# behind it is defence-in-depth for a case this makes unreachable — assert the invariant, not the
# abort.
guide = json.dumps({'blocks': [
    {'type': 'markdown', 'content': 'Example: "reftarget": "div[data-testid=\'uplot-main-div\']"'},
]}, indent=2)
code, out, res = run([], guide=guide, write=True)
check('markdown documenting a reftarget is untouched',
      code == 0 and json.loads(res) == json.loads(guide), res)

section('formatting is preserved')
guide = ('{\n  "blocks": [\n    {\n      "type": "interactive",\n'
         '      "reftarget": "div[data-testid=\'uplot-main-div\']",\n'
         '      "requirements": ["exists-reftarget"]\n    }\n  ]\n}\n')
code, out, res = run([], guide=guide, write=True)
check('only the reftarget line differs',
      [a for a, b in zip(guide.splitlines(), res.splitlines()) if a != b]
      == ['      "reftarget": "div[data-testid=\'uplot-main-div\']",'], res)

section('find-ambiguous.py sees non-prefixed values too')
with tempfile.TemporaryDirectory() as d:
    d = Path(d)
    (d / 'map.json').write_text(json.dumps({
        **MAP, 'ambiguous': {**MAP['ambiguous'], 'uplot-main-div': ['a.b', 'c.d']}}))
    (d / 'content.json').write_text(json.dumps(
        {'blocks': [{'reftarget': "div[data-testid='uplot-main-div']"}]}))
    p = subprocess.run([sys.executable, str(AMBIGUOUS), str(d / 'content.json'),
                        '--map', str(d / 'map.json')], capture_output=True, text=True)
    check('non-prefixed ambiguous value is reported',
          p.returncode == 1 and 'uplot-main-div' in p.stdout, p.stdout)

print(f'\n{"FAILED: " + ", ".join(failures) if failures else "all tests passed"}')
sys.exit(1 if failures else 0)
