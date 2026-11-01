-- Benchmark-Experiment-Host-Manager | experiments/ycsb/CedarDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for YCSB on CedarDB, run before each
--          benchmarking round with -ar. Steps of the reset contract
--          (docs/DBMS.md): 1 statistics, 2 persist, 3 counters. \timing reports
--          elapsed time per statement on stdout. Whole database.
--          No curly braces in this file: bexhoma may fill it with str.format().

\timing on

-- step 1 (statistics)
VACUUM VERBOSE ANALYZE;

-- step 2 (persist): n/a - CHECKPOINT is not implemented in CedarDB

-- step 3 (counters): n/a - no pg_stat_reset() in CedarDB
