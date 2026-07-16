-- Benchmark-Experiment-Host-Manager | experiments/ycsb/MariaDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for YCSB on MariaDB. InnoDB has no
--          user-invokable checkpoint; ANALYZE TABLE refreshes optimizer
--          statistics on usertable before each benchmarking round. FLUSH
--          STATUS zeros the cumulative SHOW GLOBAL STATUS counters so the
--          upcoming round's stats aren't mixed with earlier rounds.

ANALYZE TABLE usertable;

FLUSH STATUS;
