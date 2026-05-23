# Purpose: unittest contract coverage for the repository review workflow.

from __future__ import annotations

import os
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "review-db-code.sh"
REPORT = ROOT / "db" / "review" / "review-report.md"
DOC = ROOT / "docs" / "review-workflow.md"


class TestReviewWorkflowContract(unittest.TestCase):
    """Validate the review skeleton without Docker, Oracle, network, or secrets."""

    def test_review_script_exists_and_is_executable(self) -> None:
        self.assertTrue(SCRIPT.is_file())
        self.assertTrue(os.access(SCRIPT, os.X_OK))

    def test_review_report_exists_and_has_required_sections(self) -> None:
        report = REPORT.read_text(encoding="utf-8")
        required_sections = [
            "## Spec coverage",
            "## Infrastructure decisions coverage",
            "## Object inventory",
            "## Data model review",
            "## PL/SQL review",
            "## Security review",
            "## Deployment review",
            "## Risks",
            "## Required fixes",
            "## Optional improvements",
            "## Approval status",
        ]

        for section in required_sections:
            with self.subTest(section=section):
                self.assertIn(section, report)

    def test_review_report_has_severity_levels_and_blocker_rule(self) -> None:
        report = REPORT.read_text(encoding="utf-8")

        for severity in ["BLOCKER", "MAJOR", "MINOR", "QUESTION"]:
            with self.subTest(severity=severity):
                self.assertIn(severity, report)

        self.assertIn("A release package is not approved if any BLOCKER exists.", report)

    def test_review_workflow_documentation_exists_and_has_safety_boundaries(self) -> None:
        doc = DOC.read_text(encoding="utf-8")

        self.assertIn("## Safety Boundaries", doc)
        self.assertIn("must not connect to organizational databases", doc)
        self.assertIn("must not execute ad-hoc DDL or DML", doc)
        self.assertIn("oracle-dev-ai-lab-db", doc)
        self.assertIn("release packaging", doc)

    def test_review_script_uses_local_project_paths_and_managed_files(self) -> None:
        script = SCRIPT.read_text(encoding="utf-8")

        for expected in [
            "REPO_ROOT",
            "db/review/review-report.md",
            "db/src/tables/lab_smoke_test.sql",
            "db/install/install.sql",
            "scripts/install-db.sh",
            "scripts/run-db-tests.sh",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, script)

    def test_review_script_avoids_obvious_forbidden_targets_and_secrets(self) -> None:
        script = SCRIPT.read_text(encoding="utf-8")
        forbidden_tokens = [
            "prod-db",
            "staging-db",
            "shared-db",
            "Password123",
            "Welcome1",
            "Oracle123",
            "BEGIN RSA",
            "PRIVATE KEY",
        ]

        for token in forbidden_tokens:
            with self.subTest(token=token):
                self.assertNotIn(token, script)

    def test_review_script_does_not_require_runtime_db_by_default(self) -> None:
        script = SCRIPT.read_text(encoding="utf-8")

        self.assertNotIn("docker exec", script)
        self.assertNotIn("sqlplus", script)
        self.assertIn("repository-only", script)


if __name__ == "__main__":
    unittest.main()
