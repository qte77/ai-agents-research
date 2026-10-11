### Added

- `docs/non-cc/reference/system-1-decision-models-landscape.md`: Cloudflare Clef / Clef-flash /
  clef-omni (Workers AI, launched 2026-10-01/10-09) as a fourth major-vendor Jev-style decision
  model, and Unsloth's "train your own decision model" path (`FastDecisionModel`/`DecisionTrainer`,
  v0.1.904-beta) as a new "Train your own" section connecting Clef's head design, Laya's local
  serving, and the `LocalLLaMA/typed-decisions` dataset. Reconciles Clef's launch blog claim of
  leading "the Jev Decision Index" against its own HF cards' "internal run" label, and the blog's
  10-benchmark table against the cards' wider table where Jev leads on general-reasoning rows
  (GPQA Diamond, MMLU-Pro, BBH). Narrows (without closing) the §4 Reranking gap with Clef's own
  nDCG@10 numbers on ToolRet and BRIGHT.
