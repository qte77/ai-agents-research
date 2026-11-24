### Changed

- `docs/schema/frontmatter.schema.json`: each `status` value now has its own RDF mapping (`x-rdf-values`): the rings adopt/trial/assess/hold as a `schema:reviewRating` of 4 to 1, `research` and `reference` as `dcterms:type`, `archived` as `schema:creativeWorkStatus`; `validated_links_on` maps approximately to `schema:lastReviewed` (tests first).
