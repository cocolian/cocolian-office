#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
repo="$root/src/online.mirror/engine/translations"
commit=17fb3698d5e86169d44076f7a992c572f8f780f1
patch="$root/patches/translations/zh-cn-native-commands.patch"
if ! git -C "$repo" rev-parse --git-dir >/dev/null 2>&1 || test ! -e "$repo/.git"; then
  mkdir -p "$repo"
  git -C "$repo" init
  git -C "$repo" remote add origin https://github.com/LibreOffice/translations.git
  git -C "$repo" config remote.origin.promisor true
  git -C "$repo" config remote.origin.partialclonefilter blob:none
  git -C "$repo" sparse-checkout init --cone
  git -C "$repo" sparse-checkout set source/zh-CN
  git -C "$repo" fetch --depth 1 --filter=blob:none origin "$commit"
  git -C "$repo" checkout --detach "$commit"
fi
test "$(git -C "$repo" rev-parse HEAD)" = "$commit"
git -C "$repo" remote set-url --push origin DISABLED
if git -C "$repo" apply --reverse --check "$patch" 2>/dev/null; then
  echo 'Translation patch is already applied.'
else
  git -C "$repo" apply --check "$patch"
  git -C "$repo" apply "$patch"
fi
echo 'Restored locked zh-CN translation source; changes are versioned as a patch in the workspace repository.'
