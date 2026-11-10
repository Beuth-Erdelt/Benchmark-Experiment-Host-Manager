-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/Citus
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load durability 'relaxed' (-xld relaxed, the default), first pre-load
--          script. As PostgreSQL, on the coordinator and on all workers (where
--          the shards are): commits return before the WAL is flushed, also set
--          for this database, which wins over the postgres command line (-c,
--          also from --set). restoredurability-relaxed.sql resets it after the load.
--          No 'unsafe' level for Citus: its restore would need a sync on every worker.
--          No curly braces in this file: bexhoma may fill it with str.format().

ALTER SYSTEM SET synchronous_commit = off;
SELECT pg_reload_conf();
SELECT * FROM run_command_on_workers($cmd$ALTER SYSTEM SET synchronous_commit = off$cmd$);
SELECT * FROM run_command_on_workers($cmd$SELECT pg_reload_conf()$cmd$);
-- synchronous_commit also for this database: a database setting wins over the postgres
-- command line (-c, also from --set), ALTER SYSTEM does not; new sessions only
DO $$
BEGIN
    EXECUTE format('ALTER DATABASE %I SET synchronous_commit = off', current_database());
END
$$;
SELECT pg_sleep(1);
SELECT d.datname, s.setconfig FROM pg_db_role_setting s JOIN pg_database d ON d.oid = s.setdatabase
    WHERE d.datname = current_database() AND s.setrole = 0;

-- #848: an ERROR if a value did not take effect (reads settings and catalogs only):
-- synchronous_commit from the database setting, which only new sessions see
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_db_role_setting s JOIN pg_database d ON d.oid = s.setdatabase
                   WHERE d.datname = current_database() AND s.setrole = 0
                       AND 'synchronous_commit=off' = ANY (s.setconfig)) THEN
        RAISE EXCEPTION 'load durability: synchronous_commit=off is not set for database %', current_database();
    END IF;
END
$$;
-- the same on every worker: Citus propagates the coordinator's ALTER DATABASE (on a worker it is not allowed)
DO $$
DECLARE
    r record;
BEGIN
    FOR r IN SELECT * FROM run_command_on_workers(format('SELECT EXISTS (SELECT 1 FROM pg_db_role_setting s JOIN pg_database d ON d.oid = s.setdatabase WHERE d.datname = %L AND s.setrole = 0 AND %L = ANY (s.setconfig))', current_database(), 'synchronous_commit=off')) LOOP
        IF NOT r.success OR r.result <> 't' THEN
            RAISE EXCEPTION 'load durability: synchronous_commit=off is not set for database % on worker %:% (%)',
                current_database(), r.nodename, r.nodeport, r.result;
        END IF;
    END LOOP;
END
$$;
