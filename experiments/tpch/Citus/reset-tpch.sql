-- Benchmark-Experiment-Host-Manager | experiments/tpch/Citus
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for TPC-H on Citus, run once on the
--          coordinator before each benchmarking round with -ar. Steps of the
--          reset contract (docs/DBMS.md): 1 statistics, 2 persist, 3 counters.
--          VACUUM ANALYZE on a distributed or reference table is passed on to
--          its shards on the workers. CHECKPOINT and the pg_stat_reset* calls
--          run on the coordinator and, through run_command_on_workers, on
--          every worker; the result rows show a failing node (success = f).
--          CHECKPOINT comes after VACUUM, which dirties pages again, and keeps
--          the buffers, so caches stay warm. \timing reports elapsed time per
--          statement on stdout; VERBOSE reports page/tuple counts as NOTICEs,
--          which psql sends to stderr.
--          No curly braces in this file: bexhoma fills it with str.format().

\timing on

-- step 1 (statistics)
VACUUM VERBOSE ANALYZE customer;
VACUUM VERBOSE ANALYZE lineitem;
VACUUM VERBOSE ANALYZE nation;
VACUUM VERBOSE ANALYZE orders;
VACUUM VERBOSE ANALYZE part;
VACUUM VERBOSE ANALYZE partsupp;
VACUUM VERBOSE ANALYZE region;
VACUUM VERBOSE ANALYZE supplier;

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
