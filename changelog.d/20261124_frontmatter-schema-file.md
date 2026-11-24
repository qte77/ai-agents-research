### Added

- `docs/schema/frontmatter.schema.json` (JSON Schema 2020-12): the single source of the content-doc frontmatter rules, with each key's RDF term (`x-rdf`, e.g. `updated` → `dcterms:modified`); `doc_frontmatter.py` and `doc_status.py` read it via `lib/frontmatter_schema.py` (tests first, including one that every rule in the schema is enforced); CONTRIBUTING §1 links to it instead of restating it. An empty `title` is now flagged.
