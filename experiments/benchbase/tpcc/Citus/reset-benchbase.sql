-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/Citus
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for Benchbase TPC-C on Citus. CHECKPOINT only
--          flushes the coordinator node reached by this connection; worker
--          nodes checkpoint on their own schedule. VACUUM ANALYZE refreshes
--          planner statistics on every TPC-C table before each round.

CHECKPOINT;

VACUUM ANALYZE customer;
VACUUM ANALYZE district;
VACUUM ANALYZE history;
VACUUM ANALYZE warehouse;
VACUUM ANALYZE stock;
VACUUM ANALYZE new_order;
VACUUM ANALYZE oorder;
VACUUM ANALYZE order_line;
VACUUM ANALYZE item;
