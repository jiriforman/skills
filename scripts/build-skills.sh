#!/usr/bin/env bash
# Build a .zip for every skill folder under skills/ that has a skill.yaml.
# Folders whose name starts with "_" (e.g. _template) are skipped.
# Output goes to dist/.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

rm -rf dist
mkdir -p dist

if [[ ! -d skills ]]; then
  echo "No skills/ directory — nothing to build."
  exit 0
fi

shopt -s nullglob
built=0
for dir in skills/*/; do
  name="$(basename "$dir")"
  if [[ "$name" == _* ]]; then
    echo "Skipping template folder: $name"
    continue
  fi
  if [[ ! -f "$dir/skill.yaml" ]]; then
    echo "Skipping $name (no skill.yaml)"
    continue
  fi
  echo "Packaging $name…"
  (cd skills && zip -r -q "../dist/${name}.zip" "$name" -x "*.DS_Store" "__MACOSX/*")
  built=$((built + 1))
done

echo "Built $built skill zip(s):"
ls -la dist/ || true
