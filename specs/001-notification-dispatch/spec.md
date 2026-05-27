# Notification Dispatch Minimal Functional Specification

Purpose: define the minimal functional baseline for Oracle Notification Dispatch Lab before any functional DDL is generated.

This specification is intentionally minimal. It must be expanded with table-level implementation detail before functional DDL generation starts.

## Project boundary

Oracle Notification Dispatch Lab is an independent Oracle database-layer project for a fictional multi-channel notification and message dispatch system.

The current scope is limited to Oracle database objects and repository workflows:
- tables;
- constraints;
- indexes;
- views;
- PL/SQL packages only if justified later;
- seed data;
- SQL tests;
- review workflow;
- packaging workflow.

The following are explicitly excluded:
- real email sending;
- real WhatsApp integration;
- real Telegram integration;
- real SMS integration;
- external provider integration;
- API;
- ORDS;
- APEX;
- UI;
- external workers;
- organizational database access;
- secrets.

## Source documents

The data model must be derived from the existing repository source documents:
- `docs/data-model/notification-dispatch-erd.md`;
- `docs/data-model/notification-dispatch-erd.mmd`;
- `docs/oracle-notification-dispatch-data-model-he.html`.

Do not invent an alternative data model. Any difference between this specification and the source data model documents must be resolved before DDL is created.

## Approved database ownership

The owner schema for functional database objects is:

```text
NOTIF_APP_OWNER
```

The local owner password placeholder is:

```text
NOTIF_APP_OWNER_PWD
```

Runtime, read-only, and reviewer schema names are not finalized in this specification.

The current open names are:
- `AI_APP_RUNTIME`;
- `AI_APP_READONLY`;
- `AI_REVIEWER`.

## Functional baseline

The system records fictional notification dispatch data for local Oracle lab development only.

The baseline model includes:
- notification channels;
- dispatch and delivery status codes;
- external source systems that provide recipient identity references;
- message templates with explicit versioning beyond dispatch item content snapshots;
- recipients and recipient channel addresses;
- dispatch requests and dispatch items;
- dispatch item content snapshots;
- delivery attempts;
- fictional provider response logs with `CLOB` payload storage;
- audit records.

GitHub is the source of truth. Database state is valid only when it can be reproduced from versioned repository files and official repository scripts.

## DDL readiness rules

Before a table or related database object is implemented, the DDL task must define:
- target tables;
- columns, data types, nullability, and defaults;
- primary keys;
- foreign keys;
- unique constraints;
- check constraints;
- required indexes;
- table and column comments;
- seed data, where needed;
- SQL tests;
- partitioning, where needed;
- rollback behavior;
- success criteria.

Database changes must be represented as versioned SQL files under the appropriate `db/` path and must run only through official repository scripts.

## Candidate first DDL iteration

The candidate first functional DDL iteration is limited to:
- `NOTIF_CHANNELS`;
- `NOTIF_STATUS_CODES`;
- `NOTIF_EXTERNAL_SYSTEMS`;
- `NOTIF_AUDIT_LOG`.

`NOTIF_AUDIT_LOG` is included in the first functional database iteration.

`NOTIF_DISPATCH_REQUESTS` is not necessarily implemented in the first DDL task. When `NOTIF_DISPATCH_REQUESTS` is implemented, it must use partitioning from its first implementation.

Provider response payloads must be modeled as `CLOB` and must contain fictional local lab data only.

## Minimum validation expectation

Each functional DDL task must include a validation method appropriate to its scope, such as:
- install checks;
- SQL smoke tests;
- object inventory checks;
- invalid object checks;
- metadata checks;
- review checks;
- package generation checks.

No database-related stage is complete without an appropriate validation artifact or validation command.
