# Oracle Notification Dispatch Lab

A clean Oracle database lab for evaluating Codex-assisted development of a fictional multi-channel notification dispatch system.

This project focuses on the **database layer only**.

The fictional system is intended to manage notification dispatch requests across channels such as email, WhatsApp, Telegram, or any other channel selected later.

At this stage, the project does **not** implement real message sending, does **not** connect to external messaging providers, does **not** include an API, does **not** include a UI, and does **not** integrate with real organizational systems.

## Project Purpose

The purpose of this project is to evaluate an isolated Oracle development lab in which Oracle database objects can be developed, tested, reviewed, and packaged from Git-managed files while using Codex in a controlled workflow.

The functional domain is a fictional multi-channel notification dispatch system.

The main goal is not to build a production messaging system.  
The main goal is to test and refine a disciplined workflow for Codex-assisted Oracle database development.

## Development Model

The development process will follow this model:

1. Functional and technical analysis is performed **outside Codex**.
2. The work is divided into small tasks **outside Codex**.
3. Each task must include:
   - a clear scope;
   - success criteria;
   - the recommended model or effort level for Codex;
   - required files to create or update;
   - required validation steps.
4. Each task is then given to Codex for implementation.
5. Codex must complete the task and verify that it meets the success criteria.
6. If Codex cannot verify one or more success criteria, it must report that the task is not fully complete and explicitly state what it could not verify.
7. Every database-related task must include controlled installation or validation artifacts.
8. Every stage must include a test that demonstrates the correctness of that stage.

This workflow is intended to make Codex behavior measurable, reviewable, and repeatable when working with Oracle database development.

## Task Artifact Naming Convention

Every task file that installs, changes, or validates a database component must use the following naming convention:

```text
T{XXXX}-{task_name}-{schema_name}-{object_name}.[sql|sh]
```

Where:

- `XXXX` is a four-digit running task number, for example `0001`.
- `task_name` is a short lowercase English task name.
- Words in `task_name` must be separated with hyphens.
- `schema_name` is the Oracle schema name, normally uppercase.
- `object_name` is the Oracle object name, normally uppercase.
- The separator between `schema_name` and `object_name` is a hyphen, not a dot.
- The extension must reflect the file type: `.sql` for SQL scripts, `.sh` for shell scripts.

Examples:

```text
T0001-create-table-AI_APP_OWNER-NOTIF_CHANNELS.sql
T0002-create-index-AI_APP_OWNER-NOTIF_CHANNELS_UK1.sql
T0003-seed-data-AI_APP_OWNER-NOTIF_STATUS_CODES.sql
T0004-run-check-AI_APP_OWNER-NOTIF_CHANNELS.sh
```

Each task artifact must contain both:

- documentation explaining the purpose of the artifact;
- the actual object definition, installation logic, validation logic, or controlled operation.

## Core Principle

GitHub is the source of truth.

The local Oracle database is disposable runtime state.

No database change is valid unless it exists as a Git-managed SQL file and can be executed through an official project script.

If the database state conflicts with the Git state, the Git state wins.

## Scope

In scope:

- data model for notification dispatch;
- Oracle tables;
- constraints;
- indexes;
- views;
- PL/SQL packages when justified;
- seed data when required;
- SQL tests and smoke tests;
- controlled installation workflow;
- controlled review workflow;
- controlled packaging workflow;
- local Oracle runtime in Docker;
- GitHub as the source of truth;
- AGW for Git/GitHub workflow discipline.

Out of scope at this stage:

- real email sending;
- real WhatsApp sending;
- real Telegram sending;
- external API implementation;
- ORDS;
- APEX;
- UI or frontend work;
- external workers;
- real provider integrations;
- provider credentials;
- API keys;
- organizational database connections;
- organizational system integrations.

## Safety Rules

This project must remain isolated.

Do not connect to:

- production databases;
- organizational development databases;
- organizational test databases;
- staging databases;
- shared organizational databases;
- real messaging providers.

Do not commit:

