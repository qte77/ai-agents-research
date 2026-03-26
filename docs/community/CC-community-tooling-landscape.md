---
title: CC Community Tooling Landscape
description: Analysis of RTK (Rust Token Killer) — a CLI proxy that compresses command outputs before they reach LLM context, saving 60-90% tokens via Claude Code hook integration.
category: landscape
status: research
sources:
  - https://github.com/rtk-ai/rtk
created: 2026-03-13
updated: 2026-03-26
---

**Status**: Research (informational)

## Summary

RTK (Rust Token Killer) is a Rust-based CLI proxy that intercepts shell command outputs and compresses them before they enter the LLM context window. It integrates transparently with Claude Code via hooks, requiring no workflow changes. Claimed savings: 60-90% token reduction depending on command mix.

## What RTK Does

RTK applies four compression strategies to command output:

| Strategy | Description |
|----------|-------------|
| **Smart filtering** | Removes noise and boilerplate (e.g., npm install progress bars, build warnings) |
| **Grouping** | Aggregates similar items (e.g., 50 passing tests -> summary) |
| **Truncation** | Preserves relevant portions, trims verbose sections |
| **Deduplication** | Collapses repeated log lines with counts |

The binary is zero-dependency Rust with <10ms overhead per command.

## Installation

```bash
# Homebrew (recommended)
brew install rtk

# Curl script
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh

# Cargo
cargo install --git https://github.com/rtk-ai/rtk
```

Pre-built binaries available for macOS (x86_64/aarch64), Linux (x86_64/aarch64), Windows.

## Supported Commands

### Git & GitHub

`rtk git status/log/diff/add/commit/push/pull` — outputs compressed to one-liners (e.g., `git push` becomes `"ok main"`).

`rtk gh pr list/view/issue list/run list` — GitHub CLI output compressed.

### Test Runners

`rtk test cargo test`, `rtk pytest`, `rtk vitest run`, `rtk playwright test`, `rtk go test` — failures only, ~90% reduction on passing suites.

### Build & Lint

`rtk tsc`, `rtk lint` (ESLint/Biome), `rtk next build`, `rtk cargo build/clippy`, `rtk ruff check`, `rtk golangci-lint run`

### Package Managers

`rtk pnpm list`, `rtk pip list/outdated`

### Infrastructure

`rtk docker ps/images/logs/compose ps`, `rtk kubectl pods/logs/services`

### File Operations

`rtk ls`, `rtk read` (with `-l aggressive` for signatures only), `rtk grep`, `rtk find`, `rtk diff`

### Other

`rtk json` (JSON compression), `rtk env`, `rtk log`, `rtk curl`, `rtk summary`, `rtk proxy`

## Claude Code Hook Integration

```bash
rtk init --global
```

After CC restart, commands are transparently rewritten — `git status` becomes `rtk git status` before execution. Claude never sees the rewrite, only the compressed output.

**Rewritten commands**: git, gh, cargo, cat/head/tail, rg/grep, ls, vitest/jest, tsc, eslint/biome, prettier, playwright, prisma, ruff, pytest, pip, go, golangci-lint, docker, kubectl, curl, pnpm.

**Uninstall**: `rtk init -g --uninstall`

## Token Savings Metrics

Based on a 30-minute coding session baseline:

| Operation | Standard Tokens | RTK Tokens | Savings |
|-----------|----------------|------------|---------|
| ls/tree (10x) | 2,000 | 400 | 80% |
| cat/read (20x) | 40,000 | 12,000 | 70% |
| grep/rg (8x) | 16,000 | 3,200 | 80% |
| git status (10x) | 3,000 | 600 | 80% |
| git add/commit/push (8x) | 1,600 | 120 | 92% |
| cargo/npm test (5x) | 25,000 | 2,500 | 90% |
| pytest (4x) | 8,000 | 800 | 90% |
| **Total** | **~118,000** | **~23,900** | **~80%** |

## Configuration

`~/.config/rtk/config.toml`:

