"""Unit tests for lib/doc_graph.py — the deterministic structural doc graph (plan 0009 row G)."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".github" / "scripts"))

from lib import doc_graph as dg  # noqa: E402


class BucketTests(unittest.TestCase):
    def test_cc_native_and_non_cc_keep_their_subdirectory(self):
        self.assertEqual(dg.bucket_of("docs/cc-native/sessions/a.md"), "cc-native/sessions")
        self.assertEqual(dg.bucket_of("docs/non-cc/frameworks/b.md"), "non-cc/frameworks")

    def test_flat_top_level_sections(self):
        self.assertEqual(dg.bucket_of("docs/cc-community/c.md"), "cc-community")
        self.assertEqual(dg.bucket_of("docs/_topics/memory.md"), "_topics")
        self.assertEqual(dg.bucket_of("docs/architecture.md"), "docs")


class DocStatusTests(unittest.TestCase):
    def test_frontmatter_wins_over_badge(self):
        text = "---\nstatus: trial\n---\n\n**Status**: Assess\n\n## Body\n"
        self.assertEqual(dg.doc_status(text), "trial")

    def test_badge_is_normalized_to_its_leading_token(self):
        self.assertEqual(dg.doc_status("---\nt: x\n---\n\n**Status**: Research (informational)\n"), "research")
        self.assertEqual(dg.doc_status("**Status**: Reference (plan)\n\n## H\n"), "reference")
        self.assertEqual(dg.doc_status("**Status**: Research Preview — beta\n"), "research-preview")

    def test_none_when_no_status(self):
        self.assertIsNone(dg.doc_status("# Title\n\nbody\n"))


class TitleTests(unittest.TestCase):
    def test_frontmatter_title_then_first_h1_then_path(self):
        self.assertEqual(dg.doc_title("---\ntitle: Foo Bar\n---\n# Other\n", "docs/x.md"), "Foo Bar")
        self.assertEqual(dg.doc_title("# Heading One\n", "docs/x.md"), "Heading One")
        self.assertEqual(dg.doc_title("no heading\n", "docs/x.md"), "x")


class ExtractLinksTests(unittest.TestCase):
    def test_inline_and_reference_links_with_line_numbers(self):
        text = "intro\nsee [a](b.md#sec) and [c][ref]\n\n[ref]: https://example.com/p\n"
        self.assertEqual(
            dg.extract_links(text),
            [("b.md#sec", 2), ("https://example.com/p", 4)],
        )

    def test_links_inside_fenced_code_are_ignored(self):
        text = "```md\n[x](ignored.md)\n```\n[y](kept.md)\n"
        self.assertEqual(dg.extract_links(text), [("kept.md", 4)])

    def test_images_and_bare_anchors_are_ignored(self):
        text = "![img](pic.png)\n[same page](#section)\n"
        self.assertEqual(dg.extract_links(text), [])


class ResolveTests(unittest.TestCase):
    def test_relative_doc_link_resolves_with_fragment(self):
        self.assertEqual(
            dg.resolve("docs/non-cc/a/x.md", "../b/y.md#part"),
            ("doc", "docs/non-cc/b/y.md", "part"),
        )

    def test_external_link_becomes_domain(self):
        self.assertEqual(dg.resolve("docs/x.md", "https://www.GitHub.com/o/r"), ("domain", "github.com", None))

    def test_non_markdown_and_mailto_are_skipped(self):
        self.assertIsNone(dg.resolve("docs/x.md", "img/pic.svg"))
        self.assertIsNone(dg.resolve("docs/x.md", "mailto:a@b.c"))


# A tiny corpus: two docs linking to each other and out, one hub, one link out of the corpus.
CORPUS = {
    "docs/non-cc/a/x.md": (
        "---\ntitle: X\nstatus: trial\n---\n\n"
        "[y](../b/y.md#one) [y again](../b/y.md) [gh](https://github.com/o/r)\n"
        "[outside](../../../CONTRIBUTING.md)\n"
    ),
    "docs/non-cc/b/y.md": "# Y\n\n**Status**: Assess\n\nback to [x](../a/x.md)\n",
    "docs/_topics/memory.md": "# Topic Hub: Memory\n\n| [x](../non-cc/a/x.md) | row |\n",
}


class BuildGraphTests(unittest.TestCase):
    def setUp(self):
        self.g = dg.build_graph(CORPUS)
        self.nodes = {n["id"]: n for n in self.g["nodes"]}
        self.edges = {(e["source"], e["target"], e["kind"]): e for e in self.g["edges"]}

    def test_doc_nodes_carry_bucket_status_and_title(self):
        x = self.nodes["docs/non-cc/a/x.md"]
        self.assertEqual((x["type"], x["bucket"], x["status"], x["title"]), ("doc", "non-cc/a", "trial", "X"))
        self.assertEqual(self.nodes["docs/non-cc/b/y.md"]["status"], "assess")

    def test_repeated_links_aggregate_into_one_edge_with_all_lines_and_fragments(self):
        e = self.edges[("docs/non-cc/a/x.md", "docs/non-cc/b/y.md", "link")]
        self.assertEqual(e["lines"], [6, 6])
        self.assertEqual(e["fragments"], ["one"])

    def test_hub_docs_emit_hub_edges(self):
        self.assertIn(("docs/_topics/memory.md", "docs/non-cc/a/x.md", "hub"), self.edges)

    def test_external_links_create_domain_nodes_and_cites_edges(self):
        self.assertEqual(self.nodes["domain:github.com"]["type"], "domain")
        self.assertIn(("docs/non-cc/a/x.md", "domain:github.com", "cites"), self.edges)

    def test_links_leaving_the_corpus_create_no_edge(self):
        self.assertFalse(any(t.endswith("CONTRIBUTING.md") for (_, t, _) in self.edges))

    def test_output_is_deterministic_regardless_of_input_order(self):
        reordered = dict(reversed(list(CORPUS.items())))
        self.assertEqual(dg.to_json(dg.build_graph(reordered)), dg.to_json(self.g))

    def test_json_contract(self):
        data = json.loads(dg.to_json(self.g))
        self.assertEqual(set(data), {"nodes", "edges"})
        self.assertEqual([n["id"] for n in data["nodes"]], sorted(n["id"] for n in data["nodes"]))
        self.assertTrue(dg.to_json(self.g).endswith("\n"))


class LoadCorpusTests(unittest.TestCase):
    def test_reads_markdown_under_docs_and_excludes_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/a").mkdir(parents=True)
            (root / "docs/archive").mkdir(parents=True)
            (root / "docs/a/x.md").write_text("# X\n", encoding="utf-8")
            (root / "docs/a/note.txt").write_text("skip", encoding="utf-8")
            (root / "docs/archive/old.md").write_text("# Old\n", encoding="utf-8")
            self.assertEqual(dg.load_corpus(root), {"docs/a/x.md": "# X\n"})


if __name__ == "__main__":
    unittest.main()
