-- Benchmark-Experiment-Host-Manager | experiments/ycsb/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Step 1 (statistics) of the reset contract (docs/DBMS.md) for YCSB
--          on MySQL, run before each benchmarking round with -ar. ANALYZE
--          TABLE refreshes optimizer statistics on usertable. Steps 2
--          (persist) and 3 (counters) follow in reset-flush.sh.

ANALYZE TABLE ycsb.usertable;
