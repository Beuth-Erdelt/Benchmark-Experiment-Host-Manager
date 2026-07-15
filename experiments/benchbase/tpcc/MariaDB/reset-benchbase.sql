-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/MariaDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for Benchbase TPC-C on MariaDB. InnoDB has no
--          user-invokable checkpoint; ANALYZE TABLE refreshes optimizer
--          statistics on every TPC-C table before each round.

ANALYZE TABLE customer;
ANALYZE TABLE district;
ANALYZE TABLE history;
ANALYZE TABLE warehouse;
ANALYZE TABLE stock;
ANALYZE TABLE new_order;
ANALYZE TABLE oorder;
ANALYZE TABLE order_line;
ANALYZE TABLE item;
