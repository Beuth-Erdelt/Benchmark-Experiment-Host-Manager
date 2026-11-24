-- Benchmark-Experiment-Host-Manager | experiments/ssb/CedarDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for SSB (-xsv flat) on CedarDB, run before each
--          benchmarking round with -ar. As reset-ssb.sql, for the one table
--          lineorder_flat.
--          No curly braces in this file: bexhoma may fill it with str.format().

\timing on

-- step 1 (statistics)
VACUUM VERBOSE ANALYZE public.lineorder_flat;

-- step 2 (persist): n/a - CHECKPOINT is not implemented in CedarDB

-- step 3 (counters): n/a - no pg_stat_reset() in CedarDB
