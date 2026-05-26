-- Benchmark-Experiment-Host-Manager | experiments/ycsb/YugabyteDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Creates the YCSB usertable for YugabyteDB, reports the creation
--          timestamp and row count, and verifies tablet distribution.

-- https://docs.yugabyte.com/preview/benchmark/ycsb-jdbc
-- https://docs.yugabyte.com/stable/architecture/docdb-sharding/tablet-splitting/#ycsb-workload-with-automatic-tablet-splitting-example
-- https://www.yugabyte.com/blog/optimizing-yugabytedb-memory-tuning-for-ysql/
-- ./bin/yb-ctl --rf=3 create --master_flags "enable_automatic_tablet_splitting=true,tablet_split_low_phase_size_threshold_bytes=30000000" --tserver_flags "memstore_size_mb=10"

ALTER DATABASE yugabyte SET temp_file_limit=-1;

CREATE TABLE IF NOT EXISTS usertable (
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

SELECT current_timestamp AS "Time after creation";

SELECT COUNT(*) AS "Number of rows in usertable" FROM usertable;

SELECT 'yb_table_properties.usertable' AS msg;
SELECT * FROM yb_table_properties('usertable'::regclass);

SELECT 'yb_servers' AS msg;
SELECT *
FROM yb_servers()
JOIN yb_local_tablets ON true;
