# T001 - Reference and audit DDL

## Purpose

Define the first functional DDL iteration for the Oracle Notification Dispatch Lab.

This task introduces the foundational reference tables and the audit table required before dispatch request tables are implemented.

This task is specification-only at this stage. It must not add or execute DDL.

## Scope

Target tables:

1. `NOTIF_CHANNELS`
2. `NOTIF_STATUS_CODES`
3. `NOTIF_EXTERNAL_SYSTEMS`
4. `NOTIF_AUDIT_LOG`

The implementation of this task, in a later DDL task, must create only Oracle database-layer objects.

## Explicit exclusions

This task must not introduce:

- Real email sending.
- Real SMS sending.
- Real WhatsApp integration.
- Real Telegram integration.
- Any external provider integration.
- API objects.
- ORDS objects.
- APEX objects.
- UI objects.
- External workers.
- Organizational database access.
- Secrets.
- Password values.
- Real provider credentials.
- Real provider endpoints.
- Functional DDL for `NOTIF_DISPATCH_REQUESTS`.
- Functional DDL for dispatch items.
- Functional PL/SQL packages.

Provider-related values in this task are fictional local lab data only.

## Required table: NOTIF_CHANNELS

### Purpose

Stores supported fictional notification channels.

This table defines channel codes only. It does not imply real provider integration or message sending.

### Required columns

| Column name | Required definition |
| --- | --- |
| `CHANNEL_CODE` | `VARCHAR2(30)`; not null; stable business code |
| `CHANNEL_NAME` | `VARCHAR2(100)`; not null |
| `CHANNEL_DESCRIPTION` | `VARCHAR2(4000)`; nullable |
| `IS_ACTIVE` | `CHAR(1)`; not null; default `Y` |
| `DISPLAY_ORDER` | `NUMBER(6,0)`; not null |
| `CREATED_AT` | `TIMESTAMP(6) WITH TIME ZONE`; not null; default `SYSTIMESTAMP` |
| `CREATED_BY` | `VARCHAR2(128)`; not null |
| `UPDATED_AT` | `TIMESTAMP(6) WITH TIME ZONE`; nullable |
| `UPDATED_BY` | `VARCHAR2(128)`; nullable |

### Required constraints

| Constraint | Requirement |
| --- | --- |
| Primary key | `CHANNEL_CODE` |
| Unique constraint | `CHANNEL_NAME` |
| Check constraint | `IS_ACTIVE in ('Y', 'N')` |
| Check constraint | `CHANNEL_CODE = UPPER(CHANNEL_CODE)` |
| Check constraint | `DISPLAY_ORDER > 0` |

### Required indexes

The primary key and unique constraint indexes are sufficient for this table.

No additional non-unique index is required in this iteration.

### Required comments

Add table and column comments for all columns.

The table comment must explicitly state that channels are fictional lab reference data and do not configure real provider integration.

### Minimal seed data

Required seed rows:

| CHANNEL_CODE | CHANNEL_NAME | IS_ACTIVE |
| --- | --- | --- |
| `EMAIL` | `Email` | `Y` |
| `SMS` | `SMS` | `Y` |
| `WHATSAPP` | `WhatsApp` | `Y` |
| `TELEGRAM` | `Telegram` | `Y` |
| `IN_APP` | `In-app notification` | `Y` |

Seed data must not include real provider configuration.

## Required table: NOTIF_STATUS_CODES

### Purpose

Stores stable lifecycle status codes for future notification dispatch entities.

This table is a reference table only. It must not implement workflow transitions.

### Required columns

| Column name | Required definition |
| --- | --- |
| `STATUS_CODE` | `VARCHAR2(40)`; not null; stable business code |
| `STATUS_NAME` | `VARCHAR2(100)`; not null |
| `STATUS_DESCRIPTION` | `VARCHAR2(4000)`; nullable |
| `STATUS_DOMAIN` | `VARCHAR2(40)`; not null |
| `IS_TERMINAL` | `CHAR(1)`; not null; default `N` |
| `IS_SUCCESS` | `CHAR(1)`; not null; default `N` |
| `DISPLAY_ORDER` | `NUMBER(6,0)`; not null |
| `CREATED_AT` | `TIMESTAMP(6) WITH TIME ZONE`; not null; default `SYSTIMESTAMP` |
| `CREATED_BY` | `VARCHAR2(128)`; not null |
| `UPDATED_AT` | `TIMESTAMP(6) WITH TIME ZONE`; nullable |
| `UPDATED_BY` | `VARCHAR2(128)`; nullable |

