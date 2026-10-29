-- Benchmark-Experiment-Host-Manager | experiments/ycsb/CockroachDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Verifies the CockroachDB cluster state and range distribution
--          after the YCSB schema is loaded. waitreplicas-ycsb.sh waits for the
--          rebalancing before (a loop needs DO, which v24.2.4 does not have).

-- Ranges still missing replicas or with learners (0 after waitreplicas-ycsb.sh)
SELECT count(*) AS ranges_pending
FROM crdb_internal.ranges
WHERE array_length(learner_replicas, 1) > 0
   OR array_length(replicas, 1) < {num_worker_replicas};

-- This table contains information about the distribution of ranges across the nodes. It gives insights into the status of ranges, including which node is hosting which range.
SELECT 'crdb_internal.ranges' AS message;
SELECT * FROM crdb_internal.ranges;

-- This table provides information about the nodes in the cluster, including their status and other metadata.
SELECT 'crdb_internal.gossip_nodes' AS message;
SELECT * FROM crdb_internal.gossip_nodes;

SELECT 'crdb_internal.tables' AS message;
SELECT * FROM crdb_internal.tables;

SELECT 'crdb_internal.tables.usertable' AS message;
SELECT *
FROM crdb_internal.ranges;

SELECT 'crdb_internal.tables.usertable.replicas' AS message;
SELECT range_id, replicas, lease_holder
FROM crdb_internal.ranges;
