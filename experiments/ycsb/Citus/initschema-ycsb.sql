CREATE TABLE public.usertable (
  ycsb_key varchar(255) NOT NULL,
  FIELD0 text,
  FIELD1 text,
  FIELD2 text,
  FIELD3 text,
  FIELD4 text,
  FIELD5 text,
  FIELD6 text,
  FIELD7 text,
  FIELD8 text,
  FIELD9 text,
  PRIMARY KEY (ycsb_key)
);

-- SET citus.shard_replication_factor = {num_worker_replicas}; -- default 1
-- SET citus.shard_count = {num_worker_shards}; -- default 32

SELECT create_distributed_table('usertable', 'ycsb_key');

-- ALTER TABLE usertable SET (replication_factor = {num_worker_replicas});
-- only citus enterprise:
-- ALTER DATABASE mydb SET citus.shard_replication_factor = 2;

-- SET citus.shard_count = {num_worker_shards}; -- default 32
-- or
-- ALTER DATABASE postgres SET citus.shard_count = 32;
-- or
-- SELECT create_distributed_table('usertable', 'ycsb_key', 'hash', shard_count => {num_worker_shards});


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

SELECT logicalrelid AS tablename,
       count(*)/count(DISTINCT ps.shardid) AS replication_factor
FROM pg_dist_shard_placement ps
JOIN pg_dist_shard p ON ps.shardid=p.shardid
GROUP BY logicalrelid;
