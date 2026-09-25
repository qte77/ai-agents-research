---
title: NOOA — NVIDIA Object-Oriented Agents Framework
source: https://github.com/NVIDIA-NeMo/labs-OO-Agents
purpose: Evaluate NOOA's object-oriented Python paradigm for agent development against the workflow/graph frameworks already covered in this corpus
created: 2026-09-24
updated: 2026-09-24
validated_links: 2026-09-24
---

**Status**: Assess

## What It Is

[NVIDIA-labs Object Oriented Agents (NOOA)][nooa-gh] is a model-agnostic Python framework from
NVIDIA-NeMo Labs for building AI agents as ordinary Python classes rather than as separate
prompt/tool/workflow abstractions. An agent's state, capabilities, prompts, and typed interfaces
all live on one `Agent` subclass: fields are state, methods are capabilities, docstrings are
prompts, and type annotations are contracts (per the [repository README][nooa-gh], accessed
2026-09-24).

```python
from nooa import Agent

class SupportAgent(Agent):
    """You are a support agent."""

    order_db: OrderDB                                    # state, typed

    def is_refund_eligible(self, order: Order) -> bool:   # deterministic Python
        return order.delivered and order.days_since_delivery <= 30

    async def triage(self, message: str, order: Order) -> Ticket:  # agentic method
        """Create a typed support ticket."""
        ...
```

The GitHub repository (`NVIDIA-NeMo/labs-OO-Agents`) had 2,235 stars and 302 forks, and its
license is **Apache 2.0** (confirmed from the repo's `LICENSE` file — the GitHub UI's automatic
detector reports the ambiguous `NOASSERTION`/"Other" for this repo, so the file was read
directly). The project's latest tagged release is `v0.0.10` (published 2026-09-04, accessed
2026-09-24), and its repository was created 2026-07-20 — an early-stage, actively pushed project
(last push 2026-09-24). It ships an accompanying [arXiv paper][nooa-paper] and an
[NVIDIA developer blog post][nooa-blog] describing "six agent harness capabilities for higher
model performance."

## How It Works

**Agentic methods.** A method with a `...` body is handed to an LLM at runtime and becomes an
agentic loop; a method with a real body stays deterministic Python. Generation commits one typed
result — streaming generation needs a separate stream contract and is otherwise rejected.

**Code as action.** The model acts by writing Python in a Jupyter-style REPL with access to
`self`, imports, and helper functions. Because methods and type annotations already supply
callable interfaces, this reduces the need to hand-write separate tool-schema definitions (per
the README, accessed 2026-09-24).

**Model-agnostic.** LLM calls route through LiteLLM, so the same agent class can target multiple
providers.

**Built-in tracing.** LLM calls and code execution are automatically instrumented.

**Installation** (accessed 2026-09-24):

```bash
uv add nooa                    # core framework
uv add "nooa[cli,memory]"      # optional CLI + memory extras
```

**Safety note (first-party).** The README states plainly that the framework executes
LLM-generated code and requires OS-level sandboxing (containers, VMs) for containment — its
internal validators alone are not a security boundary.

## Adoption Decision

**Assess.** NOOA's central bet — collapsing prompt/tool/state/workflow into one typed Python
class — is a genuinely different paradigm from the graph- and workflow-centric frameworks already
tracked in [`workflow-frameworks-landscape.md`](workflow-frameworks-landscape.md) and
[`agent-frameworks-infrastructure-landscape.md`](agent-frameworks-infrastructure-landscape.md):
it leans on ordinary Python OOP (inheritance, typing, docstrings) instead of a separate DSL or
node graph, which should make agents easier to unit-test, refactor, and version-control with
standard tooling. It is backed by NVIDIA-NeMo Labs and has an arXiv paper and a dedicated
developer-blog writeup, giving it more research grounding than a typical early hobby project.

Against that: the project is under three months old, its latest tagged release is `v0.0.10`
(pre-1.0), and — like any framework that executes LLM-generated code — it inherits the sandboxing
burden the README itself flags. No first-party evidence of Claude Code or CC-adjacent tooling
integration was found as of 2026-09-24. **Assess**, not **Trial**, until the API and release
cadence stabilize past `v0.x`.

## Action Items

- Re-check after NOOA reaches a `v1.0` tag or the corpus's next `non-cc` refresh pass; re-verify
  the license (GitHub's detector currently mislabels it) if the `LICENSE` file changes.
- Read the [arXiv paper][nooa-paper] for the underlying evaluation methodology behind the "six
  agent harness capabilities" claim in the blog post — not yet independently assessed here.
- Compare NOOA's typed-class agent model against
  [`agent-design-formats-landscape.md`](infrastructure/agent-design-formats-landscape.md) if/when this repo
  extends that landscape doc.

## Sources

| Source | Content |
|---|---|
| [NVIDIA-NeMo/labs-OO-Agents README][nooa-gh] | Framework description, code example, install commands, safety note |
| [NVIDIA-NeMo/labs-OO-Agents LICENSE][nooa-license] | Apache 2.0 full text (read directly; GitHub UI license detector returns "Other/NOASSERTION" for this repo) |
| `gh api repos/NVIDIA-NeMo/labs-OO-Agents` | Stars (2,235), forks (302), created (2026-07-20), pushed (2026-09-24), accessed 2026-09-24 |
| `gh api repos/NVIDIA-NeMo/labs-OO-Agents/releases/latest` | Latest tag `v0.0.10`, published 2026-09-04, accessed 2026-09-24 |
| [arXiv:2607.20709][nooa-paper] | Accompanying paper, linked from the repo README |
| [NVIDIA developer blog][nooa-blog] | "Six agent harness capabilities for higher model performance," linked from the repo README |

[nooa-gh]: https://github.com/NVIDIA-NeMo/labs-OO-Agents
[nooa-license]: https://github.com/NVIDIA-NeMo/labs-OO-Agents/blob/main/LICENSE
[nooa-paper]: https://arxiv.org/abs/2607.20709
[nooa-blog]: https://developer.nvidia.com/blog/six-agent-harness-capabilities-for-higher-model-performance/
