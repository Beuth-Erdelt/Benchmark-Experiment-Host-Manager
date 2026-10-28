-- Benchmark-Experiment-Host-Manager | experiments/ssb/MonetDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for SSB on MonetDB, run before each
--          benchmarking round with -ar. Steps of the reset contract
--          (docs/DBMS.md): 1 statistics, 2 persist, 3 counters. ANALYZE
--          refreshes the column statistics of every table in schema sys, so
--          both schema variants (normal and flat) are covered. MonetDB applies
--          its write-ahead log in the background and has no call to force it.
--          No curly braces in this file: bexhoma may fill it with str.format().

-- step 1 (statistics)
ANALYZE sys;

-- step 2 (persist): n/a - no user-invokable flush of the write-ahead log

-- step 3 (counters): n/a - MonetDB has no resettable cumulative activity counters
