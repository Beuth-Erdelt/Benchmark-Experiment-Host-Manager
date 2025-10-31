SELECT tidb_version();

SET CONFIG pd max-replicas = {num_worker_replicas};

SELECT * FROM information_schema.cluster_info;

SELECT * FROM INFORMATION_SCHEMA.TIKV_STORE_STATUS;

SELECT * FROM INFORMATION_SCHEMA.TIKV_REGION_STATUS LIMIT 20;
SELECT * FROM INFORMATION_SCHEMA.TIKV_REGION_PEERS LIMIT 20;

-- CREATE PLACEMENT POLICY bexhoma_replicas FOLLOWERS=2;
-- ALTER TABLE my_table PLACEMENT POLICY=bexhoma_replicas;
-- SHOW PLACEMENT POLICIES;

-- Switch to or create a database
CREATE DATABASE benchbase;
-- USE ycsb;

