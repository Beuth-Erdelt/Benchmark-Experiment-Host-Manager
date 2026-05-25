-- Benchmark-Experiment-Host-Manager | experiments/ycsb/TiDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Configures replication, creates the ycsb database and usertable
--          for TiDB, and reports cluster and TiKV region status.

SELECT tidb_version();

SET CONFIG pd max-replicas = {num_worker_replicas};

SELECT * FROM information_schema.cluster_info;

SELECT * FROM INFORMATION_SCHEMA.TIKV_STORE_STATUS;

SELECT * FROM INFORMATION_SCHEMA.TIKV_REGION_STATUS LIMIT 20;
SELECT * FROM INFORMATION_SCHEMA.TIKV_REGION_PEERS LIMIT 20;

CREATE DATABASE ycsb;

-- Create table with hash sharding for better distribution
CREATE TABLE ycsb.usertable (
    YCSB_KEY  VARCHAR(255) PRIMARY KEY,
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
