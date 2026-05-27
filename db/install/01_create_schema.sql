-- Purpose: Managed schema-level setup placeholder for Oracle Notification Dispatch Lab.
-- This file reserves the managed install location for schema setup while keeping
-- business functionality out of the Infrastructure MVP.

set echo off
set feedback on
set heading on
set verify off

prompt Preparing Oracle Notification Dispatch Lab schema setup skeleton.

-- The Infrastructure MVP creates no business tables, packages, views, triggers,
-- seed data, or release-management implementation. This preserves DEC-013 and
-- DEC-014: the first MVP is infrastructure-only and functional work starts later.

-- LAB_SMOKE_TEST is intentionally installed from db/src/tables/lab_smoke_test.sql
-- through db/install/install.sql. Keeping the object in db/src preserves the rule
-- that DB changes live as versioned source files and install runs through the
-- official entry point.

-- TODO(infrastructure): Add additional infrastructure setup only after the smoke
-- workflow is reviewed and runtime validation is in scope.

-- TODO(functional goals): Add release-management schema objects only after the
-- Infrastructure MVP is complete and functional iteration readiness is approved.

prompt Schema setup remains a safe managed placeholder.
