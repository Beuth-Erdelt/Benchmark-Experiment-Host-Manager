-- Benchmark-Experiment-Host-Manager | experiments/ssb/Citus
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for SSB (-xsv flat) on Citus, run once on the
--          coordinator before each benchmarking round with -ar. As reset-ssb.sql,
--          for the one table lineorder_flat.
--          No curly braces in this file: bexhoma may fill it with str.format().

\timing on

-- step 1 (statistics)
VACUUM VERBOSE ANALYZE public.lineorder_flat;

-- step 2 (persist)
CHECKPOINT;
SELECT * FROM run_command_on_workers($cmd$CHECKPOINT$cmd$);

-- step 3 (counters)
SELECT pg_stat_reset();
SELECT pg_stat_reset_shared('bgwriter');
SELECT pg_stat_reset_shared('checkpointer');
SELECT pg_stat_reset_shared('io');
SELECT pg_stat_reset_shared('wal');
SELECT * FROM run_command_on_workers($cmd$SELECT pg_stat_reset()$cmd$);
SELECT * FROM run_command_on_workers($cmd$SELECT pg_stat_reset_shared('bgwriter')$cmd$);
SELECT * FROM run_command_on_workers($cmd$SELECT pg_stat_reset_shared('checkpointer')$cmd$);
SELECT * FROM run_command_on_workers($cmd$SELECT pg_stat_reset_shared('io')$cmd$);
SELECT * FROM run_command_on_workers($cmd$SELECT pg_stat_reset_shared('wal')$cmd$);
