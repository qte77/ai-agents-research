#!/usr/bin/env bash
# cc-multi-account.sh — run N Claude Code accounts concurrently in one OS.
#
# WHY THIS WORKS: CLAUDE_CONFIG_DIR overrides where CC keeps settings.json +
# .credentials.json. One config dir = one logged-in account. Point each terminal
# at a different dir → N independent `claude` processes, N accounts, no OS/user
# switching. Companion to docs/cc-community/CC-multi-account-switching-landscape.md.
#
# PLATFORM: Linux / WSL2 / Codespaces store credentials INSIDE the config dir,
# so this isolates accounts cleanly. On macOS credentials live in the Keychain
# and carry over between dirs — use a tool (claude-swap / claude-multiprofile)
# there instead; see the landscape doc.
#
# ─────────────────────────────────────────────────────────────────────────────
# ZERO-INSTALL ALTERNATIVE (no functions, no sourcing this file):
# just put one alias per account in ~/.bashrc — same mechanism, fewer moving
# parts. Use these if you don't want the helpers below:
#
#   alias claude-work='CLAUDE_CONFIG_DIR=$HOME/.claude-work         command claude'
#   alias claude-personal='CLAUDE_CONFIG_DIR=$HOME/.claude-personal command claude'
#
# Then run `claude-work` in one terminal and `claude-personal` in another —
# first run of each prompts /login for that account; they run concurrently.
# ─────────────────────────────────────────────────────────────────────────────
#
# TWO WAYS TO USE IT
#
# 1. Executed directly (one-off, no setup):
#      ./cc-multi-account.sh work        # launch CC on the "work" account
#      ./cc-multi-account.sh usage work  # that account's usage/cost stats
#      ./cc-multi-account.sh list        # list configured profiles
#      ./cc-multi-account.sh sync work   # re-apply shared settings to a profile
#      ./cc-multi-account.sh --help      # this help
#
# 2. Sourced (persistent short commands — put in ~/.bashrc):
#      source /path/to/cc-multi-account.sh
#    then:
#      ccp work            # launch CC on the "work" account (first run → /login)
#      ccp personal        # launch CC on the "personal" account
#      ccu work            # per-account usage/cost stats (needs: npm i -g ccusage)
#      ccl                 # list configured profiles
#      ccsync work         # re-apply ~/.claude/settings.json to that profile
#      ccsync --all        # ...to every profile
#
# Sourcing is required for the short `ccp`/`ccu`/`ccl` commands because the file
# defines shell functions — running it in a child shell would define them there
# and discard them on exit.

: "${CC_PROFILE_HOME:=$HOME/.claude-profiles}"   # where per-account dirs live

# ccsync knobs (see ccsync below).
: "${CC_BASE_SETTINGS:=$HOME/.claude/settings.json}"   # the canonical, shared settings
# Keys a profile OWNS. CC writes these itself (theme picker, dismissed warnings,
# notification prefs), and they're per-account by nature — so ccsync never
# overwrites them. Everything else is shared and comes from CC_BASE_SETTINGS.
: "${CC_PROFILE_KEEP:=theme preferredNotifChannel agentPushNotifEnabled skipWorkflowUsageWarning}"

# Launch CC scoped to one account. Run in separate terminals to go concurrent.
ccp() {
  local name="${1:?usage: ccp <profile>}"; shift
  local dir="$CC_PROFILE_HOME/$name"
  mkdir -p "$dir"
  # .credentials.json lives in here. A default umask leaves the dir 755, so
  # every local user can list it and read history.jsonl / projects/ transcripts.
  chmod 700 "$CC_PROFILE_HOME" "$dir" 2>/dev/null
  echo "▶ CC profile '$name'  (CLAUDE_CONFIG_DIR=$dir)"
  CLAUDE_CONFIG_DIR="$dir" command claude "$@"   # first run prompts /login for THIS account
}

# Per-account usage/cost — reads only that profile's transcripts, no cross-talk.
# Requires: npm i -g ccusage   (see docs/cc-community/CC-usage-tooling-landscape.md)
ccu() {
  local name="${1:?usage: ccu <profile>}"; shift
  local dir="$CC_PROFILE_HOME/$name"
  [ -d "$dir" ] || { echo "no such profile: $name"; return 1; }
  CLAUDE_CONFIG_DIR="$dir" ccusage "$@"          # daily/blocks/etc. scoped to this account
}

