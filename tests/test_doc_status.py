"""Unit tests for lib/doc_status.py (pure doc-status validation logic, #348)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".github" / "scripts"))

from lib import doc_status as ds  # noqa: E402

CLEAN = "---\ntitle: X\nstatus: adopt\n---\n\n## What It Is\n\nbody\n"
BADGE = "---\ntitle: X\n---\n\n**Status**: Adopt\n\n## What It Is\n\nbody\n"
BADGE_AND_FM = "---\ntitle: X\nstatus: research\n---\n\n**Status**: Research (informational)\n\n## Body\n"
# A doc badge in the preamble, plus a `**Status**:` line under a later section.
INBODY = (
    "---\ntitle: X\nstatus: assess\n---\n\n**Status**: Assess\n\n"
    "## Section\n\n**Status**: In progress with community collaboration\n"
)
# Post-migration state (cf. agent-observability-methods-analysis.md): fm status,
# NO preamble badge, only an in-section `**Status**:` line describing upstream.
MIGRATED_INBODY = (
    "---\ntitle: X\nstatus: assess\n---\n\n"
    "## Section\n\n**Status**: In progress with community collaboration\n"
)


class FrontmatterStatusTests(unittest.TestCase):
    def test_reads_token(self):
        self.assertEqual(ds.frontmatter_status(CLEAN), "adopt")

    def test_none_without_status_or_frontmatter(self):
        self.assertIsNone(ds.frontmatter_status(BADGE))
        self.assertIsNone(ds.frontmatter_status("no frontmatter here"))


class PreambleBadgeTests(unittest.TestCase):
    def test_finds_doc_badge(self):
        self.assertEqual(ds.preamble_badge(BADGE), "Adopt")

    def test_ignores_status_line_under_a_heading(self):
        # Only the preamble badge counts; the in-section line is left alone.
        self.assertEqual(ds.preamble_badge(INBODY), "Assess")

    def test_none_when_no_badge(self):
        self.assertIsNone(ds.preamble_badge(CLEAN))


class CheckDocTests(unittest.TestCase):
    def test_lenient_passes_valid_token(self):
        self.assertEqual(ds.check_doc("d.md", CLEAN, strict=False), [])

    def test_lenient_flags_invalid_token(self):
        text = "---\nstatus: bogus\n---\n\n## B\n"
        v = ds.check_doc("d.md", text, strict=False)
        self.assertEqual(len(v), 1)
        self.assertEqual(v[0].kind, "invalid-token")

    def test_lenient_ignores_badge(self):
        # A body badge alone is not a lenient-mode violation (mid-migration).
        self.assertEqual(ds.check_doc("d.md", BADGE, strict=False), [])

    def test_strict_flags_residual_badge(self):
        v = ds.check_doc("d.md", BADGE_AND_FM, strict=True)
        self.assertEqual([x.kind for x in v], ["residual-badge"])

    def test_strict_flags_preamble_badge_even_with_in_section_line(self):
        # A preamble badge is still a violation; the in-section line is ignored.
        v = ds.check_doc("d.md", INBODY, strict=True)
        self.assertEqual([x.kind for x in v], ["residual-badge"])
        self.assertIn("Assess", v[0].detail)

    def test_strict_ignores_in_section_status_line(self):
        # Post-migration: fm token + only an in-section **Status**: line -> clean.
        self.assertEqual(ds.check_doc("d.md", MIGRATED_INBODY, strict=True), [])

    def test_strict_still_flags_invalid_token(self):
        text = "---\nstatus: bogus\n---\n\n**Status**: Bogus\n\n## B\n"
        kinds = sorted(x.kind for x in ds.check_doc("d.md", text, strict=True))
        self.assertEqual(kinds, ["invalid-token", "residual-badge"])


class VocabTests(unittest.TestCase):
    def test_vocab_is_lifecycle_plus_plan_tokens(self):
        # Plan 0015 F3: status is lifecycle only (CONTRIBUTING §2); plans add their own four.
        self.assertEqual(ds.VOCAB, ds.DOC_STATUS_VOCAB | ds.PLAN_STATUS_VOCAB)
        self.assertEqual(
            ds.DOC_STATUS_VOCAB,
            {"adopt", "trial", "assess", "hold", "research", "reference", "archived"},
        )
        self.assertEqual(ds.PLAN_STATUS_VOCAB, {"draft", "approved", "done", "superseded"})

    def test_release_and_licence_tokens_rejected(self):
        # These moved to the **Details:** line in F3; a status: carrying one is invalid.
        for token in ("generally-available", "beta", "open-source", "verified", "completed"):
            v = ds.check_doc("d.md", f"---\nstatus: {token}\n---\n\n## B\n", strict=False)
            self.assertEqual([x.kind for x in v], ["invalid-token"], token)


class ReportTests(unittest.TestCase):
    def test_ok_when_clean(self):
        self.assertEqual(ds.render_report([]), "doc-status: OK")

    def test_lists_violations(self):
        v = ds.check_doc("d.md", "---\nstatus: bogus\n---\n\n## B\n", strict=False)
        report = ds.render_report(v)
        self.assertIn("1 violation", report)
        self.assertIn("d.md", report)


if __name__ == "__main__":
    unittest.main()
