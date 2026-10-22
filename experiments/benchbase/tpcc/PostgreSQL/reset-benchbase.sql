-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for Benchbase TPC-C on PostgreSQL (also
--          PGBouncer), run before each benchmarking round with -ar. Steps of
--          the reset contract (docs/DBMS.md): 1 statistics, 2 persist,
--          3 counters. CHECKPOINT comes after VACUUM, which dirties pages
--          again. It writes dirty buffers but keeps them, so caches stay
--          warm. \timing reports elapsed time per statement on stdout;
--          VERBOSE reports page/tuple counts as NOTICEs, which psql sends to
--          stderr. Whole database, so every tenant schema is covered.
--          No curly braces in this file: bexhoma may fill it with str.format().

\timing on

-- step 1 (statistics)
VACUUM VERBOSE ANALYZE;

-- step 2 (persist)
CHECKPOINT;

-- step 3 (counters)
SELECT pg_stat_reset();
SELECT pg_stat_reset_shared('bgwriter');
SELECT pg_stat_reset_shared('checkpointer');
SELECT pg_stat_reset_shared('io');
SELECT pg_stat_reset_shared('wal');
