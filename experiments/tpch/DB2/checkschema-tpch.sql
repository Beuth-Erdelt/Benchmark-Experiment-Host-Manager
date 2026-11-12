-- Benchmark-Experiment-Host-Manager | experiments/tpch/DB2
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Post-load checks for TPC-H on IBM Db2 (initscripts key 'Checks').
--          Runs last after loading: reports the version and license, writes the
--          dirty pages of the load to disk (FLUSH BUFFERPOOLS ALL), and reports
--          row counts, sizes, the log written so far and the configuration of
--          the database, including that the AI optimizer (Technology Preview
--          Code) is off. The schema is DB2INST1 (default schema of the CLP
--          session of /tmp/bexhoma-run.sh).
--          No curly braces in this file: bexhoma may fill it with str.format().

-- Version and license
SELECT CAST(service_level AS VARCHAR(30)) AS service_level FROM TABLE(SYSPROC.ENV_GET_INST_INFO());
SELECT CAST(installed_prod_fullname AS VARCHAR(40)) AS product,
       CAST(prod_release AS VARCHAR(10)) AS release,
       CAST(license_type AS VARCHAR(20)) AS license
FROM sysibmadm.env_prod_info
WHERE license_installed = 'Y';

-- Persist: write the dirty pages of the load
FLUSH BUFFERPOOLS ALL;

-- Row counts per table (exact)
SELECT 'customer' AS tab, COUNT(*) AS num_rows FROM customer
UNION ALL SELECT 'lineitem', COUNT(*) FROM lineitem
UNION ALL SELECT 'nation',   COUNT(*) FROM nation
UNION ALL SELECT 'orders',   COUNT(*) FROM orders
UNION ALL SELECT 'part',     COUNT(*) FROM part
UNION ALL SELECT 'partsupp', COUNT(*) FROM partsupp
UNION ALL SELECT 'region',   COUNT(*) FROM region
UNION ALL SELECT 'supplier', COUNT(*) FROM supplier;

-- Sizes of tables and indexes (KiB)
SELECT CAST(tabname AS VARCHAR(20)) AS tabname,
       data_object_p_size AS data_kib,
       index_object_p_size AS index_kib
FROM sysibmadm.admintabinfo
WHERE tabschema = CURRENT SCHEMA
ORDER BY data_object_p_size DESC;

SELECT SUM(data_object_p_size + index_object_p_size) / 1024 AS user_data_mib
FROM sysibmadm.admintabinfo
WHERE tabschema = CURRENT SCHEMA;

-- Log written since the activation of the database, i.e. mostly by the load (pages of 4 KiB)
SELECT log_writes, num_log_write_io, total_log_used
FROM TABLE(MON_GET_TRANSACTION_LOG(-2));

-- Configuration of the database and the instance
SELECT CAST(name AS VARCHAR(20)) AS name, CAST(value AS VARCHAR(30)) AS value
FROM sysibmadm.dbcfg
WHERE name IN ('ai_optimizer', 'auto_ai_optimizer', 'auto_ai_maint', 'logfilsiz', 'logprimary',
               'logsecond', 'logarchmeth1', 'self_tuning_mem', 'database_memory', 'dft_table_org',
               'dft_degree', 'pagesize')
ORDER BY name;

SELECT CAST(name AS VARCHAR(20)) AS name, CAST(value AS VARCHAR(30)) AS value
FROM sysibmadm.dbmcfg
WHERE name IN ('instance_memory', 'intra_parallel')
ORDER BY name;
