-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/MariaDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Step 1 (statistics) of the reset contract (docs/DBMS.md) for
--          Benchbase TPC-C on MariaDB, run before each benchmarking round
--          with -ar. ANALYZE TABLE refreshes optimizer statistics on every
--          TPC-C table. Steps 2 (persist) and 3 (counters) follow in
--          reset-flush.sh.
--          MariaDB's loadData selects no database, so the tables are
--          qualified with benchbase (as in checkschema-benchbase.sql).


ANALYZE TABLE benchbase.customer;
ANALYZE TABLE benchbase.district;
ANALYZE TABLE benchbase.history;
ANALYZE TABLE benchbase.warehouse;
ANALYZE TABLE benchbase.stock;
ANALYZE TABLE benchbase.new_order;
ANALYZE TABLE benchbase.oorder;
ANALYZE TABLE benchbase.order_line;
ANALYZE TABLE benchbase.item;
