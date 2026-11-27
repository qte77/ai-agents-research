---
title: "Distributed Systems Concepts for Agent Systems — Landscape"
purpose: Concept map of distributed systems (fallacies, papers, borders, contracts, communication, layers, topologies, patterns) read through multi-agent systems, with first-party sources.
created: 2026-11-27
updated: 2026-11-27
validated_links_on: 2026-11-27
status: assess
---

**Details:** a concept map, not a tutorial. Each row points at the paper, spec or vendor page that states
the idea. Mappings from a concept to an agent system are marked **our synthesis**: they are our reading,
not a claim the cited source makes.

## What It Is

A distributed system is a set of independent processes that cooperate only by passing messages over a
network that can lose, delay, duplicate and reorder them, with no shared clock and no shared memory.
Most of the field's vocabulary (consensus, delivery semantics, contracts, backoff, sagas) exists because
of that one constraint.

**Agent lens (our synthesis).** An agent system crosses that constraint at every hop, so the field's
failure modes apply to it unchanged:

| Agent-system hop | Distributed-systems view |
|---|---|
| Model API call from a harness | Remote call with timeouts, retries, partial failure |
| Tool call to a Model Context Protocol ([MCP][mcp-spec]) server | Request/response over stdio or Streamable HTTP, with a schema contract |
| Agent-to-agent call (Agent2Agent, [A2A][a2a-spec]) | Cross-trust-boundary RPC between independently run services |
| Remote or cloud sandbox ([cloud sessions](../cc-native/ci-remote/CC-cloud-sessions-analysis.md)) | Failure domain and trust boundary behind a network link |
| Parallel subagents, shared files or queues | Concurrent writers with no shared clock; message passing |
| Long task with side effects (deploys, payments) | Multi-step transaction needing compensation, not rollback |

## Fallacies of Distributed Computing

The list is eight false assumptions that programmers new to distributed applications make. The
original statements are in Arnon Rotem-Gal-Oz's "Fallacies of Distributed Computing Explained" PDF, which
the Wikipedia page cites ([rgo-pdf][rgo-pdf]); **that PDF timed out when fetched on 2026-11-27 and was
not read**, so the wording below comes from the secondary [Wikipedia page][wiki-fallacies] (read
2026-11-27), which lists them as "The network is reliable; Latency is zero; Bandwidth is infinite; The
network is secure; Topology doesn't change; There is one administrator; Transport cost is zero; The
network is homogeneous". Wikipedia describes the list as "a set of assertions made by L. Peter Deutsch
and others at Sun Microsystems".

| # | Fallacy | Agent-system example (our synthesis) |
|---|---|---|
| 1 | The network is reliable | An MCP tool call drops mid-flight; the agent cannot tell whether the side effect ran. |
| 2 | Latency is zero | A planner loop that makes 40 sequential remote tool calls is slow by construction, whatever the model speed. |
| 3 | Bandwidth is infinite | Returning a full file tree or a large JSON blob as tool output floods the context window and the link. |
| 4 | The network is secure | A tool server on a shared network can read or alter requests; agent traffic needs transport security and auth ([identity](agent-identity-auth-landscape.md)). |
| 5 | Topology doesn't change | Endpoints, agent cards and MCP server URLs move; hard-coded addresses break. |
| 6 | There is one administrator | The model vendor, the MCP server owner and the sandbox host each set their own limits and policies. |
| 7 | Transport cost is zero | Every hop costs tokens, money or rate-limit budget, not only time. |
| 8 | The network is homogeneous | Agents and servers differ in protocol version, schema dialect and capability set. |

