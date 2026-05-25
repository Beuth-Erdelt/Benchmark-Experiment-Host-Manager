-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/CockroachDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Cluster topology and table distribution verification for the
--          benchbase TPC-C schema on CockroachDB.

-- Shows range distribution across nodes and which node hosts which range.
SELECT 'crdb_internal.ranges' AS message;
SELECT * FROM crdb_internal.ranges;

-- Shows node status and metadata for all nodes in the cluster.
SELECT 'crdb_internal.gossip_nodes' AS message;
SELECT * FROM crdb_internal.gossip_nodes;

SELECT 'crdb_internal.tables' AS message;
SELECT * FROM crdb_internal.tables;

SELECT 'crdb_internal.tables' AS message;
SELECT *
FROM crdb_internal.ranges;

SELECT 'crdb_internal.tables.replicas' AS message;
SELECT range_id, replicas, lease_holder
FROM crdb_internal.ranges;
