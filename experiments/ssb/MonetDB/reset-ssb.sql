-- Benchmark-Experiment-Host-Manager | experiments/ssb/MonetDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for SSB (star schema) on MonetDB, run before
--          each benchmarking round with -ar. Steps of the reset contract
--          (docs/DBMS.md): 1 statistics, 2 persist, 3 counters. ANALYZE
--          refreshes the column statistics of each SSB table. MonetDB applies
--          its write-ahead log in the background and has no call to force it.
--          -xsv flat uses reset-ssb-flat.sql.
--          No curly braces in this file: bexhoma may fill it with str.format().

-- step 1 (statistics)
ANALYZE sys.customer;
ANALYZE sys.supplier;
ANALYZE sys.part;
ANALYZE sys.dates;
ANALYZE sys.lineorder;

-- step 2 (persist): n/a - no user-invokable flush of the write-ahead log

-- step 3 (counters): n/a - MonetDB has no resettable cumulative activity counters
