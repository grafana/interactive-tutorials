---
name: convert-guide-selectors
description: Use when a guide's reftargets are hand-written CSS, hardcoded data-testid strings, localized aria-label/placeholder/title matches, or :contains() text matching, and you want them on Grafana's official e2e selectors. Also use when a step needs a selector Grafana does not expose yet.
---

# Convert Guide Selectors

Move a guide's `reftarget` values onto `@grafana/e2e-selectors` using Pathfinder's **symbolic**
selector syntax, and hand off to grafana/grafana when a selector doesn't exist yet.

**Core principle:** a resolved `data-testid` string is a *snapshot of one Grafana version*. The
symbolic form is a *reference*. Always ship the reference.

**REQUIRED BACKGROUND:** Read [symbolic-selector-syntax.md](symbolic-selector-syntax.md) before
converting anything. It defines the three forms, the version-resolution behaviour, and four traps
that silently break guides.

---

## The output contract

Every reftarget you touch ends as **exactly one** of these four shapes:

| Shape | When |
| --- | --- |
| `grafana:<path>` | the whole reftarget is one package selector |
| `grafana:<path>:<arg>` | the selector is parameterized |
| `{grafana:<path>}` embedded in CSS | the selector is scoped, or combined with a non-package part |
| **unchanged** | no package selector exists, or it is a documented exception |

A converted reftarget contains **no resolved selector text**. If the result still contains
`data-testid ` followed by a literal value, the conversion is not done — that is the snapshot, not
the reference.

```json
// the reference — resolves per running Grafana version
"reftarget": "grafana:components.TimePicker.openButton"

// the snapshot — pinned to whichever version you happened to look at
"reftarget": "button[data-testid='data-testid TimePicker Open Button']"
```

Steps whose reftarget is already a literal `data-testid` are **in scope**. "It already uses a
test id" is not a reason to skip it; that is the exact case this skill exists for.

---

## Never ship a selector that isn't released

A guide runs against Grafana instances that exist **today**. A selector you just added to
grafana/grafana, or that sits on an unmerged branch, resolves to nothing.

**When a step needs a selector Grafana does not expose in a shipped release:**

