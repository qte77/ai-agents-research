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


class HeadingSlugTests(unittest.TestCase):
    def test_github_slug_rules(self):
        text = (
            "# Title\n"
            "## Coding Agents & IDEs\n"
            "## 3. Agents _Performing_ SCA/DCA (agent-as-scanner)\n"
            "## Skills API (`/v1/skills`)\n"
            "## [Linked](https://x.y) heading\n"
            "### my_var **bold**\n"
            "## Notes\n"
            "## Notes\n"
            "```\n## not a heading\n```\n"
            '<a id="custom-anchor"></a>\n'
        )
        self.assertEqual(dc.heading_slugs(text), {
            "title", "coding-agents--ides", "3-agents-performing-scadca-agent-as-scanner",
            "skills-api-v1skills", "linked-heading", "my_var-bold", "notes", "notes-1",
            "custom-anchor",
        })


class CheckAnchorsTests(unittest.TestCase):
    DOCS = {
        "docs/a.md": "# A\n\n[ok](b.md#section-one) [bad](b.md#gone)\n[case](b.md#Section-One)\n",
        "docs/b.md": "# B\n\n## Section One\n",
    }

    def test_missing_fragment_is_reported_with_its_lines(self):
        self.assertEqual(dc.check_anchors(self.DOCS), ["docs/a.md:3: #gone not found in docs/b.md"])


class HubCoverageTests(unittest.TestCase):
    DOCS = {
        "docs/_topics/README.md": "# Hubs\n\n| [m](memory.md) | x |\n",
        "docs/_topics/memory.md": (
            "# Memory\n\n| Doc | Note |\n|---|---|\n"
            "| [L § 4](../non-cc/frameworks/l-landscape.md#4-memory) | catalog |\n"
            "| [L § 4](../non-cc/frameworks/l-landscape.md#4-memory) | product B, see also [z](../sdlc-lcm/z-analysis.md) |\n"
            "| [L § 7](../non-cc/frameworks/l-landscape.md#7-rag) | other section |\n"
            "\nSee [L](../non-cc/frameworks/l-landscape.md) and, again, [L](../non-cc/frameworks/l-landscape.md).\n"
            "Graph rows live in [L](../non-cc/frameworks/l-landscape.md).\n"
        ),
        "docs/non-cc/frameworks/l-landscape.md": "# L\n## 4. Memory\n## 7. RAG\n",
        "docs/non-cc/frameworks/x-analysis.md": "# X\n",
        "docs/non-cc/agents/p-analysis.md": "# P\n",
        "docs/non-cc/agents/q-landscape.md": "# Q\n",
        "docs/sdlc-lcm/z-analysis.md": "# Z\n",
        "docs/sdlc-lcm/lcm-spec.md": "# Spec\n",
        "docs/sdlc-lcm/release-runbook.md": "# Runbook\n",
        "docs/sdlc-lcm/orphan-analysis.md": "# O\n",
        "docs/architecture.md": "# A\n",
    }

    def test_exemptions_follow_d6(self):
        for path in ("docs/architecture.md", "docs/non-cc/agents/p-analysis.md",
                     "docs/non-cc/frameworks/x-analysis.md", "docs/sdlc-lcm/lcm-spec.md",
                     "docs/sdlc-lcm/release-runbook.md"):
            self.assertTrue(dc.hub_exempt(path), path)
        for path in ("docs/non-cc/agents/q-landscape.md", "docs/non-cc/frameworks/l-landscape.md",
                     "docs/sdlc-lcm/orphan-analysis.md"):
            self.assertFalse(dc.hub_exempt(path), path)

    def test_unhubbed_lists_non_exempt_content_docs_no_hub_links(self):
        # z is hubbed through a link inside a row's description; the hub index is not a hub.
        self.assertEqual(dc.unhubbed(self.DOCS), ["docs/non-cc/agents/q-landscape.md",
                                                  "docs/sdlc-lcm/orphan-analysis.md"])

    def test_hub_filing_splits_docs_without_a_hub_the_way_check_coverage_does(self):
        # Plan 0015 N4: the doc graph's "Unfiled" must mean what check_coverage means.
        docs = {**self.DOCS, "docs/sdlc-lcm/README.md": "# Index\n", "docs/plans/p.md": "# Plan\n"}
        filing = dc.hub_filing(docs)
        self.assertEqual(filing["docs/non-cc/frameworks/l-landscape.md"], "hubbed")
        self.assertEqual(filing["docs/sdlc-lcm/z-analysis.md"], "hubbed")
        for path in ("docs/architecture.md", "docs/non-cc/agents/p-analysis.md", "docs/sdlc-lcm/lcm-spec.md"):
            self.assertEqual(filing[path], "exempt", path)
        for path in ("docs/sdlc-lcm/README.md", "docs/plans/p.md", "docs/_topics/memory.md"):
            self.assertEqual(filing[path], "not-hub-content", path)
        self.assertEqual(sorted(p for p, f in filing.items() if f == "unfiled"), dc.unhubbed(docs))
        self.assertEqual(set(filing), set(docs))

    def test_duplicate_rows_are_same_hub_doc_and_section(self):
        self.assertEqual(dc.check_hub_duplicates(self.DOCS), [
            "docs/_topics/memory.md:6: duplicate row for docs/non-cc/frameworks/l-landscape.md#4-memory "
            "(first at line 5); merge them",
        ])


