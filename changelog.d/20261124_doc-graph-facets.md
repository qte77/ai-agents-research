### Added

- Doc graph (`ui/doc-graph.json`): each doc now carries clustering facets: `status`, `doc_type` (from the filename suffix) and `platforms` (from `platform_scope`, or `claude-code` for `cc-native/` and `cc-community/` docs without one); tests first. The page does not filter on them yet.
