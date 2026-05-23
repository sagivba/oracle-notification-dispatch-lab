-- Purpose: SQL smoke test for local lab database connectivity.
-- This file is read-only and exists to fail clearly if the managed SQL test
-- runner cannot connect to the local Oracle lab PDB.

set echo off
set feedback on
set heading on
set verify off
whenever sqlerror exit sql.sqlcode

prompt Checking local lab DB connectivity.

select
  sys_context('USERENV', 'CON_NAME') as CON_NAME,
  sys_context('USERENV', 'CURRENT_SCHEMA') as CURRENT_SCHEMA
from dual;

exit success