```toml
[tracking]
database_path = "/path/to/custom.db"

[hooks]
exclude_commands = ["curl", "playwright"]

[tee]
enabled = true
mode = "failures"   # "failures" | "always" | "never"
max_files = 20
```

The `tee` feature saves full unfiltered output to `~/.local/share/rtk/tee/` on command failure — nothing is permanently lost from compression.

## Analytics (`rtk gain`)

```bash
rtk gain                          # Summary stats
rtk gain --graph                  # ASCII graph (last 30 days)
rtk gain --history                # Recent command history
rtk gain --daily                  # Day-by-day breakdown
rtk gain --all --format json      # JSON export for dashboards
```

Discovery mode finds missed savings opportunities:

```bash
rtk discover                      # Current project
rtk discover --all --since 7      # All projects, last 7 days
```

Global flags: `-u/--ultra-compact` (ASCII icons, extra savings), `-v/-vv/-vvv` (verbosity).

## Validated Findings (2026-03-26, v0.33.1)

Independent benchmark: 5 repos (83–74K files, 568K–8.2G), 9 categories, 10 iterations, 3 runs = 2,100 measurements. Deterministic: 699/700 ops <10-byte variance. Issue filed: [rtk-ai/rtk#839](https://github.com/rtk-ai/rtk/issues/839).

| Operation | Claimed | Measured | Verdict |
|-----------|---------|----------|---------|
| `ls` | -80% | **-72%** | Matches on verbose; dominated by large repos |
| `git log` | -80% | **-98%** | Truncation, not compression (544K→1.8K) |
| `git status` | -80% | **-46%** | Verbose only; `-s`/`--porcelain` = 0% |
| `git diff` | -75% | **-20%** | Full diff only; `--stat` = 0% |
| `docker ps` | -80% | **-38%** | `docker ps` = 75%; `docker ps -a` = 0% |
| `tree` | -80% | **-4%** | Near-passthrough |
| `cat` | -70% | **0%** | Byte-identical passthrough |
| `grep` | -80% | **-0%** | Adds bytes (RTK overhead) |
| `ruff` | -80% | **-1%** | Adds bytes |
| `pytest` | -90% | **0%** | 185,962B unchanged |

**Key finding**: 6 of 9 categories show 0% or negative savings. The 72% grand total is dominated by `git log` truncation and `ls -laR` on large repos. `cat` and `grep` — the two highest-volume claimed categories (54% of total claim) — deliver zero.

## Adoption Considerations

**Strengths**:

- Zero-friction integration via hooks — no workflow changes needed
- Lossless on failure: `tee` mode preserves full output for debugging
- Measurable ROI via `rtk gain` analytics
- Effective on `ls` (72%), verbose `git log` (up to 98%), `docker ps` (75%)

**Risks**:

- Compression may remove context needed for complex debugging (mitigated by `tee`)
- Hook rewrite intercepting is opaque — Claude doesn't know outputs are compressed
- Third-party binary in the command path (security consideration for CI environments)
- **Savings claims overstate breadth**: independent testing shows ~22% in sandboxed CC, ~72% unsandboxed (inflated by `git log` truncation and large `ls`). `cat`, `grep`, `pytest`, `ruff` deliver 0% or negative

**Relevance to context management**: RTK addresses the same problem as CC's built-in context compaction but at the tool output layer rather than the conversation layer. The two approaches are complementary — RTK reduces input noise, CC's `/compact` reduces accumulated context.

## Recommendation

**Keep RTK installed.** Real savings on `ls` and verbose git output are free — the hook adds negligible latency. But set expectations: "Solid on `ls`/`git log`/`docker ps`; zero on `cat`/`grep`/`pytest`/`ruff`." The 80% headline does not hold under independent testing.

## Cross-References

- [CC-hooks-system-analysis.md](../cc-native/configuration/CC-hooks-system-analysis.md) — hooks system that RTK integrates with
- [CC-extended-context-analysis.md](../cc-native/context-memory/CC-extended-context-analysis.md) — context window management (complementary approach)
