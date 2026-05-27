-- Purpose: SQL smoke test for invalid objects in the lab owner schema.
-- This file is a diagnostics-only check and does not modify database state.

set echo off
set feedback on
set heading on
set verify off
whenever sqlerror exit sql.sqlcode

prompt Checking for invalid objects in NOTIF_APP_OWNER.

declare
  l_invalid_count number;
begin
  select count(*)
    into l_invalid_count
    from all_objects
   where owner = 'NOTIF_APP_OWNER'
     and status <> 'VALID';

  if l_invalid_count != 0 then
    raise_application_error(-20003, 'NOTIF_APP_OWNER has invalid objects.');
  end if;
end;
/

exit success
