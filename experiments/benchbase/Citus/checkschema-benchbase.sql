-- Distribute main tables by warehouse_id
SELECT create_distributed_table('warehouse', 'w_id');
SELECT create_distributed_table('district', 'd_w_id', colocate_with => 'warehouse');
SELECT create_distributed_table('customer', 'c_w_id', colocate_with => 'warehouse');
SELECT create_distributed_table('oorder', 'o_w_id', colocate_with => 'warehouse');
SELECT create_distributed_table('new_order', 'no_w_id', colocate_with => 'warehouse');
SELECT create_distributed_table('stock', 's_w_id', colocate_with => 'warehouse');

SELECT create_distributed_table('order_line', 'ol_w_id');
SELECT create_distributed_table('history', 'h_w_id', colocate_with => 'warehouse');

-- Replicate Small Lookup Tables
SELECT create_reference_table('item');


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

