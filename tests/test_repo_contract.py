# Purpose: Repository contract tests for Goals 005, 007, and 008 of oracle-dev-ai-lab.

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestRepositoryContract(unittest.TestCase):
    """Validate the repository structure and core governance contracts."""

    def test_required_files_exist(self) -> None:
        required_files = [
            "AGENTS.md",
            "TODO.md",
            "docs/project-charter.md",
            "docs/safety-rules.md",
            "docs/decision-log.md",
            "docs/repository-structure.md",
            "docs/codex-workflow.md",
            "docs/testing-strategy.md",
            "docs/install-workflow.md",
            "scripts/test.sh",
            "scripts/lint.sh",
            "scripts/install-db.sh",
            "scripts/run-db-tests.sh",
            "docker-compose.yml",
            "docs/docker-lab-design.md",
            "db/install/install.sql",
            "db/install/00_create_lab_users.sql",
            "db/install/01_create_schema.sql",
            "db/rollback/rollback.sql",
            "db/src/tables/lab_smoke_test.sql",
            "db/tests/sql/001_db_connectivity.sql",
            "db/tests/sql/002_object_inventory.sql",
            "db/tests/sql/003_no_invalid_objects.sql",
            "docs/stages/stage-08-task-G008-db-smoke-tests.html",
        ]

        for relative_path in required_files:
            with self.subTest(path=relative_path):
                self.assertTrue((ROOT / relative_path).is_file(), relative_path)

    def test_required_directories_exist(self) -> None:
        required_directories = [
            "docs/stages",
            "db",
            "db/install",
            "db/src",
            "db/src/tables",
            "db/src/constraints",
            "db/src/indexes",
            "db/src/views",
            "db/src/packages",
            "db/src/triggers",
            "db/src/seed",
            "db/rollback",
            "db/tests",
            "db/tests/sql",
            "db/tests/utplsql",
            "db/review",
            "db/generated",
            "db/dist",
            "specs/001-release-management",
            "specs/001-release-management/tasks",
            "tools",
        ]

        for relative_path in required_directories:
            with self.subTest(path=relative_path):
                self.assertTrue((ROOT / relative_path).is_dir(), relative_path)

    def test_scripts_test_sh_supports_quick_and_full(self) -> None:
        test_script = (ROOT / "scripts/test.sh").read_text(encoding="utf-8")

        self.assertIn('MODE="${1:-quick}"', test_script)
        self.assertIn("quick)", test_script)
        self.assertIn("full)", test_script)
        self.assertIn('python -m unittest discover -s tests -p "test_*.py"', test_script)

    def test_python_testing_framework_is_unittest(self) -> None:
        test_script = (ROOT / "scripts/test.sh").read_text(encoding="utf-8")
        lint_script = (ROOT / "scripts/lint.sh").read_text(encoding="utf-8")

        self.assertNotIn("pytest", test_script)
        self.assertNotIn("pytest", lint_script)

        strategy_doc = (ROOT / "docs/testing-strategy.md").read_text(encoding="utf-8")
        self.assertIn("unittest", strategy_doc)
        self.assertIn("Do not require `pytest`.", strategy_doc)

    def test_goal_007_install_sql_references_managed_files(self) -> None:
        install_sql = (ROOT / "db/install/install.sql").read_text(encoding="utf-8")

        self.assertIn("@@00_create_lab_users.sql", install_sql)
        self.assertIn("@@01_create_schema.sql", install_sql)
        self.assertIn('define ORACLE_AI_LAB_DB_ROOT = "&5"', install_sql)
        self.assertIn(
            "@@&&ORACLE_AI_LAB_DB_ROOT/src/tables/lab_smoke_test.sql",
            install_sql,
        )

    def test_goal_008_install_creates_required_lab_users(self) -> None:
        users_sql = (ROOT / "db/install/00_create_lab_users.sql").read_text(encoding="utf-8")

        for user_name in [
            "AI_APP_OWNER",
            "AI_APP_RUNTIME",
            "AI_APP_READONLY",
            "AI_REVIEWER",
        ]:
            with self.subTest(user=user_name):
                self.assertIn(user_name, users_sql)

        self.assertIn("&&AI_APP_OWNER_PWD", users_sql)
        self.assertIn("&&AI_APP_RUNTIME_PWD", users_sql)
        self.assertIn("&&AI_APP_READONLY_PWD", users_sql)
        self.assertIn("&&AI_REVIEWER_PWD", users_sql)
        self.assertIn("grant create table to AI_APP_OWNER", users_sql)
        self.assertIn("grant create session to AI_APP_OWNER", users_sql)
        self.assertIn("quota unlimited on USERS", users_sql)
        self.assertNotRegex(users_sql, r"(?i)grant\s+dba\b")
        self.assertNotRegex(users_sql, r"(?i)grant\s+resource\b")

    def test_goal_007_install_script_targets_local_lab_only(self) -> None:
        install_script = (ROOT / "scripts/install-db.sh").read_text(encoding="utf-8")

        self.assertIn("db/install", install_script)
        self.assertIn("install.sql", install_script)
        self.assertIn("oracle-dev-ai-lab-db", install_script)
        self.assertIn("FREEPDB1", install_script)
        self.assertIn('"$REMOTE_DB_DIR"', install_script)
        self.assertIn("sqlplus_output_has_error", install_script)
        self.assertIn("SP2-", install_script)
        self.assertIn("ORA-", install_script)
        self.assertIn("PLS-", install_script)

    def test_goal_008_smoke_test_runner_targets_local_lab_only(self) -> None:
        run_tests_script = (ROOT / "scripts/run-db-tests.sh").read_text(encoding="utf-8")

        self.assertIn("db/tests/sql", run_tests_script)
        self.assertIn("oracle-dev-ai-lab-db", run_tests_script)
        self.assertIn("FREEPDB1", run_tests_script)
        self.assertIn("sqlplus", run_tests_script)

    def test_goal_008_smoke_object_is_infrastructure_only(self) -> None:
        checked_files = [
            "db/src/tables/lab_smoke_test.sql",
            "db/tests/sql/001_db_connectivity.sql",
            "db/tests/sql/002_object_inventory.sql",
            "db/tests/sql/003_no_invalid_objects.sql",
            "scripts/run-db-tests.sh",
        ]
        forbidden_business_terms = [
            "RELEASE_REQUESTS",
            "RELEASE_ITEMS",
            "RELEASE_ENVIRONMENTS",
            "RELEASE_STATUSES",
            "RELEASE_APPROVALS",
            "RELEASE_EXECUTION_LOG",
        ]

        for relative_path in checked_files:
            content = (ROOT / relative_path).read_text(encoding="utf-8")
            for forbidden_term in forbidden_business_terms:
                with self.subTest(path=relative_path, term=forbidden_term):
                    self.assertNotIn(forbidden_term, content)

    def test_goal_008_runner_is_executable(self) -> None:
        self.assertTrue((ROOT / "scripts/run-db-tests.sh").stat().st_mode & 0o111)

    def test_goal_007_files_do_not_contain_obvious_example_secrets(self) -> None:
        checked_files = [
            "db/install/install.sql",
            "db/install/00_create_lab_users.sql",
            "db/install/01_create_schema.sql",
            "db/rollback/rollback.sql",
            "scripts/install-db.sh",
            "scripts/run-db-tests.sh",
            "docs/install-workflow.md",
        ]
        obvious_secret_pattern = re.compile(r"(?i)(oracle|welcome|passw(?:or)?d)[0-9]+")

        for relative_path in checked_files:
            content = (ROOT / relative_path).read_text(encoding="utf-8")
            with self.subTest(path=relative_path):
                self.assertIsNone(obvious_secret_pattern.search(content))

    def test_goal_005_does_not_require_later_goal_artifacts(self) -> None:
        optional_paths = [
            "scripts/review-db-code.sh",
            "scripts/package-release.sh",
        ]

        for relative_path in optional_paths:
            with self.subTest(path=relative_path):
                path = ROOT / relative_path
                self.assertTrue(
                    not path.exists() or path.is_file(),
                    relative_path,
                )
