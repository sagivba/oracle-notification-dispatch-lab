# Purpose: unittest contract coverage for the repository packaging workflow.

from __future__ import annotations

import os
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "package-release.sh"
HELPER = ROOT / "tools" / "package_release.py"
DOC = ROOT / "docs" / "packaging-workflow.md"
DIST_README = ROOT / "db" / "dist" / "README.md"
RELEASE_ROOT = ROOT / "db" / "dist" / "release_001"
OBJECT_TYPE_DIRS = [
    "tables",
    "constraints",
    "indexes",
    "views",
    "packages",
    "triggers",
    "seed",
]
PACKAGE_METADATA_FILES = {"README.md"}


class TestPackagingWorkflowContract(unittest.TestCase):
    """Validate the packaging skeleton without Docker, Oracle, network, or secrets."""

    def test_package_script_exists_is_executable_and_has_purpose_header(self) -> None:
        self.assertTrue(SCRIPT.is_file())
        self.assertTrue(os.access(SCRIPT, os.X_OK))

        script = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("# Purpose:", script.splitlines()[1])

    def test_package_script_calls_python_helper(self) -> None:
        script = SCRIPT.read_text(encoding="utf-8")

        self.assertIn("tools/package_release.py", script)
        self.assertIn("PYTHON_BIN", script)
        self.assertIn("set -euo pipefail", script)
        self.assertIn("AGENTS.md", script)

    def test_python_helper_exists_and_has_purpose_header(self) -> None:
        self.assertTrue(HELPER.is_file())

        helper = HELPER.read_text(encoding="utf-8")
        self.assertTrue(helper.startswith('"""Purpose:'))

    def test_package_output_contract_files_and_folders_exist(self) -> None:
        required_files = [
            "manifest.md",
            "install.sql",
            "rollback.sql",
            "test-report.md",
            "review-report.md",
            "deployment-notes.md",
        ]

        for filename in required_files:
            with self.subTest(filename=filename):
                self.assertTrue((RELEASE_ROOT / filename).is_file(), filename)

        for folder in OBJECT_TYPE_DIRS:
            with self.subTest(folder=folder):
                self.assertTrue((RELEASE_ROOT / "src" / folder).is_dir(), folder)

    def test_package_output_files_start_with_purpose_headers(self) -> None:
        for path in [
            RELEASE_ROOT / "manifest.md",
            RELEASE_ROOT / "install.sql",
            RELEASE_ROOT / "rollback.sql",
            RELEASE_ROOT / "test-report.md",
            RELEASE_ROOT / "review-report.md",
            RELEASE_ROOT / "deployment-notes.md",
        ]:
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                first_line = path.read_text(encoding="utf-8").splitlines()[0]
                self.assertIn("Purpose", first_line)

    def test_package_includes_only_approved_src_object_type_folders(self) -> None:
        src_root = RELEASE_ROOT / "src"
        actual_folders = sorted(path.name for path in src_root.iterdir() if path.is_dir())

        self.assertEqual(sorted(OBJECT_TYPE_DIRS), actual_folders)

        for file_path in src_root.rglob("*"):
            if file_path.is_file():
                rel_parts = file_path.relative_to(src_root).parts
                self.assertIn(rel_parts[0], OBJECT_TYPE_DIRS)
                self.assertTrue(
                    file_path.suffix == ".sql" or file_path.name in PACKAGE_METADATA_FILES,
                    file_path.relative_to(RELEASE_ROOT).as_posix(),
                )

    def test_empty_package_folders_have_deterministic_git_markers(self) -> None:
        for folder in OBJECT_TYPE_DIRS:
            folder_path = RELEASE_ROOT / "src" / folder
            sql_files = sorted(folder_path.glob("*.sql"))
            marker_path = folder_path / "README.md"

            if sql_files:
                self.assertFalse(marker_path.exists())
                continue

            with self.subTest(folder=folder):
                marker = marker_path.read_text(encoding="utf-8")
                self.assertIn("Git does not track empty directories", marker)
                self.assertIn("no managed SQL files exist", marker)
                self.assertIn(f"`src/{folder}/`", marker)
                self.assertNotIn(str(ROOT), marker)

    def test_local_env_files_and_obvious_secrets_are_not_packaged(self) -> None:
        package_paths = [
            path.relative_to(RELEASE_ROOT).as_posix() for path in RELEASE_ROOT.rglob("*")
        ]

        for rel_path in package_paths:
            with self.subTest(path=rel_path):
                self.assertFalse(rel_path.startswith(".env"))
                self.assertNotIn("/.env", rel_path)

        package_text = "\n".join(
            path.read_text(encoding="utf-8") for path in RELEASE_ROOT.rglob("*") if path.is_file()
        )
        obvious_secret_pattern = re.compile(
            r"Password123|Welcome1|Oracle123|BEGIN RSA PRIVATE KEY|PRIVATE KEY"
        )

        self.assertIsNone(obvious_secret_pattern.search(package_text))

    def test_helper_rejects_env_and_secret_patterns(self) -> None:
        helper = HELPER.read_text(encoding="utf-8")

        self.assertIn(r"(^|/)\.env(\..*)?$", helper)
        self.assertIn("SECRET_FILENAME_PATTERNS", helper)
        self.assertIn("SECRET_CONTENT_PATTERNS", helper)
        self.assertIn("Refusing to package possible secret-bearing file", helper)

    def test_helper_does_not_contain_oracle_connection_or_docker_logic(self) -> None:
        helper = HELPER.read_text(encoding="utf-8")
        forbidden_tokens = [
            "sqlplus",
            "cx_Oracle",
            "oracledb.connect",
            "docker",
            "docker compose",
            "CREATE TABLE",
            "INSERT INTO",
        ]

        for token in forbidden_tokens:
            with self.subTest(token=token):
                self.assertNotIn(token, helper)

    def test_blocker_behavior_is_represented_in_contract(self) -> None:
        helper = HELPER.read_text(encoding="utf-8")
        manifest = (RELEASE_ROOT / "manifest.md").read_text(encoding="utf-8")
        deployment_notes = (RELEASE_ROOT / "deployment-notes.md").read_text(encoding="utf-8")
        doc = DOC.read_text(encoding="utf-8")

        self.assertIn("review_report_has_blocker_finding", helper)
        self.assertIn("NOT APPROVED - review approval not recorded", manifest)
        self.assertIn("A release package is not approved if any BLOCKER exists", deployment_notes)
        self.assertIn("A release package is not approved if any BLOCKER exists", doc)

    def test_docs_and_dist_readme_describe_package_boundaries(self) -> None:
        doc = DOC.read_text(encoding="utf-8")
        readme = DIST_README.read_text(encoding="utf-8")

        for content in [doc, readme]:
            normalized = " ".join(content.split())
            with self.subTest():
                self.assertIn("package", normalized.lower())
                self.assertIn("does not connect to Oracle", normalized)
                self.assertIn("does not run Docker", normalized)
                self.assertIn("does not execute ad-hoc DDL or DML", normalized)

    def test_packaging_tests_are_unittest_based(self) -> None:
        test_file = Path(__file__).read_text(encoding="utf-8")

        self.assertIn("import unittest", test_file)
        self.assertIn("unittest.TestCase", test_file)
        self.assertNotIn("py" + "test", test_file)


if __name__ == "__main__":
    unittest.main()
