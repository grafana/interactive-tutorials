#!/usr/bin/env python3
"""Build one raw-evidence dossier per multi-milestone learning path (*-lj).

Deterministic extraction only: no classification. Classification of prerequisites
happens in a separate, reviewed step (see test-stack/README.md).
Run from the repo root: python3 test-stack/scripts/extract-dossiers.py
"""
import json, re, glob, os, collections

OUT = "test-stack/dossiers"

def load(p):
    with open(p) as f:
        return json.load(f)

def walk(node):
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from walk(v)
    elif isinstance(node, list):
        for v in node:
            yield from walk(v)

def before_you_begin(blocks):
    out = []
    for b in walk(blocks):
        if b.get("type") == "markdown":
            c = b.get("content", "")
            if re.search(r"before you begin|prerequisite|you need|requirements", c, re.I):
                out.append(c)
    return out

def collect(content):
    reqs, targets, navs = collections.Counter(), collections.Counter(), []
    for b in walk(content):
        r = b.get("requirements")
        if isinstance(r, list):
            reqs.update(x for x in r if isinstance(x, str))
        elif isinstance(r, str):
            reqs.update(x.strip() for x in r.split(",") if x.strip())
        if b.get("reftarget") and b.get("targetaction") in ("navigate",) or b.get("type") == "navigate":
            navs.append(b.get("reftarget") or b.get("url"))
    return reqs, navs

dossiers = []
for mpath in sorted(glob.glob("*-lj/manifest.json")):
    d = os.path.dirname(mpath)
    m = load(mpath)
    ms = m.get("milestones", [])
    entry = {
        "path": d,
        "id": m.get("id"),
        "type": m.get("type"),
        "milestoneCount": len(ms),
        "startingLocation": m.get("startingLocation"),
        "testEnvironment": m.get("testEnvironment"),
        "targeting": m.get("targeting"),
        "manifestPrerequisites": m.get("prerequisites"),
        "pathBeforeYouBegin": before_you_begin(load(f"{d}/content.json").get("blocks", [])),
        "milestones": [],
    }
    # milestone ids are package ids; locate the directory by manifest id
    id2dir = {}
    for mm in glob.glob(f"{d}/*/manifest.json"):
        id2dir[load(mm).get("id")] = os.path.dirname(mm)
    for mid in ms:
        md = id2dir.get(mid)
        if not md:
            entry["milestones"].append({"id": mid, "error": "directory not found"})
            continue
        c = load(f"{md}/content.json")
        reqs, navs = collect(c)
        entry["milestones"].append({
            "id": mid, "dir": md,
            "requirements": dict(reqs),
            "navigate": navs,
            "needsText": before_you_begin(c.get("blocks", [])),
        })
    dossiers.append(entry)
    with open(f"{OUT}/{d}.json", "w") as f:
        json.dump(entry, f, indent=2)
print(f"{len(dossiers)} dossiers written to {OUT}")
print("single/zero-milestone paths:", [e["path"] for e in dossiers if e["milestoneCount"] < 2])
