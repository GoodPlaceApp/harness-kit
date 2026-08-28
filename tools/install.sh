#!/usr/bin/env bash
# Install harness-kit at user level, so its skills work in EVERY project on this machine.
#
# This is the route that does not depend on the plugin system being available. Symlinks
# rather than copies, so edits to the kit take effect with no reinstall.
#
# Pass --copy if symlinked skills are not picked up; re-run after editing the kit.
set -euo pipefail
KIT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODE="${1:-symlink}"

mkdir -p ~/.claude/skills ~/.claude/agents

for d in "$KIT"/skills/*/; do
  name="$(basename "$d")"
  rm -rf ~/.claude/skills/"$name"
  if [ "$MODE" = "--copy" ]; then cp -R "$d" ~/.claude/skills/"$name"
  else ln -sfn "$d" ~/.claude/skills/"$name"; fi
  echo "skill  $name"
done
for f in "$KIT"/agents/*.md; do
  name="$(basename "$f")"
  rm -f ~/.claude/agents/"$name"
  if [ "$MODE" = "--copy" ]; then cp "$f" ~/.claude/agents/"$name"
  else ln -sfn "$f" ~/.claude/agents/"$name"; fi
  echo "agent  ${name%.md}"
done

echo
echo "installed from $KIT"
echo "Set HARNESS_KIT=$KIT in your shell profile if the kit lives anywhere unusual."
