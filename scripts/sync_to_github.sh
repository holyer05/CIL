#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

git config core.hooksPath .githooks

git add -A
if git diff --cached --quiet; then
  echo "No project changes to sync."
  exit 0
fi

message="${*:-chore: sync project $(date '+%Y-%m-%d %H:%M:%S %z')}"
git commit -m "$message"
git push origin "$(git branch --show-current)"
