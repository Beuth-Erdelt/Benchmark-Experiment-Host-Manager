-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/TiDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for Benchbase TPC-C on TiDB, run before each
--          benchmarking round with -ar. Steps of the reset contract
--          (docs/DBMS.md): 1 statistics, 2 persist, 3 counters. ANALYZE TABLE
--          forces fresh histograms (cluster-wide) instead of relying on the
--          timing of TiDB's auto-analyze job. Benchbase loads into the
--          database of the JDBC configuration (test), which loadData also uses,
--          so table names stay unqualified.
--          No curly braces in this file: bexhoma fills it with str.format().

-- step 1 (statistics)
ANALYZE TABLE customer;
ANALYZE TABLE district;
ANALYZE TABLE history;
ANALYZE TABLE warehouse;
ANALYZE TABLE stock;
ANALYZE TABLE new_order;
ANALYZE TABLE oorder;
ANALYZE TABLE order_line;
ANALYZE TABLE item;

-- step 2 (persist): n/a - TiKV/RocksDB has no user-invokable flush in SQL

-- step 3 (counters): status counters of the TiDB server this connection reaches
FLUSH STATUS;