# Re-apply the shared settings to a profile, keeping that profile's own UI keys.
#
# WHY NOT A SYMLINK: CLAUDE_CONFIG_DIR relocates the whole config dir, so each
# profile gets its own settings.json and they drift apart. Symlinking them to one
# file looks like the fix and isn't — CC *writes* to settings.json (that's where
# theme and dismissed warnings land), so N concurrent profiles would race on one
# file, and an atomic write (tmp + rename) silently replaces the symlink with a
# copy. Re-applying explicitly is race-free and can't decay into a lie.
#
# Only settings are copied. Credentials are never touched: .credentials.json
# stays per-profile, which is the entire point of the tool.
ccsync() {
  local name="${1:?usage: ccsync <profile> | ccsync --all}"

  command -v jq >/dev/null 2>&1 || { echo "ccsync needs jq" >&2; return 1; }
  [ -r "$CC_BASE_SETTINGS" ] || { echo "no readable base settings: $CC_BASE_SETTINGS" >&2; return 1; }

  if [ "$name" = "--all" ]; then
    local rc=0 d
    for d in "$CC_PROFILE_HOME"/*/; do
      [ -d "$d" ] || continue                     # no glob match → literal pattern
      ccsync "${d%/}" || rc=1
    done
    return "$rc"
  fi
  name=$(basename "$name")                        # tolerate a full path from --all

  local dir="$CC_PROFILE_HOME/$name" target kept merged
  [ -d "$dir" ] || { echo "no such profile: $name" >&2; return 1; }
  target="$dir/settings.json"

  kept='{}'
  [ -s "$target" ] && kept=$(cat "$target")
  merged=$(jq -n \
    --argjson base "$(cat "$CC_BASE_SETTINGS")" \
    --argjson kept "$kept" \
    --arg keep "$CC_PROFILE_KEEP" \
    '$base * ($kept | with_entries(select(.key as $k | ($keep | split(" ")) | index($k))))'
  ) || { echo "merge failed for '$name' — is one of the files invalid JSON?" >&2; return 1; }

  # Anything the profile had that neither the base nor CC_PROFILE_KEEP covers is
  # about to disappear. Usually that's stale junk — but it is also how a NEW
  # setting CC writes per-profile (advisorModel, say) would be silently deleted.
  # Say what's going, so a real setting can be promoted into the base instead.
  local dropped
  dropped=$(jq -r --argjson base "$(cat "$CC_BASE_SETTINGS")" --arg keep "$CC_PROFILE_KEEP" '
      keys - ($base | keys) - ($keep | split(" ")) | join(" ")' <<<"$kept")
  [ -n "$dropped" ] && echo "  ! dropping from '$name': $dropped" >&2

  [ -s "$target" ] && cp "$target" "$target.bak"  # last-known-good, overwritten each sync
  printf '%s\n' "$merged" >"$target"
  chmod 700 "$dir" 2>/dev/null
  echo "✔ synced '$name'  ($(jq -r 'keys|length' <<<"$merged") keys; kept: $CC_PROFILE_KEEP)"
}

# List profiles you've created.
ccl() {
  echo "profiles in $CC_PROFILE_HOME:"
  find "$CC_PROFILE_HOME" -maxdepth 1 -mindepth 1 -type d -printf '  %f\n' 2>/dev/null || echo "  (none yet)"
}

# Print the usage header (everything between the shebang and the first blank
# line after the comment block) — used for --help and bare invocation.
cch() { sed -n '2,/^$/p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; }

# Dispatch when EXECUTED rather than sourced. Sourcing skips this entirely and
# just leaves ccp/ccu/ccl defined in your shell.
if [ "${BASH_SOURCE[0]}" = "$0" ]; then
  case "${1:-}" in
    ""|-h|--help|help) cch; exit 0 ;;
    list|ls)           ccl ;;
    usage|stats)       shift; ccu "$@" ;;
    sync)              shift; ccsync "$@" ;;
    -*)                echo "unknown option: $1" >&2; echo >&2; cch >&2; exit 2 ;;
    *)                 ccp "$@" ;;
  esac
fi
