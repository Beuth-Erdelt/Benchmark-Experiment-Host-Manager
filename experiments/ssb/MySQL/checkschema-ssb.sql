-- Benchmark-Experiment-Host-Manager | experiments/ssb/MySQL
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

-- Row counts per table (exact counts; for reference: lineorder SF 10 = 59,986,052)
SELECT 'customer' AS table_name, COUNT(*) AS row_count FROM ssb.customer
UNION ALL SELECT 'dates',     COUNT(*) FROM ssb.dates
UNION ALL SELECT 'lineorder', COUNT(*) FROM ssb.lineorder
UNION ALL SELECT 'part',      COUNT(*) FROM ssb.part
UNION ALL SELECT 'supplier',  COUNT(*) FROM ssb.supplier;

-- Primary and foreign keys per table (5 primary keys; with -xic 5 foreign keys)
SELECT TABLE_NAME, CONSTRAINT_TYPE, COUNT(*) AS constraint_count
FROM information_schema.TABLE_CONSTRAINTS
WHERE CONSTRAINT_SCHEMA = 'ssb'
  AND CONSTRAINT_TYPE IN ('PRIMARY KEY', 'FOREIGN KEY')
GROUP BY TABLE_NAME, CONSTRAINT_TYPE
ORDER BY TABLE_NAME, CONSTRAINT_TYPE;

-- Sizes (InnoDB estimates)
SELECT table_name,
       ROUND(data_length / 1024 / 1024)  AS data_mib,
       ROUND(index_length / 1024 / 1024) AS index_mib
FROM information_schema.tables
WHERE table_schema = 'ssb'
ORDER BY data_length + index_length DESC;

SELECT ROUND(SUM(data_length + index_length) / 1024 / 1024) AS database_mib
FROM information_schema.tables
WHERE table_schema = 'ssb';

-- Redo log written since server start, i.e. mostly by the load
SHOW GLOBAL STATUS WHERE Variable_name IN ('Innodb_os_log_written', 'Innodb_data_written', 'Innodb_redo_log_enabled');
