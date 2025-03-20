-- This table contains information about the distribution of ranges across the nodes. It gives insights into the status of ranges, including which node is hosting which range.
SELECT 'crdb_internal.ranges' AS message;
SELECT * FROM crdb_internal.ranges;

-- This table provides information about the nodes in the cluster, including their status and other metadata.
SELECT 'crdb_internal.gossip_nodes' AS message;
SELECT * FROM crdb_internal.gossip_nodes;

-- This table provides statistics about the performance and health of ranges, such as the number of keys, the number of queries, and the number of operations on the range.
SELECT 'crdb_internal.range_stats' AS message;
SELECT * FROM crdb_internal.range_stats;

-- This table offers information about the health and status of nodes in the CockroachDB cluster.
SELECT 'crdb_internal.node_status' AS message;
SELECT * FROM crdb_internal.node_status;

SELECT 'crdb_internal.tables' AS message;
SELECT * FROM crdb_internal.tables;

SELECT 'crdb_internal.tables.usertable' AS message;
SELECT * 
FROM crdb_internal.ranges 
WHERE table_id = (SELECT table_id FROM crdb_internal.tables WHERE name = 'usertable');

SELECT 'crdb_internal.tables.usertable.replicas' AS message;
SELECT range_id, replicas, lease_holder 
FROM crdb_internal.ranges 
WHERE table_id = (SELECT table_id FROM crdb_internal.tables WHERE name = 'usertable');



