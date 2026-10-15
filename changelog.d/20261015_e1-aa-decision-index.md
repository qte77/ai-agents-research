### Added

- `docs/non-cc/reference/system-1-decision-models-landscape.md`: the Artificial Analysis Decision
  Index v1.0 (third-party benchmark, launched 2026-10-13) — composition (four 25%-weighted evals:
  AA-Omniscience-Decision, HLE-MultiChoice, When2Call, WildGuardTest), the full 13-decision-model
  comparison table (cost, latency, sub-scores) reconciled against the live leaderboard's own
  embedded data (including its own `defaultSlugs` field, which distinguishes AA's "default" 11 from
  the 2 it excludes — Jev 1.13 and Clef-Flash), per-eval leaders, LLM baselines (Claude Haiku 5.5
  Low, GPT-6 Luna Low), and calibration notes from the launch article's own frozen snapshot.
  Explicitly distinguishes this from the unrelated community "Decision Index"
  (`multimodalart/jev-decision-index`) already cited for Perplexity's pplx-decider, Fastino's
  GLiDE, and Liquid AI's d1. Adds four decision models new to this corpus, named in the AA legend:
  GLiDE (Fastino Labs, a separate "thinking" model distinct from GLiNER2.5-Decide, confirmed via
  Fastino's own comparison-table post), Celeris-1 Decision (Celeris Labs, diffusion-based, hosted
  only — "no open weights and no fine-tuning in this release"), d1 (Liquid AI, hosted + open-weight
  `d1-3B`/`d1-omni-600M` under a custom `lfm1.0` license, plus the same-day `d1-ultra` launch, now
  the index's top scorer), and Mercury Decide (Inception Labs, hosted-only, documented only at
  `docs.inceptionlabs.ai`, no mention on the company's own homepage or blog). Flags a contrast
  between GLiDE's self-reported lead over Jev on the community index (64.81 vs. 57.91) and its
  materially different, lower score on the independent AA index (53.91, below either tracked Jev
  version).
