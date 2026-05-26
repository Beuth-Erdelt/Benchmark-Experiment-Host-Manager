-- Benchmark-Experiment-Host-Manager | experiments/ycsb/TiDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Verifies the TiDB cluster state and TiKV region distribution
--          after the YCSB workload completes.

SELECT tidb_version();

SELECT * FROM information_schema.cluster_info;

SELECT * FROM INFORMATION_SCHEMA.TIKV_STORE_STATUS;

SELECT * FROM INFORMATION_SCHEMA.TIKV_REGION_STATUS LIMIT 20;
SELECT * FROM INFORMATION_SCHEMA.TIKV_REGION_PEERS LIMIT 20;
