# AGENTS.md

Instructions for Codex CLI, ChatGPT, and any other AI-assisted workflow operating in this repository.

These rules are mandatory. They are not suggestions.

## 1. Project Identity

Repository:

```text
oracle-notification-dispatch-lab
```

Project display name:

```text
Oracle Notification Dispatch Lab
```

Project purpose:

```text
Develop the Oracle database layer of a fictional multi-channel notification and message dispatch system.
```

This repository is not a generic Oracle template.

This repository is not the infrastructure-building project that created the original lab.

This repository is the working lab for developing database objects for the notification and messaging domain.

## 2. Functional Domain

The functional domain is a fictional notification and message dispatch system.

Relevant domain concepts may include:

- notification channels;
- message templates;
- recipients;
- recipient groups;
- dispatch requests;
- dispatch items;
- delivery attempts;
- delivery statuses;
- retry metadata;
- provider response logs;
- audit data.

The system may conceptually refer to channels such as email, WhatsApp, Telegram, SMS, or other channels selected later.

This project must not implement real delivery to any external channel unless explicitly approved in a future project decision.

## 3. Existing Infrastructure

The repository already contains an Oracle lab baseline.

The following infrastructure must be treated as existing project infrastructure:

- Oracle Docker lab scripts;
- database install scripts;
- database test scripts;
- review workflow;
- packaging workflow;
- Python repository contract tests;
- AGW integration under `tools/ai-git-workflow-tools`.

AI agents must use this infrastructure.

AI agents must not rebuild, replace, redesign, or reintroduce the old infrastructure-building workflow unless explicitly instructed.

AI agents must not recreate the old project history, old goal files, old stage reports, old experiments, or the previous release-management use case.

## 4. Core Operating Principles

### 4.1 GitHub is the single source of truth

GitHub and the files versioned in this repository are the only source of truth.

The local Oracle database is disposable runtime state only.

The local Oracle database must be reproducible from Git-managed files.

If database state conflicts with Git state, Git state wins.

No database change is valid unless it exists as a versioned file in this repository and can be executed through an official project script.

### 4.2 Verify everything that can reasonably be verified

For every task, AI agents must verify every success criterion that can reasonably be verified.

AI agents must not claim that a task is complete unless the relevant checks were actually performed.

Verification may include, depending on the task:

- repository checks;
- Python `unittest` checks;
- shell syntax checks;
- SQL install checks;
- SQL smoke tests;
- object inventory checks;
- invalid object checks;
- metadata checks;
- review scripts;
- package generation checks.

### 4.3 Report exactly what was verified

Every task result must explicitly report:

- what was checked;
- how it was checked;
- which commands were run;
- what the result was;
- what was not checked;
- why it was not checked;
- whether any missing check limits confidence in the result.

If a required check cannot be performed, the agent must say so directly.

### 4.4 Partial verification means partial completion

If an agent cannot verify one or more required success criteria, it must not report the task as fully complete.

It must report the task as one of:

- complete and verified;
- implemented but partially verified;
- blocked;
- failed.

### 4.5 No hidden database state

Agents must not rely on database state that cannot be reproduced from Git.

Any object, data, grant, package, index, view, trigger, seed data, rollback step, or test required by the project must be represented in a versioned repository file.

### 4.6 Official scripts are the execution boundary

Database work must be executed through official project scripts.

Agents must not perform ad-hoc DDL or DML directly against the database.

SELECT statements are allowed only for diagnostics, metadata inspection, compile checks, test verification, and review.

## 5. Current Work Mode

The repository is currently being stabilized manually.

Codex or other implementation agents may work only when the repository owner gives an explicit task.

Agents must not assume that Codex-driven implementation is currently enabled by default.

Until explicitly instructed otherwise, agents must help stabilize the repository, project instructions, documentation, tests, and task model before functional database development begins.

## 6. Git and GitHub Workflow

AGW is the preferred workflow tool for Git and GitHub operations when it provides a relevant function.

Load AGW from the repository root:

```bash
source tools/ai-git-workflow-tools/scripts/load-agw.sh
```

Basic checks:

```bash
agw_status
agw_review_output --run
```

If AGW does not cover a required operation, direct `git` or `gh` commands may be used, but the agent must report that direct commands were used.

Agents must not perform force push, branch deletion, tag deletion, repository deletion, or destructive Git operations unless explicitly instructed.

## 7. Branch Discipline

Use task branches for changes.

Do not work directly on `main` unless explicitly instructed.

When AGW is used for manual tasks, its default manual branch convention may be used.

When a Codex-specific branch is explicitly required, use a clear branch name such as:

```text
codex-cli/T0001-short-task-name
```

Agents must run `git fetch` or an AGW equivalent before starting branch work.

## 8. Database Change Rules

Every database change must be represented as a versioned repository file.

Database changes must be placed under the appropriate `db/` path.

Typical locations:

```text
db/install/
db/src/tables/
db/src/constraints/
db/src/indexes/
db/src/views/
db/src/packages/
db/src/triggers/
db/src/seed/
db/rollback/
db/tests/sql/
```

Database changes must be installed only through official scripts, such as:

```bash
scripts/install-db.sh
```

Database validation must use official scripts, such as:

```bash
scripts/run-db-tests.sh smoke
scripts/review-db-code.sh
```

Agents must not execute manual DDL or DML against the database.

