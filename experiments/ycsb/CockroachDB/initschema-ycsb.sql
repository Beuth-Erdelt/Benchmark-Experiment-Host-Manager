-- Benchmark-Experiment-Host-Manager | experiments/ycsb/CockroachDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Creates the YCSB usertable for CockroachDB with a hash-partitioned
--          primary key, configures zone replication, and reports cluster
--          range and node distribution.

CREATE TABLE public.usertable (
    YCSB_KEY  VARCHAR(255) PRIMARY KEY USING HASH,
    FIELD0    TEXT,
    FIELD1    TEXT,
    FIELD2    TEXT,
    FIELD3    TEXT,
    FIELD4    TEXT,
    FIELD5    TEXT,
    FIELD6    TEXT,
    FIELD7    TEXT,
    FIELD8    TEXT,
    FIELD9    TEXT
);

ALTER TABLE public.usertable CONFIGURE ZONE USING num_replicas = {num_worker_replicas};

SELECT 'SHOW ZONE CONFIGURATION' AS message;
SHOW ZONE CONFIGURATION FROM TABLE public.usertable;

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
