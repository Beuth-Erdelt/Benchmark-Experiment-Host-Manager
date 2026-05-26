-- Benchmark-Experiment-Host-Manager | experiments/tpcc/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Post-load maintenance for the TPC-C schema on PostgreSQL. Runs
--          VACUUM ANALYZE on all TPC-C tables to update planner statistics.

VACUUM ANALYZE customer;
VACUUM ANALYZE district;
VACUUM ANALYZE history;
VACUUM ANALYZE warehouse;
VACUUM ANALYZE stock;
VACUUM ANALYZE new_order;
VACUUM ANALYZE orders;
VACUUM ANALYZE order_line;
VACUUM ANALYZE item;
