-- Benchmark-Experiment-Host-Manager | experiments/ssb/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for SSB (star schema) on PostgreSQL, run before
--          each benchmarking round with -ar. Steps of the reset contract
--          (docs/DBMS.md): 1 statistics, 2 persist, 3 counters. CHECKPOINT
--          comes after VACUUM, which dirties pages again. It writes dirty
--          buffers but keeps them, so caches stay warm. \timing reports
--          elapsed time per statement on stdout; VERBOSE reports page/tuple
--          counts as NOTICEs, which psql sends to stderr. -xsv flat uses
--          reset-ssb-flat.sql.
--          No curly braces in this file: bexhoma may fill it with str.format().

\timing on

-- step 1 (statistics)
VACUUM VERBOSE ANALYZE public.customer;
VACUUM VERBOSE ANALYZE public.supplier;
VACUUM VERBOSE ANALYZE public.part;
VACUUM VERBOSE ANALYZE public.dates;
VACUUM VERBOSE ANALYZE public.lineorder;

-- step 2 (persist)
CHECKPOINT;

-- step 3 (counters)
SELECT pg_stat_reset();
SELECT pg_stat_reset_shared('bgwriter');
SELECT pg_stat_reset_shared('checkpointer');
SELECT pg_stat_reset_shared('io');
SELECT pg_stat_reset_shared('wal');
