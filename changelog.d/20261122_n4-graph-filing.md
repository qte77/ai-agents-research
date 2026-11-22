### Changed

- The doc graph no longer lumps every doc in no topic hub under "Unfiled": it splits them as `make check_coverage` does, into "Unfiled" (the docs the hub ratchet counts), "Exempt by rule" (D6) and "Not hub content" (README indexes, plans, research notes and example files), each with its own checkbox and count. Both read one function, `doc_coverage.hub_filing` (plan 0015 N4)
