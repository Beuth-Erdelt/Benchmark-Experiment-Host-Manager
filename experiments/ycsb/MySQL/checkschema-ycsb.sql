-- Benchmark-Experiment-Host-Manager | experiments/ycsb/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Post-load checks for YCSB on MySQL (initscripts key 'Checks').
--          Restores the settings relaxed for the load to the startup values
--          saved by initschema-ycsb.sql, and reports the row count, sizes, the
--          redo log written so far and the non-default configuration.
--          No curly braces in this file: bexhoma may fill it with str.format().

-- Restore the settings saved before the load (SET GLOBAL x = DEFAULT would give
-- compiled defaults, not the server's startup values). @v starts at the current
-- value, so a setting without a saved row stays as it is.
SET @v = @@GLOBAL.innodb_flush_log_at_trx_commit;
SELECT CAST(value AS UNSIGNED) INTO @v FROM bexhoma.saved_settings WHERE name = 'innodb_flush_log_at_trx_commit';
SET GLOBAL innodb_flush_log_at_trx_commit = @v;
SET @v = @@GLOBAL.innodb_log_buffer_size;
SELECT CAST(value AS UNSIGNED) INTO @v FROM bexhoma.saved_settings WHERE name = 'innodb_log_buffer_size';
SET GLOBAL innodb_log_buffer_size = @v;

SELECT name, value AS saved_value FROM bexhoma.saved_settings ORDER BY name;
SELECT @@GLOBAL.innodb_flush_log_at_trx_commit, @@GLOBAL.innodb_log_buffer_size;

-- Row count (exact)
SELECT COUNT(*) AS row_count FROM ycsb.usertable;

-- Sizes (InnoDB estimates)
SELECT table_name,
       ROUND(data_length / 1024 / 1024)  AS data_mib,
       ROUND(index_length / 1024 / 1024) AS index_mib
FROM information_schema.tables
WHERE table_schema = 'ycsb';

-- Redo log written since server start, i.e. mostly by the load
SHOW GLOBAL STATUS WHERE Variable_name IN ('Innodb_os_log_written', 'Innodb_data_written', 'Innodb_redo_log_enabled');

-- Configuration that differs from the compiled defaults
SELECT vi.VARIABLE_NAME, gv.VARIABLE_VALUE, vi.VARIABLE_SOURCE
FROM performance_schema.variables_info vi
JOIN performance_schema.global_variables gv ON gv.VARIABLE_NAME = vi.VARIABLE_NAME
WHERE vi.VARIABLE_SOURCE <> 'COMPILED'
ORDER BY vi.VARIABLE_NAME;
