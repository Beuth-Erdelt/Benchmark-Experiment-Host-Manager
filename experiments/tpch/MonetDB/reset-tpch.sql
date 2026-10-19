-- Benchmark-Experiment-Host-Manager | experiments/tpch/MonetDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for TPC-H on MonetDB, run before each
--          benchmarking round with -ar. Steps of the reset contract
--          (docs/DBMS.md): 1 statistics, 2 persist, 3 counters. ANALYZE
--          refreshes the column statistics; sys.flush_log() moves the changes
--          in the write-ahead log into the persistent BATs, so that work does
--          not fall into the measured round. Tables are in schema sys.

-- step 1 (statistics)
ANALYZE sys.customer;
ANALYZE sys.lineitem;
ANALYZE sys.nation;
ANALYZE sys.orders;
ANALYZE sys.part;
ANALYZE sys.partsupp;
ANALYZE sys.region;
ANALYZE sys.supplier;

-- step 2 (persist)
CALL sys.flush_log();

-- step 3 (counters): n/a - MonetDB has no resettable cumulative activity counters
