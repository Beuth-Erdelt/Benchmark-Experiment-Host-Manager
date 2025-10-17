-- Overview of all regions
SELECT * FROM INFORMATION_SCHEMA.TIKV_REGION_STATUS;

-- Count regions per table
SELECT table_id, COUNT(*) AS region_count
FROM INFORMATION_SCHEMA.TIKV_REGION_STATUS
GROUP BY table_id;

-- Regions of a specific table
SELECT *
FROM INFORMATION_SCHEMA.TIKV_REGION_STATUS
WHERE table_id = (SELECT table_id FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='usertable');


-- Replica info per region
SELECT region_id, store_id, peer_id, is_leader
FROM INFORMATION_SCHEMA.TIKV_REGION_PEERS;

-- For a specific table
SELECT r.region_id, p.store_id, p.peer_id, p.is_leader
FROM INFORMATION_SCHEMA.TIKV_REGION_STATUS r
JOIN INFORMATION_SCHEMA.TIKV_REGION_PEERS p ON r.region_id = p.region_id
WHERE r.table_id = (SELECT table_id FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='usertable');


-- Cluster node information
SELECT * FROM INFORMATION_SCHEMA.TIKV_STORE_STATUS;

-- Optional: count of regions per node
SELECT store_id, COUNT(*) AS region_count
FROM INFORMATION_SCHEMA.TIKV_REGION_PEERS
GROUP BY store_id;


-- Number of replicas for a table
SELECT r.table_id, COUNT(*) AS replicas
FROM INFORMATION_SCHEMA.TIKV_REGION_PEERS p
JOIN INFORMATION_SCHEMA.TIKV_REGION_STATUS r ON p.region_id = r.region_id
WHERE r.table_id = (SELECT table_id FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='usertable')
GROUP BY r.table_id;

-- Leader distribution per table
SELECT r.table_id, SUM(CASE WHEN p.is_leader THEN 1 ELSE 0 END) AS leaders
FROM INFORMATION_SCHEMA.TIKV_REGION_PEERS p
JOIN INFORMATION_SCHEMA.TIKV_REGION_STATUS r ON p.region_id = r.region_id
WHERE r.table_id = (SELECT table_id FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='usertable')
GROUP BY r.table_id;


