-- Distribute main tables by warehouse_id
-- SELECT create_distributed_table('warehouse', 'w_id');
-- SELECT create_distributed_table('district', 'd_w_id', colocate_with => 'warehouse');
-- SELECT create_distributed_table('customer', 'c_w_id', colocate_with => 'warehouse');
-- SELECT create_distributed_table('oorder', 'o_w_id', colocate_with => 'warehouse');
-- SELECT create_distributed_table('new_order', 'no_w_id', colocate_with => 'warehouse');
-- SELECT create_distributed_table('stock', 's_w_id', colocate_with => 'warehouse');

-- SELECT create_distributed_table('order_line', 'ol_w_id');
-- SELECT create_distributed_table('history', 'h_w_id', colocate_with => 'warehouse');

-- Replicate Small Lookup Tables
-- SELECT create_reference_table('item');

-- ERROR:  canceling the transaction since it was involved in a distributed deadlock
-- SELECT run_command_on_workers('ANALYZE VERBOSE warehouse');
-- SELECT run_command_on_workers('ANALYZE VERBOSE district');
-- SELECT run_command_on_workers('ANALYZE VERBOSE customer');
-- SELECT run_command_on_workers('ANALYZE VERBOSE oorder');
-- SELECT run_command_on_workers('ANALYZE VERBOSE new_order');
-- SELECT run_command_on_workers('ANALYZE VERBOSE stock');
-- SELECT run_command_on_workers('ANALYZE VERBOSE order_line');
-- SELECT run_command_on_workers('ANALYZE VERBOSE history');
-- SELECT run_command_on_workers('ANALYZE VERBOSE item');

VACUUM warehouse;
VACUUM district;
VACUUM customer;
VACUUM oorder;
VACUUM new_order;
VACUUM stock;
VACUUM order_line;
VACUUM history;
VACUUM item;


ANALYZE warehouse;
ANALYZE district;
ANALYZE customer;
ANALYZE oorder;
ANALYZE new_order;
ANALYZE stock;
ANALYZE order_line;
ANALYZE history;
ANALYZE item;


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

