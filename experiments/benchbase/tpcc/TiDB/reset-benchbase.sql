-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/TiDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for Benchbase TPC-C on TiDB. The TiKV/RocksDB
--          storage layer has no user-invokable checkpoint. ANALYZE TABLE
--          forces fresh histograms on every TPC-C table before each round,
--          rather than relying on TiDB's async auto-analyze job timing.

ANALYZE TABLE customer;
ANALYZE TABLE district;
ANALYZE TABLE history;
ANALYZE TABLE warehouse;
ANALYZE TABLE stock;
ANALYZE TABLE new_order;
ANALYZE TABLE oorder;
ANALYZE TABLE order_line;
ANALYZE TABLE item;