GLOSSARY = """# Glossary

| Term | Expansion | Owner |
|---|---|---|
| MCP | Model Context Protocol | [x][x] |
| Hybrid search, RRF | RRF = Reciprocal Rank Fusion | [x][x] |
| MOC, PARA | MOC = Map of Content; PARA = Projects, Areas, Resources, Archives | [x][x] |
| Reranker | — | [x][x] |
| Property graph | — | [x][x] |
"""


class GlossaryTests(unittest.TestCase):
    def test_parses_abbreviations_and_expansions(self):
        self.assertEqual(dc.parse_glossary(GLOSSARY), {
            "MCP": "Model Context Protocol",
            "RRF": "Reciprocal Rank Fusion",
            "MOC": "Map of Content",
            "PARA": "Projects, Areas, Resources, Archives",
        })


class AbbreviationTests(unittest.TestCase):
    ABBR = {"MCP": "Model Context Protocol", "RRF": "Reciprocal Rank Fusion"}

    def check(self, text, path="docs/non-cc/x/a.md"):
        return dc.check_abbreviations({path: text}, self.ABBR)

    def test_flags_use_without_expansion(self):
        self.assertEqual(self.check("# A\n\nUses MCP and RRF.\n"), ["docs/non-cc/x/a.md: MCP, RRF not expanded"])

    def test_expansion_anywhere_counts_case_insensitive(self):
        self.assertEqual(self.check("# A\n\nThe model context protocol (MCP) and RRF (reciprocal rank fusion).\n"), [])

    def test_hyphens_and_spaces_match_either_way(self):
        abbr = {"RAG": "Retrieval-Augmented Generation"}
        self.assertEqual(dc.check_abbreviations({"docs/a/b.md": "RAG (retrieval augmented generation)"}, abbr), [])

    def test_link_to_glossary_counts(self):
        self.assertEqual(self.check("# A\n\nUses MCP, see [glossary](../../glossary.md) for RRF.\n"), [])

    def test_ignores_reference_link_definitions(self):
        text = '# A\n\nSee [c].\n\n[c]: https://example.com/x "Connectors and MCP Apps"\n'
        self.assertEqual(self.check(text), [])

    def test_ignores_urls_link_targets_comments_and_frontmatter(self):
        text = ("---\ntitle: MCP notes\n---\n\n# A\n\nSee [spec](https://x/MCP/y), [x](../MCP-x.md) and https://h/RRF/z.\n"
                "<!-- MCP draft -->\n")
        self.assertEqual(self.check(text), [])

    def test_expansion_in_frontmatter_url_or_comment_does_not_count(self):
        for text in ("---\npurpose: Model Context Protocol notes\n---\n\nUses MCP.\n",
                     "# A\n\nUses MCP, see https://x/model-context-protocol.\n",
                     "# A\n\nUses MCP.\n<!-- Model Context Protocol -->\n"):
            self.assertEqual(self.check(text), ["docs/non-cc/x/a.md: MCP not expanded"], text)

    def test_expansion_wrapped_across_lines_counts(self):
        self.assertEqual(self.check("# A\n\nThe Model Context\nProtocol (MCP).\n"), [])

    def test_plural_counts_as_use(self):
        self.assertEqual(self.check("# A\n\nTwo MCPs.\n"), ["docs/non-cc/x/a.md: MCP not expanded"])

    def test_hyphen_compound_counts_as_use(self):
        self.assertEqual(self.check("# A\n\nAn MCP-based tool.\n"), ["docs/non-cc/x/a.md: MCP not expanded"])

    def test_glossary_must_be_a_relative_link(self):
        self.assertEqual(self.check("# A\n\nUses MCP; see glossary.md.\n"), ["docs/non-cc/x/a.md: MCP not expanded"])
        self.assertEqual(self.check("# A\n\nUses [MCP](https://other.org/glossary.md).\n"), ["docs/non-cc/x/a.md: MCP not expanded"])

    def test_reference_style_glossary_link_counts(self):
        self.assertEqual(self.check("# A\n\nUses MCP, see the [glossary][g].\n\n[g]: ../../glossary.md\n"), [])

    def test_tilde_line_inside_backtick_fence_stays_fenced(self):
        self.assertEqual(self.check("# A\n\n```\n~~~\nMCP\n```\n\nplain\n"), [])
        self.assertEqual(self.check("# A\n\n```\n~~~\n```\n\nUses MCP.\n"), ["docs/non-cc/x/a.md: MCP not expanded"])

    def test_longer_fence_holds_a_shorter_one(self):
        self.assertEqual(self.check("# A\n\n````\n```\nMCP\n```\n````\n"), [])

    def test_ignores_code_and_partial_words(self):
        self.assertEqual(self.check("# A\n\n`MCP` and MCPServer and Google-MCP and mcp\n\n```\nMCP\n```\n"), [])

    def test_skips_glossary_and_non_content(self):
        for path in ("docs/glossary.md", "docs/non-cc/README.md", "docs/plans/2026-01-01-0001-x.md",
                     "docs/_topics/rag.md", "docs/research/r.md", "docs/learnings/per-repo/some-repo.md"):
            self.assertEqual(self.check("MCP", path=path), [], path)


if __name__ == "__main__":
    unittest.main()
