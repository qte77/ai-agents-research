"""Unit tests for the pure link-rewriting logic in scripts/restructure_links.py
(#309 Phase 1: docs/non-cc/ subdir restructure).

Only the pure functions are tested — git mv / subprocess / argparse are thin IO
wrappers not covered here (same split as tests/test_pages_build.py and
tests/test_doc_status.py). Stdlib `unittest`, no deps.

Run: python3 -m unittest discover -s tests
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import restructure_links as rl  # noqa: E402

# A single conceptual move used across most tests: the "Orchestrators" section
# moving from docs/non-cc/ into docs/non-cc/orchestrators/.
MOVES = {
    "docs/non-cc/air-analysis.md": "docs/non-cc/orchestrators/air-analysis.md",
    "docs/non-cc/deerflow-analysis.md": "docs/non-cc/orchestrators/deerflow-analysis.md",
    "docs/non-cc/omnigent-analysis.md": "docs/non-cc/orchestrators/omnigent-analysis.md",
}
KNOWN_PATHS = frozenset(
    MOVES.keys()
    | {
        "docs/non-cc/README.md",
        "docs/non-cc/agent-frameworks-infrastructure-landscape.md",
        "docs/non-cc/pi-analysis.md",
        "docs/cc-native/agents-skills/CC-agent-teams-orchestration.md",
    }
)


class IsLocalPathLinkTests(unittest.TestCase):
    def test_relative_path_is_local(self):
        self.assertTrue(rl.is_local_path_link("air-analysis.md"))
        self.assertTrue(rl.is_local_path_link("../README.md"))

    def test_anchor_only_is_not_local(self):
        self.assertFalse(rl.is_local_path_link("#cross-references"))

    def test_empty_is_not_local(self):
        self.assertFalse(rl.is_local_path_link(""))

    def test_repo_absolute_is_not_local(self):
        self.assertFalse(rl.is_local_path_link("/docs/non-cc/air-analysis.md"))

    def test_uri_schemes_are_not_local(self):
        self.assertFalse(rl.is_local_path_link("https://air.dev"))
        self.assertFalse(rl.is_local_path_link("mailto:a@b.com"))


class SplitAnchorTests(unittest.TestCase):
    def test_splits_path_and_anchor(self):
        self.assertEqual(rl.split_anchor("file.md#section"), ("file.md", "#section"))

    def test_no_anchor_returns_empty_suffix(self):
        self.assertEqual(rl.split_anchor("file.md"), ("file.md", ""))


class ResolveRepoPathTests(unittest.TestCase):
    def test_sibling(self):
        self.assertEqual(
            rl.resolve_repo_path("air-analysis.md", "docs/non-cc"),
            "docs/non-cc/air-analysis.md",
        )

    def test_parent_traversal(self):
        self.assertEqual(
            rl.resolve_repo_path("../README.md", "docs/non-cc/orchestrators"),
            "docs/non-cc/README.md",
        )

    def test_repo_root_from_dir(self):
        self.assertEqual(rl.resolve_repo_path("README.md", ""), "README.md")


class RelativeLinkTests(unittest.TestCase):
    def test_sibling(self):
        self.assertEqual(
            rl.relative_link("docs/non-cc/README.md", "docs/non-cc"), "README.md"
        )

    def test_into_subdir(self):
        self.assertEqual(
            rl.relative_link("docs/non-cc/orchestrators/air-analysis.md", "docs/non-cc"),
            "orchestrators/air-analysis.md",
        )

    def test_out_of_subdir(self):
        self.assertEqual(
            rl.relative_link("docs/non-cc/README.md", "docs/non-cc/orchestrators"),
            "../README.md",
        )

    def test_across_other_top_level_dir(self):
        self.assertEqual(
            rl.relative_link(
                "docs/non-cc/orchestrators/air-analysis.md",
                "docs/cc-native/agents-skills",
            ),
            "../../non-cc/orchestrators/air-analysis.md",
        )


class RewriteLinkTargetTests(unittest.TestCase):
    def test_sibling_link_to_moved_target(self):
        # A file staying in docs/non-cc/ links to a doc that moves.
        got = rl.rewrite_link_target(
            "deerflow-analysis.md", "docs/non-cc", "docs/non-cc", MOVES, KNOWN_PATHS
        )
        self.assertEqual(got, "orchestrators/deerflow-analysis.md")

    def test_dotdot_link_from_other_dir(self):
        # cc-native/agents-skills/ file links up-and-over into non-cc/.
        got = rl.rewrite_link_target(
            "../../non-cc/air-analysis.md",
            "docs/cc-native/agents-skills",
            "docs/cc-native/agents-skills",
            MOVES,
            KNOWN_PATHS,
        )
        self.assertEqual(got, "../../non-cc/orchestrators/air-analysis.md")

    def test_moved_file_linking_to_unmoved_sibling(self):
        # omnigent-analysis.md itself moves; its link to a doc that stays put
        # must gain a leading '../'.
        got = rl.rewrite_link_target(
            "agent-frameworks-infrastructure-landscape.md",
            "docs/non-cc",
            "docs/non-cc/orchestrators",
            MOVES,
            KNOWN_PATHS,
        )
        self.assertEqual(got, "../agent-frameworks-infrastructure-landscape.md")

    def test_moved_file_linking_to_another_moved_file_stays_sibling(self):
        # Two files moving into the same new subdir keep a bare sibling link.
        got = rl.rewrite_link_target(
            "deerflow-analysis.md",
            "docs/non-cc",
            "docs/non-cc/orchestrators",
            MOVES,
            KNOWN_PATHS,
        )
        self.assertEqual(got, "deerflow-analysis.md")

    def test_anchor_is_preserved(self):
        got = rl.rewrite_link_target(
            "air-analysis.md#pricing", "docs/non-cc", "docs/non-cc", MOVES, KNOWN_PATHS
        )
        self.assertEqual(got, "orchestrators/air-analysis.md#pricing")

    def test_same_file_anchor_untouched(self):
        got = rl.rewrite_link_target(
            "#cross-references", "docs/non-cc", "docs/non-cc/orchestrators", MOVES, KNOWN_PATHS
        )
        self.assertEqual(got, "#cross-references")

    def test_absolute_url_untouched(self):
        got = rl.rewrite_link_target(
            "https://air.dev", "docs/non-cc", "docs/non-cc", MOVES, KNOWN_PATHS
        )
        self.assertEqual(got, "https://air.dev")

    def test_already_at_new_path_is_a_noop(self):
        # Idempotency at the target-resolution level: a link already pointing
        # at the post-move path is returned unchanged.
        got = rl.rewrite_link_target(
            "orchestrators/air-analysis.md", "docs/non-cc", "docs/non-cc", MOVES, KNOWN_PATHS
        )
        self.assertEqual(got, "orchestrators/air-analysis.md")

    def test_unrelated_unknown_path_untouched(self):
        # Guard rail: a path that is neither a move target nor a known repo
        # file is left alone (protects reference-def prose from being mangled).
        got = rl.rewrite_link_target(
            "some-made-up-thing.md", "docs/non-cc", "docs/non-cc/orchestrators", MOVES, KNOWN_PATHS
        )
        self.assertEqual(got, "some-made-up-thing.md")

    def test_unmoved_referencer_and_unmoved_target_left_verbatim(self):
        # Neither this file nor its target are part of the move: a pre-existing
        # (if non-canonical, e.g. redundant '../non-cc/') link to a KNOWN,
        # unmoved file must be left byte-for-byte alone — out of scope for this
        # move, not a general link-canonicalization pass.
        got = rl.rewrite_link_target(
            "../non-cc/agent-frameworks-infrastructure-landscape.md",
            "docs/non-cc",
            "docs/non-cc",
            MOVES,
            KNOWN_PATHS,
        )
        self.assertEqual(got, "../non-cc/agent-frameworks-infrastructure-landscape.md")

    def test_unmoved_referencer_redundant_dot_slash_to_unmoved_target_untouched(self):
        got = rl.rewrite_link_target(
            "./agent-frameworks-infrastructure-landscape.md",
            "docs/non-cc",
            "docs/non-cc",
            MOVES,
            KNOWN_PATHS,
        )
        self.assertEqual(got, "./agent-frameworks-infrastructure-landscape.md")


class RewriteMarkdownLinksTests(unittest.TestCase):
    def test_sibling_inline_link_rewritten(self):
        text = "See [deerflow-analysis.md](deerflow-analysis.md) for details.\n"
        got = rl.rewrite_markdown_links(
            text, "docs/non-cc/goclaw-analysis.md", "docs/non-cc/goclaw-analysis.md",
            MOVES, KNOWN_PATHS,
        )
        self.assertIn("](orchestrators/deerflow-analysis.md)", got)

    def test_dotdot_link_from_other_dir_rewritten(self):
        text = "cf. [air](../../non-cc/air-analysis.md).\n"
        got = rl.rewrite_markdown_links(
            text,
            "docs/cc-native/agents-skills/CC-agent-teams-orchestration.md",
            "docs/cc-native/agents-skills/CC-agent-teams-orchestration.md",
            MOVES,
            KNOWN_PATHS,
        )
        self.assertIn("](../../non-cc/orchestrators/air-analysis.md)", got)

    def test_reference_style_definition_rewritten(self):
        text = (
            "See [everos] for more.\n\n"
            "[everos]: agent-frameworks-infrastructure-landscape.md\n"
        )
        got = rl.rewrite_markdown_links(
            text, "docs/non-cc/omnigent-analysis.md", "docs/non-cc/orchestrators/omnigent-analysis.md",
            MOVES, KNOWN_PATHS,
        )
        self.assertIn("[everos]: ../agent-frameworks-infrastructure-landscape.md", got)

    def test_reference_style_prose_not_mangled(self):
        # '[Note]: some text' is prose, not a link definition to a real file —
        # the guard rail in rewrite_link_target must leave it untouched.
        text = "[Note]: some text about things\n"
        got = rl.rewrite_markdown_links(
            text, "docs/non-cc/omnigent-analysis.md", "docs/non-cc/orchestrators/omnigent-analysis.md",
            MOVES, KNOWN_PATHS,
        )
        self.assertEqual(got, text)

    def test_anchor_kept_through_full_rewrite(self):
        text = "[pricing](air-analysis.md#pricing)\n"
        got = rl.rewrite_markdown_links(
            text, "docs/non-cc/README.md", "docs/non-cc/README.md", MOVES, KNOWN_PATHS
        )
        self.assertIn("](orchestrators/air-analysis.md#pricing)", got)

    def test_code_block_untouched(self):
        text = (
            "Example:\n\n"
            "```markdown\n"
            "[deerflow-analysis.md](deerflow-analysis.md)\n"
            "```\n"
        )
        got = rl.rewrite_markdown_links(
            text, "docs/non-cc/goclaw-analysis.md", "docs/non-cc/goclaw-analysis.md",
            MOVES, KNOWN_PATHS,
        )
        self.assertEqual(got, text)

    def test_link_outside_code_block_still_rewritten(self):
        text = (
            "[deerflow-analysis.md](deerflow-analysis.md)\n\n"
            "```markdown\n"
            "[deerflow-analysis.md](deerflow-analysis.md)\n"
            "```\n\n"
            "[deerflow-analysis.md](deerflow-analysis.md) again\n"
        )
        got = rl.rewrite_markdown_links(
            text, "docs/non-cc/goclaw-analysis.md", "docs/non-cc/goclaw-analysis.md",
            MOVES, KNOWN_PATHS,
        )
        lines = got.split("\n")
        self.assertIn("orchestrators/deerflow-analysis.md", lines[0])
        self.assertIn("(deerflow-analysis.md)", lines[3])  # inside fence, unchanged
        self.assertIn("orchestrators/deerflow-analysis.md", lines[6])

    def test_already_rewritten_text_is_idempotent(self):
        text = "See [deerflow-analysis.md](deerflow-analysis.md) for details.\n"
        once = rl.rewrite_markdown_links(
            text, "docs/non-cc/goclaw-analysis.md", "docs/non-cc/goclaw-analysis.md",
            MOVES, KNOWN_PATHS,
        )
        twice = rl.rewrite_markdown_links(
            once, "docs/non-cc/goclaw-analysis.md", "docs/non-cc/goclaw-analysis.md",
            MOVES, KNOWN_PATHS,
        )
        self.assertEqual(once, twice)

    def test_unrelated_file_and_unrelated_link_untouched(self):
        # A file that doesn't move, linking to a target that doesn't move
        # either, must come back byte-for-byte identical — even if the
        # existing link is written in a non-canonical (but valid) form.
        text = "**See**: [x](../non-cc/agent-frameworks-infrastructure-landscape.md)\n"
        got = rl.rewrite_markdown_links(
            text,
            "docs/non-cc/agent-observability-methods-analysis.md",
            "docs/non-cc/agent-observability-methods-analysis.md",
            MOVES,
            KNOWN_PATHS,
        )
        self.assertEqual(got, text)

    def test_moved_file_own_links_repointed(self):
        # omnigent-analysis.md itself moves and links to a sibling that stays.
        text = "Cross-ref: [AFI](agent-frameworks-infrastructure-landscape.md)\n"
        got = rl.rewrite_markdown_links(
            text, "docs/non-cc/omnigent-analysis.md", "docs/non-cc/orchestrators/omnigent-analysis.md",
            MOVES, KNOWN_PATHS,
        )
        self.assertIn("](../agent-frameworks-infrastructure-landscape.md)", got)


class LoadMovesTsvTests(unittest.TestCase):
    def test_parses_tsv_ignoring_header_and_comments(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "moves.tsv"
            p.write_text(
                "# comment\n"
                "old_path\tnew_path\n"
                "docs/non-cc/air-analysis.md\tdocs/non-cc/orchestrators/air-analysis.md\n"
                "\n"
            )
            got = rl.load_moves_tsv(p)
        self.assertEqual(
            got,
            {"docs/non-cc/air-analysis.md": "docs/non-cc/orchestrators/air-analysis.md"},
        )


class DeriveMovesFromMapTests(unittest.TestCase):
    def test_filters_to_requested_section(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "map.tsv"
            p.write_text(
                "filename\tsubdir\n"
                "air-analysis.md\torchestrators\n"
                "goose-analysis.md\tagents\n"
                "raven-analysis.md\torchestrators\n"
            )
            got = rl.derive_moves_from_map(p, "orchestrators", "docs/non-cc")
        self.assertEqual(
            got,
            {
                "docs/non-cc/air-analysis.md": "docs/non-cc/orchestrators/air-analysis.md",
                "docs/non-cc/raven-analysis.md": "docs/non-cc/orchestrators/raven-analysis.md",
            },
        )


if __name__ == "__main__":
    unittest.main()