### Required constraints

| Constraint | Requirement |
| --- | --- |
| Primary key | `STATUS_CODE` |
| Unique constraint | `STATUS_DOMAIN`, `STATUS_NAME` |
| Check constraint | `STATUS_CODE = UPPER(STATUS_CODE)` |
| Check constraint | `STATUS_DOMAIN = UPPER(STATUS_DOMAIN)` |
| Check constraint | `STATUS_DOMAIN in ('DISPATCH_REQUEST', 'DISPATCH_ITEM', 'PROVIDER_ATTEMPT', 'SYSTEM')` |
| Check constraint | `IS_TERMINAL in ('Y', 'N')` |
| Check constraint | `IS_SUCCESS in ('Y', 'N')` |
| Check constraint | `DISPLAY_ORDER > 0` |
| Check constraint | `IS_SUCCESS = 'N' or IS_TERMINAL = 'Y'` |

### Required indexes

| Index | Columns | Requirement |
| --- | --- | --- |
| `NOTIF_STATUS_CODES_I1` | `STATUS_DOMAIN`, `DISPLAY_ORDER` | Required for status lookup by domain |

Primary key and unique constraint indexes are also required.

### Required comments

Add table and column comments for all columns.

The table comment must state that this table defines status codes only and does not implement workflow transition rules.

### Minimal seed data

Required seed rows:

| STATUS_CODE | STATUS_NAME | STATUS_DOMAIN | IS_TERMINAL | IS_SUCCESS |
| --- | --- | --- | --- | --- |
| `REQUEST_DRAFT` | `Draft` | `DISPATCH_REQUEST` | `N` | `N` |
| `REQUEST_ACCEPTED` | `Accepted` | `DISPATCH_REQUEST` | `N` | `N` |
| `REQUEST_REJECTED` | `Rejected` | `DISPATCH_REQUEST` | `Y` | `N` |
| `REQUEST_CANCELLED` | `Cancelled` | `DISPATCH_REQUEST` | `Y` | `N` |
| `ITEM_PENDING` | `Pending` | `DISPATCH_ITEM` | `N` | `N` |
| `ITEM_READY` | `Ready` | `DISPATCH_ITEM` | `N` | `N` |
| `ITEM_COMPLETED` | `Completed` | `DISPATCH_ITEM` | `Y` | `Y` |
| `ITEM_FAILED` | `Failed` | `DISPATCH_ITEM` | `Y` | `N` |
| `PROVIDER_NOT_ATTEMPTED` | `Not attempted` | `PROVIDER_ATTEMPT` | `N` | `N` |
| `PROVIDER_ACCEPTED` | `Accepted by fictional provider` | `PROVIDER_ATTEMPT` | `Y` | `Y` |
| `PROVIDER_REJECTED` | `Rejected by fictional provider` | `PROVIDER_ATTEMPT` | `Y` | `N` |
| `SYSTEM_RECORDED` | `Recorded` | `SYSTEM` | `Y` | `Y` |

Seed data must remain fictional and must not imply real external delivery.

## Required table: NOTIF_EXTERNAL_SYSTEMS

### Purpose

Stores fictional source systems that may submit or own notification dispatch requests in later iterations.

This table must not contain real organizational system identifiers unless they are fictionalized for the lab.

### Required columns

| Column name | Required definition |
| --- | --- |
| `EXTERNAL_SYSTEM_CODE` | `VARCHAR2(40)`; not null; stable business code |
| `EXTERNAL_SYSTEM_NAME` | `VARCHAR2(150)`; not null |
| `SYSTEM_DESCRIPTION` | `VARCHAR2(4000)`; nullable |
| `OWNER_LABEL` | `VARCHAR2(150)`; nullable; fictional owner label only |
| `IS_ACTIVE` | `CHAR(1)`; not null; default `Y` |
| `CREATED_AT` | `TIMESTAMP(6) WITH TIME ZONE`; not null; default `SYSTIMESTAMP` |
| `CREATED_BY` | `VARCHAR2(128)`; not null |
| `UPDATED_AT` | `TIMESTAMP(6) WITH TIME ZONE`; nullable |
| `UPDATED_BY` | `VARCHAR2(128)`; nullable |

