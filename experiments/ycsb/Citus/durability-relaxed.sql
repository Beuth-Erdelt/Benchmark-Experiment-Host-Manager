-- Benchmark-Experiment-Host-Manager | experiments/ycsb/Citus
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load durability 'relaxed' (-xld relaxed, the default), first pre-load
--          script. As PostgreSQL, on the coordinator and on all workers (where
--          the shards are): commits return before the WAL is flushed.
--          restoredurability-relaxed.sql resets it after the load.
--          No 'unsafe' level for Citus: its restore would need a sync on every worker.
--          No curly braces in this file: bexhoma may fill it with str.format().

ALTER SYSTEM SET synchronous_commit = off;
SELECT pg_reload_conf();
SELECT * FROM run_command_on_workers($cmd$ALTER SYSTEM SET synchronous_commit = off$cmd$);
SELECT * FROM run_command_on_workers($cmd$SELECT pg_reload_conf()$cmd$);
SELECT pg_sleep(1);
SHOW synchronous_commit;
SELECT * FROM run_command_on_workers($cmd$SHOW synchronous_commit$cmd$);
