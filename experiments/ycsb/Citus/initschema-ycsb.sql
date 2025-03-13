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

SELECT create_distributed_table('usertable', 'ycsb_key');

-- ALTER TABLE usertable SET (replication_factor = {num_worker_replicas});
-- only citus enterprise:
-- ALTER DATABASE mydb SET citus.shard_replication_factor = 2;

SELECT "pg_stat_replication";
SELECT * FROM pg_stat_replication;

SELECT "pg_dist_partition";
SELECT * from pg_dist_partition;

SELECT "pg_dist_shard";
SELECT * from pg_dist_shard;

SELECT "citus_shards";
SELECT * FROM citus_shards;

SELECT "pg_dist_placement";
SELECT * from pg_dist_placement;

SELECT "pg_dist_node";
SELECT * from pg_dist_node;

SELECT "citus_tables";
SELECT * FROM citus_tables;

SELECT "citus_get_active_worker_nodes";
SELECT * FROM citus_get_active_worker_nodes();

