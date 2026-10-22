-- Benchmark-Experiment-Host-Manager | experiments/benchbase/ycsb/PostgreSQL
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

ALTER SYSTEM SET fsync = off;
ALTER SYSTEM SET full_page_writes = off;
SELECT pg_reload_conf();
SELECT pg_sleep(1);
SHOW fsync;
SHOW full_page_writes;
