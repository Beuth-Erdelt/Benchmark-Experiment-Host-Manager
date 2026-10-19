-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Step 1 (statistics) of the reset contract (docs/DBMS.md) for
--          Benchbase TPC-C on MySQL, run before each benchmarking round with
--          -ar. ANALYZE TABLE refreshes optimizer statistics on every TPC-C
--          table. Steps 2 (persist) and 3 (counters) follow in reset-flush.sh.

USE benchbase;

ANALYZE TABLE customer;
ANALYZE TABLE district;
ANALYZE TABLE history;
ANALYZE TABLE warehouse;
ANALYZE TABLE stock;
ANALYZE TABLE new_order;
ANALYZE TABLE oorder;
ANALYZE TABLE order_line;
ANALYZE TABLE item;
