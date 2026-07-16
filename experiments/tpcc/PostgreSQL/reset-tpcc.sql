-- Benchmark-Experiment-Host-Manager | experiments/tpcc/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for HammerDB TPC-C on PostgreSQL. Flushes
--          dirty pages to disk and collects fresh statistics so each
--          benchmarking round starts from a consistent, cold state. \timing
--          reports elapsed time per statement on stdout; VERBOSE reports
--          page/tuple counts as NOTICEs, which psql sends to stderr. The
--          pg_stat_reset* calls zero the cumulative activity counters so
--          the upcoming round's stats aren't mixed with earlier rounds.

\timing on
CHECKPOINT;
VACUUM VERBOSE ANALYZE customer;
VACUUM VERBOSE ANALYZE district;
VACUUM VERBOSE ANALYZE history;
VACUUM VERBOSE ANALYZE warehouse;
VACUUM VERBOSE ANALYZE stock;
VACUUM VERBOSE ANALYZE new_order;
VACUUM VERBOSE ANALYZE orders;
VACUUM VERBOSE ANALYZE order_line;
VACUUM VERBOSE ANALYZE item;

SELECT pg_stat_reset();
SELECT pg_stat_reset_shared('bgwriter');
