#!/usr/bin/env bash
set -euf -o pipefail

function usage {
  cat <<EOF
Assemble an external package repository under test-env/generated/ from this
repo's own packages, so the local stack can serve and launch them without
publishing to the CDN.

It copies the package into generated/, builds repository.json with the
grafana-pathfinder-app CLI, and rewrites the package's targeting to
targetPlatform: oss so it is recommended on a local OSS stack.

Usage:
  scripts/build-external-repo.bash --cli <path-to-pathfinder-cli-index.js> [--package <id>]

Options:
  --cli       Path to grafana-pathfinder-app dist/cli/cli/index.js. Defaults to
              ../../grafana-pathfinder-app/dist/cli/cli/index.js relative to the repo root.
  --package   Package directory name to serve. Default: drilldown-metrics-lj.
  -h, --help  Show this message.
EOF
}

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
TEST_ENV_DIR=$(cd -- "${SCRIPT_DIR}/.." && pwd)
REPO_ROOT=$(cd -- "${TEST_ENV_DIR}/.." && pwd)

CLI="${REPO_ROOT}/../grafana-pathfinder-app/dist/cli/cli/index.js"
PACKAGE=drilldown-metrics-lj

while [[ $# -gt 0 ]]; do
  case "$1" in
    --cli) CLI="$2"; shift 2 ;;
    --package) PACKAGE="$2"; shift 2 ;;
    -h | --help) usage && exit 0 ;;
    *) echo "unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done

[[ -f "${CLI}" ]] || { echo "pathfinder CLI not found at ${CLI}; build it or pass --cli" >&2; exit 66; }
[[ -d "${REPO_ROOT}/${PACKAGE}" ]] || { echo "package not found: ${REPO_ROOT}/${PACKAGE}" >&2; exit 66; }

GEN="${TEST_ENV_DIR}/generated"
rm -rf "${GEN}"
mkdir -p "${GEN}"
cp -R "${REPO_ROOT}/${PACKAGE}" "${GEN}/${PACKAGE}"

node "${CLI}" build-repository "${GEN}" -o "${GEN}/repository.json"

# The published manifests target targetPlatform: cloud, and some use a urlRegex
# predicate the OSS built-in matcher does not support (it then fails the whole
# match closed). Rewrite the served index entry to supported predicates on oss
# so the path is recommended on a local OSS stack. This edits only the generated
# index, never the repo's manifests.
python3 - "${GEN}/repository.json" "${PACKAGE}" <<'PY'
import json, sys
path = sys.argv[1]
pkg = sys.argv[2]
repo = json.load(open(path))
entry = repo.get(pkg)
if entry is None:
    raise SystemExit(f"{pkg} missing from generated repository.json")
starting = entry.get("startingLocation", "/")
entry["targeting"] = {"match": {"and": [{"urlPrefix": starting}, {"targetPlatform": "oss"}]}}
json.dump(repo, open(path, "w"), indent=2)
print(f"served {len(repo)} packages; {pkg} targeted at oss urlPrefix {starting}")
PY

echo "Wrote ${GEN}/repository.json"
