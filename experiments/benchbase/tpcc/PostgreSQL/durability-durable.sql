-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load durability 'durable' (-xld durable), first pre-load script.
--          The load runs crash-safe, whatever the server was started with
--          (as long as it is not fixed on the command line, see below): commits
--          wait for the WAL flush, data is fsynced, full page images are logged.
--          restoredurability-durable.sql returns to the configured state after the load.
--          ALTER SYSTEM cannot override a parameter given on the postgres command
--          line (-c, also from --set): such a parameter keeps its value.
--          No curly braces in this file: bexhoma may fill it with str.format().

ALTER SYSTEM SET synchronous_commit = on;
ALTER SYSTEM SET fsync = on;
ALTER SYSTEM SET full_page_writes = on;
SELECT pg_reload_conf();
SELECT pg_sleep(1);
SHOW synchronous_commit;
SHOW fsync;
SHOW full_page_writes;
