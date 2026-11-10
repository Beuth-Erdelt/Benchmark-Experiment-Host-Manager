-- Benchmark-Experiment-Host-Manager | experiments/benchbase/resourcestresser/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load durability 'relaxed' (-xld relaxed, the default), first pre-load
--          script. Commits return before the WAL is flushed; a crash loses the
--          last commits but never corrupts data. restoredurability-relaxed.sql
--          resets it after the load (ALTER SYSTEM survives restarts). Also set
--          for this database, which wins over the postgres command line (-c,
--          also from --set): -xld relaxed --set synchronous_commit=on loads
--          relaxed and benchmarks with synchronous commits.
--          No curly braces in this file: bexhoma may fill it with str.format().

ALTER SYSTEM SET synchronous_commit = off;
SELECT pg_reload_conf();
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
