-- Benchmark-Experiment-Host-Manager | experiments/ycsb/YugabyteDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for YCSB on YugabyteDB, run from the helper pod
--          before each benchmarking round with -ar. Steps of the reset
--          contract (docs/DBMS.md): 1 statistics, 2 persist, 3 counters.
--          ANALYZE is cluster-wide. \timing reports elapsed time per
--          statement on stdout; VERBOSE reports row counts as NOTICEs, which
--          ysqlsh sends to stderr.

\timing on

-- step 1 (statistics)
ANALYZE VERBOSE usertable;

-- step 2 (persist): n/a - YSQL has no CHECKPOINT, and the helper pod has no yb-admin for flush_table

-- step 3 (counters): reset-counters.sh, on every tserver
