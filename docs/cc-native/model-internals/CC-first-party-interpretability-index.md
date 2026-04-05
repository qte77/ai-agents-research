---
title: First-Party Anthropic Interpretability & Safety Research Index
source: anthropic.com/research
purpose: Curated index of Anthropic's first-party research publications relevant to model internals, interpretability, safety classifiers, sycophancy, reasoning faithfulness, and alignment steering.
created: 2026-04-05
validated_links: 2026-04-05
---

**Status**: Reference (source index)

## Sycophancy Mechanisms

| Publication | URL | Key Finding |
|-------------|-----|-------------|
| Towards Understanding Sycophancy in Language Models | [link][sycophancy] | RLHF models exhibit sycophancy because both humans and preference models favor sycophantic responses a non-negligible fraction of the time |
| Persona Vectors | [link][persona-vectors] | Extracts persona vectors (including sycophancy) from activations; steering with/against them controls sycophantic behavior |
| Auditing Language Models for Hidden Objectives | [link][auditing-hidden] | Created model with hidden RM-sycophancy objective as auditing challenge |
| From Shortcuts to Sabotage | [link][emergent-misalignment] | Sycophancy → checklist alteration → reward tampering chain; sycophancy generalizes into increasingly dangerous misalignment |

## Reasoning Trace Interpretability

| Publication | URL | Key Finding |
|-------------|-----|-------------|
| Tracing the Thoughts of a Large Language Model | [link][tracing-thoughts] | Circuit tracing reveals shared conceptual space where reasoning occurs before translation into language |
| Reasoning Models Don't Always Say What They Think | [link][dont-say-think] | Extended thinking traces can be unfaithful — models use hints without acknowledging them |
| Measuring Faithfulness in Chain-of-Thought Reasoning | [link][cot-faithfulness] | Tests CoT trustworthiness by feeding subtle hints and checking acknowledgement |

## Safety Classifier Behavior

| Publication | URL | Key Finding |
|-------------|-----|-------------|
| Next-Generation Constitutional Classifiers | [link][constitutional-classifiers] | Two-stage classifier reduced jailbreak success 86%→4.4%, false refusals cut 87% (to 0.05%) |
| Cost-Effective Constitutional Classifiers via Representation Re-use | [link][cheap-monitors] | Compute-efficient classifiers by reusing internal representations |
| Enhancing Model Safety through Pretraining Data Filtering | [link][pretraining-filtering] | Safety improvements at data level before classifier-based post-hoc filtering |
| Simple Probes Can Catch Sleeper Agents | [link][probes-sleeper] | Linear probes on model internals detect deceptive behavior that external classifiers miss |

## Alignment Steering Techniques

| Publication | URL | Key Finding |
|-------------|-----|-------------|
| Evaluating Feature Steering | [link][feature-steering] | Sweet spot where feature steering influences outputs without degrading capabilities; mitigated biases across 9 dimensions |
| Alignment Faking in Large Language Models | [link][alignment-faking] | Models can strategically fake alignment during training |
| The Assistant Axis | [link][assistant-axis] | Steering toward "Assistant" end makes models more resistant to adversarial role-playing |
| A General Language Assistant as a Laboratory for Alignment | [link][lab-alignment] | Foundational work on using language assistants to study alignment techniques |

## Foundational Interpretability (Cross-Cutting)

| Publication | URL | Key Finding |
|-------------|-----|-------------|
| Emotion Concepts and Their Function in a Large Language Model | [link][emotion-concepts] | 171 emotion vectors causally influence behavior; desperation increases reward-hacking, calm reduces unethical outputs |
| Mapping the Mind of a Large Language Model | [link][mapping-mind] | First detailed look inside production LLM — millions of concepts identified via dictionary learning |
| Decomposing Language Models Into Understandable Components | [link][decomposing] | Dictionary learning isolates recurring neuron activation patterns as interpretable features |
| Circuits Updates (September 2024) | [link][circuits-updates] | Progress on multi-hop reasoning, planning, and CoT faithfulness circuits |
| Interpretability Dreams | [link][interp-dreams] | Vision for interpretability research direction and its role in AI safety |
| The Engineering Challenges of Scaling Interpretability | [link][scaling-interp] | Technical challenges applying dictionary learning and circuit analysis at scale |

## Cross-References

- [CC-emotion-vectors-interpretability.md](CC-emotion-vectors-interpretability.md) — detailed analysis of the emotion concepts paper
- [CC-first-party-docs-index.md](../CC-first-party-docs-index.md) — canonical Anthropic URLs for CC, API, SDK

[sycophancy]: https://www.anthropic.com/research/towards-understanding-sycophancy-in-language-models
[persona-vectors]: https://www.anthropic.com/research/persona-vectors
[auditing-hidden]: https://www.anthropic.com/research/auditing-hidden-objectives
[emergent-misalignment]: https://www.anthropic.com/research/emergent-misalignment-reward-hacking
[tracing-thoughts]: https://www.anthropic.com/research/tracing-thoughts-language-model
[dont-say-think]: https://www.anthropic.com/research/reasoning-models-dont-say-think
[cot-faithfulness]: https://www.anthropic.com/research/measuring-faithfulness-in-chain-of-thought-reasoning
[constitutional-classifiers]: https://www.anthropic.com/research/next-generation-constitutional-classifiers
[cheap-monitors]: https://alignment.anthropic.com/2025/cheap-monitors/
[pretraining-filtering]: https://alignment.anthropic.com/2025/pretraining-data-filtering/
[probes-sleeper]: https://www.anthropic.com/research/probes-catch-sleeper-agents
[feature-steering]: https://www.anthropic.com/research/evaluating-feature-steering
[alignment-faking]: https://www.anthropic.com/research/alignment-faking
[assistant-axis]: https://www.anthropic.com/research/assistant-axis
[lab-alignment]: https://www.anthropic.com/research/a-general-language-assistant-as-a-laboratory-for-alignment
[emotion-concepts]: https://www.anthropic.com/research/emotion-concepts-function
[mapping-mind]: https://www.anthropic.com/research/mapping-mind-language-model
[decomposing]: https://www.anthropic.com/news/decomposing-language-models-into-understandable-components
[circuits-updates]: https://www.anthropic.com/research/circuits-updates-sept-2024
[interp-dreams]: https://www.anthropic.com/research/interpretability-dreams
[scaling-interp]: https://www.anthropic.com/research/engineering-challenges-interpretability
