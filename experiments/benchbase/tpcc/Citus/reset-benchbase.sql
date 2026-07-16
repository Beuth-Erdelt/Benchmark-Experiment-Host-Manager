-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/Citus
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for Benchbase TPC-C on Citus. CHECKPOINT only
--          flushes the coordinator node reached by this connection; worker
--          nodes checkpoint on their own schedule. VACUUM ANALYZE refreshes
--          planner statistics on every TPC-C table before each round. \timing
--          reports elapsed time per statement on stdout; VERBOSE reports
--          page/tuple counts as NOTICEs, which psql sends to stderr. The
--          pg_stat_reset* calls zero the cumulative activity counters, but
--          (like CHECKPOINT) only for the coordinator this connection reaches.

\timing on
CHECKPOINT;

VACUUM VERBOSE ANALYZE customer;
VACUUM VERBOSE ANALYZE district;
VACUUM VERBOSE ANALYZE history;
VACUUM VERBOSE ANALYZE warehouse;
VACUUM VERBOSE ANALYZE stock;
VACUUM VERBOSE ANALYZE new_order;
VACUUM VERBOSE ANALYZE oorder;
VACUUM VERBOSE ANALYZE order_line;
VACUUM VERBOSE ANALYZE item;

SELECT pg_stat_reset();
SELECT pg_stat_reset_shared('bgwriter');
