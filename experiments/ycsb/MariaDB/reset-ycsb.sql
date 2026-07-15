-- Benchmark-Experiment-Host-Manager | experiments/ycsb/MariaDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for YCSB on MariaDB. InnoDB has no
--          user-invokable checkpoint; ANALYZE TABLE refreshes optimizer
--          statistics on usertable before each benchmarking round.

ANALYZE TABLE usertable;
