#!/usr/bin/env bash
# Validate a learning path (or a single content.json) the same way CI does.
#
# CI (.github/workflows/validate-json.yml) runs:
#   node pathfinder-app/dist/cli/cli/index.js validate --strict <content.json>
# then:
#   node pathfinder-app/dist/cli/cli/index.js validate --package <dir>
#
# `validate --packages` is not enough: it is depth-1 and is not --strict, so
# unknown fields (for example hint on a multistep block) pass locally and fail
# on push.
#
# Usage (from the interactive-tutorials repo root):
#   scripts/validate-path.sh {path_dir}
#   scripts/validate-path.sh path/to/content.json
#   scripts/validate-path.sh --fetch {path_dir}
#
# Exit: 0 pass, 1 schema/package failure, 2 CLI missing (and --fetch not used
# or fetch failed before validate).

set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/validate-path.sh [--fetch] <path_dir|content.json>

Run Pathfinder validate --strict on every content.json under the path, then
validate --package on each directory that has a manifest.json.

  --fetch   If the CLI is missing, clone the grafana-pathfinder-app SHA pinned
            in .github/workflows/validate-json.yml into .pathfinder-cli/ (gitignored)
            and build it.

Environment:
  PATHFINDER_CLI   Absolute path to dist/cli/cli/index.js
  PATHFINDER_APP   Checkout of grafana-pathfinder-app (uses dist/cli/cli/index.js)
EOF
}

FETCH=0
TARGET=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --fetch) FETCH=1; shift ;;
    -h|--help) usage; exit 0 ;;
    --) shift; break ;;
    -*) echo "Unknown flag: $1" >&2; usage >&2; exit 2 ;;
    *) TARGET="$1"; shift ;;
  esac
done

if [[ -z "$TARGET" ]]; then
  usage >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

if [[ "$TARGET" = /* ]]; then
  TARGET_PATH="$TARGET"
else
  TARGET_PATH="$REPO_ROOT/$TARGET"
fi

if [[ ! -e "$TARGET_PATH" ]]; then
  echo "❌ Not found: $TARGET_PATH" >&2
  exit 2
fi

WORKFLOW="$REPO_ROOT/.github/workflows/validate-json.yml"

cli_pin() {
  awk '
    /repository: grafana\/grafana-pathfinder-app/ { in_block=1 }
    in_block && /ref:/ {
      gsub(/^[[:space:]]*ref:[[:space:]]*/, "")
      print
      exit
    }
  ' "$WORKFLOW"
}

find_cli() {
  local candidate
  if [[ -n "${PATHFINDER_CLI:-}" && -f "$PATHFINDER_CLI" ]]; then
    echo "$PATHFINDER_CLI"
    return 0
  fi
  if [[ -n "${PATHFINDER_APP:-}" && -f "$PATHFINDER_APP/dist/cli/cli/index.js" ]]; then
    echo "$PATHFINDER_APP/dist/cli/cli/index.js"
    return 0
  fi
  # Prefer the CI pin (.pathfinder-cli from --fetch) over a sibling checkout,
  # which may be an older CLI that rejects current flags or unknown fields.
  for candidate in \
    "$REPO_ROOT/.pathfinder-cli/dist/cli/cli/index.js" \
    "$REPO_ROOT/pathfinder-app/dist/cli/cli/index.js" \
    "$REPO_ROOT/../grafana-pathfinder-app/dist/cli/cli/index.js"
  do
    if [[ -f "$candidate" ]]; then
      echo "$candidate"
      return 0
    fi
  done
  return 1
}

find_app_src() {
  local candidate
  if [[ -n "${PATHFINDER_APP:-}" && -f "$PATHFINDER_APP/package.json" ]]; then
    echo "$PATHFINDER_APP"
    return 0
  fi
  for candidate in \
    "$REPO_ROOT/../grafana-pathfinder-app" \
    "$REPO_ROOT/pathfinder-app" \
    "$REPO_ROOT/.pathfinder-cli"
  do
    if [[ -f "$candidate/package.json" ]]; then
      echo "$candidate"
      return 0
    fi
  done
  return 1
}

build_cli() {
  local app="$1"
  echo "Building Pathfinder CLI in $app"
  (
    cd "$app"
    if [[ ! -d node_modules ]]; then
      npm ci --ignore-scripts
    fi
    npm run build:cli
  )
}

fetch_cli() {
  local pin app
  pin="$(cli_pin)"
  if [[ -z "$pin" ]]; then
    echo "❌ Could not read grafana-pathfinder-app pin from $WORKFLOW" >&2
    return 1
  fi
  app="$REPO_ROOT/.pathfinder-cli"
  echo "Fetching grafana-pathfinder-app@$pin into $app"
  if [[ -d "$app/.git" ]]; then
    git -C "$app" fetch --depth 1 origin "$pin"
    git -C "$app" checkout --detach "$pin"
  else
    rm -rf "$app"
    if command -v gh >/dev/null 2>&1; then
      gh repo clone grafana/grafana-pathfinder-app "$app" -- --depth 1
    else
      git clone --depth 1 https://github.com/grafana/grafana-pathfinder-app.git "$app"
    fi
    git -C "$app" fetch --depth 1 origin "$pin"
    git -C "$app" checkout --detach "$pin"
  fi
  build_cli "$app"
}

CLI=""
if CLI="$(find_cli)"; then
  :
elif APP_SRC="$(find_app_src)"; then
  echo "Pathfinder CLI is not built. Building from $APP_SRC"
  build_cli "$APP_SRC"
  CLI="$APP_SRC/dist/cli/cli/index.js"
