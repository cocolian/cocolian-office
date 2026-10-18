#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
for name in office-core online.mirror collabora-online-sdk-examples; do
  repo="$root/src/$name"
  git -C "$repo" rev-parse --git-dir >/dev/null 2>&1 || { echo "Missing clone: $repo" >&2; exit 1; }
  git -C "$repo" fetch upstream --prune
  git -C "$repo" status --short --branch
done
printf '%s\n' 'Fetched only. To update a clean base branch, use git merge --ff-only upstream/<branch>; then review before pushing origin.'
