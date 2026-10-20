-- Benchmark-Experiment-Host-Manager | experiments/tpch/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Last post-load script, always run (also without -xii/-xic/-xis).
--          Reports the settings in effect, row counts, primary and foreign
--          keys, sizes, the redo log written so far and the non-default
--          configuration. Load settings (-xld) are restored before, by
--          restoredurability-*.sql.
--          No curly braces in this file: bexhoma may fill it with str.format().

SELECT @@GLOBAL.innodb_flush_log_at_trx_commit, @@GLOBAL.foreign_key_checks,
       @@GLOBAL.unique_checks, @@GLOBAL.autocommit;

-- Row counts per table (exact counts; for reference: lineitem SF 10 = 59,986,052)
SELECT 'customer' AS table_name, COUNT(*) AS row_count FROM tpch.customer
UNION ALL SELECT 'lineitem', COUNT(*) FROM tpch.lineitem
UNION ALL SELECT 'nation',   COUNT(*) FROM tpch.nation
UNION ALL SELECT 'orders',   COUNT(*) FROM tpch.orders
UNION ALL SELECT 'part',     COUNT(*) FROM tpch.part
UNION ALL SELECT 'partsupp', COUNT(*) FROM tpch.partsupp
UNION ALL SELECT 'region',   COUNT(*) FROM tpch.region
UNION ALL SELECT 'supplier', COUNT(*) FROM tpch.supplier;

-- Primary and foreign keys per table (8 primary keys; with -xic 9 foreign keys)
SELECT TABLE_NAME, CONSTRAINT_TYPE, COUNT(*) AS constraint_count
FROM information_schema.TABLE_CONSTRAINTS
WHERE CONSTRAINT_SCHEMA = 'tpch'
  AND CONSTRAINT_TYPE IN ('PRIMARY KEY', 'FOREIGN KEY')
GROUP BY TABLE_NAME, CONSTRAINT_TYPE
ORDER BY TABLE_NAME, CONSTRAINT_TYPE;

-- Sizes (InnoDB estimates)
SELECT table_name,
       ROUND(data_length / 1024 / 1024)  AS data_mib,
       ROUND(index_length / 1024 / 1024) AS index_mib
FROM information_schema.tables
WHERE table_schema = 'tpch'
ORDER BY data_length + index_length DESC;

SELECT ROUND(SUM(data_length + index_length) / 1024 / 1024) AS database_mib
FROM information_schema.tables
WHERE table_schema = 'tpch';

-- Redo log written since server start, i.e. mostly by the load
SHOW GLOBAL STATUS WHERE Variable_name IN ('Innodb_os_log_written', 'Innodb_data_written', 'Innodb_redo_log_enabled');

-- Configuration that differs from the compiled defaults
SELECT vi.VARIABLE_NAME, gv.VARIABLE_VALUE, vi.VARIABLE_SOURCE
FROM performance_schema.variables_info vi
JOIN performance_schema.global_variables gv ON gv.VARIABLE_NAME = vi.VARIABLE_NAME
WHERE vi.VARIABLE_SOURCE <> 'COMPILED'
ORDER BY vi.VARIABLE_NAME;
