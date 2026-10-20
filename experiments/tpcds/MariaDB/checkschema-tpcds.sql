-- Benchmark-Experiment-Host-Manager | experiments/tpcds/MariaDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Last post-load script, always run (also without -xii/-xic/-xis).
--          Reports row counts, primary and foreign keys, sizes, the redo log
--          written so far and the non-default configuration. The init scripts relax no durability
--          setting, so nothing is restored here.
--          No curly braces in this file: bexhoma may fill it with str.format().

-- Row counts per table (exact counts)
SELECT 'call_center' AS table_name, COUNT(*) AS row_count FROM tpcds.call_center
UNION ALL SELECT 'catalog_page',           COUNT(*) FROM tpcds.catalog_page
UNION ALL SELECT 'catalog_returns',        COUNT(*) FROM tpcds.catalog_returns
UNION ALL SELECT 'catalog_sales',          COUNT(*) FROM tpcds.catalog_sales
UNION ALL SELECT 'customer',               COUNT(*) FROM tpcds.customer
UNION ALL SELECT 'customer_address',       COUNT(*) FROM tpcds.customer_address
UNION ALL SELECT 'customer_demographics',  COUNT(*) FROM tpcds.customer_demographics
UNION ALL SELECT 'date_dim',               COUNT(*) FROM tpcds.date_dim
UNION ALL SELECT 'dbgen_version',          COUNT(*) FROM tpcds.dbgen_version
UNION ALL SELECT 'household_demographics', COUNT(*) FROM tpcds.household_demographics
UNION ALL SELECT 'income_band',            COUNT(*) FROM tpcds.income_band
UNION ALL SELECT 'inventory',              COUNT(*) FROM tpcds.inventory
UNION ALL SELECT 'item',                   COUNT(*) FROM tpcds.item
UNION ALL SELECT 'promotion',              COUNT(*) FROM tpcds.promotion
UNION ALL SELECT 'reason',                 COUNT(*) FROM tpcds.reason
UNION ALL SELECT 'ship_mode',              COUNT(*) FROM tpcds.ship_mode
UNION ALL SELECT 'store',                  COUNT(*) FROM tpcds.store
UNION ALL SELECT 'store_returns',          COUNT(*) FROM tpcds.store_returns
UNION ALL SELECT 'store_sales',            COUNT(*) FROM tpcds.store_sales
UNION ALL SELECT 'time_dim',               COUNT(*) FROM tpcds.time_dim
UNION ALL SELECT 'warehouse',              COUNT(*) FROM tpcds.warehouse
UNION ALL SELECT 'web_page',               COUNT(*) FROM tpcds.web_page
UNION ALL SELECT 'web_returns',            COUNT(*) FROM tpcds.web_returns
UNION ALL SELECT 'web_sales',              COUNT(*) FROM tpcds.web_sales
UNION ALL SELECT 'web_site',               COUNT(*) FROM tpcds.web_site;

-- Primary and foreign keys (primary keys from initschema-tpcds.sql, foreign keys
-- from initconstraints-tpcds.sql with -xic): totals, then per table
SELECT CONSTRAINT_TYPE, COUNT(*) AS constraint_count
FROM information_schema.TABLE_CONSTRAINTS
WHERE CONSTRAINT_SCHEMA = 'tpcds'
  AND CONSTRAINT_TYPE IN ('PRIMARY KEY', 'FOREIGN KEY')
GROUP BY CONSTRAINT_TYPE
ORDER BY CONSTRAINT_TYPE;

SELECT TABLE_NAME, CONSTRAINT_TYPE, COUNT(*) AS constraint_count
FROM information_schema.TABLE_CONSTRAINTS
WHERE CONSTRAINT_SCHEMA = 'tpcds'
  AND CONSTRAINT_TYPE IN ('PRIMARY KEY', 'FOREIGN KEY')
GROUP BY TABLE_NAME, CONSTRAINT_TYPE
ORDER BY TABLE_NAME, CONSTRAINT_TYPE;

-- Sizes (InnoDB estimates)
SELECT table_name,
       ROUND(data_length / 1024 / 1024)  AS data_mib,
       ROUND(index_length / 1024 / 1024) AS index_mib
FROM information_schema.tables
WHERE table_schema = 'tpcds'
ORDER BY data_length + index_length DESC;

SELECT ROUND(SUM(data_length + index_length) / 1024 / 1024) AS database_mib
FROM information_schema.tables
WHERE table_schema = 'tpcds';

-- Redo log written since server start, i.e. mostly by the load
SHOW GLOBAL STATUS WHERE Variable_name IN ('Innodb_os_log_written', 'Innodb_data_written', 'Innodb_lsn_current');

-- Configuration that differs from the compiled defaults
SELECT VARIABLE_NAME, GLOBAL_VALUE, GLOBAL_VALUE_ORIGIN
FROM information_schema.SYSTEM_VARIABLES
WHERE GLOBAL_VALUE_ORIGIN <> 'COMPILE-TIME'
ORDER BY VARIABLE_NAME;
