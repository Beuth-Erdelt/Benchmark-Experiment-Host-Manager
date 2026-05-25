-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/TiDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Configure TiDB replica count and verify cluster topology before
--          benchbase TPC-C loading. Creates the benchbase database.

SELECT tidb_version();

SET CONFIG pd max-replicas = {num_worker_replicas};

SELECT * FROM information_schema.cluster_info;

SELECT * FROM INFORMATION_SCHEMA.TIKV_STORE_STATUS;

SELECT * FROM INFORMATION_SCHEMA.TIKV_REGION_STATUS LIMIT 20;
SELECT * FROM INFORMATION_SCHEMA.TIKV_REGION_PEERS LIMIT 20;

-- Switch to or create a database
CREATE DATABASE benchbase;
