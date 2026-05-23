-- Purpose: SQL smoke test for LAB_SMOKE_TEST inventory and columns.
-- This file performs metadata-only checks against the local lab catalog.

set echo off
set feedback on
set heading on
set verify off
whenever sqlerror exit sql.sqlcode

prompt Checking LAB_SMOKE_TEST object inventory.

declare
  l_table_count number;
  l_column_count number;
begin
  select count(*)
    into l_table_count
    from all_objects
   where owner = 'AI_APP_OWNER'
     and object_name = 'LAB_SMOKE_TEST'
     and object_type = 'TABLE';

  if l_table_count != 1 then
    raise_application_error(-20001, 'Expected table AI_APP_OWNER.LAB_SMOKE_TEST was not found.');
  end if;

  select count(*)
    into l_column_count
    from all_tab_columns
   where owner = 'AI_APP_OWNER'
     and table_name = 'LAB_SMOKE_TEST'
     and (
       (column_name = 'ID' and data_type = 'NUMBER')
       or (column_name = 'CREATED_AT' and data_type like 'TIMESTAMP%')
       or (column_name = 'MESSAGE' and data_type = 'VARCHAR2')
     );

  if l_column_count != 3 then
    raise_application_error(-20002, 'LAB_SMOKE_TEST does not expose the expected smoke-test columns.');
  end if;
end;
/

exit success