Forbidden examples unless explicitly represented in versioned files and executed through official scripts:

```sql
CREATE TABLE ...
ALTER TABLE ...
DROP TABLE ...
INSERT ...
UPDATE ...
DELETE ...
MERGE ...
GRANT ...
REVOKE ...
```

## 9. Task Artifact Naming Convention

Every task file that installs, changes, or validates a database component must use this naming convention:

```text
T{XXXX}-{task_name}-{schema_name}-{object_name}.[sql|sh]
```

Rules:

- `XXXX` must be a four-digit running number, for example `0001`.
- `task_name` must be a short lowercase English task name.
- Words in `task_name` must be separated with hyphens.
- `schema_name` must be the Oracle schema name, normally uppercase.
- `object_name` must be the Oracle object name, normally uppercase.
- The separator between `schema_name` and `object_name` must be a hyphen.
- Do not use a dot between `schema_name` and `object_name`.
- The file extension must reflect the file type.

Examples:

```text
T0001-create-table-AI_APP_OWNER-NOTIF_CHANNELS.sql
T0002-create-index-AI_APP_OWNER-NOTIF_CHANNELS_UK1.sql
T0003-seed-data-AI_APP_OWNER-NOTIF_STATUS_CODES.sql
T0004-run-check-AI_APP_OWNER-NOTIF_CHANNELS.sh
```

Each task artifact must contain:

- a short purpose header;
- the reason the artifact exists;
- the object definition, installation logic, validation logic, or controlled operation;
- enough context for review.

## 10. Required Test Per Stage

Every development stage must include a test that demonstrates that the stage works.

A database-related stage is not complete without an appropriate validation artifact or validation command.

Possible validation methods include:

- SQL smoke tests;
- object inventory checks;
- invalid object checks;
- metadata checks;
- install checks;
- review checks;
- package generation checks.

If a test cannot be created or run, the agent must report the limitation explicitly.

## 11. Static Repository Mode

Static repository mode is appropriate for work that does not require access to Docker or Oracle runtime.

Examples:

- editing documentation;
- editing specifications;
- reviewing repository files;
- updating Python repository tests;
- running `unittest`;
- running shell syntax checks;
- inspecting Git status and diffs;
- preparing task definitions.

Static work must not claim Oracle runtime validation.

## 12. Local Oracle Runtime Mode

Local Oracle runtime mode is required when a task must prove behavior inside the local Oracle database.

Examples:

- Docker inspection;
- starting the Oracle lab;
- running `scripts/install-db.sh`;
- running `scripts/run-db-tests.sh`;
- using SQLcl against `localhost:1521/FREEPDB1`;
- using SQLPlus inside the container;
- checking real Oracle objects;
- checking invalid objects;
- checking grants.

Runtime work must be explicitly authorized by the task.

Runtime work must use only the local lab database.

## 13. External Systems Are Forbidden

Agents must not connect to real external systems.

Forbidden unless explicitly approved in a future decision:

- real email providers;
- WhatsApp APIs;
- Telegram APIs;
- SMS providers;
- organizational services;
- production systems;
- staging systems;
- organizational development databases;
- organizational test databases.

Agents must not add credentials, API keys, tokens, or real provider configuration.

## 14. Secrets Policy

Agents must not commit or print secrets.

Forbidden:

- passwords;
- tokens;
- API keys;
- private keys;
- certificates;
- real connection strings;
- provider credentials;
- `.env` files;
- local secret-bearing files.

Tracked examples such as `.env.example` may contain placeholders only.

## 15. Destructive Operations

The following operations are forbidden unless explicitly approved by the repository owner:

```text
docker rm
docker volume rm
docker network rm
scripts/lab-reset.sh
rm -rf
sudo
force push
branch deletion
tag deletion
repository deletion
```

If a destructive operation is requested, the agent must restate the target and risk before execution.

## 16. Python Testing Rules

This project uses Python `unittest`.

Agents must not introduce `pytest`.

Repository checks should use the project scripts where possible:

```bash
scripts/test.sh quick
scripts/lint.sh
```

If a script fails, the agent must report the failure and must not claim success.

## 17. Documentation Rules

Documentation must describe the current project, not the old infrastructure-building project.

Do not reintroduce documentation for:

- old Codex goals;
- old stage reports;
- old boundary experiments;
- old release-management use case;
- old project setup history;
- generic Oracle templates.

Documentation should support the current goal: controlled Oracle database development for the fictional notification and messaging system.

## 18. Task Result Format

Every task response must include:

```text
Summary
Files created
Files updated
Commands run
Checks run
Checks not run and why
Verification result
Assumptions
Limitations
Recommended next step
```

If no commands were run, state that explicitly.

If no runtime validation was performed, state that explicitly.

If the task is only partially verified, state that explicitly.

## 19. Stop Conditions

Agents must stop and ask for guidance when:

- requirements are ambiguous;
- a change would affect unrelated files;
- a database operation would be destructive;
- a task requires secrets;
- a task requires access to an external provider;
- a task requires organizational database access;
- a required success criterion cannot be interpreted;
- the requested change conflicts with these instructions.

Agents must not guess through safety, scope, or data-boundary conflicts.

## 20. Final Rule

Use the existing lab infrastructure.

Develop only the database layer of the fictional notification and messaging system.

Verify everything that can be verified.

Report exactly what was verified and what was not verified.

Keep GitHub as the single source of truth.
