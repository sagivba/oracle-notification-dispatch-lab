-- Purpose: Controlled local Oracle Notification Dispatch Lab user and schema setup.
-- This managed SQL file creates or updates only the local lab users required by
-- the install workflow. It stores no secrets and receives passwords from
-- db/install/install.sql substitution variables.

set echo off
set feedback on
set heading on
set verify off
whenever sqlerror exit sql.sqlcode

prompt Creating or updating Oracle Notification Dispatch Lab local users.

-- The install path must work on a clean disposable lab PDB. This helper keeps
-- CREATE USER idempotent enough for repeated local installs by creating missing
-- users and resetting expected attributes for users that already exist.
create or replace procedure NOTIF_LAB_ENSURE_USER (
  p_username in varchar2,
  p_password in varchar2,
  p_owner_schema in varchar2
) authid current_user
as
  l_username varchar2(128);
  l_password varchar2(4000);
  l_create_sql varchar2(32767);
begin
  l_username := upper(p_username);

  if l_username not in (
    'NOTIF_APP_OWNER',
    'NOTIF_APP_RUNTIME',
    'NOTIF_APP_READONLY',
    'NOTIF_REVIEWER'
  ) then
    raise_application_error(-20010, 'Unexpected Oracle Notification Dispatch Lab user: ' || p_username);
  end if;

  if p_password is null then
    raise_application_error(-20011, 'Password value is required for ' || l_username);
  end if;

  -- Passwords are local runtime values. They are quoted for SQL execution here
  -- but are never written to Git.
  l_password := '"' || replace(p_password, '"', '""') || '"';

  l_create_sql :=
    'create user ' || l_username ||
    ' identified by ' || l_password ||
    ' default tablespace USERS temporary tablespace TEMP account unlock';

  if p_owner_schema = 'Y' then
    l_create_sql := l_create_sql || ' quota unlimited on USERS';
  end if;

  begin
    execute immediate l_create_sql;
  exception
    when others then
      if sqlcode = -1920 then
        execute immediate
          'alter user ' || l_username ||
          ' identified by ' || l_password ||
          ' default tablespace USERS temporary tablespace TEMP account unlock';
      else
        raise;
      end if;
  end;

  if p_owner_schema = 'Y' then
    execute immediate 'alter user ' || l_username || ' quota unlimited on USERS';
  else
    execute immediate 'alter user ' || l_username || ' quota 0 on USERS';
  end if;
end;
/

begin
  NOTIF_LAB_ENSURE_USER('NOTIF_APP_OWNER', q'[&&NOTIF_APP_OWNER_PWD]', 'Y');
  NOTIF_LAB_ENSURE_USER('NOTIF_APP_RUNTIME', q'[&&NOTIF_APP_RUNTIME_PWD]', 'N');
  NOTIF_LAB_ENSURE_USER('NOTIF_APP_READONLY', q'[&&NOTIF_APP_READONLY_PWD]', 'N');
  NOTIF_LAB_ENSURE_USER('NOTIF_REVIEWER', q'[&&NOTIF_REVIEWER_PWD]', 'N');
end;
/

grant create session to NOTIF_APP_OWNER;
grant create table to NOTIF_APP_OWNER;

grant create session to NOTIF_APP_RUNTIME;
grant create session to NOTIF_APP_READONLY;
grant create session to NOTIF_REVIEWER;

drop procedure NOTIF_LAB_ENSURE_USER;

prompt Oracle Notification Dispatch Lab local users are ready for infrastructure install.
