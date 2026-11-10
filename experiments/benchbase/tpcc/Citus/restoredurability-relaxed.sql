-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/Citus
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Undo load durability 'relaxed' after the load (post-load phase, right
--          before the check script), on the coordinator and all workers. Resets
--          the server and the database setting of synchronous_commit.
--          No curly braces in this file: bexhoma may fill it with str.format().

ALTER SYSTEM RESET synchronous_commit;
SELECT pg_reload_conf();
SELECT * FROM run_command_on_workers($cmd$ALTER SYSTEM RESET synchronous_commit$cmd$);
SELECT * FROM run_command_on_workers($cmd$SELECT pg_reload_conf()$cmd$);
DO $$
BEGIN
    EXECUTE format('ALTER DATABASE %I RESET synchronous_commit', current_database());
END
$$;
SELECT * FROM run_command_on_workers(format('ALTER DATABASE %I RESET synchronous_commit', current_database()));
SELECT pg_sleep(1);
-- SHOW synchronous_commit would show the load value: this session started with the
-- database setting; new sessions get the configured value (no database setting left)
SELECT d.datname, s.setconfig FROM pg_db_role_setting s JOIN pg_database d ON d.oid = s.setdatabase
    WHERE d.datname = current_database() AND s.setrole = 0;

-- #848: an ERROR if the database setting is still there (reads catalogs only)
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_db_role_setting s JOIN pg_database d ON d.oid = s.setdatabase
               WHERE d.datname = current_database() AND s.setrole = 0
                   AND EXISTS (SELECT 1 FROM unnest(s.setconfig) c WHERE c LIKE 'synchronous_commit=%')) THEN
        RAISE EXCEPTION 'load durability: synchronous_commit is still set for database %', current_database();
    END IF;
END
$$;
-- the same on every worker (whether Citus propagated the coordinator's ALTER DATABASE or not)
DO $$
DECLARE
    r record;
BEGIN
    FOR r IN SELECT * FROM run_command_on_workers(format('SELECT EXISTS (SELECT 1 FROM pg_db_role_setting s JOIN pg_database d ON d.oid = s.setdatabase, unnest(s.setconfig) c WHERE d.datname = %L AND s.setrole = 0 AND c LIKE %L)', current_database(), 'synchronous_commit=%')) LOOP
        IF NOT r.success OR r.result <> 'f' THEN
            RAISE EXCEPTION 'load durability: synchronous_commit is still set for database % on worker %:% (%)',
                current_database(), r.nodename, r.nodeport, r.result;
        END IF;
    END LOOP;
END
$$;
