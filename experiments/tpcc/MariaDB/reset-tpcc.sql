-- Benchmark-Experiment-Host-Manager | experiments/tpcc/MariaDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for HammerDB TPC-C on MariaDB. InnoDB has no
--          user-invokable checkpoint; ANALYZE TABLE refreshes optimizer
--          statistics on every TPC-C table before each round. FLUSH STATUS
--          zeros the cumulative SHOW GLOBAL STATUS counters so the upcoming
--          round's stats aren't mixed with earlier rounds.

ANALYZE TABLE customer;
ANALYZE TABLE district;
ANALYZE TABLE history;
ANALYZE TABLE warehouse;
ANALYZE TABLE stock;
ANALYZE TABLE new_order;
ANALYZE TABLE orders;
ANALYZE TABLE order_line;
ANALYZE TABLE item;

FLUSH STATUS;
