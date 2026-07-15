-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/YugabyteDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for Benchbase TPC-C on YugabyteDB. YSQL does
--          not implement CHECKPOINT, so only ANALYZE VERBOSE runs here to
--          refresh planner statistics on every TPC-C table before each round.

ANALYZE VERBOSE customer;
ANALYZE VERBOSE district;
ANALYZE VERBOSE history;
ANALYZE VERBOSE warehouse;
ANALYZE VERBOSE stock;
ANALYZE VERBOSE new_order;
ANALYZE VERBOSE oorder;
ANALYZE VERBOSE order_line;
ANALYZE VERBOSE item;
