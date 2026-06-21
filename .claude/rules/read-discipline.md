# Read Discipline

Read/edit hygiene for a docs corpus. The read:edit and re-reading points echo the
token-waste patterns [CodeBurn][codeburn] surfaces — it is a usage tracker, not a
ruleset (see the repo's own analysis,
[CC-community-tooling-landscape.md](../../docs/cc-community/CC-community-tooling-landscape.md#codeburn-agentseal)).
Precise citation is local discipline for our subagent fan-outs.

- **Know the blast radius before you touch it.** The Edit tool already blocks editing
  an unread file — the discipline is the step before: before renaming or moving a doc,
  or changing a heading or anchor, grep for inbound links and cross-references so you
  don't break them. `lychee` is the backstop, not the first line of defense.
- **Read enough, not more.** Understand what references a file, then stop — bulk-reading
  "to be safe" fights the 40–60% context target in `context-management.md`. Don't
  re-read a file you already hold; re-reading after a compaction is the exception.
- **Cite precisely.** In prompts — and especially in subagent briefs — name
  `<file>:<lines>`, never "the sandboxing doc." Scoped briefs are what keep fan-out
  subagents on task.
- **Verify subagent findings before acting.** Treat a subagent's "no coverage" /
  "file doesn't exist" / structural report as *advisory*. Before creating a doc,
  deleting, or concluding absence, confirm with your own `git grep` + `Read` —
  sweeps in this repo have repeatedly returned false negatives (missed
  already-existing docs and whole sections). Calibrate by grepping a string you
  know exists. See [AGENT_LEARNINGS.md](../../AGENT_LEARNINGS.md) ("Subagent
  reference sweeps can return false negatives").

[codeburn]: https://github.com/getagentseal/codeburn#optimize
