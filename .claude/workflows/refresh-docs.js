// refresh-docs.js — generalized stale-fact refresh workflow.
// Re-verifies existing docs against their first-party sources and returns an
// adversarially-verified corrections list; the calling session applies edits.
//
// Invoke via Workflow({name: 'refresh-docs'}, args) with args = array of doc
// paths (strings) or {path, hint} objects. Repo-agnostic: paths are relative
// to the session working directory. Read-only — agents never edit files.

export const meta = {
  name: 'refresh-docs',
  description: 'Re-verify docs against first-party sources → adversarially-verified stale-claim corrections',
  phases: [{ title: 'Refresh', detail: 'one read-only checker per doc' },
           { title: 'Verify', detail: 'adversarially re-check proposed corrections' }],
}

// Some harnesses deliver args as a JSON-encoded string — tolerate both shapes.
let input = args
if (typeof input === 'string') { try { input = JSON.parse(input) } catch { log('args string is not valid JSON') } }
const docs = (Array.isArray(input) ? input : (input && input.paths) || [])
  .map(d => (typeof d === 'string' ? { path: d } : d))
  .filter(d => d && d.path)

if (!docs.length) { log('No doc paths in args — pass args: ["docs/…", …]'); return [] }
log(`Refreshing ${docs.length} doc(s) against first-party sources.`)

const REPORT = {
  type: 'object',
  properties: {
    path: { type: 'string' },
    checked_sources: { type: 'array', items: { type: 'string' } },
    stale_claims: { type: 'array', items: {
      type: 'object',
      properties: { claim: { type: 'string' }, correction: { type: 'string' }, source_url: { type: 'string' } },
      required: ['claim', 'correction'],
    } },
    unreachable_sources: { type: 'array', items: { type: 'string' } },
    version_gate_note: { type: 'string' },
    ok: { type: 'boolean' },
  },
  required: ['path', 'ok', 'stale_claims'],
}
const VERDICT = {
  type: 'object',
  properties: { holds: { type: 'boolean' }, corrections: { type: 'string' } },
  required: ['holds'],
}

const results = await pipeline(
  docs,
  (d) => agent(
    `READ-ONLY stale-fact check of ${d.path}${d.hint ? ` (hint: ${d.hint})` : ''}. Do NOT edit any file. `
    + `1) Read the doc. 2) List its version-gated / vendor-behavior / count / pricing claims and its primary first-party sources `
    + `(frontmatter source: + the key body/Sources URLs). 3) Re-fetch those first-party pages (WebFetch; gh api for repo metadata) `
    + `and diff reality against the doc's claims. Report ONLY defensible corrections — each with the exact stale claim text, the `
    + `correction, and the first-party source_url proving it. Note renamed features (vendor-rename => replace in place per the repo's `
    + `CONTRIBUTING maintenance table), dead/redirected URLs under unreachable_sources, and set version_gate_note if the doc's version `
    + `gates need bumping. ok=true if the doc needed no changes. Do not propose stylistic rewrites — facts only.`,
    { label: `refresh:${d.path}`, phase: 'Refresh', schema: REPORT }),
  (r, d) => (r && r.stale_claims.length)
    ? agent(
        `Adversarially verify these proposed doc corrections by independently re-fetching the cited first-party sources. `
        + `Set holds=false with corrections text if any proposed correction is unsupported or itself wrong.\n\n${JSON.stringify(r)}`,
        { label: `verify:${d.path}`, phase: 'Verify', schema: VERDICT })
        .then(v => ({ ...r, verified: v }))
    : r,
)

const ok = results.filter(Boolean)
const stale = ok.filter(r => r.stale_claims.length)
log(`Done: ${ok.length}/${docs.length} checked; ${stale.length} doc(s) with corrections.`)
return ok
