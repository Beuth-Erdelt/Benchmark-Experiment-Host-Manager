-- Benchmark-Experiment-Host-Manager | experiments/tpch/MonetDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for TPC-H on MonetDB, run before each
--          benchmarking round with -ar. Steps of the reset contract
--          (docs/DBMS.md): 1 statistics, 2 persist, 3 counters. ANALYZE
--          refreshes the column statistics. MonetDB applies its write-ahead log
--          to the persistent BATs in the background and has no call to force it
--          (no sys.flush_log() in Dec2025; suspend/resume_log_flushing only pause
--          the background flusher). Tables are in schema sys.

-- step 1 (statistics)
ANALYZE sys.customer;
ANALYZE sys.lineitem;
ANALYZE sys.nation;
ANALYZE sys.orders;
ANALYZE sys.part;
ANALYZE sys.partsupp;
ANALYZE sys.region;
ANALYZE sys.supplier;

-- step 2 (persist): n/a - no user-invokable flush of the write-ahead log

-- step 3 (counters): n/a - MonetDB has no resettable cumulative activity counters
