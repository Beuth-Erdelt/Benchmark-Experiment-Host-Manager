-- Benchmark-Experiment-Host-Manager | experiments/ycsb/TiDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for YCSB on TiDB, run before each benchmarking
--          round with -ar. Steps of the reset contract (docs/DBMS.md):
--          1 statistics, 2 persist, 3 counters. ANALYZE TABLE forces fresh
--          histograms (cluster-wide) instead of relying on the timing of
--          TiDB's auto-analyze job.
--          No curly braces in this file: bexhoma fills it with str.format().

-- step 1 (statistics)
ANALYZE TABLE ycsb.usertable;

-- step 2 (persist): n/a - TiKV/RocksDB has no user-invokable flush in SQL

-- step 3 (counters): status counters of the TiDB server this connection reaches
FLUSH STATUS;
