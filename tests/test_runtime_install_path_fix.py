# Purpose: unittest coverage for the current runtime install path contract.

import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestRuntimeInstallPathFix(unittest.TestCase):
    """Validate the focused runtime install contract without connecting to Oracle."""

    def test_env_example_lists_required_local_password_placeholders(self) -> None:
        env_example = (ROOT / ".env.example").read_text(encoding="utf-8")

        for variable_name in [
            "NOTIF_APP_OWNER_PWD",
            "AI_APP_RUNTIME_PWD",
            "AI_APP_READONLY_PWD",
            "AI_REVIEWER_PWD",
        ]:
            with self.subTest(variable=variable_name):
                self.assertIn(
                    f"{variable_name}=change_me_in_local_env",
                    env_example,
                )

    def test_env_example_project_name_is_bash_source_safe(self) -> None:
        env_example = (ROOT / ".env.example").read_text(encoding="utf-8")

        self.assertIn('PROJECT_NAME="Oracle Notification Dispatch Lab"', env_example)

        completed = subprocess.run(
            [
                "bash",
                "-c",
                "set -euo pipefail; source .env.example; printf '%s' \"$PROJECT_NAME\"",
            ],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )

        self.assertEqual("Oracle Notification Dispatch Lab", completed.stdout)

    def test_install_sql_terminates_sqlplus(self) -> None:
        install_sql_lines = [
            line.strip().lower()
            for line in (ROOT / "db/install/install.sql").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

        self.assertEqual("exit success", install_sql_lines[-1])

    def test_install_script_fails_after_sqlplus_error_markers(self) -> None:
        install_script = (ROOT / "scripts/install-db.sh").read_text(encoding="utf-8")

        self.assertIn("install_output=", install_script)
        self.assertIn("install_status=$?", install_script)
        self.assertIn('[[ "$install_status" -ne 0 ]]', install_script)
        self.assertIn('sqlplus_output_has_error "$install_output"', install_script)
        self.assertIn("(SP2-|ORA-|PLS-)", install_script)
        self.assertIn(
            "SQLPlus install output contained SP2-, ORA-, or PLS- errors.",
            install_script,
        )

    def test_success_message_is_shell_gated_not_sql_gated(self) -> None:
        install_sql = (ROOT / "db/install/install.sql").read_text(encoding="utf-8")
        install_script = (ROOT / "scripts/install-db.sh").read_text(encoding="utf-8")

        self.assertNotIn("Oracle AI Lab controlled install completed.", install_sql)
        self.assertIn("Oracle AI Lab controlled install completed.", install_script)

    def test_smoke_object_uses_explicit_remote_db_root(self) -> None:
        install_sql = (ROOT / "db/install/install.sql").read_text(encoding="utf-8")
        install_script = (ROOT / "scripts/install-db.sh").read_text(encoding="utf-8")

        self.assertIn('define ORACLE_AI_LAB_DB_ROOT = "&5"', install_sql)
        self.assertIn(
            "@@&&ORACLE_AI_LAB_DB_ROOT/src/tables/lab_smoke_test.sql",
            install_sql,
        )
        self.assertIn('"$REMOTE_DB_DIR" 2>&1)', install_script)
        self.assertNotIn("@@../src/tables/lab_smoke_test.sql", install_sql)

    def test_all_managed_sql_smoke_tests_terminate_sqlplus(self) -> None:
        smoke_test_dir = ROOT / "db/tests/sql"

        for sql_file in sorted(smoke_test_dir.glob("*.sql")):
            with self.subTest(path=sql_file.name):
                sql_lines = [
                    line.strip().lower()
                    for line in sql_file.read_text(encoding="utf-8").splitlines()
                    if line.strip()
                ]

                self.assertEqual("exit success", sql_lines[-1])


if __name__ == "__main__":
    unittest.main()