**History (dated, secondary).** Wikipedia says Deutsch first listed seven fallacies in 1994, taking four
from earlier work by Bill Joy and "Dave Lyon" ("Tom Lyon" in the APNIC post), and that James Gosling added the
eighth around 1997. The [APNIC blog post][apnic] (2025-12-08, read 2026-11-27) agrees that the first
four came from Joy and Lyon, that Deutsch added three and that Gosling added the last. The sources
disagree on Lyon's first name; we did not resolve it and do not use either. Wikipedia also records a ninth
fallacy that Deutsch stated later in a podcast ("The party you are communicating with is trustworthy"), and
three more added in 2020 by Mark Richards and Neal Ford: "Versioning is simple", "Compensating updates
always work", "Observability is optional". Those extensions are secondary-only claims. The
[AlgoMaster page][algomaster] (lead, read 2026-11-27) restates the eight as an explainer and adds no
first-party evidence.

## Timeline of Key Papers and Results

All rows are first-party paper or author pages. "Read" means the URL was fetched on 2026-11-27 and
resolved; except for Raft, the PDF bodies were not text-extracted here, so authors, years and venues
come from the papers' standard citations, not from re-reading the PDFs.

| Year | Result | Authors | Source |
|---|---|---|---|
| 1978 | Logical clocks and a happened-before order replace wall-clock time for ordering events | Lamport | ["Time, Clocks, and the Ordering of Events"][lamport-clocks] |
| 1981/84 | End-to-end argument: correctness functions belong at the endpoints, not in lower layers | Saltzer, Reed, Clark | ["End-to-End Arguments in System Design"][e2e] |
| 1982 | Byzantine generals: agreement under arbitrary (malicious) faults needs enough honest nodes | Lamport, Shostak, Pease | ["The Byzantine Generals Problem"][byz] |
| 1985 | FLP: no deterministic consensus in an asynchronous system if even one process may crash | Fischer, Lynch, Paterson | ["Impossibility of Distributed Consensus with One Faulty Process"][flp] |
| 1987 | Sagas: a long transaction as local transactions with compensations | Garcia-Molina, Salem | ["Sagas"][sagas-paper] |
| 1998 | Paxos: consensus by a replicated log of decrees (paper written earlier, published 1998) | Lamport | ["The Part-Time Parliament"][paxos] |
| 2000/02 | CAP: conjecture (2000), formal proof (2002): a service cannot have consistency, availability and partition tolerance together | Brewer; Gilbert, Lynch | ["Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services"][cap] |
| 2007 | Dynamo: always-writable key-value store with eventual consistency and vector clocks | DeCandia et al. (Amazon) | ["Dynamo"][dynamo] |
| 2011 | CRDTs: data types whose replicas converge without coordination | Shapiro, Preguiça, Baquero, Zawirski | ["Conflict-free Replicated Data Types"][crdt] |
| 2012 | PACELC: under partition choose availability or consistency; else latency or consistency | Abadi | ["Consistency Tradeoffs in Modern Distributed Database System Design"][pacelc] |
| 2014 | Raft: consensus designed to be understandable, "equivalent to Paxos in fault-tolerance and performance" | Ongaro, Ousterhout | [Raft site][raft-site]; [paper][raft-paper] |

Raft's own page defines consensus as "multiple servers agreeing on values" and says that "a cluster of
5 servers can continue to operate even if 2 servers fail" (read 2026-11-27).

Left out: Chandra–Toueg failure detectors, Spanner/TrueTime, Calvin, Jepsen reports and the CALM theorem.
They are real but narrower for agent systems; add a row if a task needs them.

## System Borders

A border is where assumptions change: who is trusted, who owns the model, what can fail together.

