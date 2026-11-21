"""Unit tests for lib/doc_frontmatter.py — the CONTRIBUTING §1–§2 frontmatter schema (plan 0015 F2)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".github" / "scripts"))

from lib import doc_frontmatter as df  # noqa: E402

GOOD = (
    "---\ntitle: T\npurpose: P\ncreated: 2026-01-02\nupdated: 2026-11-21\n"
    "validated_links: 2026-11-21\nstatus: assess\nsource: https://x.y\n"
    "platform_scope: [claude-code, cursor]\n---\n\n# T\n"
)


class InScopeTests(unittest.TestCase):
    def test_content_docs_are_in_scope(self):
        self.assertTrue(df.in_scope("docs/non-cc/agents/x.md"))
        self.assertTrue(df.in_scope("docs/architecture.md"))

    def test_indexes_hubs_plans_examples_archive_and_generated_files_are_not(self):
        for path in ("docs/non-cc/README.md", "docs/_topics/memory.md", "docs/plans/2026-11-20-0015-x.md",
                     "docs/cc-native/examples/rules/r.md", "docs/archive/old.md",
                     "docs/research/rxiv-agentic-papers.md"):
            self.assertFalse(df.in_scope(path), path)


class CheckDocTests(unittest.TestCase):
    def test_valid_doc_has_no_problems(self):
        self.assertEqual(df.check_doc(GOOD), [])

    def test_missing_frontmatter(self):
        self.assertEqual(df.check_doc("# No frontmatter\n"), ["no frontmatter"])

    def test_missing_required_keys_are_listed(self):
        text = "---\ntitle: T\nstatus: assess\n---\n"
        self.assertEqual(df.check_doc(text), [
            "missing required key: purpose", "missing required key: created",
            "missing required key: updated", "missing required key: validated_links",
        ])

    def test_dates_must_be_iso(self):
        text = GOOD.replace("created: 2026-01-02", "created: 2026-1-2").replace(
            "updated: 2026-11-21", "updated: '2026-11-21'")
        self.assertEqual(df.check_doc(text), ["created is not an ISO date (YYYY-MM-DD): 2026-1-2"])

    def test_keys_that_left_frontmatter_and_unknown_keys(self):
        text = GOOD.replace("status: assess\n", "status: assess\ncategory: landscape\ndescription: d\nfoo: 1\n")
        self.assertEqual(df.check_doc(text), [
            "key not allowed (see CONTRIBUTING §1): category",
            "key not allowed (see CONTRIBUTING §1): description",
            "unknown key: foo",
        ])

    def test_nested_yaml_lines_are_not_keys(self):
        text = GOOD.replace("platform_scope: [claude-code, cursor]\n", "platform_scope:\n  - claude-code\n  - cursor\n")
        self.assertEqual(df.check_doc(text), [])

    def test_status_must_be_lifecycle(self):
        self.assertEqual(df.check_doc(GOOD.replace("status: assess", "status: generally-available")),
                         ["status not in the lifecycle vocabulary (CONTRIBUTING §2): generally-available"])

    def test_plan_tokens_are_not_doc_statuses(self):
        self.assertEqual(df.check_doc(GOOD.replace("status: assess", "status: done")),
                         ["status not in the lifecycle vocabulary (CONTRIBUTING §2): done"])

    def test_source_is_one_url(self):
        self.assertEqual(df.check_doc(GOOD.replace("source: https://x.y", "source: https://a.b, https://c.d")),
                         ["source must be one URL (others go in the Sources section): https://a.b, https://c.d"])
        self.assertEqual(df.check_doc(GOOD.replace("source: https://x.y", "source: vendor docs")),
                         ["source must be one URL (others go in the Sources section): vendor docs"])


if __name__ == "__main__":
    unittest.main()
