---
title: Corpus update + new-sources arc — backlog drain, fresh mining, stale-fact refresh
status: approved
issue: 374
created: 2026-07-23
updated: 2026-07-23
---

**Status**: Reference (plan)

Two workstreams decided 2026-07-23: (1) **add new sources** from three channels — the
[#374](https://github.com/qte77/ai-agents-research/issues/374) scout backlog, fresh triage/rxiv
mining, owner-supplied URLs; (2) **update the corpus** — stale-fact refresh + open trackers
[#383](https://github.com/qte77/ai-agents-research/issues/383)/[#382](https://github.com/qte77/ai-agents-research/issues/382)
and [#321](https://github.com/qte77/ai-agents-research/issues/321). Graph rebuild happens **once,
at the end** (full uniform rebuild only — never partial-update; see AGENT_LEARNINGS).

## Source map

### Channel 1 — #374 scout backlog (13 items, placements pre-decided)

Dup-checks executed 2026-07-23 (calibrated `git grep`, 12 known hits for control term): all four
flagged items hit only the auto-generated `docs/research/rxiv-agentic-papers.md` → resolution is
**extend the named landscape, no new doc**.

| Item | Action | Target |
|---|---|---|
| parry (prompt-injection scanner) | new/extend | `docs/cc-community/` |
| Dippy (auto-approve safe bash) | new/extend | `docs/cc-community/` |
| sudocode (agent-orchestration DSL) | new/extend | `docs/cc-community/` |
| cc-sessions (production session tool) | new/extend | `docs/cc-community/` |
| AB Method | **extend** | `docs/non-cc/spec-driven-frameworks-landscape.md` |
| MOSS (arXiv 2605.22794) | new | `docs/non-cc/` |
| When Errors Become Narratives (2606.14589) | new | `docs/sdlc-lcm/` |
| Sovereign Execution Brokers (2606.20520) | new | `docs/sdlc-lcm/` |
| LedgerAgent (2606.20529) | new | `docs/sdlc-lcm/` |
| Every Eval Ever (2606.14516) | **extend** | `docs/sdlc-lcm/evaluation-data-resources-landscape.md` |
| Contagion Networks (2606.20493) | **extend** | `docs/sdlc-lcm/mas-benchmarking-best-practices.md` |
| Probe-and-Refine Tuning (2606.20512) | new | `docs/cc-native/context-memory/` |
| Perplexity Computer study (2606.07489) | **extend** | `docs/non-cc/research-agents-landscape.md` |

"new/extend" for CC tools: default is extending
`docs/cc-community/CC-community-tooling-landscape.md`; a standalone
`CC-<tool>-analysis.md` only if first-party research shows analysis depth (per
prefer-extending convention).

### Channel 2 — fresh mining (scout DONE 2026-07-23, awaiting owner OK)

Swept: `triage/` 2026-07-20 outputs + rxiv index W22–W25 (W25 = newest, late-June 2026).
Changelog-triage and outage archive yielded no new-source candidates (CC's own feature stream →
routes to existing cc-native doc updates, not new docs). All 15 candidates grep-verified
zero-coverage (index stubs in `rxiv-agentic-papers.md` don't count as coverage).

| # | Candidate | Placement |
|---|---|---|
| T1.1 | Probabilistic Verification for AI Agents (2606.20510) | `sdlc-lcm/` new |
| T1.2 | Defensive Misdirection vs automated attacks (2606.20470) | extend `sdlc-lcm/agentic-ai-vulnerability-landscape.md` |
| T1.3 | DoS on LLM Agent Guardrails (2606.14517) | extend `sdlc-lcm/agentic-ai-vulnerability-landscape.md` |
| T1.4 | Code-Correctness Signals in Hidden States (2606.14530) | `cc-native/model-internals/` |
| T1.5 | Hierarchical Recovery, Cross-Device Agents (2606.20487) | extend `non-cc/agent-frameworks-infrastructure-landscape.md` |
| T2.1 | MemoryWAM (2606.20562) | `non-cc/agent-frameworks-infrastructure-landscape.md` |
| T2.2 | Marginal Advantage Accumulation (2606.20475) | `non-cc/agent-frameworks-infrastructure-landscape.md` |
| T2.3 | StreamMemBench (2606.14571) | extend `sdlc-lcm/agent-evaluation-metrics-landscape.md` |
| T2.4 | UltraQuant 4-bit KV caching (2606.20474) | extend `non-cc/kv-cache-serving-landscape.md` |
| T2.5 | Multi-LCB / LiveCodeBench multi-lang (2606.20517) | extend `sdlc-lcm/mas-benchmarking-best-practices.md` |
| T2.6 | SIMMER latent-planning-failure bench (2606.14574) | `sdlc-lcm/agent-evaluation-metrics-landscape.md` |
| T3.1 | Execution-State Capsules (2606.20537) | `non-cc/` (robotics-flavored, low priority) |
| C1 | roampal-core (memory MCP for CC) | `cc-community/` — **URL truncated in triage, re-resolve from live awesome-claude-code** |
| C2 | cc-costline (spend statusline) | `cc-community/` — URL truncated, re-resolve |
| C3 | agents-md-cookbook (AGENTS.md templates) | `cc-community/` — URL truncated, re-resolve |

### Channel 3 — owner URLs (gate, non-blocking) + multi-account ask (scout DONE)

Owner drops URLs anytime; batch runs when they land.

**Multi-account CC research (2026-07-23, verified first-party + `gh api` repo metadata):**
mechanism = `CLAUDE_CONFIG_DIR` per shell → N independent `claude` processes with independent
`.credentials.json`; no native profile switcher (upstream FRs #44687/#35856/#64376/#37554 open).
Tools: **claude-swap** (realiti4, 1,276★, pushed 2026-07-23, MIT — concurrent + rate-limit
rotation + usage TUI; top pick), claude-multiprofile (42★, adds Claude Desktop via
`--user-data-dir`), claude-code-profiles (56★, sequential switching, not the concurrency case),
claude-multisession (1★, stale), manual alias/direnv gists. Intake items (folded into A2-B1):

- NEW `docs/cc-community/CC-multi-account-switching-landscape.md` — mechanism + tool table
  (distinct category from `CC-usage-tooling-landscape.md` = cost observability)
- EXTEND `docs/cc-native/configuration/CC-env-vars-reference.md` — add `CLAUDE_CONFIG_DIR`
  (verified zero-coverage gap, `git grep -c` 2026-07-23)
- Cross-ref from `CC-model-provider-configuration.md:260` (CLIProxyAPI = gateway-level
  multi-account quota harvesting) → new landscape (native CLI multi-account) to disambiguate

## Phases

### Phase A — intake (agent-only, one PR per topic batch)

- [x] A1: dup-checks (4/4) + both scouts fired AND reported (2026-07-23; findings persisted above)
- [ ] A2-B1: cc-community CC tools — parry, Dippy, sudocode, cc-sessions, AB Method +
      multi-account trio (new landscape, env-vars extend, model-provider cross-ref)
- [ ] A2-B2: sdlc-lcm papers — Errors-Narratives, Sovereign Execution Brokers, LedgerAgent (new);
      Every Eval Ever, Contagion Networks (extends)
- [ ] A2-B3: non-cc + cc-native — MOSS (new), Perplexity Computer (extend), Probe-and-Refine (new)
- [ ] A2-B4: mined shortlist — owner APPROVED ALL 15 (2026-07-23): T1 (5) + T2 (6) + T3 (1) +
      CC tools C1–C3 (URLs re-resolved from live awesome-claude-code first)
- [ ] A2-B5: owner URLs (when supplied)

**Done-when per source**: first-party verified (license from LICENSE, counts from live README) ·
Sources table + reference-style links · both subdir README and `cc-native/README.md` counts (where
applicable) · changelog fragment · `make lint` green · squash-merged.

### Phase B — corpus update

- [ ] Stale-fact refresh — target cohort identified 2026-07-23: 27 live docs with
      `validated_links: 2026-03-*` (`git grep -l "validated_links: 2026-03" -- docs/`, minus 2
      `docs/archive/` files which stay frozen). Link liveness is already covered by the weekly
      link-rot monitor — the refresh targets **content drift**. Priority order: CC vendor-behavior
      docs first (CC ships weekly): `configuration/CC-fast-mode-analysis.md`,
      `CC-bash-mode-analysis.md`, `CC-hooks-system-analysis.md`, the `sandboxing/` trio,
      `sessions/CC-session-cost-analysis.md`, `ci-remote/CC-cloud-sessions-analysis.md`,
      `plugins-ecosystem/CC-connectors-overview.md` + `CC-chrome-extension-analysis.md`; then the
      remaining cohort. Per doc: re-fetch first-party page, update version gates, bump `updated:`
      (+`validated_links:` if lychee re-run)
- [ ] Tracker #383/#382: on-device semantic-search landscape (new doc, Technology-Radar verdicts)
- [ ] Tracker #321: spec-frameworks follow-ups (surgical adds)

### Phase C — close-out

- [ ] Graph rebuild: `/graphify` full uniform rebuild (scope `docs/` only) + `make graph-page`,
      commit `ui/graph.html` — only if Phase A landed substantial new *concept* content
- [ ] Advance #374 (check off shipped backlog items; close if drained), advance/close #383, #321
- [ ] Update this plan `status: done`

## Standing decisions & watch-outs

- **Own/bot PRs+issues only** (owner directive 2026-07-23): foreign-authored issues/PRs → ask
  owner first, never autonomous triage.
- Extend-over-create for the 4 dup-flagged items (decided, above).
- Verify subagent findings with own `git grep` + `Read` before acting (read-discipline).
- Never fire two same-day `rxiv-paper-eval` dispatches (CONTRIBUTING).
- Lychee flakes: known intermittents (skywork.ai, cohere.com/rerank) — do not add excludes.
- Merge routine: squash-merge; owner `--admin` for signature gate; serialize via update-branch.
