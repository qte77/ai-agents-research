---
title: On-Device / Local-First Semantic Search Landscape
purpose: Survey of the embedder + embedded-vector-store stack for local-first semantic search — ternlight (Hold) as trigger, the Python-native scalable alternatives (Assess), and the decouple-the-layers lesson.
category: landscape
created: 2026-07-23
updated: 2026-07-23
validated_links: 2026-07-23
---

**Status**: Assess

> Promoted from tracker [#383][gh-383] (research completed there 2026-07-12; durable
> doc requested in the 2026-07-23 corpus-update arc). [#382][gh-382] tracks how this
> informs the `azure-doc-workflows` semantic-search feature
> (`azure-doc-workflows#165` — private repo, not hyperlinked).

## What It Is

A survey of tooling for **local-first / on-device semantic search** — the *embedder +
vector-store* stack behind "search my corpus by meaning" **without** a managed vector
DB. Anchored on **ternlight** (the trigger) and broadened to the Python-native,
embedded options that scale. The recurring lesson: ternlight fuses "embedder +
brute-force scan" into one WASM blob — the durable pattern is to **decouple the two
layers** and pick each independently. Per-item Technology-Radar verdicts below:
**Hold** for ternlight, **Assess** for the Python-native stack.

## Trigger: ternlight — Hold

[soycaporal/ternlight][ternlight] ([demo][ternlight-demo]) — on-device semantic
embeddings in a 5–7 MB WASM bundle. Ternary-quantized (BitNet b1.58) 2-layer
transformer distilled from `all-MiniLM-L6-v2`; runs on CPU **in the browser** (SIMD
WASM), no API/GPU. `embed()` → 384-dim (base) / 256-dim (mini); `similar(query, docs,
{topK})` = brute-force cosine. npm `@ternlight/base` (7.2 MB) / `@ternlight/mini`
(5.0 MB). MIT.

- **Quality** vs teacher `all-MiniLM-L6-v2`: base Spearman **0.844** / SciFact
  NDCG@10 **0.465**; mini **0.820** / **0.439** ("~30× compression, modest accuracy
  drop"). Latency ~5 ms/embed (base).
- **Verdict — Hold.** Impressive in-browser demo, but: **JS/WASM-only** (not
  reachable from a Python backend), **no ANN index** (brute-force O(n)),
  **128-token cap**, and **English-teacher distillation**. Fits pure client-side,
  zero-install search only.

## Layer A — Local Embedders (Python, CPU, no API) — Assess

| Tool | What | Runtime | Multilingual (de/en) | License |
|---|---|---|---|---|
| [fastembed][fastembed] (Qdrant) | ONNX embedder, no torch/CUDA | Python | via `multilingual-e5` / `bge-m3` | Apache-2.0 |
| [sentence-transformers][sbert] | de-facto encoder family | Python (torch) | `paraphrase-multilingual-MiniLM-L12-v2` | Apache-2.0 |
| [model2vec / potion][model2vec] (Minish Lab) | static embeddings, pure-NumPy inference, fastest on CPU (~94.7% of MiniLM quality) | Python | `potion-multilingual-128M` | MIT |
| [Transformers.js][transformers-js] | in-browser/Node ONNX (the ternlight-style runtime) | JS (not Python) | model-dependent | Apache-2.0 |

## Layer B — Embedded Vector Stores (scale past brute-force) — Assess

| Tool | Embedded | Python | ANN | License |
|---|---|---|---|---|
| [FAISS][faiss] (Meta) | yes | yes | Flat/IVF/HNSW/PQ | MIT |
| [usearch][usearch] (Unum) | yes (single-file) | yes | HNSW | Apache-2.0 |
| [hnswlib][hnswlib] | yes (header-only) | yes | HNSW (+deletes) | Apache-2.0 |
| [LanceDB][lancedb] | yes (serverless) | yes | IVF-PQ + SQL/FTS filter | Apache-2.0 |
| [Chroma][chroma] `PersistentClient` | yes | yes | HNSW | Apache-2.0 |
| [Qdrant local mode][qdrant-client] | yes (`:memory:`/path) | yes | HNSW | Apache-2.0 |
| [DuckDB `vss`][duckdb-vss] | yes | yes | HNSW (uses usearch) | MIT |
| [sqlite-vec][sqlite-vec] | yes | yes | ⚠️ **brute-force only today** | Apache-2.0/MIT |
| [Voy][voy] | yes (WASM) | no (JS) | k-d tree | MIT/Apache-2.0 |

**Key gotcha:** `sqlite-vec` is **brute-force only** today — ANN is roadmap, not
shipped ([asg017/sqlite-vec#25][sqlite-vec-25]). It does **not** buy scale over a
naive scan. For SQLite-native ANN, use `usearch` or the `Vec1` extension instead.

## Multimodal (indexing VLM / image outputs) — Assess

Two strategies: (1) embed the VLM **text** description/keywords with a Layer-A
encoder — simplest, one vector space, keep the image as linked metadata; (2) embed
the **image** with a CLIP-style model for true visual similarity — a second vector
space, ~2× embed/index maintenance. **Start text-first**; add visual only on a
concrete "find visually similar images" need.

- [OpenCLIP][openclip] · [SigLIP2][siglip2] (multilingual) ·
  [Azure AI Vision multimodal embeddings][azure-vision] (managed API)

## Recommended Stack (Python, local-first, scalable)

`fastembed` (`multilingual-e5-small`) or `sentence-transformers` → **LanceDB**
(embedded IVF-PQ + metadata filtering) — or **Chroma `PersistentClient`** as the
simpler fallback; **FAISS/usearch** if you want just an index, no store. Where
residency allows a managed path: **Azure OpenAI embeddings → Azure AI Search** (the
residency-aware gate `azure-doc-workflows#165` proposes).

## Where Each Wins

- **ternlight**: pure in-browser, zero-install, no Python runtime, no model-download
  step.
- **The Python stack**: real ANN at thousands–millions of items, native to a
  Python/Streamlit backend, and de/en multilingual — the three places ternlight's
  O(n) brute-force + JS/WASM runtime become the bottleneck.

## Cross-References

- [CC-memory-tooling-landscape.md](../cc-community/CC-memory-tooling-landscape.md) —
  CC-side persistent-memory tools (several embed + retrieve internally; this doc
  covers the underlying local stack)
- [agent-frameworks-infrastructure-landscape.md §7](agent-frameworks-infrastructure-landscape.md)
  — RAG & retrieval infrastructure (hosted/managed side)

## Sources

| Source | Content |
|---|---|
| [ternlight][ternlight] · [demo][ternlight-demo] | Trigger tool: WASM ternary embedder (first-party README, npm sizes, quality table) |
| [fastembed][fastembed] · [sentence-transformers][sbert] · [model2vec][model2vec] · [Transformers.js][transformers-js] | Layer-A embedders (first-party repos/docs) |
| [FAISS][faiss] · [usearch][usearch] · [hnswlib][hnswlib] · [LanceDB][lancedb] · [Chroma][chroma] · [Qdrant client][qdrant-client] · [DuckDB vss][duckdb-vss] · [sqlite-vec][sqlite-vec] · [Voy][voy] | Layer-B embedded stores (first-party repos/docs) |
| [asg017/sqlite-vec#25][sqlite-vec-25] | sqlite-vec ANN = roadmap-only confirmation |
| [OpenCLIP][openclip] · [SigLIP2][siglip2] · [Azure AI Vision][azure-vision] | Multimodal encoders |
| [#383][gh-383] (research 2026-07-12) | Original survey + Radar verdicts this doc promotes |

[ternlight]: https://github.com/soycaporal/ternlight
[ternlight-demo]: https://ternlight-demo.vercel.app/
[fastembed]: https://github.com/qdrant/fastembed
[sbert]: https://www.sbert.net/docs/sentence_transformer/pretrained_models.html
[model2vec]: https://github.com/MinishLab/model2vec
[transformers-js]: https://github.com/huggingface/transformers.js
[faiss]: https://github.com/facebookresearch/faiss
[usearch]: https://github.com/unum-cloud/usearch
[hnswlib]: https://github.com/nmslib/hnswlib
[lancedb]: https://github.com/lancedb/lancedb
[chroma]: https://github.com/chroma-core/chroma
[qdrant-client]: https://github.com/qdrant/qdrant-client
[duckdb-vss]: https://duckdb.org/docs/current/core_extensions/vss
[sqlite-vec]: https://github.com/asg017/sqlite-vec
[sqlite-vec-25]: https://github.com/asg017/sqlite-vec/issues/25
[voy]: https://github.com/tantaraio/voy
[openclip]: https://github.com/mlfoundations/open_clip
[siglip2]: https://huggingface.co/google/siglip2-base-patch16-224
[azure-vision]: https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/concept-image-retrieval
[gh-383]: https://github.com/qte77/ai-agents-research/issues/383
[gh-382]: https://github.com/qte77/ai-agents-research/issues/382
