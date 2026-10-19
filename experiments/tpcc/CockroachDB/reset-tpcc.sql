-- Benchmark-Experiment-Host-Manager | experiments/tpcc/CockroachDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for HammerDB TPC-C on CockroachDB (not offered
--          by hammerdb.py). Steps of the reset contract (docs/DBMS.md):
--          1 statistics, 2 persist, 3 counters. ANALYZE and the SQL stats
--          reset are cluster-wide.
--          No curly braces in this file: bexhoma may fill it with str.format().

-- step 1 (statistics)
ANALYZE customer;
ANALYZE district;
ANALYZE history;
ANALYZE warehouse;
ANALYZE stock;
ANALYZE new_order;
ANALYZE orders;
ANALYZE order_line;
ANALYZE item;

-- step 2 (persist): n/a - Pebble flushes and compacts on its own schedule; there is no SQL command for it

-- step 3 (counters)
SELECT crdb_internal.reset_sql_stats();