1. Leave the step's reftarget **exactly as it is**, so the guide keeps working.
2. Add the selector in grafana/grafana (see [Handoff](#handoff-to-grafanagrafana)).
3. Record the pending swap in the guide PR: step, current selector, target path.

### Red flags — STOP

- "I just added this selector, so I'll use it"
- "It's on my branch / it'll ship soon"
- "The old selector is ugly, the new one is correct"
- "I'll note the risk in the PR" — noting it is not a substitute for the guide working

**All of these mean: revert that reftarget and record it as pending.**

### Three things the tooling cannot tell you

Do not read a clean run as permission.

1. **Merged is not released.** `--merged-map` compares against `origin/main`, which is a `-pre`
   version — nothing on it has shipped. It rules out *your branch*, not *unreleased*. The real
   floor is the oldest Grafana your guide supports; check the selector's version key against it by
   hand.
2. **`pending=0` does not mean "nothing pending."** The converter can only gate conversions it
   proposes, and it only proposes them for reftargets that already contain a literal
   `data-testid`. A step still on `aria-label` / `placeholder` / text whose replacement you just
   added lands in UNTOUCHED, invisible to the gate. **Run `find-unmerged-paths.py` and read its
   list against the UNTOUCHED list** — that is the only thing that catches this case.
3. **A defined selector may be unwired.** The package can carry a selector for months while the
   element still lacks the attribute (`QueryTab.queryInspectorButton` was defined in 13.1.0 but not
   wired into Explore). Confirm against a live instance.

---

## Workflow

```dot
digraph convert {
  "Extract reftargets" [shape=box];
  "Build value->path map" [shape=box];
  "Ambiguous value?" [shape=diamond];
  "Pin path explicitly" [shape=box];
  "Package selector exists?" [shape=diamond];
  "On merged ref?" [shape=diamond];
  "Apply output contract" [shape=box];
  "Leave as-is + record pending" [shape=box];
  "Handoff to grafana/grafana" [shape=box];
  "Verify" [shape=doublecircle];

  "Extract reftargets" -> "Build value->path map" -> "Ambiguous value?";
  "Ambiguous value?" -> "Pin path explicitly" [label="yes"];
  "Ambiguous value?" -> "Package selector exists?" [label="no"];
  "Pin path explicitly" -> "Package selector exists?";
  "Package selector exists?" -> "On merged ref?" [label="yes"];
  "Package selector exists?" -> "Handoff to grafana/grafana" [label="no"];
  "On merged ref?" -> "Apply output contract" [label="yes"];
  "On merged ref?" -> "Leave as-is + record pending" [label="no"];
  "Handoff to grafana/grafana" -> "Leave as-is + record pending";
  "Apply output contract" -> "Verify";
  "Leave as-is + record pending" -> "Verify";
}
```

Set `GRAFANA_REPO` to your grafana/grafana checkout; the scripts load the selectors package from
there.

### 1. Map — current tree, and the merged ref

```bash
export GRAFANA_REPO=~/Repos/grafana
SK=.cursor/skills/convert-guide-selectors

tsx $SK/scripts/build-selector-map.ts 13.2.0 > /tmp/selmap.json

# A second map from the merged ref. This powers the gate.
git -C $GRAFANA_REPO worktree add --detach /tmp/grafana-merged origin/main
ln -sfn $GRAFANA_REPO/node_modules /tmp/grafana-merged/node_modules   # resolver needs semver
GRAFANA_REPO=/tmp/grafana-merged tsx $SK/scripts/build-selector-map.ts 13.2.0 > /tmp/merged.json

# Which selectors are yours-and-unmerged? Keep this list in front of you.
python3 $SK/scripts/find-unmerged-paths.py --map /tmp/selmap.json --merged-map /tmp/merged.json

python3 $SK/scripts/find-ambiguous.py <guide>/content.json --map /tmp/selmap.json   # pin what it reports
```

### 2. Rewrite

```bash
python3 $SK/scripts/convert-reftargets.py <guide>/content.json \
  --map /tmp/selmap.json --merged-map /tmp/merged.json \
  --pin "data-testid prometheus type=components.DataSource.Prometheus.queryEditor.type"   # dry run

# add --write to apply
```

Anything the gate reports as **PENDING** is left unchanged — that is the rule above being
enforced, not a failure. Copy that list into the guide PR.

Omitting `--merged-map` disables the gate and prints a warning. Don't.
(`find-ambiguous.py` needs only `--map`; ambiguity is independent of release status.)

`convert-reftargets.py` edits the raw text, so existing formatting survives, and it asserts the
parsed JSON is structurally identical apart from reftargets. **Never** rewrite the guide by
`json.load` → `json.dump`; that reflows the whole file and buries the real change in hundreds of
formatting-only lines.

### 3. Verify (all of these are gates, not optional)

```bash
python3 -m json.tool <guide>/content.json > /dev/null            # still valid JSON

PATHS=$(grep -o 'grafana:[A-Za-z0-9_.]*' <guide>/content.json \
        | sed 's/^grafana://' | sort -u | jq -R . | jq -sc .)
tsx $SK/scripts/validate-paths.ts "$PATHS" "<min-version>,<current-version>"

# only reftarget lines changed (the converter also asserts this structurally)
git diff --stat <guide>/content.json 2>/dev/null \
  || diff <(git show HEAD:<guide>/content.json) <guide>/content.json
```

Then confirm in a live instance: for a sample of converted steps, evaluate
`document.querySelectorAll(':is([data-testid="V"], [aria-label="V"])').length === 1`.

Validate at your **minimum supported Grafana version as well as current**. Be precise about what
this catches: it surfaces selectors whose older form was matched by `aria-label` instead of
`data-testid`. It does **not** prove a selector existed back then — `resolveSelectors` falls back to
the newest version key, so a `12.4.0`-gated selector still reports OK when asked for `11.0.0`.
`validate-paths.ts` prints a "Resolves differently per version" section; treat every entry there as
a reason to keep the symbolic form.

---

## Handoff to grafana/grafana

Cross-repo: skills are resolved from the working directory, so you cannot invoke Grafana's skill
from this repo. Both checkouts must be available.

1. In the grafana checkout, invoke its **`add-e2e-selectors`** skill for the element.
2. Prefer fixing the *cause*: if a value derives from a `t()`-wrapped string, make the component
   pass an explicit stable test id rather than encoding English in the guide.
3. Open that PR first; keep the guide PR's reftarget unchanged and cross-link the two.

---

## Common mistakes

| Mistake | Why it bites |
| --- | --- |
| Converting nav menu items | Breaks Pathfinder's collapsed-menu auto-fix — see trap 1 |
| Skipping steps that already have a `data-testid` | Those are version-pinned snapshots; they are the point |
| Using a just-added selector | Resolves to nothing on every released Grafana |
| Trusting the first path found for a value | Several values map to multiple paths — pin them |
| `json.dump` round-trip | Reflows the file; the real diff disappears |
| Validating only against current Grafana | Misses selectors whose older form matched `aria-label` |
| Treating a `data-testid` as i18n-safe | It is only as stable as the string that produced it |
