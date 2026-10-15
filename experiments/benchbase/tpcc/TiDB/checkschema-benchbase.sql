-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/TiDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Cluster topology verification for the benchbase TPC-C schema on TiDB.
--          Reports TiDB version, cluster info, and TiKV region distribution.

SELECT tidb_version();

SELECT * FROM information_schema.cluster_info;

SELECT * FROM INFORMATION_SCHEMA.TIKV_STORE_STATUS;

SELECT * FROM INFORMATION_SCHEMA.TIKV_REGION_STATUS LIMIT 20;
SELECT * FROM INFORMATION_SCHEMA.TIKV_REGION_PEERS LIMIT 20;
