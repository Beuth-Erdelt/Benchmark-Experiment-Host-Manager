-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/CockroachDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for Benchbase TPC-C on CockroachDB. There is no
--          user-invokable checkpoint: the Pebble storage engine flushes and
--          compacts on its own internal schedule. ANALYZE refreshes planner
--          statistics on every TPC-C table before each round.

ANALYZE customer;
ANALYZE district;
ANALYZE history;
ANALYZE warehouse;
ANALYZE stock;
ANALYZE new_order;
ANALYZE oorder;
ANALYZE order_line;
ANALYZE item;
