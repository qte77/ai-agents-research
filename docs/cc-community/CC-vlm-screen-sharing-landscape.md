---
title: VLM Screen-Sharing Landscape for Claude Code
purpose: Survey of Vision Language Models, local runtimes, image token math, and architecture patterns for integrating screen-sharing / visual-context workflows with Claude Code.
status: research
platform_scope: [claude-code]
created: 2026-04-11
updated: 2026-11-26
validated_links_on: 2026-06-26
---

## What It Is

This doc surveys the option space for giving Claude Code visual context from a user's screen — either via Claude's own vision API or by running a small local Vision Language Model (VLM) and forwarding its text output. It is a **neutral catalogue**, not a recommendation. Readers pick a point on the tradeoff curve based on their token budget, privacy constraints, platform, and latency tolerance.

For an observed plugin integration, see the [Observed implementations](#observed-implementations) section at the end.

## Small VLM Landscape (≤ ~4B parameters)

The following models are the main candidates for local-VLM workflows on developer laptops as of 2026-04. Parameter counts come from the Hugging Face model card; names can mislead (e.g. Qwen2.5-VL-3B's card reports 4B total params).

| Model | Params | License | Released | Strengths (from model card) |
| ----- | ------ | ------- | -------- | --------------------------- |
| [Qwen2.5-VL-3B][qwen25-vl] | 4B (card) | See card | Jan 2025 | OCR, UI agent (ScreenSpot 55.5), DocVQA 93.9, video understanding |
| [Qwen3-VL-2B][qwen3-vl] | 2B | Apache-2.0 | Dec 2025 | 256K native context, OCR 32 languages, GUI agent, code gen from images |
| [LFM2-VL-3B][lfm2-vl] | ~3B (2.6B lang + 400M vision) | LFM Open License v1.0 | Nov 2025 | MMStar 57.73, RealWorldQA 71.37, OCRBench 822, hybrid conv+attention |
| [SmolVLM-500M][smolvlm] | 500M | Apache-2.0 | — | DocVQA, image captioning, ~1.23 GB GPU RAM, Idefics3-based |
| [GOT-OCR2][got-ocr2] | Not in card | Apache-2.0 | — | Plain + formatted OCR, LaTeX render, multi-crop, multilingual |
| [Moondream2][moondream2] | 2B | Apache-2.0 | — | ScreenSpot F1@0.5 = 80.4, DocVQA 79.3, object detection, grounded reasoning |
| [PaddleOCR-VL-0.9B][paddleocr-vl] | 0.9B | Apache-2.0 | Oct 2025 | OmniDocBench v1.5 SOTA, 109 languages, tables/formulas/charts |
| [GLM-OCR-0.9B][glm-ocr] | 0.9B | MIT | Mar 2026 | OmniDocBench v1.5 94.62 (#1), olmOCR-bench 75.2, CogViT + GLM-0.5B |

Licenses differ — LFM2-VL-3B in particular uses Liquid AI's own "LFM Open License v1.0", not Apache-2.0. Verify license terms on the model card before production use.

**Long-document OCR / document parsing (edge of scope).** [baidu/Unlimited-OCR][unlimited-ocr] (MIT) targets *one-shot long-horizon parsing* — multi-page documents and PDFs in a single inference pass (32K-token context; `gundam`/`base` modes; HF Transformers + SGLang; OpenAI-compatible streaming), building on DeepSeek-OCR. [opendatalab/MinerU][mineru] (MinerU Open Source License, Apache-2.0-based) is the broader sibling — PDFs/DOCX/PPTX/XLSX/images → LLM-ready Markdown/JSON *for agentic workflows* (dual VLM + OCR engines, 109 languages, formulas→LaTeX, tables→HTML), shipping a Model Context Protocol (MCP) server usable from Claude Desktop/Cursor plus LangChain/LlamaIndex integrations. Both are document-parsing tools rather than screen-context VLMs, so they sit at the edge of this doc's scope — noted here for the visual-OCR-subagent routing pattern below. Deeper scraping / document-extraction tooling lives in this repo's single-source-of-truth catalog, [web-scraping-extraction-landscape.md](../non-cc/infrastructure/web-scraping-extraction-landscape.md).

## Local VLM Runtimes

Options for running a local VLM on a developer laptop. All four are MIT-licensed OSS. Pick based on platform, deployment model (in-process vs. server), and whether you want an OpenAI-compatible HTTP surface.

| Runtime | VLM support | Platform | Deployment model |
| ------- | ----------- | -------- | ---------------- |
| [llama-cpp-python][llamacpp-py] | LLaVA v1.5/v1.6, Moondream2, Nanollava, Llama-3-Vision-Alpha, MiniCPM-V, Qwen2.5-VL | Linux / macOS / Windows | In-process Python bindings OR OpenAI-compatible web server |
| [llama.cpp][llamacpp] | Same as above (upstream) | Linux / macOS / Windows | Native C++ binary; includes standalone `server` |
| [Ollama][ollama] | Multimodal models supported via library | Linux / macOS / Windows | HTTP REST API server; model management via CLI |
| [mlx-vlm][mlx-vlm] / [MLX][mlx] | VLMs optimized for Apple Silicon | macOS only (Apple Silicon) | Python library; native Metal acceleration |

The in-process Python path (llama-cpp-python) keeps everything in one process, at the cost of coupling your tool's runtime lifecycle to the model's. HTTP-server paths (Ollama, llama.cpp server, llama-cpp-python's bundled server) decouple model lifetime from callers at the cost of inter-process overhead. Pick per your constraint.

## Claude Code Image Token Economics

All numbers below are from the [official Anthropic vision documentation][anthropic-vision]. These govern Tier 1 (CC-native vision) cost.

**Token formula** (when the image is not auto-resized; patch-based per the vision docs, checked 2026-11-26, replacing the earlier width x height / 750 formula):

```text
tokens = ceil(width_px / 28) * ceil(height_px / 28)   # one visual token per 28x28 px patch
```

**Resize limits** (two tiers, automatic, no beta header; checked 2026-11-26): the high-resolution tier (Claude 4.7 and later) allows a 2,576 px long edge and 4,784 visual tokens; the standard tier (all other models) allows 1,568 px and 1,568 visual tokens. Images over either limit are downscaled while preserving aspect ratio. Downscaling increases time-to-first-token with no benefit to output quality (earlier-read claim, not re-confirmed).

**Minimum edge**: the docs now say Claude may hallucinate or make mistakes on low-quality, rotated, or very small images under 200 pixels.

**Hard rejection**: images larger than 8000×8000 px are rejected. Above 20 images in one request a stricter per-image limit applies (the docs advise keeping each dimension at or below 3,000 px, or using 20 or fewer image and document blocks); the earlier 2000×2000 figure is no longer stated. Per-request caps: 100 images for models with a 200k-token context window, 600 otherwise; 10 MB base64 per image on the Claude API (5 MB on Amazon Bedrock).

**Sizing advice**: the earlier "1.15 megapixel, within 1568 px" recommendation and the Sonnet 4.6 aspect-ratio ceiling table are no longer on the vision page (checked 2026-11-26), which instead advises downsampling before sending when the extra fidelity isn't needed and notes high-resolution images can use up to about 3x the visual tokens of a standard-tier model; the 1.15 MP figure below is therefore unverified. Example downsizing: 1920×1080 goes to 1456×819 on the standard tier and stays unresized on the high-resolution tier.

**Example token counts** (from the docs, checked 2026-11-26; the earlier Sonnet 4.6 dollar figures are not stated by the docs and are dropped as unverified):

| Image size | Tokens |
| ---------- | ------ |
| 200×200 px (0.04 MP) | 64 |
| 1000×1000 px (1 MP)  | 1,296 |
| 1092×1092 px (1.19 MP) | 1,521 |

The docs' worked costs: at Claude Haiku 4.5's $1 per million input tokens, a 1000×1000 image is about $1.30 per 1k images; at Claude Opus 5.5's $4 per million on the high-resolution tier, about $5.18 per 1k, and a 4K image about $19.14 per 1k.

Supported image formats: JPEG, PNG, GIF, WebP. Token cost is pixel-based, so format choice does not affect cost (only upload size).

## Architecture Tiers

Three architecture patterns for integrating visual context with Claude Code, presented as a tradeoff curve.

| Tier | Approach | Token footprint | Privacy | Winning use case |
| ---- | -------- | --------------- | ------- | ---------------- |
| 1. CC-native vision   | Capture → resize to ≤ 1.15 MP → send as image block to Claude | Per formula above; 1,521 tokens / 1092² image | Sent to Anthropic API | You already pay for Claude tokens; minimum complexity |
| 2. Local VLM → text   | Capture → local VLM inference → text description → Claude text request | Only the text output tokens | Vision is fully local | Heavy visual workloads; sensitive screen content |
| 3. Hybrid             | Local VLM preprocessing + a compressed image sent to Claude for deeper reasoning | Mixed | Partial local | Want both local preprocessing and Claude's vision |

None of these is strictly better. Tier 1 wins on simplicity; Tier 2 wins on token budget and privacy; Tier 3 trades complexity for a middle ground. The [Claude Code Feature Requests](#claude-code-feature-requests--gaps) section notes a structural gap relevant to Tier 1 (real-time streaming).

## Screen Capture and MCP Servers

For Tier 2 / Tier 3 pipelines, a screen-capture primitive is needed. The two tools below are verified via their repositories; others in this category exist but are not cataloged here pending verification.

| Tool | License | Platform | Notes |
| ---- | ------- | -------- | ----- |
| [python-mss][python-mss] | MIT | Windows / macOS / Linux | Ctypes-based screenshot library; no runtime dependencies, thread-safe; integrates with NumPy / OpenCV / PIL |
| [Peekaboo][peekaboo] | MIT | macOS only (15.0+) | CLI **and** MCP server; supports multiple VLM providers including local Ollama, OpenAI, Anthropic, Gemini, xAI |

Peekaboo is one example of a screen-capture MCP server that delegates VLM inference to an external provider (local or remote) rather than hosting its own model. See the [gaps](#claude-code-feature-requests--gaps) section below for the open slot.

## Claude Code Feature Requests & Gaps

Three FRs on the `anthropics/claude-code` issue tracker are relevant to visual context workflows. All are first-party sources.

| FR | Status (2026-04-11) | What it asks for |
| -- | ------------------- | ---------------- |
| [anthropics/claude-code#22903][cc-22903] | **CLOSED — NOT_PLANNED** (closed 2026-03-05, locked 2026-03-12) | Bidirectional real-time visual streaming via CLI pipes (`ffmpeg -f x11grab \| claude --visual-in …`) |
| [anthropics/claude-code#38698][cc-38698] | **OPEN** | Per-agent model provider routing (e.g. route subagents to local Ollama while keeping orchestrator on Anthropic) |

**Structural gaps** (as of 2026-04-11):

1. **No native CC real-time streaming** — FR #22903 was closed as not planned. Any screen-sharing workflow has to pull-capture (periodic screenshots) rather than push-stream.
2. **No VLM-native MCP server with local inference** — existing screen-capture MCP servers delegate to external VLM providers. A server that both hosts a small local VLM and exposes screen analysis via MCP is an open slot.
3. **No per-agent provider routing** — FR #38698 remains open. Mixing a local VLM for cheap visual passes and Claude for reasoning within a single session requires out-of-band routing tooling.

## Claude Code Routing Options (for LLM-agnostic flows)

If a workflow needs to route different tasks (e.g. visual OCR vs. code generation) to different model providers within a single Claude Code session, the current community answer is an external router. [claude-code-router][cc-router] (~38.4K stars as of 2026-11-26, multi-provider) is the most prominent example; it sits in front of Claude Code and routes requests per task to OpenRouter, DeepSeek, Ollama, Gemini, and others. See [CC-model-provider-configuration.md][cc-router-config] for setup and the full routing-scenario list.

Using a router is orthogonal to the VLM landscape above — a Tier 2 workflow could route visual-OCR subagents to local Ollama and reasoning subagents to Anthropic, without waiting for FR #38698.

## Related: Computer-Use Agents

This doc covers feeding screens to a VLM for context, not agents that act on the GUI. For computer-use models, the OSWorld benchmarks and safety guidance see [computer-use-agents-landscape.md](../non-cc/agents/computer-use-agents-landscape.md).

## Observed Implementations

- [qte77/cc-voice-plugin-prototype][cc-voice] — plugin integration demonstrating a Tier 2 pipeline (local VLM → text) for a voice-driven CC workflow. See the repo's own docs and ADRs for the specific model / runtime / resize choices adopted there.
- [StarTrail-org/PixelRAG][pixelrag] — **pixel-native RAG**: renders pages/PDFs to image tiles and retrieves by visual similarity with a fine-tuned [Qwen3-VL][qwen3-vl]-Embedding model, skipping text parsing entirely. Ships a Claude Code **`pixelbrowse`** plugin (`claude plugin install pixelbrowse@pixelrag-plugins`) — a skill calling `pixelshot` (Playwright/CDP) via a `/screenshot <url>` command; no MCP server or backend. A Tier 1 (CC-native plugin) visual-retrieval pattern, distinct from the Tier 2 local-VLM→text prototype above. ~11k★ (v0.4.0, 2026-07-16; checked 2026-11-26); the `pixelbrowse` plugin and install-command claims were not re-checked against the README (unverified).

## Sources

| Source | Content |
| ------ | ------- |
| [Anthropic vision documentation][anthropic-vision] | Token formula, resize thresholds, format support, recommended sizes, cost tables |
| Model cards listed in the Small VLM Landscape table above | Parameter counts, licenses, release dates, benchmark scores |
| [baidu/Unlimited-OCR][unlimited-ocr] | Long-document OCR VLM — one-shot multi-page/PDF parsing (MIT) |
| [opendatalab/MinerU][mineru] | Document (PDF/Office/image)→Markdown/JSON extraction for agentic workflows; MCP server (Claude Desktop/Cursor) |
| [llama.cpp][llamacpp], [llama-cpp-python][llamacpp-py], [Ollama][ollama], [MLX][mlx] | Runtime capability and VLM support |
| [python-mss][python-mss], [Peekaboo][peekaboo] | Screen capture primitives |
| [anthropics/claude-code#22903][cc-22903], [anthropics/claude-code#38698][cc-38698] | First-party feature-request status |
| [claude-code-router][cc-router] | Community routing layer |
| [StarTrail-org/PixelRAG][pixelrag] | Pixel-native Retrieval-Augmented Generation (RAG) + Claude Code `pixelbrowse` plugin (Qwen3-VL-Embedding) |

[anthropic-vision]: https://platform.claude.com/docs/en/build-with-claude/vision
[qwen25-vl]: https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct
[qwen3-vl]: https://huggingface.co/Qwen/Qwen3-VL-2B-Instruct
[lfm2-vl]: https://huggingface.co/LiquidAI/LFM2-VL-3B
[smolvlm]: https://huggingface.co/HuggingFaceTB/SmolVLM-500M-Instruct
[got-ocr2]: https://huggingface.co/stepfun-ai/GOT-OCR2_0
[moondream2]: https://huggingface.co/vikhyatk/moondream2
[paddleocr-vl]: https://huggingface.co/PaddlePaddle/PaddleOCR-VL
[glm-ocr]: https://huggingface.co/zai-org/GLM-OCR
[unlimited-ocr]: https://github.com/baidu/Unlimited-OCR
[mineru]: https://github.com/opendatalab/MinerU
[llamacpp]: https://github.com/ggml-org/llama.cpp
[llamacpp-py]: https://github.com/abetlen/llama-cpp-python
[ollama]: https://github.com/ollama/ollama
[mlx]: https://github.com/ml-explore/mlx
[mlx-vlm]: https://github.com/Neywa-Labs/mlx-vlm
[python-mss]: https://github.com/BoboTiG/python-mss
[peekaboo]: https://github.com/openclaw/Peekaboo
[cc-22903]: https://github.com/anthropics/claude-code/issues/22903
[cc-38698]: https://github.com/anthropics/claude-code/issues/38698
[cc-router]: https://github.com/musistudio/claude-code-router
[cc-router-config]: ../cc-native/configuration/CC-model-provider-configuration.md
[cc-voice]: https://github.com/qte77/cc-voice-plugin-prototype
[pixelrag]: https://github.com/StarTrail-org/PixelRAG
