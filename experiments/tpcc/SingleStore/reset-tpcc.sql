-- Benchmark-Experiment-Host-Manager | experiments/tpcc/SingleStore
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for HammerDB TPC-C on SingleStore. There is no
--          user-invokable checkpoint; ANALYZE TABLE refreshes optimizer
--          statistics on every TPC-C table before each round.

ANALYZE TABLE tpcc.customer;
ANALYZE TABLE tpcc.district;
ANALYZE TABLE tpcc.history;
ANALYZE TABLE tpcc.warehouse;
ANALYZE TABLE tpcc.stock;
ANALYZE TABLE tpcc.new_order;
ANALYZE TABLE tpcc.orders;
ANALYZE TABLE tpcc.order_line;
ANALYZE TABLE tpcc.item;