### Required constraints

| Constraint | Requirement |
| --- | --- |
| Primary key | `EXTERNAL_SYSTEM_CODE` |
| Unique constraint | `EXTERNAL_SYSTEM_NAME` |
| Check constraint | `EXTERNAL_SYSTEM_CODE = UPPER(EXTERNAL_SYSTEM_CODE)` |
| Check constraint | `IS_ACTIVE in ('Y', 'N')` |

### Required indexes

The primary key and unique constraint indexes are sufficient for this table.

No additional non-unique index is required in this iteration.

### Required comments

Add table and column comments for all columns.

The table comment must explicitly state that rows are fictional source-system labels for the local lab.

### Minimal seed data

Required seed rows:

| EXTERNAL_SYSTEM_CODE | EXTERNAL_SYSTEM_NAME | IS_ACTIVE |
| --- | --- | --- |
| `STUDENT_PORTAL_LAB` | `Student portal lab` | `Y` |
| `CRM_LAB` | `CRM lab` | `Y` |
| `BATCH_JOB_LAB` | `Batch job lab` | `Y` |
| `TEST_HARNESS` | `Test harness` | `Y` |

Seed data must not reference real organizational systems.

## Required table: NOTIF_AUDIT_LOG

### Purpose

Stores append-only audit events for reference data and future dispatch processing.

This table is included in the first functional DDL iteration by prior project decision.

The audit table must support correlation and troubleshooting, but it must not store secrets.

### Required columns

| Column name | Required definition |
| --- | --- |
| `AUDIT_ID` | `NUMBER`; generated identity if supported by the project baseline; not null |
| `EVENT_TS` | `TIMESTAMP(6) WITH TIME ZONE`; not null; default `SYSTIMESTAMP` |
| `EVENT_TYPE` | `VARCHAR2(60)`; not null |
| `ACTION_CODE` | `VARCHAR2(60)`; not null |
| `ACTOR_SCHEMA` | `VARCHAR2(128)`; nullable |
| `ACTOR_NAME` | `VARCHAR2(128)`; nullable |
| `SOURCE_SYSTEM_CODE` | `VARCHAR2(40)`; nullable |
| `CHANNEL_CODE` | `VARCHAR2(30)`; nullable |
| `STATUS_CODE` | `VARCHAR2(40)`; nullable |
| `TARGET_TABLE_NAME` | `VARCHAR2(128)`; nullable |
| `TARGET_PK_VALUE` | `VARCHAR2(400)`; nullable |
| `CORRELATION_ID` | `VARCHAR2(100)`; nullable |
| `EVENT_SUMMARY` | `VARCHAR2(1000)`; not null |
| `EVENT_PAYLOAD` | `CLOB`; nullable |
| `CREATED_AT` | `TIMESTAMP(6) WITH TIME ZONE`; not null; default `SYSTIMESTAMP` |
| `CREATED_BY` | `VARCHAR2(128)`; not null |

### Required constraints

| Constraint | Requirement |
| --- | --- |
| Primary key | `AUDIT_ID` |
| Foreign key | `SOURCE_SYSTEM_CODE` references `NOTIF_EXTERNAL_SYSTEMS(EXTERNAL_SYSTEM_CODE)` |
| Foreign key | `CHANNEL_CODE` references `NOTIF_CHANNELS(CHANNEL_CODE)` |
| Foreign key | `STATUS_CODE` references `NOTIF_STATUS_CODES(STATUS_CODE)` |
| Check constraint | `EVENT_TYPE = UPPER(EVENT_TYPE)` |
| Check constraint | `ACTION_CODE = UPPER(ACTION_CODE)` |
| Check constraint | `TARGET_TABLE_NAME is null or TARGET_TABLE_NAME = UPPER(TARGET_TABLE_NAME)` |
| Check constraint | `EVENT_PAYLOAD is json` if supported by the project Oracle baseline; otherwise omit this check and document why |

### Required indexes

