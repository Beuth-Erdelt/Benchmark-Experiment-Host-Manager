-- Benchmark-Experiment-Host-Manager | experiments/tpch/Citus
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load durability 'durable' (-xld durable), first pre-load script.
--          The load runs crash-safe on the coordinator and all workers, whatever
--          they were started with. restoredurability-durable.sql returns to the
--          configured state after the load. synchronous_commit is also set for
--          this database (coordinator and workers), which wins over the postgres
--          command line (-c, also from --set).
--          No curly braces in this file: bexhoma may fill it with str.format().
-- server-wide: fsync=on full_page_writes=on
--          (server-wide only: bexhoma refuses to load when --set fixes them differently)

ALTER SYSTEM SET synchronous_commit = on;
ALTER SYSTEM SET fsync = on;
ALTER SYSTEM SET full_page_writes = on;
SELECT pg_reload_conf();
SELECT * FROM run_command_on_workers($cmd$ALTER SYSTEM SET synchronous_commit = on$cmd$);
SELECT * FROM run_command_on_workers($cmd$ALTER SYSTEM SET fsync = on$cmd$);
SELECT * FROM run_command_on_workers($cmd$ALTER SYSTEM SET full_page_writes = on$cmd$);
SELECT * FROM run_command_on_workers($cmd$SELECT pg_reload_conf()$cmd$);
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
-- the same on every worker: Citus propagates the coordinator's ALTER DATABASE (on a worker it is not allowed)
DO $$
DECLARE
    r record;
BEGIN
    FOR r IN SELECT * FROM run_command_on_workers(format('SELECT EXISTS (SELECT 1 FROM pg_db_role_setting s JOIN pg_database d ON d.oid = s.setdatabase WHERE d.datname = %L AND s.setrole = 0 AND %L = ANY (s.setconfig))', current_database(), 'synchronous_commit=on')) LOOP
        IF NOT r.success OR r.result <> 't' THEN
            RAISE EXCEPTION 'load durability: synchronous_commit=on is not set for database % on worker %:% (%)',
                current_database(), r.nodename, r.nodeport, r.result;
        END IF;
    END LOOP;
END
$$;
