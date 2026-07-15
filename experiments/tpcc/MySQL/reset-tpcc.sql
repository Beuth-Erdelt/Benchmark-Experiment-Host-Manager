-- Benchmark-Experiment-Host-Manager | experiments/tpcc/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for HammerDB TPC-C on MySQL. InnoDB has no
--          user-invokable checkpoint; ANALYZE TABLE refreshes optimizer
--          statistics on every TPC-C table before each round. The warehouse
--          table uses the MEMORY engine (see experiments/tpcc/README.md), so
--          its ANALYZE has no persisted dirty pages to act on.

ANALYZE TABLE customer;
ANALYZE TABLE district;
ANALYZE TABLE history;
ANALYZE TABLE warehouse;
ANALYZE TABLE stock;
ANALYZE TABLE new_order;
ANALYZE TABLE orders;
ANALYZE TABLE order_line;
ANALYZE TABLE item;
