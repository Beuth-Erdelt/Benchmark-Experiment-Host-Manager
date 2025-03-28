
VACUUM usertable;


ANALYZE usertable;


-- Verify Distribution
SELECT * FROM citus_shards;


SELECT 'pg_stat_replication' AS message;
SELECT * FROM pg_stat_replication;

SELECT 'pg_dist_partition' AS message;
SELECT * from pg_dist_partition;

SELECT 'pg_dist_shard' AS message;
SELECT * from pg_dist_shard;

SELECT 'citus_shards' AS message;
SELECT * FROM citus_shards;

SELECT 'pg_dist_placement' AS message;
SELECT * from pg_dist_placement;

SELECT 'pg_dist_node' AS message;
SELECT * from pg_dist_node;

SELECT 'citus_tables' AS message;
SELECT * FROM citus_tables;

SELECT 'citus_get_active_worker_nodes' AS message;
SELECT * FROM citus_get_active_worker_nodes();


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

