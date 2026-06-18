"""Unit tests for lib/native_sources.py (pure extractors + GraphQL navigation)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".github" / "scripts"))

from lib import native_sources as ns  # noqa: E402


class ExtractBlogEntriesTests(unittest.TestCase):
    def test_extracts_dedups_and_skips_short_and_strips_noise(self):
        html = (
            "<script>x</script>"
            '<a href="/news/claude-code-update">Claude Code Update</a>'
            '<a href="/news/claude-code-update">Claude Code Update</a>'  # dup URL
            '<a href="/news/short">hi</a>'                                # title < 5
            '<a href="/news/agents">New <b>agent</b> teams</a>'           # inner tags stripped
        )
        entries = ns.extract_blog_entries(html)
        urls = [e["url"] for e in entries]
        self.assertEqual(urls, [
            "https://www.anthropic.com/news/claude-code-update",
            "https://www.anthropic.com/news/agents",
        ])
        self.assertEqual(entries[1]["name"], "New agent teams")
        self.assertEqual(entries[0]["heading"], "Anthropic Blog")


class ExtractIssuesTests(unittest.TestCase):
    def test_skips_prs_and_truncates_body(self):
        pages = [[
            {"title": "Feature X", "html_url": "u1", "body": "b" * 300},
            {"title": "A PR", "html_url": "u2", "pull_request": {}},
        ]]
        entries = ns.extract_issues(pages)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["name"], "Feature X")
        self.assertEqual(len(entries[0]["description"]), 200)


class ExtractDiscussionsTests(unittest.TestCase):
    def test_maps_fields_and_category(self):
        nodes = [{"title": "T", "url": "u", "body": None, "category": {"name": "Feature Requests"}}]
        entries = ns.extract_discussions(nodes)
        self.assertEqual(entries[0]["name"], "T")
        self.assertEqual(entries[0]["description"], "")
        self.assertEqual(entries[0]["heading"], "GitHub Discussions (Feature Requests)")


class GraphQLNavigationTests(unittest.TestCase):
    def test_feature_category_id(self):
        data = {"data": {"repository": {"discussionCategories": {"nodes": [
            {"id": "c1", "name": "General"}, {"id": "c2", "name": "Feature Requests"},
        ]}}}}
        self.assertEqual(ns.feature_category_id(data), "c2")
        self.assertIsNone(ns.feature_category_id(None))
        self.assertIsNone(ns.feature_category_id({"data": {"repository": {"discussionCategories": {"nodes": []}}}}))

    def test_discussion_page(self):
        data = {"data": {"repository": {"discussions": {
            "nodes": [{"title": "D"}], "pageInfo": {"hasNextPage": True, "endCursor": "X"},
        }}}}
        nodes, page = ns.discussion_page(data)
        self.assertEqual(nodes, [{"title": "D"}])
        self.assertTrue(page["hasNextPage"])
        self.assertEqual(ns.discussion_page(None), ([], {}))


if __name__ == "__main__":
    unittest.main()
