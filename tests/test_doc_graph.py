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
    def test_frontmatter_status(self):
        text = "---\nstatus: trial\n---\n\n**Status**: Assess\n\n## Body\n"
        self.assertEqual(dg.doc_status(text), "trial")

    def test_body_badge_is_ignored(self):
        # check_status forbids body badges (#348), so frontmatter is the only source (plan 0015 G2).
        self.assertIsNone(dg.doc_status("**Status**: Reference (plan)\n\n## H\n"))

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
            ("docs/non-cc/b/y.md", "part"),
        )

    def test_external_link_is_skipped(self):
        self.assertIsNone(dg.resolve("docs/x.md", "https://www.GitHub.com/o/r"))

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
    # Real docs put the badge in the preamble, before the first heading (doc_status semantics).
    "docs/non-cc/b/y.md": "---\nstatus: assess\n---\n\n# Y\n\nback to [x](../a/x.md)\n",
    "docs/_topics/memory.md": (
        "# Topic Hub: Memory\n\n| [x](../non-cc/a/x.md) | row |\n"
        "| [x § part](../non-cc/a/x.md#part) | second row, same doc |\n"
    ),
    "docs/_topics/README.md": "# Hubs\n\n[memory](memory.md)\n",
    "docs/z.md": "# Z\n\nno links\n",
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

    def test_external_links_create_no_nodes_or_edges(self):
        self.assertFalse(any(n["type"] != "doc" for n in self.g["nodes"]))
        self.assertTrue(all(t in CORPUS for (_, t, _) in self.edges))

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


class FacetTests(unittest.TestCase):
    """Clustering facets derived per doc: status, doc type and platforms (plan 0015 N32)."""

    CORPUS = {
        "docs/non-cc/a/foo-landscape.md": "---\ntitle: F\nstatus: assess\nplatform_scope: [codex, cursor]\n---\n",
        "docs/cc-native/c/CC-bar-analysis.md": "---\ntitle: B\nstatus: adopt\n---\n",
        "docs/cc-community/CC-baz-reference.md": "---\ntitle: Z\nstatus: reference\nplatform_scope: [claude-code, zed]\n---\n",
        "docs/sdlc-lcm/ops-runbook.md": "# R\n",
    }

    def setUp(self):
        self.nodes = {n["id"]: n for n in dg.site_graph(dg.build_graph(self.CORPUS))["nodes"]}

    def test_doc_type_comes_from_the_filename_suffix(self):
        self.assertEqual(self.nodes["docs/non-cc/a/foo-landscape.md"]["doc_type"], "landscape")
        self.assertEqual(self.nodes["docs/cc-native/c/CC-bar-analysis.md"]["doc_type"], "analysis")
        self.assertEqual(self.nodes["docs/cc-community/CC-baz-reference.md"]["doc_type"], "reference")
        self.assertEqual(self.nodes["docs/sdlc-lcm/ops-runbook.md"]["doc_type"], "runbook")

    def test_platforms_come_from_frontmatter_or_the_cc_folders(self):
        self.assertEqual(self.nodes["docs/non-cc/a/foo-landscape.md"]["platforms"], ["codex", "cursor"])
        self.assertEqual(self.nodes["docs/cc-native/c/CC-bar-analysis.md"]["platforms"], ["claude-code"])
        self.assertEqual(self.nodes["docs/cc-community/CC-baz-reference.md"]["platforms"], ["claude-code", "zed"])
        self.assertEqual(self.nodes["docs/sdlc-lcm/ops-runbook.md"]["platforms"], [])

    def test_status_is_carried_and_none_when_missing(self):
        self.assertEqual(self.nodes["docs/cc-native/c/CC-bar-analysis.md"]["status"], "adopt")
        self.assertIsNone(self.nodes["docs/sdlc-lcm/ops-runbook.md"]["status"])


