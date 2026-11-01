-- Benchmark-Experiment-Host-Manager | experiments/ycsb/Cassandra
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Shows keyspace, table and ring after the load. Rows are not counted:
--          SELECT count(*) scans the whole table and runs into the server's
--          range timeout; save-snapshot.sh logs the estimate per node.

SELECT keyspace_name, durable_writes, replication
FROM system_schema.keyspaces
WHERE keyspace_name = 'ycsb';

SELECT table_name, compaction, compression
FROM system_schema.tables
WHERE keyspace_name = 'ycsb';

SELECT cluster_name, data_center, rack, release_version
FROM system.local;

SELECT peer, data_center, rack, release_version
FROM system.peers;
