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
# HELPERS (source this file from ~/.bashrc:  source /path/to/cc-multi-account.sh):
#   ccp work            # launch CC on the "work" account (first run → /login)
#   ccp personal        # launch CC on the "personal" account
#   ccu work            # per-account usage/cost stats (needs: npm i -g ccusage)
#   ccl                 # list configured profiles

: "${CC_PROFILE_HOME:=$HOME/.claude-profiles}"   # where per-account dirs live

# Launch CC scoped to one account. Run in separate terminals to go concurrent.
ccp() {
  local name="${1:?usage: ccp <profile>}"; shift
  local dir="$CC_PROFILE_HOME/$name"
  mkdir -p "$dir"
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

# List profiles you've created.
ccl() {
  echo "profiles in $CC_PROFILE_HOME:"
  find "$CC_PROFILE_HOME" -maxdepth 1 -mindepth 1 -type d -printf '  %f\n' 2>/dev/null || echo "  (none yet)"
}