| Index | Columns | Requirement |
| --- | --- | --- |
| `NOTIF_AUDIT_LOG_I1` | `EVENT_TS` | Required for chronological audit review |
| `NOTIF_AUDIT_LOG_I2` | `CORRELATION_ID` | Required for tracing a logical operation |
| `NOTIF_AUDIT_LOG_I3` | `TARGET_TABLE_NAME`, `TARGET_PK_VALUE` | Required for reviewing events by audited entity |
| `NOTIF_AUDIT_LOG_I4` | `SOURCE_SYSTEM_CODE`, `EVENT_TS` | Required for source-system audit review |
| `NOTIF_AUDIT_LOG_I5` | `CHANNEL_CODE`, `EVENT_TS` | Required for channel-level audit review |
| `NOTIF_AUDIT_LOG_I6` | `STATUS_CODE`, `EVENT_TS` | Required for status-level audit review |

### Required comments

Add table and column comments for all columns.

The table comment must state:

- The table is append-only audit storage.
- Payload data is fictional local lab data.
- Secrets must not be stored.
- Provider payloads, if any appear in future tasks, must be fictional only.

### Minimal seed data

`NOTIF_AUDIT_LOG` must not have static seed rows unless the existing project convention requires seed verification rows.

If seed verification rows are required by the test framework, they must be clearly fictional and must not include secrets, credentials, tokens, real email addresses, phone numbers, or provider endpoints.

## Required SQL tests

The later implementation task must add SQL tests using the existing project test conventions.

At minimum, tests must verify:

### Object existence

- `NOTIF_CHANNELS` exists.
- `NOTIF_STATUS_CODES` exists.
- `NOTIF_EXTERNAL_SYSTEMS` exists.
- `NOTIF_AUDIT_LOG` exists.

### Column existence

Tests must verify all required columns listed in this task.

### Constraint existence

Tests must verify:

- Primary keys exist for all four tables.
- Required unique constraints exist.
- Required check constraints exist.
- Required foreign keys on `NOTIF_AUDIT_LOG` exist.

### Index existence

Tests must verify all required non-unique indexes listed in this task.

### Comments

Tests must verify that table comments exist.

Tests should verify column comments where the existing test framework makes this practical.

### Seed data

Tests must verify the required seed rows for:

- `NOTIF_CHANNELS`
- `NOTIF_STATUS_CODES`
- `NOTIF_EXTERNAL_SYSTEMS`

Tests must verify that seed rows do not contain obvious secret-like values such as:

- `PASSWORD`
- `TOKEN`
- `SECRET`
- `API_KEY`
- `PRIVATE_KEY`

### Safety exclusions

Tests or contract checks must verify that this task does not introduce:

- ORDS files.
- APEX files.
- API implementation files.
- External worker implementation files.
- Real provider configuration.
- Real provider endpoints.
- Password values.
- Secret values.

## Rollback behavior

The later implementation task must include rollback behavior through the official project script structure.

Rollback must:

1. Drop dependent objects before parent objects.
2. Drop `NOTIF_AUDIT_LOG` before reference tables.
3. Drop `NOTIF_EXTERNAL_SYSTEMS`, `NOTIF_STATUS_CODES`, and `NOTIF_CHANNELS` after dependent objects are removed.
4. Be safe to run in a local lab environment.
5. Avoid touching objects outside the notification lab scope.
6. Avoid dropping users or schemas.
7. Avoid deleting unrelated lab objects.

Rollback must not require manual cleanup of secrets because this task must not create secrets.

## DDL execution rules

This task document must not execute DDL.

The later implementation task must ensure that:

- All DB changes are versioned SQL files.
- SQL files are run only through the official project scripts.
- No ad-hoc manual DDL execution is required.
- No DDL is embedded in Python tests.
- Python tests may inspect metadata but must not create schema objects directly.
- `python3` is used for Python execution.
- `unittest` is used, not `pytest`.

## Success criteria

This task is complete when the repository contains a reviewed task specification that precisely defines:

- Target tables.
- Required columns.
- Required primary keys.
- Required unique constraints.
- Required foreign keys.
- Required check constraints.
- Required indexes.
- Required comments.
- Minimal seed data.
- Required SQL tests.
- Rollback behavior.
- Explicit exclusions.
- DDL execution boundaries.

This task is not complete if it adds functional DDL files, executes DDL, or introduces any out-of-scope integration.

## Notes for the later implementation task

Before starting the later implementation task, Codex must run:

```bash
git fetch
```

The later implementation task must inspect the repository conventions before choosing exact file locations for DDL, rollback SQL, seed SQL, and tests.

The later implementation task must keep changes small and measurable.
