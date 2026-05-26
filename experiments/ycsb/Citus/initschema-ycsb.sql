-- Benchmark-Experiment-Host-Manager | experiments/ycsb/Citus
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Creates the YCSB usertable in the public schema for Citus,
--          distributes it by ycsb_key, and verifies shard placement.

CREATE TABLE public.usertable (
    ycsb_key  VARCHAR(255)  NOT NULL,
    FIELD0    TEXT,
    FIELD1    TEXT,
    FIELD2    TEXT,
    FIELD3    TEXT,
    FIELD4    TEXT,
    FIELD5    TEXT,
    FIELD6    TEXT,
    FIELD7    TEXT,
    FIELD8    TEXT,
    FIELD9    TEXT,
    PRIMARY KEY (ycsb_key)
);

SET citus.shard_count = {num_worker_shards}; -- default 32

-- only citus enterprise:
SET citus.shard_replication_factor = {num_worker_replicas}; -- default 1

SELECT create_distributed_table('usertable', 'ycsb_key');

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

SELECT logicalrelid AS tablename,
       count(*)/count(DISTINCT ps.shardid) AS replication_factor
FROM pg_dist_shard_placement ps
JOIN pg_dist_shard p ON ps.shardid=p.shardid
GROUP BY logicalrelid;

SELECT
    table_name,
    shardid,
    shard_name,
    citus_table_type,
    colocation_id,
    nodename,
    nodeport,
    pg_size_pretty(shard_size::bigint) AS shard_size_readable
FROM citus_shards;
