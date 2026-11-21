"""Unit tests for lib/doc_coverage.py — README-index and inbound-link coverage (plan 0015 X1)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".github" / "scripts"))

from lib import doc_coverage as dc  # noqa: E402

CORPUS = {
    "docs/non-cc/README.md": "# Non-CC\n\n[a](agents/a.md) [b](frameworks/b.md)\n",
    "docs/non-cc/agents/a.md": "# A\n\n[b](../frameworks/b.md)\n",
    "docs/non-cc/frameworks/b.md": "# B\n",
    "docs/non-cc/frameworks/orphan.md": "# Orphan\n\nlinks out only: [a](../agents/a.md)\n",
    "docs/cc-native/README.md": "# CC\n\n[s](sessions/README.md)\n",
    "docs/cc-native/sessions/README.md": "# Sessions\n\n[x](x.md)\n",
    "docs/cc-native/sessions/x.md": "# X\n",
    "docs/cc-native/sessions/y.md": "# Y\n\nlinked from a peer only\n",
    "docs/cc-native/sessions/z.md": "# Z\n\n[y](y.md)\n",
    "docs/cc-native/examples/rules/r.md": "# Example rule\n",
    "docs/UserStory.md": "# Stories\n",
    "docs/architecture.md": "# Arch\n",
}
ROOT = {"README.md": "[stories](docs/UserStory.md)\n"}


class IndexOfTests(unittest.TestCase):
    def test_nearest_readme_inside_docs(self):
        self.assertEqual(dc.index_of("docs/cc-native/sessions/x.md", CORPUS), "docs/cc-native/sessions/README.md")
        self.assertEqual(dc.index_of("docs/non-cc/frameworks/b.md", CORPUS), "docs/non-cc/README.md")

    def test_docs_root_files_have_no_index(self):
        self.assertIsNone(dc.index_of("docs/architecture.md", CORPUS))

    def test_a_readme_is_indexed_by_the_readme_above_it(self):
        self.assertEqual(dc.index_of("docs/cc-native/sessions/README.md", CORPUS), "docs/cc-native/README.md")


class CheckCoverageTests(unittest.TestCase):
    def setUp(self):
        self.problems = dc.check_coverage(CORPUS, ROOT)

    def test_doc_missing_from_its_index_is_reported(self):
        self.assertIn("docs/non-cc/frameworks/orphan.md: not linked from its index docs/non-cc/README.md",
                      self.problems)
        self.assertIn("docs/cc-native/sessions/y.md: not linked from its index docs/cc-native/sessions/README.md",
                      self.problems)
        self.assertIn("docs/cc-native/sessions/z.md: not linked from its index docs/cc-native/sessions/README.md",
                      self.problems)

    def test_doc_with_no_inbound_link_is_reported(self):
        self.assertIn("docs/non-cc/frameworks/orphan.md: no inbound link from any other doc", self.problems)
        self.assertIn("docs/architecture.md: no inbound link from any other doc", self.problems)

    def test_a_link_from_a_repo_root_file_counts(self):
        self.assertFalse(any(p.startswith("docs/UserStory.md") for p in self.problems))

    def test_peer_link_satisfies_inbound_but_not_the_index(self):
        y = [p for p in self.problems if p.startswith("docs/cc-native/sessions/y.md")]
        self.assertEqual(len(y), 1)

    def test_readmes_and_examples_are_not_content(self):
        self.assertFalse(any("README.md:" in p or "/examples/" in p for p in self.problems))

    def test_covered_docs_pass_and_output_is_sorted(self):
        self.assertFalse(any(p.startswith(("docs/non-cc/agents/a.md", "docs/cc-native/sessions/x.md"))
                             for p in self.problems))
        self.assertEqual(self.problems, sorted(self.problems))


if __name__ == "__main__":
    unittest.main()
