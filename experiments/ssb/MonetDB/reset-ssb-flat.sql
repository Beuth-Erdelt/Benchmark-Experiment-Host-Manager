-- Benchmark-Experiment-Host-Manager | experiments/ssb/MonetDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for SSB (-xsv flat) on MonetDB, run before each
--          benchmarking round with -ar. As reset-ssb.sql, for the one table
--          lineorder_flat.
--          No curly braces in this file: bexhoma may fill it with str.format().

-- step 1 (statistics)
ANALYZE sys.lineorder_flat;

-- step 2 (persist): n/a - no user-invokable flush of the write-ahead log

-- step 3 (counters): n/a - MonetDB has no resettable cumulative activity counters
