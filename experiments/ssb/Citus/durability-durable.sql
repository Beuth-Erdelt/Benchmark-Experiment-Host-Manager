-- Benchmark-Experiment-Host-Manager | experiments/ssb/Citus
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load durability 'durable' (-xld durable), first pre-load script.
--          The load runs crash-safe on the coordinator and all workers, whatever
--          they were started with. restoredurability-durable.sql returns to the
--          configured state after the load.
--          No curly braces in this file: bexhoma may fill it with str.format().

ALTER SYSTEM SET synchronous_commit = on;
ALTER SYSTEM SET fsync = on;
ALTER SYSTEM SET full_page_writes = on;
SELECT pg_reload_conf();
SELECT * FROM run_command_on_workers($cmd$ALTER SYSTEM SET synchronous_commit = on$cmd$);
SELECT * FROM run_command_on_workers($cmd$ALTER SYSTEM SET fsync = on$cmd$);
SELECT * FROM run_command_on_workers($cmd$ALTER SYSTEM SET full_page_writes = on$cmd$);
SELECT * FROM run_command_on_workers($cmd$SELECT pg_reload_conf()$cmd$);
SELECT pg_sleep(1);
SHOW synchronous_commit;
SELECT * FROM run_command_on_workers($cmd$SHOW synchronous_commit$cmd$);
