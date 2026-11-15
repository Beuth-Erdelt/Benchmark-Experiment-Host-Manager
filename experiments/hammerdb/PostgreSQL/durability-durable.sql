-- Benchmark-Experiment-Host-Manager | experiments/hammerdb/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load durability 'durable' (-xld durable), first pre-load script.
--          The load runs crash-safe, whatever the server was started with:
--          commits wait for the WAL flush, data is fsynced, full page images
--          are logged. restoredurability-durable.sql returns to the configured
--          state after the load. synchronous_commit is also set for this
--          database, which wins over the postgres command line (-c, also from
--          --set); fsync and full_page_writes are server-wide only: given on the
--          command line they keep their value and the check at the end fails.
--          No curly braces in this file: bexhoma may fill it with str.format().
-- server-wide: fsync=on full_page_writes=on
--          (server-wide only: bexhoma refuses to load when --set fixes them differently)

ALTER SYSTEM SET synchronous_commit = on;
ALTER SYSTEM SET fsync = on;
ALTER SYSTEM SET full_page_writes = on;
SELECT pg_reload_conf();
-- synchronous_commit also for this database: a database setting wins over the postgres
-- command line (-c, also from --set), ALTER SYSTEM does not; new sessions only
DO $$
BEGIN
    EXECUTE format('ALTER DATABASE %I SET synchronous_commit = on', current_database());
END
$$;
SELECT pg_sleep(1);
SHOW fsync;
SHOW full_page_writes;
SELECT d.datname, s.setconfig FROM pg_db_role_setting s JOIN pg_database d ON d.oid = s.setdatabase
    WHERE d.datname = current_database() AND s.setrole = 0;

-- #848: an ERROR if a value did not take effect (reads settings and catalogs only):
-- synchronous_commit from the database setting, which only new sessions see
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_db_role_setting s JOIN pg_database d ON d.oid = s.setdatabase
                   WHERE d.datname = current_database() AND s.setrole = 0
                       AND 'synchronous_commit=on' = ANY (s.setconfig)) THEN
        RAISE EXCEPTION 'load durability: synchronous_commit=on is not set for database %', current_database();
    END IF;
    IF current_setting('fsync') <> 'on' THEN
        RAISE EXCEPTION 'load durability: fsync is %, not on', current_setting('fsync');
    END IF;
    IF current_setting('full_page_writes') <> 'on' THEN
        RAISE EXCEPTION 'load durability: full_page_writes is %, not on', current_setting('full_page_writes');
    END IF;
END
$$;
