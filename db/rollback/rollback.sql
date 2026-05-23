-- Purpose: Conservative rollback reference for the Oracle AI Lab install workflow.
-- Rollback is intentionally conservative until destructive teardown behavior is
-- explicitly designed, reviewed, and validated against the disposable local lab.

set echo off
set feedback on
set heading on
set verify off
whenever sqlerror exit sql.sqlcode

prompt Oracle AI Lab rollback skeleton.

-- This rollback reference does not provide executable DROP USER, DROP TABLE, or cleanup DDL.
-- Future rollback must remain represented in managed SQL files and must run only
-- through official repository scripts.

-- TODO(infrastructure): Define controlled teardown behavior for infrastructure
-- smoke objects after the install workflow is runtime validated.

-- TODO(functional goals): Add release-management rollback only together with the
-- matching versioned functional SQL implementation.

prompt No rollback action executed by this conservative reference.
