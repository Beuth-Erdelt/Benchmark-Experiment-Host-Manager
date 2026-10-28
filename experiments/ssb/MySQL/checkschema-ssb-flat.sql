-- Benchmark-Experiment-Host-Manager | experiments/ssb/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Last post-load script of -xsv flat, always run (also without
--          -xii/-xis). Reports the settings in effect, the row count, size and
--          redo log written so far. Load settings (-xld) are restored before, by
--          restoredurability-*.sql.
--          No curly braces in this file: bexhoma may fill it with str.format().

SELECT @@GLOBAL.innodb_flush_log_at_trx_commit, @@GLOBAL.foreign_key_checks,
       @@GLOBAL.unique_checks, @@GLOBAL.autocommit;

-- Row count (exact count; for reference: lineorder SF 10 = 59,986,052)
SELECT 'lineorder_flat' AS table_name, COUNT(*) AS row_count FROM ssb.lineorder_flat;

-- Sizes (InnoDB estimates)
SELECT table_name,
       ROUND(data_length / 1024 / 1024)  AS data_mib,
       ROUND(index_length / 1024 / 1024) AS index_mib
FROM information_schema.tables
WHERE table_schema = 'ssb'
ORDER BY data_length + index_length DESC;

-- Redo log written since server start, i.e. mostly by the load
SHOW GLOBAL STATUS WHERE Variable_name IN ('Innodb_os_log_written', 'Innodb_data_written', 'Innodb_redo_log_enabled');
