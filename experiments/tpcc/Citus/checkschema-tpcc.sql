
VACUUM warehouse;
VACUUM district;
VACUUM customer;
VACUUM orders;
VACUUM new_order;
VACUUM stock;
VACUUM order_line;
VACUUM history;
VACUUM item;


ANALYZE warehouse;
ANALYZE district;
ANALYZE customer;
ANALYZE orders;
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