class DatesAndPurposeTests(unittest.TestCase):
    """created, updated and purpose reach the site graph for the details panel and timeline (plan 0016 N34)."""

    CORPUS = {
        "docs/a-analysis.md": '---\ntitle: A\npurpose: "Why A: matters."\ncreated: 2026-06-14\nupdated: 2026-11-23\n---\n',
        "docs/b-analysis.md": "---\ntitle: B\ncreated: not-a-date\n---\n",
        "docs/c.md": "# C\n\ncreated: 2026-01-01\n",
    }

    def setUp(self):
        self.nodes = {n["id"]: n for n in dg.site_graph(dg.build_graph(self.CORPUS))["nodes"]}

    def test_dates_and_purpose_are_read_from_frontmatter(self):
        a = self.nodes["docs/a-analysis.md"]
        self.assertEqual((a["created"], a["updated"]), ("2026-06-14", "2026-11-23"))
        self.assertEqual(a["purpose"], "Why A: matters.")

    def test_missing_or_malformed_values_are_none(self):
        b = self.nodes["docs/b-analysis.md"]
        self.assertEqual((b["created"], b["updated"], b["purpose"]), (None, None, None))

    def test_body_text_is_not_frontmatter(self):
        c = self.nodes["docs/c.md"]
        self.assertEqual((c["created"], c["updated"], c["purpose"]), (None, None, None))

    def test_build_graph_nodes_carry_them_too(self):
        node = dg.build_graph(self.CORPUS)["nodes"][0]
        self.assertEqual(node["updated"], "2026-11-23")


class SiteGraphTests(unittest.TestCase):
    """The slim projection the Pages site loads (plan 0015 G2)."""

    def setUp(self):
        self.site = dg.site_graph(dg.build_graph(CORPUS))
        self.nodes = {n["id"]: n for n in self.site["nodes"]}

    def test_nodes_carry_title_bucket_hubs_and_facets(self):
        self.assertEqual(self.nodes["docs/non-cc/a/x.md"],
                         {"id": "docs/non-cc/a/x.md", "title": "X", "bucket": "non-cc/a",
                          "hubs": ["docs/_topics/memory.md"], "status": "trial",
                          "doc_type": "other", "platforms": [], "purpose": None, "created": None, "updated": None})

    def test_hub_rows_pointing_at_a_section_count_once(self):
        self.assertEqual(self.nodes["docs/non-cc/a/x.md"]["hubs"], ["docs/_topics/memory.md"])

    def test_hub_index_is_not_a_hub(self):
        self.assertEqual(self.nodes["docs/_topics/memory.md"]["hubs"], [])

    def test_unfiled_doc_has_no_hubs(self):
        self.assertEqual(self.nodes["docs/z.md"]["hubs"], [])
        self.assertEqual(self.nodes["docs/non-cc/b/y.md"]["hubs"], [])

    def test_one_edge_per_linked_pair_regardless_of_direction(self):
        self.assertEqual(self.site["edges"], [
            ["docs/_topics/README.md", "docs/_topics/memory.md"],
            ["docs/_topics/memory.md", "docs/non-cc/a/x.md"],
            ["docs/non-cc/a/x.md", "docs/non-cc/b/y.md"],
        ])

    def test_filing_is_copied_onto_nodes_when_given(self):
        # Plan 0015 N4: build-doc-graph passes doc_coverage.hub_filing so the site splits "no hub".
        filing = {path: "unfiled" for path in CORPUS}
        filing["docs/non-cc/a/x.md"] = "hubbed"
        nodes = {n["id"]: n for n in dg.site_graph(dg.build_graph(CORPUS), filing)["nodes"]}
        self.assertEqual(nodes["docs/z.md"]["filing"], "unfiled")
        self.assertEqual(nodes["docs/non-cc/a/x.md"]["filing"], "hubbed")

    def test_deterministic(self):
        again = dg.site_graph(dg.build_graph(dict(reversed(list(CORPUS.items())))))
        self.assertEqual(dg.to_json(again), dg.to_json(self.site))


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
