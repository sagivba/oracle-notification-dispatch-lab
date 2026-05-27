# Purpose: unittest contract coverage for the current repository packaging workflow baseline.

from __future__ import annotations

import os
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "package-release.sh"


class TestPackagingWorkflowContract(unittest.TestCase):
    """Validate the current packaging entry point without Docker, Oracle, network, or secrets."""

    def test_package_script_exists_is_executable_and_has_purpose_header(self) -> None:
        self.assertTrue(SCRIPT.is_file())
        self.assertTrue(os.access(SCRIPT, os.X_OK))

        script = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("# Purpose:", script.splitlines()[1])

    def test_package_script_is_repository_local_entry_point(self) -> None:
        script = SCRIPT.read_text(encoding="utf-8")

        self.assertIn("set -euo pipefail", script)
        self.assertIn("REPO_ROOT", script)
        self.assertIn("AGENTS.md", script)
        self.assertIn("tools/package_release.py", script)
        self.assertIn("PYTHON_BIN", script)

    def test_package_script_does_not_connect_to_runtime_or_external_systems(self) -> None:
        script = SCRIPT.read_text(encoding="utf-8")

        forbidden_tokens = [
            "docker exec",
            "docker compose up",
            "sqlplus",
            "cx_Oracle",
            "oracledb.connect",
            "CREATE TABLE",
            "INSERT INTO",
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

    def test_current_packaging_contract_does_not_require_generated_package_yet(self) -> None:
        """The current baseline has only the shell entry point; package output is future work."""

        self.assertTrue(SCRIPT.is_file())
        self.assertFalse((ROOT / "tools" / "package_release.py").exists())
        self.assertFalse((ROOT / "docs" / "packaging-workflow.md").exists())
        self.assertFalse((ROOT / "db" / "dist" / "release_001").exists())

    def test_packaging_tests_are_unittest_based(self) -> None:
        test_file = Path(__file__).read_text(encoding="utf-8")

        self.assertIn("import unittest", test_file)
        self.assertIn("unittest.TestCase", test_file)
        self.assertNotIn("py" + "test", test_file)


if __name__ == "__main__":
    unittest.main()
