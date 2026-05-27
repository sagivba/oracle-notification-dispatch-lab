# Purpose: Repository contract tests for the current Oracle Notification Dispatch Lab baseline.

import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestRepositoryContract(unittest.TestCase):
    """Validate the current repository baseline and core governance contracts."""

    def test_required_current_files_exist(self) -> None:
        required_files = [
            ".env.example",
            ".gitignore",
            ".gitmodules",
            "AGENTS.md",
            "MANIFEST.txt",
            "README.md",
            "docker-compose.yml",
            "pyproject.toml",
            "requirements.txt",
            "scripts/test.sh",
            "scripts/lint.sh",
            "scripts/lab-up.sh",
            "scripts/lab-down.sh",
            "scripts/lab-reset.sh",
            "scripts/lab-backup.sh",
            "scripts/lab-restore.sh",
            "scripts/install-db.sh",
            "scripts/run-db-tests.sh",
            "db/install/install.sql",
            "db/install/00_create_lab_users.sql",
            "db/install/01_create_schema.sql",
            "db/rollback/rollback.sql",
            "db/src/tables/lab_smoke_test.sql",
            "db/tests/sql/001_db_connectivity.sql",
            "db/tests/sql/002_object_inventory.sql",
            "db/tests/sql/003_no_invalid_objects.sql",
            "docs/data-model/notification-dispatch-erd.md",
            "docs/data-model/notification-dispatch-erd.mmd",
            "docs/oracle-notification-dispatch-data-model-he.html",
            "specs/001-notification-dispatch/spec.md",
            "docs/decision-log.md",
        ]

        for relative_path in required_files:
            with self.subTest(path=relative_path):
                self.assertTrue((ROOT / relative_path).is_file(), relative_path)

    def test_required_current_directories_exist(self) -> None:
        required_directories = [
            "db",
            "db/install",
            "db/rollback",
            "db/src",
            "db/src/tables",
            "db/tests",
            "db/tests/sql",
            "db/review",
            "docs",
            "docs/data-model",
            "scripts",
            "tests",
            "tools",
            "tools/ai-git-workflow-tools",
        ]

        for relative_path in required_directories:
            with self.subTest(path=relative_path):
                self.assertTrue((ROOT / relative_path).is_dir(), relative_path)

    def test_project_identity_is_notification_dispatch_lab(self) -> None:
        env_example = (ROOT / ".env.example").read_text(encoding="utf-8")
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

        self.assertIn('PROJECT_NAME="Oracle Notification Dispatch Lab"', env_example)
        self.assertIn('name = "oracle-notification-dispatch-lab"', pyproject)
        self.assertIn("Oracle Notification Dispatch Lab", readme)
        self.assertIn("Oracle Notification Dispatch Lab", agents)

    def test_env_example_is_bash_source_safe(self) -> None:
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

    def test_python_testing_uses_unittest_and_python3_default(self) -> None:
        test_script = (ROOT / "scripts/test.sh").read_text(encoding="utf-8")
        lint_script = (ROOT / "scripts/lint.sh").read_text(encoding="utf-8")

        self.assertIn('unittest discover -s tests -p "test_*.py"', test_script)
        self.assertIn("${PYTHON_BIN:-python3}", test_script)
        self.assertNotIn("pytest", test_script)
        self.assertNotIn("pytest", lint_script)

    def test_database_install_uses_managed_entry_point(self) -> None:
        install_sql = (ROOT / "db/install/install.sql").read_text(encoding="utf-8")

        self.assertIn("@@00_create_lab_users.sql", install_sql)
        self.assertIn("@@01_create_schema.sql", install_sql)
        self.assertIn('define NOTIF_LAB_DB_ROOT = "&5"', install_sql)
        self.assertIn(
            "@@&&NOTIF_LAB_DB_ROOT/src/tables/lab_smoke_test.sql",
            install_sql,
        )
        self.assertEqual("exit success", install_sql.strip().splitlines()[-1].lower())

    def test_current_smoke_schema_uses_existing_ai_app_owner(self) -> None:
        checked_files = [
            "db/install/00_create_lab_users.sql",
            "db/src/tables/lab_smoke_test.sql",
            "db/tests/sql/002_object_inventory.sql",
            "db/tests/sql/003_no_invalid_objects.sql",
        ]

        for relative_path in checked_files:
            with self.subTest(path=relative_path):
                content = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn("NOTIF_APP_OWNER", content)

    def test_scripts_target_current_local_lab_container(self) -> None:
        checked_files = [
            "docker-compose.yml",
            "scripts/lab-up.sh",
            "scripts/lab-down.sh",
            "scripts/lab-reset.sh",
            "scripts/lab-backup.sh",
            "scripts/lab-restore.sh",
            "scripts/install-db.sh",
            "scripts/run-db-tests.sh",
        ]

        for relative_path in checked_files:
            with self.subTest(path=relative_path):
                content = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn("oracle-notification-dispatch-lab-db", content)

    def test_no_obvious_example_secrets_in_managed_files(self) -> None:
        checked_files = [
            ".env.example",
            "db/install/install.sql",
            "db/install/00_create_lab_users.sql",
            "db/install/01_create_schema.sql",
            "db/rollback/rollback.sql",
            "scripts/install-db.sh",
            "scripts/run-db-tests.sh",
        ]
        obvious_secret_pattern = re.compile(r"(?i)(oracle|welcome|passw(?:or)?d)[0-9]+")

        for relative_path in checked_files:
            content = (ROOT / relative_path).read_text(encoding="utf-8")
            with self.subTest(path=relative_path):
                self.assertIsNone(obvious_secret_pattern.search(content))

    def test_notification_dispatch_data_model_documents_cover_core_tables(self) -> None:
        documents = [
            (ROOT / "docs/data-model/notification-dispatch-erd.md").read_text(encoding="utf-8"),
            (ROOT / "docs/data-model/notification-dispatch-erd.mmd").read_text(encoding="utf-8"),
            (ROOT / "docs/oracle-notification-dispatch-data-model-he.html").read_text(
                encoding="utf-8"
            ),
        ]

        for table_name in [
            "NOTIF_CHANNELS",
            "NOTIF_STATUS_CODES",
            "NOTIF_DISPATCH_REQUESTS",
            "NOTIF_DISPATCH_ITEMS",
            "NOTIF_AUDIT_LOG",
        ]:
            for document in documents:
                with self.subTest(table=table_name):
                    self.assertIn(table_name, document)

    def test_decision_log_and_minimal_spec_capture_approved_baseline(self) -> None:
        decision_log = (ROOT / "docs/decision-log.md").read_text(encoding="utf-8")
        spec = (ROOT / "specs/001-notification-dispatch/spec.md").read_text(
            encoding="utf-8"
        )

        for expected in [
            "DEC-001",
            "DEC-006",
            "DEC-007",
            "DEC-008",
            "DEC-009",
            "DEC-010",
            "NOTIF_APP_OWNER",
            "NOTIF_APP_OWNER_PWD",
            "NOTIF_AUDIT_LOG",
            "NOTIF_DISPATCH_REQUESTS",
            "CLOB",
            "unittest",
            "NOTIF_APP_RUNTIME",
            "NOTIF_APP_READONLY",
            "NOTIF_REVIEWER",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, decision_log)

        for expected in [
            "docs/data-model/notification-dispatch-erd.md",
            "docs/data-model/notification-dispatch-erd.mmd",
            "docs/oracle-notification-dispatch-data-model-he.html",
            "Do not invent an alternative data model",
            "NOTIF_APP_OWNER",
            "NOTIF_APP_OWNER_PWD",
            "NOTIF_CHANNELS",
            "NOTIF_STATUS_CODES",
            "NOTIF_EXTERNAL_SYSTEMS",
            "NOTIF_AUDIT_LOG",
            "NOTIF_DISPATCH_REQUESTS",
            "CLOB",
            "target tables",
            "primary keys",
            "foreign keys",
            "check constraints",
            "SQL tests",
            "partitioning",
            "rollback behavior",
            "success criteria",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, spec)

        combined = f"{decision_log}\n{spec}".lower()
        for forbidden_boundary in [
            "real email sending",
            "real whatsapp integration",
            "real telegram integration",
            "real sms integration",
            "external provider integration",
            "organizational database access",
            "secrets",
        ]:
            with self.subTest(boundary=forbidden_boundary):
                self.assertIn(forbidden_boundary, combined)


if __name__ == "__main__":
    unittest.main()
