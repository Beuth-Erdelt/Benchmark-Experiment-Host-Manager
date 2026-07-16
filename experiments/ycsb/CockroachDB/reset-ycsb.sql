-- Benchmark-Experiment-Host-Manager | experiments/ycsb/CockroachDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for YCSB on CockroachDB. There is no
--          user-invokable checkpoint: the Pebble storage engine flushes and
--          compacts on its own internal schedule. ANALYZE refreshes planner
--          statistics on usertable before each benchmarking round.

ANALYZE usertable;
