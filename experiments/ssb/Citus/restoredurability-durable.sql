-- Benchmark-Experiment-Host-Manager | experiments/ssb/Citus
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Undo load durability 'durable' after the load (post-load phase, right
--          before the check script), on the coordinator and all workers: back
--          to the configured values (template and --set arguments).
--          No curly braces in this file: bexhoma may fill it with str.format().

ALTER SYSTEM RESET synchronous_commit;
ALTER SYSTEM RESET fsync;
ALTER SYSTEM RESET full_page_writes;
SELECT pg_reload_conf();
SELECT * FROM run_command_on_workers($cmd$ALTER SYSTEM RESET synchronous_commit$cmd$);
SELECT * FROM run_command_on_workers($cmd$ALTER SYSTEM RESET fsync$cmd$);
SELECT * FROM run_command_on_workers($cmd$ALTER SYSTEM RESET full_page_writes$cmd$);
SELECT * FROM run_command_on_workers($cmd$SELECT pg_reload_conf()$cmd$);
SELECT pg_sleep(1);
SHOW synchronous_commit;
SELECT * FROM run_command_on_workers($cmd$SHOW synchronous_commit$cmd$);