| Border | Meaning | Source |
|---|---|---|
| Trust boundary | Data crossing it is untrusted until validated; fallacy 4 and the later "trustworthy party" fallacy | [Wikipedia][wiki-fallacies] (secondary) |
| Bounded context | A scope inside which one model and vocabulary is consistent; Fowler: DDD divides "a large system into Bounded Contexts, each of which can have a unified model" | [Fowler, Bounded Context][bc] |
| Failure domain | Set of components that fail together; the [bulkhead pattern](#patterns) isolates them | [Azure bulkhead][bulkhead] |
| Administrative domain | One owner and policy set (fallacy 6) | [Wikipedia][wiki-fallacies] (secondary) |

**Agent sandbox borders (our synthesis).** A sandbox is a trust boundary and a failure domain at once:
see [mas-security-framework.md](mas-security-framework.md), [NVIDIA OpenShell](../non-cc/infrastructure/nvidia-openshell-analysis.md),
[Microsoft MXC](../non-cc/infrastructure/microsoft-mxc-analysis.md) and
[cloud sessions](../cc-native/ci-remote/CC-cloud-sessions-analysis.md). A bounded context maps to a
tool or skill with its own vocabulary: the same word ("ticket", "customer") can mean different things in two MCP servers.

## System Contracts

A contract states what each side promises across a border, so either side can change inside it.

| Kind | Standard | What it fixes | Source |
|---|---|---|---|
| HTTP API description | OpenAPI Specification | A "language-agnostic interface description for HTTP APIs" | [OAS][oas] |
| Message-driven API description | AsyncAPI | Channels and messages over any protocol, including Kafka and MQTT | [AsyncAPI v3.1.0][asyncapi] |
| Data shape | JSON Schema (current version 2020-12, read 2026-11-27) | Structure and validation of JSON | [JSON Schema][jsonschema] |
| Binary schema and RPC | Protocol Buffers | Typed messages with a field-number compatibility rule | [proto3 guide][proto3] |
| Consumer-driven contract tests | Pact | Tests that "assert that inter-application messages conform to a shared understanding that is documented in a contract" | [Pact docs][pact] |

**Versioning.** Compatibility rules (add optional fields, never reuse a field number) are what let two
sides upgrade at different times; the proto3 guide states the field-number rules. The fallacy extension
"Versioning is simple" is a secondary-only claim ([Wikipedia][wiki-fallacies]).

**Agent contracts.** [MCP][mcp-spec] (version 2026-07-28 was latest, read 2026-11-27) uses JSON-RPC 2.0
messages over stdio or Streamable HTTP. [A2A][a2a-spec] describes itself as "an open standard designed
to facilitate communication and interoperability between independent, potentially opaque AI agent
systems", with an Agent Card for discovery and "Opaque Execution" (agents need not share internals).
KB coverage: [Agent-User Interaction (AG-UI) protocol landscape](../non-cc/protocols/ag-ui-protocol-landscape.md),
[agent plugins standard](../non-cc/protocols/agent-plugins-standard-analysis.md),
[CC cross-session messaging](../cc-native/agents-skills/CC-cross-session-messaging-analysis.md).
**Our synthesis:** an MCP tool schema is the consumer-visible contract, but a model reads its
description, so the contract also includes natural-language text that no schema validator checks.

## Communication

| Axis | Choices | Notes |
|---|---|---|
| Coupling in time | Synchronous request/response vs asynchronous messaging | Sync is simple but ties availability together; async needs correlation ids and a place for replies. |
| Delivery semantics | At most once; at least once; exactly once | Kafka defines them as "Messages may be lost but are never redelivered", "Messages are never lost but may be redelivered", and "Each message is processed once and only once" ([Kafka design][kafka]). |
| Exactly-once caution | Read the fine print | Kafka warns that many "exactly-once" claims "are misleading" once producers or consumers can fail ([Kafka design][kafka]). |
| Idempotency | Same request, same effect | AWS: "APIs with side effects aren't safe to retry unless they provide idempotency" ([Builders' Library][aws-retries]). Kafka's idempotent producer, since 0.11.0.0, stops resends from creating duplicates. |
| Timeouts | Bound every wait | Without one, a caller can "stall or infinitely wait" (Wikipedia on fallacy effects, secondary). |
| Backpressure | Slow producers when consumers lag | Backoff and load shedding are the client-side forms ([patterns](#patterns)). |

**Our synthesis:** at-least-once plus idempotent handlers is the default for agent tool calls. A
retried "create issue" or "send payment" call needs an idempotency key, or the model will happily do it twice.

## Layers and Topologies

**Layers.** [RFC 1122][rfc1122] defines host requirements for "the communications protocol layers: link
layer, IP layer, and transport layer", and its companion RFC 1123 covers the application layer.

| Layer | Role | Agent-system analogue (our synthesis) |
|---|---|---|
| Link | Delivery on one network segment | Local machine or container network |
| Internet (IP) | Addressing and routing between networks | Endpoint addressing of MCP and A2A servers |
| Transport (TCP, UDP) | Process-to-process delivery, reliability | Streamable HTTP / stdio session |
| Application | Meaning of messages | JSON-RPC methods, Agent Cards, tool schemas |

The end-to-end argument ([timeline](#timeline-of-key-papers-and-results)) says reliability of an
operation must ultimately be checked at the endpoints. **Our synthesis:** a tool's success must be
verified by the agent or harness (read back the state), however reliable the transport below it is.

**Topologies (our synthesis).**

| Topology | Distributed-systems form | Multi-agent form | KB doc |
|---|---|---|---|
| Client-server | One server, many clients | One tool server per agent; harness calls tools | [MCP section above](#system-contracts) |
| Hub-and-spoke / broker | Central broker routes messages | Orchestrator with workers | [orchestrators](../non-cc/orchestrators/orchestrators-landscape.md) |
| Peer-to-peer | Equal nodes, no coordinator | A2A between independent agents | [mas-design-principles](mas-design-principles.md) |
| Mesh | Many-to-many links | Agent swarms with shared state; hardest to reason about | [workflow frameworks](../non-cc/frameworks/workflow-frameworks-landscape.md) |

## Patterns

| Pattern | Problem | Agent-system analogue (our synthesis) | Source |
|---|---|---|---|
| Retry with exponential backoff and jitter | Immediate retries pile load on a failing service | Rate-limited model API calls; most AWS SDKs implement it (read 2026-11-27) | [AWS Architecture Blog][aws-backoff], [Builders' Library][aws-retries] |
| Circuit breaker | Calls to a failing dependency waste time and load | Stop calling a dead MCP server after repeated errors; Fowler: once failures reach a threshold, "the circuit breaker trips" | [Fowler][cb], [Azure][azure-cb] |
| Bulkhead | One failure drains shared resources | Separate concurrency pools per tool server or per tenant | [Azure bulkhead][bulkhead] |
| Saga | No atomic transaction across services | Multi-step agent task with compensating actions: "a reliably coordinated sequence of local transactions" | [Garcia-Molina and Salem][sagas-paper], [microservices.io][saga] |
| Transactional outbox | State change and message send must both happen | Write task state and the "next action" message in one local commit | [microservices.io][outbox] |
| Event sourcing | Need history and replay | Agent traces as an append-only log; Fowler: "all changes to application state are stored as a sequence of events" | [Fowler][evsrc]; see [agent traces](automata-agent-traces-analysis.md) |
| Leader election | One node must act for a group | One orchestrator instance owns a task queue | [Raft site][raft-site] |
| Consensus | Replicas must agree on one history | Rarely needed inside an agent; use a database or lock service that provides it | [Raft paper][raft-paper], [Paxos][paxos] |

Rule of thumb (our synthesis): prefer a managed queue, database or lock service over writing consensus,
leader election or an outbox yourself.

## Not included

Entries removed under the [pruning rule](../../CONTRIBUTING.md#pruning-entries-well-known-performance-optimised-filter)
(checked 2026-11-27).

| Name | Reason | Date | Link |
|---|---|---|---|
| Rotem-Gal-Oz fallacies PDF as a source | Fetch timed out; the page was not read, so not quoted | 2026-11-27 | [PDF][rgo-pdf] |
| Richards/Ford "three more fallacies" as established | Seen only on Wikipedia; stated as secondary-only | 2026-11-27 | [Wikipedia][wiki-fallacies] |
| AlgoMaster explainer as evidence | Tutorial site with no first-party sourcing; lead only | 2026-11-27 | [AlgoMaster][algomaster] |

## Sources

| Source | Content |
|---|---|
| [Wikipedia fallacies][wiki-fallacies], [APNIC][apnic], [AlgoMaster][algomaster], [Rotem-Gal-Oz PDF][rgo-pdf] | Fallacies list and history (secondary; PDF unread) |
| [Lamport clocks][lamport-clocks], [Byzantine][byz], [Paxos][paxos], [End-to-end][e2e], [FLP][flp], [CAP][cap], [Dynamo][dynamo], [CRDT][crdt], [PACELC][pacelc], [Sagas][sagas-paper] | Papers (URL resolved; body not text-read) |
| [Raft site][raft-site], [Raft paper][raft-paper] | Raft (site read) |
| [Fowler bounded context][bc], [circuit breaker][cb], [event sourcing][evsrc] | Concept definitions |
| [AWS backoff][aws-backoff], [AWS retries][aws-retries], [Azure bulkhead][bulkhead], [Azure circuit breaker][azure-cb], [saga][saga], [outbox][outbox] | Resilience and consistency patterns |
| [OAS][oas], [AsyncAPI][asyncapi], [JSON Schema][jsonschema], [proto3][proto3], [Pact][pact] | Contract standards |
| [MCP][mcp-spec], [A2A][a2a-spec] | Agent protocol specifications |
| [Kafka design][kafka], [RFC 1122][rfc1122] | Delivery semantics; layering |

[wiki-fallacies]: https://en.wikipedia.org/wiki/Fallacies_of_distributed_computing
[apnic]: https://blog.apnic.net/2025/12/08/21-years-and-counting-of-eight-fallacies-of-distributed-computing/
[algomaster]: https://algomaster.io/learn/computer-networks/fallacies-of-distributed-computing
[rgo-pdf]: https://www.rgoarchitects.com/Files/fallacies.pdf
[lamport-clocks]: https://lamport.azurewebsites.net/pubs/time-clocks.pdf
[byz]: https://lamport.azurewebsites.net/pubs/byz.pdf
[paxos]: https://lamport.azurewebsites.net/pubs/lamport-paxos.pdf
[e2e]: https://web.mit.edu/Saltzer/www/publications/endtoend/endtoend.pdf
[flp]: https://groups.csail.mit.edu/tds/papers/Lynch/jacm85.pdf
[cap]: https://users.ece.cmu.edu/~adrian/731-sp04/readings/GL-cap.pdf
[dynamo]: https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf
[crdt]: https://inria.hal.science/inria-00555588
[pacelc]: https://www.cs.umd.edu/~abadi/papers/abadi-pacelc.pdf
[sagas-paper]: https://www.cs.cornell.edu/andru/cs711/2002fa/reading/sagas.pdf
[raft-site]: https://raft.github.io/
[raft-paper]: https://raft.github.io/raft.pdf
[bc]: https://martinfowler.com/bliki/BoundedContext.html
[cb]: https://martinfowler.com/bliki/CircuitBreaker.html
[evsrc]: https://martinfowler.com/eaaDev/EventSourcing.html
[aws-backoff]: https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/
[aws-retries]: https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter
[bulkhead]: https://learn.microsoft.com/en-us/azure/architecture/patterns/bulkhead
[azure-cb]: https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker
[saga]: https://microservices.io/patterns/data/saga.html
[outbox]: https://microservices.io/patterns/data/transactional-outbox.html
[oas]: https://spec.openapis.org/oas/latest.html
[asyncapi]: https://www.asyncapi.com/docs/reference/specification/v3.1.0
[jsonschema]: https://json-schema.org/specification
[proto3]: https://protobuf.dev/programming-guides/proto3/
[pact]: https://docs.pact.io/
[mcp-spec]: https://modelcontextprotocol.io/specification/2026-07-28
[a2a-spec]: https://a2a-protocol.org/latest/specification/
[kafka]: https://kafka.apache.org/documentation/design/
[rfc1122]: https://www.rfc-editor.org/rfc/rfc1122
