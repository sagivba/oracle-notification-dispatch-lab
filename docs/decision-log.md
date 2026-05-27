# Purpose: Decision log for Oracle Notification Dispatch Lab.

This file records approved project decisions that affect repository structure, database ownership, runtime naming, and the first functional database iterations.

## Approved decisions

### DEC-001: Project identity

The repository is named Oracle Notification Dispatch Lab.

It is an independent project and must not be treated as the DEVELOPMENT in Oracle using AI Lab project.

### DEC-002: Functional domain

The functional domain is a fictional multi-channel notification and message dispatch system.

### DEC-003: Scope boundary

The current scope is Oracle database layer only.

Allowed scope:
- Oracle database tables.
- Constraints.
- Indexes.
- Views.
- PL/SQL packages when justified.
- Seed data.
- SQL tests.
- Review workflow.
- Packaging workflow.

Excluded scope:
- Real email sending.
- Real WhatsApp integration.
- Real Telegram integration.
- Real SMS integration.
- External provider integrations.
- API.
- ORDS.
- APEX.
- UI.
- External workers.
- Organizational database access.
- Secrets.

### DEC-004: Source of truth

GitHub is the source of truth.

All database changes must exist as versioned SQL files and must run only through official repository scripts.

### DEC-005: Local runtime naming

Local Docker/runtime resources use the Oracle Notification Dispatch Lab name.

Current local runtime identifiers:
- Container: `oracle-notification-dispatch-lab-db`
- Volume: `oracle-notification-dispatch-lab-u01`
- Network: `oracle-notification-dispatch-lab-net`

### DEC-006: Owner schema

The application owner schema is `NOTIF_APP_OWNER`.

The local owner password placeholder is `NOTIF_APP_OWNER_PWD`.

### DEC-007: First functional iteration includes audit

`NOTIF_AUDIT_LOG` is included in the first functional database iteration.

### DEC-008: Dispatch requests partitioning

`NOTIF_DISPATCH_REQUESTS` must use partitioning from the first functional implementation.

### DEC-009: Provider payload storage

Provider response payloads are stored as fictional local lab data only.

The provider payload must be modeled as a `CLOB`.

No real provider payloads, secrets, tokens, or external response data may be stored in this repository.

### DEC-010: Template versioning

Message templates require an explicit versioning mechanism beyond the dispatch item content snapshot.

The exact table design is deferred to the first functional DDL specification.

### DEC-011: Codex usage

Codex must be used only for small, explicit, measurable tasks with success criteria.

Codex must run `git fetch` before starting work.

Codex must not invent the data model.

### DEC-012: Test framework

Python tests use `unittest`.

Do not introduce `pytest` for this project unless this decision is explicitly changed.

### DEC-013: Runtime, read-only, and reviewer schemas

The runtime, read-only, and reviewer schemas use notification-specific names.

Current schema names:
- `NOTIF_APP_RUNTIME`
- `NOTIF_APP_READONLY`
- `NOTIF_REVIEWER`

Current local password placeholders:
- `NOTIF_APP_RUNTIME_PWD`
- `NOTIF_APP_READONLY_PWD`
- `NOTIF_REVIEWER_PWD`
