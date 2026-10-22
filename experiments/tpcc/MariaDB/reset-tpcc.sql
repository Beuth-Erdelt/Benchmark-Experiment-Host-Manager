-- Benchmark-Experiment-Host-Manager | experiments/tpcc/MariaDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Step 1 (statistics) of the reset contract (docs/DBMS.md) for
--          HammerDB TPC-C on MariaDB, run before each benchmarking round with
--          -ar. ANALYZE TABLE refreshes optimizer statistics on every TPC-C
--          table in database tpcc. Steps 2 (persist) and 3 (counters) follow
--          in reset-flush.sh.

USE tpcc;

ANALYZE TABLE customer;
ANALYZE TABLE district;
ANALYZE TABLE history;
ANALYZE TABLE warehouse;
ANALYZE TABLE stock;
ANALYZE TABLE new_order;
ANALYZE TABLE orders;
ANALYZE TABLE order_line;
ANALYZE TABLE item;
