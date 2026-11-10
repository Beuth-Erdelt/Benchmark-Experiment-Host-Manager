-- Benchmark-Experiment-Host-Manager | experiments/tpcc/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load durability 'unsafe' (-xld unsafe), runs after durability-relaxed.sql.
--          WAL and data files are written but never flushed, and no full page
--          images are logged: a crash of the server or node during the load can
--          corrupt the database. restoredurability-unsafe.sql/.sh switch both
--          back, checkpoint and flush the OS cache after the load.
--          No curly braces in this file: bexhoma may fill it with str.format().
-- server-wide: fsync=off full_page_writes=off
--          (server-wide only: bexhoma refuses to load when --set fixes them differently)

ALTER SYSTEM SET fsync = off;
ALTER SYSTEM SET full_page_writes = off;
SELECT pg_reload_conf();
SELECT pg_sleep(1);
SHOW fsync;
SHOW full_page_writes;

-- #848: an ERROR if a value did not take effect, e.g. because the postgres command
-- line fixes it (-c, also from --set); reads the settings only
DO $$
BEGIN
    IF current_setting('fsync') <> 'off' THEN
        RAISE EXCEPTION 'load durability: fsync is %, not off', current_setting('fsync');
    END IF;
    IF current_setting('full_page_writes') <> 'off' THEN
        RAISE EXCEPTION 'load durability: full_page_writes is %, not off', current_setting('full_page_writes');
    END IF;
END
$$;