- passwords;
- tokens;
- API keys;
- certificates;
- private keys;
- real connection strings;
- `.env` files;
- provider credentials.

Do not execute ad-hoc DDL or DML directly against the database.

All schema and data changes must be represented as versioned files in Git and executed only through official project scripts.

## Required Test Per Stage

Every development stage must include a test that demonstrates that the stage works.

For database work, this may include:

- SQL smoke tests;
- object inventory checks;
- invalid object checks;
- metadata checks;
- controlled functional checks;
- review scripts;
- installation checks.

If a task cannot prove its success criteria, the task must be reported as incomplete or partially verified.

## Basic Project Structure

```text
db/
  install/
  rollback/
  src/
    tables/
    constraints/
    indexes/
    views/
    packages/
    triggers/
    seed/
  tests/
    sql/
    utplsql/
  review/
  generated/
  dist/

scripts/
tests/
tools/
  ai-git-workflow-tools/
```

## Important Directories

### `db/`

Contains Oracle database source files, installation files, rollback files, tests, review output, generated files, and release packages.

### `db/install/`

Contains controlled installation entry points and setup scripts.

### `db/src/`

Contains source definitions for Oracle database objects.

### `db/tests/`

Contains database tests.

### `db/review/`

Contains review reports or review templates.

### `db/dist/`

Contains generated release-package output.

Package output is generated state. It should not be treated as the source of truth.

### `scripts/`

Contains official operational entry points.

Typical scripts include:

```text
scripts/lab-up.sh
scripts/lab-down.sh
scripts/lab-reset.sh
scripts/install-db.sh
scripts/run-db-tests.sh
scripts/review-db-code.sh
scripts/package-release.sh
scripts/test.sh
scripts/lint.sh
```

### `tests/`

Contains Python repository contract tests.

This project uses `unittest`, not `pytest`.

### `tools/ai-git-workflow-tools/`

Contains AGW as a Git submodule.

AGW should be used where possible for controlled Git/GitHub workflows.

## Initial Setup

Clone the repository with submodules:

```bash
git clone --recurse-submodules https://github.com/sagivba/oracle-notification-dispatch-lab.git
cd oracle-notification-dispatch-lab
```

If the repository was cloned without submodules:

```bash
git submodule update --init --recursive
```

Load AGW:

```bash
source tools/ai-git-workflow-tools/scripts/load-agw.sh
agw_status
```

Run repository checks:

```bash
scripts/test.sh quick
```

## Local Oracle Runtime

Local Oracle runtime is used only when a task requires actual database validation.

Runtime work may include:

- starting the Oracle Docker lab;
- installing database objects;
- running SQL tests;
- checking object inventory;
- checking invalid objects;
- running review scripts;
- generating release package output.

Local runtime must be executed only through official project scripts unless explicitly approved.

## Static Work vs Runtime Work

Static repository work includes:

- editing documentation;
- editing specifications;
- reviewing files;
- running repository tests;
- inspecting Git state;
- preparing task definitions.

Runtime work includes:

- Docker inspection;
- Oracle startup;
- database installation;
- SQL tests;
- SQLcl checks;
- SQLPlus checks;
- object validation inside Oracle.

The task definition must state which mode is required.

## Current Project State

This repository is a clean baseline derived from an existing Oracle lab infrastructure.

Historical build documentation, old goals, old stage reports, old experiments, old release-management specifications, and old project instructions were intentionally excluded.

The repository currently contains infrastructure needed to start stabilizing a new Oracle notification dispatch lab.

Before Codex-driven functional database development starts, the project must still define:

- stable project instructions;
- task workflow rules;
- database development rules;
- runtime validation rules;
- the first notification-dispatch specification;
- the first set of controlled Codex-ready tasks.

## Intended Use of Codex

Codex will be used only after the repository instructions and task structure are stable.

Codex tasks must be small, explicit, and measurable.

A Codex task must not invent requirements.

A Codex task must not perform unapproved database operations.

A Codex task must report honestly when it cannot validate a success criterion.

## License

No license has been selected yet.
