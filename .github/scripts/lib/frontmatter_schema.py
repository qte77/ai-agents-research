"""Load the frontmatter schema file, the single source of the frontmatter rules (plan 0015 N28).

``docs/schema/frontmatter.schema.json`` is JSON Schema 2020-12; each key also names its RDF
term (``x-rdf``). ``doc_status`` and ``doc_frontmatter`` take their vocabularies and key lists
from here, so the rules live in one file.
"""
from __future__ import annotations

import json
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parents[3] / "docs" / "schema" / "frontmatter.schema.json"
SCHEMA = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
PROPERTIES = SCHEMA["properties"]
