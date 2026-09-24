---
title: HarnessRouter Analysis
source: https://github.com/HarnessRouter/harnessrouter
purpose: Unified multi-harness API for AI coding-agent backends (Codex, Claude Code, Hermes, DeepSeek Harness, Pi) — architecture, protocol, and fit with this corpus's agent-integration research.
created: 2026-09-24
updated: 2026-09-24
validated_links: 2026-09-24
platform_scope: [claude-code, codex, hermes, deepseek-harness, pi]
---

**Status**: Assess

## What It Is

[HarnessRouter][repo] positions itself as "the unified interface for agent harnesses" — a single
API that lets an application drive multiple AI coding-agent backends (**harnesses**) without a
bespoke integration per backend. Per the repo description and README, it unifies **Codex, Claude
Code, Hermes, Pi, and DSH (DeepSeek Harness)**, with individual harness CLIs installing
automatically on first launch. It ships as **HarnessRouter Community Edition**, self-hosted under
**Apache-2.0** ([`gh api repos/HarnessRouter/harnessrouter`][repo], verified 2026-09-24: license
`Apache-2.0`, 2,496 stars, latest release `v0.23.11` (2026-09-23), repo created 2026-08-09,
actively pushed same day as this check). The repo's own description calls it "the self-hosted,
Apache-2.0 edition of the unified interface for agent harnesses," implying a separate hosted tier;
a managed **HarnessRouter Cloud** offering is described on the project's marketing site
([harnessrouter.ai][site]), whose specifics are marketing-only and out of scope for the
self-hosted analysis here.

## How It Works

The repo's top-level directory listing ([repo][repo], verified 2026-09-24) confirms three main
components, matching the README's description:

- **`gateway/`** — handles API routing between the client application and the selected harness
- **`runner/`** — executes harnesses inside isolated per-task session workspaces
- **`ui/`** — a web console (default `:3000`) for inspecting sessions

A separate **`protocol/`** directory holds the Unified Harness Protocol (UHP) definition (see
below).

Deployment is a single Docker command:

```bash
docker run -d --name harnessrouter -p 127.0.0.1:3000:3000 \
  -v harnessrouter:/data harnessrouter/harnessrouter
```

(~4GB disk, a provider API key, no HarnessRouter account required — per [README][repo]).

The unifying contract is the **Unified Harness Protocol (UHP)**, described as an open standard
covering: persistent sessions across multiple interactions, Server-Sent Event streaming for live
progress, file upload/retrieval, task cancellation, structured error handling with execution
traces, and OpenAI Responses API compatibility. UHP is the thing worth tracking for this corpus —
it is an attempt at the same "one contract, many backends" problem that CC's own
[model-provider gateway layer][gateway-doc] solves for *model* routing, but one layer up, at the
*harness/CLI* level.

## Adoption Decision

**Assess.** The Apache-2.0 self-hosted core, real Docker image, tagged releases (`v0.23.11`,
2026-09-23), and documented protocol are genuine open infrastructure, not vaporware — but the repo
is young (created 2026-08-09, roughly six weeks old as of this check). The marketing site makes
backing/funding claims that neither the README nor the repo metadata corroborate; this doc omits
them rather than repeat unverified marketing copy. Track for a future pass once the protocol and
harness-coverage matrix have had more time to stabilize, and once independent (non-vendor) usage
reports exist.

Cross-ref: [CC-model-provider-configuration.md][gateway-doc] — the analogous unification problem
one layer down, at the model-provider/gateway level rather than the harness/CLI level.

## Sources

| Source | Content |
|---|---|
| [HarnessRouter/harnessrouter][repo] (GitHub API) | License (Apache-2.0), stars, latest release, creation/push dates, top-level directory listing (`gateway/`, `runner/`, `ui/`, `protocol/`) — `gh api repos/HarnessRouter/harnessrouter`, `.../releases/latest`, `.../contents`, 2026-09-24 |
| [README][repo] | UHP feature list, Docker install command |
| [harnessrouter.ai][site] | Marketing site — harness list corroborated by the README; Cloud-tier specifics and backing/funding claims are site-only and unverified, omitted from the Adoption Decision |

[repo]: https://github.com/HarnessRouter/harnessrouter
[site]: https://harnessrouter.ai
[gateway-doc]: ../cc-native/configuration/CC-model-provider-configuration.md
