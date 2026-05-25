-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/Citus
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Post-load maintenance and distribution verification for the benchbase
--          TPC-C tables on Citus. Runs VACUUM ANALYZE on all 9 tables, then
--          queries Citus catalog views to confirm shard placement.

VACUUM ANALYZE customer;
VACUUM ANALYZE district;
VACUUM ANALYZE history;
VACUUM ANALYZE warehouse;
VACUUM ANALYZE stock;
VACUUM ANALYZE new_order;
VACUUM ANALYZE oorder;
VACUUM ANALYZE order_line;
VACUUM ANALYZE item;

-- Verify Distribution
SELECT * FROM citus_shards;

SELECT 'pg_stat_replication' AS message;
SELECT * FROM pg_stat_replication;

SELECT 'pg_dist_partition' AS message;
SELECT * FROM pg_dist_partition;

SELECT 'pg_dist_shard' AS message;
SELECT * FROM pg_dist_shard;

SELECT 'citus_shards' AS message;
SELECT * FROM citus_shards;

SELECT 'pg_dist_placement' AS message;
SELECT * FROM pg_dist_placement;

SELECT 'pg_dist_node' AS message;
SELECT * FROM pg_dist_node;

SELECT 'citus_tables' AS message;
SELECT * FROM citus_tables;

SELECT 'citus_get_active_worker_nodes' AS message;
SELECT * FROM citus_get_active_worker_nodes();
