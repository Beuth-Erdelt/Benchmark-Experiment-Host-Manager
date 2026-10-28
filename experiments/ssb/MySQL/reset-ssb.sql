-- Benchmark-Experiment-Host-Manager | experiments/ssb/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Step 1 (statistics) of the reset contract (docs/DBMS.md) for
--          SSB (star schema) on MySQL, run before each benchmarking round with -ar.
--          ANALYZE TABLE refreshes optimizer statistics on every SSB table.
--          Steps 2 (persist) and 3 (counters) follow in reset-flush.sh.
--          No curly braces in this file: bexhoma may fill it with str.format().

ANALYZE TABLE ssb.customer;
ANALYZE TABLE ssb.supplier;
ANALYZE TABLE ssb.part;
ANALYZE TABLE ssb.dates;
ANALYZE TABLE ssb.lineorder;