elif [[ "$FETCH" -eq 1 ]]; then
  fetch_cli
  CLI="$REPO_ROOT/.pathfinder-cli/dist/cli/cli/index.js"
else
  pin="$(cli_pin || true)"
  cat >&2 <<EOF
❌ Pathfinder CLI not found (dist/cli/cli/index.js).

This is the same check CI runs. Without it, unknown JSON fields (for example
hint on a multistep) pass locally and fail on push.

Fix, then re-run this script:
  1. Clone grafana-pathfinder-app next to this repo, check out ${pin:-the SHA in .github/workflows/validate-json.yml},
     then: npm ci --ignore-scripts && npm run build:cli
  2. Or set PATHFINDER_APP / PATHFINDER_CLI
  3. Or re-run with --fetch to clone the pinned SHA into .pathfinder-cli/

EOF
  exit 2
fi

if [[ ! -f "$CLI" ]]; then
  echo "❌ CLI path is not a file: $CLI" >&2
  exit 2
fi

echo "Using Pathfinder CLI: $CLI"

pin="$(cli_pin || true)"
CLI_APP="$(cd "$(dirname "$CLI")/../../.." && pwd)"
if [[ -n "$pin" && -d "$CLI_APP/.git" ]]; then
  cli_head="$(git -C "$CLI_APP" rev-parse HEAD 2>/dev/null || true)"
  if [[ -n "$cli_head" && "$cli_head" != "$pin"* && "${cli_head:0:9}" != "${pin:0:9}" ]]; then
    echo "⚠️  CLI checkout $cli_head does not match the CI pin $pin. Unknown-field results may differ. Use --fetch to match CI."
  fi
fi

SNIPPET_ARGS=()
if [[ -d "$REPO_ROOT/shared/snippets" ]]; then
  if node "$CLI" validate --help 2>&1 | grep -q -- '--snippets-catalog'; then
    SNIPPET_INDEX="$(mktemp -t pathfinder-snippets.XXXXXX.json)"
    trap 'rm -f "$SNIPPET_INDEX"' EXIT
    if node "$CLI" build-snippets "$REPO_ROOT/shared/snippets" -o "$SNIPPET_INDEX"; then
      SNIPPET_ARGS=(--snippets-catalog "$SNIPPET_INDEX")
    else
      echo "⚠️  Snippet catalog build failed; continuing without snippet-reference checks."
    fi
  else
    echo "⚠️  This CLI does not support --snippets-catalog. Skipping snippet-reference checks. Use --fetch to match CI."
  fi
fi

CONTENT_FILES=()
PACKAGE_DIRS=()

if [[ -f "$TARGET_PATH" ]]; then
  if [[ "$(basename "$TARGET_PATH")" != "content.json" ]]; then
    echo "❌ File must be named content.json: $TARGET_PATH" >&2
    exit 2
  fi
  CONTENT_FILES+=("$TARGET_PATH")
  PKG_DIR="$(dirname "$TARGET_PATH")"
  if [[ -f "$PKG_DIR/manifest.json" ]]; then
    PACKAGE_DIRS+=("$PKG_DIR")
  fi
else
  while IFS= read -r file; do
    CONTENT_FILES+=("$file")
  done < <(find "$TARGET_PATH" -name content.json -type f \
             -not -path '*/pathfinder-app/*' \
             -not -path '*/.pathfinder-cli/*' \
             -not -path '*/shared/*' \
             | sort)

  while IFS= read -r manifest; do
    PACKAGE_DIRS+=("$(dirname "$manifest")")
  done < <(find "$TARGET_PATH" -name manifest.json -type f \
             -not -path '*/pathfinder-app/*' \
             -not -path '*/.pathfinder-cli/*' \
             -not -path '*/shared/*' \
             | sort)
fi

if [[ ${#CONTENT_FILES[@]} -eq 0 ]]; then
  echo "❌ No content.json under $TARGET_PATH" >&2
  exit 1
fi

# Usage: run_cli validate --strict <file> | run_cli validate --package <dir>
run_cli() {
  local cmd="$1" flag="$2" target="$3"
  if [[ ${#SNIPPET_ARGS[@]} -gt 0 ]]; then
    node "$CLI" "$cmd" "$flag" "${SNIPPET_ARGS[@]}" "$target"
  else
    node "$CLI" "$cmd" "$flag" "$target"
  fi
}

FAILED=0
PASSED=0

echo ""
echo "=== validate --strict (CI content.json check) ==="
for file in "${CONTENT_FILES[@]}"; do
  rel="${file#"$REPO_ROOT"/}"
  echo "📄 $rel"
  if run_cli validate --strict "$file"; then
    PASSED=$((PASSED + 1))
  else
    echo "❌ Validation failed for: $rel"
    FAILED=$((FAILED + 1))
  fi
done

echo ""
echo "=== validate --package ==="
PKG_PASSED=0
PKG_FAILED=0
if [[ ${#PACKAGE_DIRS[@]} -gt 0 ]]; then
  for dir in "${PACKAGE_DIRS[@]}"; do
    rel="${dir#"$REPO_ROOT"/}"
    echo "📦 $rel"
    if run_cli validate --package "$dir"; then
      PKG_PASSED=$((PKG_PASSED + 1))
    else
      echo "❌ Package validation failed: $rel"
      PKG_FAILED=$((PKG_FAILED + 1))
    fi
  done
fi

echo ""
echo "content.json --strict:  passed $PASSED  failed $FAILED"
echo "packages:               passed $PKG_PASSED  failed $PKG_FAILED"

if [[ "$FAILED" -gt 0 || "$PKG_FAILED" -gt 0 ]]; then
  echo "❌ Path validation failed."
  exit 1
fi

echo "✅ Path validation passed."
exit 0
