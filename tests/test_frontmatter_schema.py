"""The frontmatter schema file is the single source of the rules (plan 0015 N28)."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".github" / "scripts"))

from lib import doc_frontmatter as df  # noqa: E402
from lib import doc_status as ds  # noqa: E402

SCHEMA = json.loads((ROOT / "docs" / "schema" / "frontmatter.schema.json").read_text(encoding="utf-8"))


class SchemaFileTests(unittest.TestCase):
    def test_is_json_schema_2020_12_object_without_extra_keys(self):
        self.assertEqual(SCHEMA["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(SCHEMA["type"], "object")
        self.assertIs(SCHEMA["additionalProperties"], False)

    def test_required_keys_are_properties(self):
        self.assertTrue(set(SCHEMA["required"]) <= set(SCHEMA["properties"]))

    def test_every_status_value_has_its_own_rdf_mapping(self):
        status = SCHEMA["properties"]["status"]
        self.assertEqual(set(status["x-rdf-values"]), set(status["enum"]))
        rings = {v: m for v, m in status["x-rdf-values"].items() if m["property"] == "schema:reviewRating"}
        self.assertEqual(sorted(rings, key=lambda v: -rings[v]["ratingValue"]), ["adopt", "trial", "assess", "hold"])
        for m in status["x-rdf-values"].values():
            self.assertIn(m["property"].split(":")[0], SCHEMA["x-rdf-prefixes"])

    def test_every_key_names_its_rdf_term_or_null(self):
        prefixes = SCHEMA["x-rdf-prefixes"]
        for key, spec in SCHEMA["properties"].items():
            self.assertIn("x-rdf", spec, key)
            term = spec["x-rdf"]
            if term is not None:
                self.assertIn(term.split(":")[0], prefixes, key)


# Keywords the hand-rolled checker enforces, per key (values are parsed as strings, so
# "type": "string" holds by construction). A keyword added to the schema without checker
# support would be silently ignored; this list makes that a test failure instead.
ENFORCED = {
    "title": {"type", "minLength"},
    "purpose": {"type", "minLength", "maxLength"},
    "created": {"type", "format"},
    "updated": {"type", "format"},
    "validated_links_on": {"type", "format"},
    "status": {"enum"},
    "source": {"type", "format", "pattern"},
    "platform_scope": {"type", "items"},
    "test_run": set(),
}
ANNOTATIONS = {"description", "x-rdf", "x-rdf-values"}


class EnforcedKeywordsTests(unittest.TestCase):
    def test_every_rule_in_the_schema_is_enforced_by_the_checker(self):
        self.assertEqual(set(SCHEMA["properties"]), set(ENFORCED))
        for key, spec in SCHEMA["properties"].items():
            self.assertLessEqual(set(spec) - ANNOTATIONS, ENFORCED[key], key)

    def test_empty_title_is_flagged(self):
        good = ("---\ntitle: T\npurpose: P\ncreated: 2026-01-02\nupdated: 2026-11-21\n"
                "validated_links_on: 2026-11-21\nstatus: assess\n---\n")
        self.assertEqual(df.check_doc(good.replace("title: T", "title:")), ["title must not be empty"])


class CheckerReadsSchemaTests(unittest.TestCase):
    def test_both_modules_load_the_one_schema_file(self):
        path = ROOT / "docs" / "schema" / "frontmatter.schema.json"
        self.assertEqual(df.SCHEMA_PATH.resolve(), path)
        self.assertIs(ds.SCHEMA_PATH, df.SCHEMA_PATH)

    def test_required_optional_removed_come_from_the_schema(self):
        self.assertEqual(df.REQUIRED, tuple(SCHEMA["required"]))
        self.assertEqual(df.OPTIONAL, frozenset(SCHEMA["properties"]) - frozenset(SCHEMA["required"]))
        self.assertEqual(df.REMOVED, frozenset(SCHEMA["x-removed"]))

    def test_dates_purpose_limit_and_status_come_from_the_schema(self):
        props = SCHEMA["properties"]
        self.assertEqual(set(df.DATE_KEYS), {k for k, v in props.items() if v.get("format") == "date"})
        self.assertEqual(df.PURPOSE_MAX, props["purpose"]["maxLength"])
        self.assertEqual(df._ONE_URL.pattern, props["source"]["pattern"])
        self.assertEqual(df.PLATFORMS, frozenset(props["platform_scope"]["items"]["enum"]))
        self.assertEqual(ds.DOC_STATUS_VOCAB, frozenset(props["status"]["enum"]))
        self.assertEqual(ds.PLAN_STATUS_VOCAB, frozenset(SCHEMA["$defs"]["plan"]["properties"]["status"]["enum"]))


if __name__ == "__main__":
    unittest.main()
