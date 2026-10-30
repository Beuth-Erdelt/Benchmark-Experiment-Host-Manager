-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/MariaDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Post-load checks for the benchbase TPC-C schema on MariaDB.
--          Reports the settings in effect, row counts, sizes, the redo log
--          written so far and the non-default configuration. Load settings
--          (-xld) are restored before, by restoredurability-*.sh.
--          Benchbase loads into database benchbase. Reports only: unlike
--          MySQL's script it runs no ANALYZE TABLE.

SELECT @@GLOBAL.innodb_flush_log_at_trx_commit, @@GLOBAL.innodb_log_buffer_size;

-- Row counts per table (exact counts)
SELECT 'customer' AS table_name, COUNT(*) AS row_count FROM benchbase.customer
UNION ALL SELECT 'district',   COUNT(*) FROM benchbase.district
UNION ALL SELECT 'history',    COUNT(*) FROM benchbase.history
UNION ALL SELECT 'item',       COUNT(*) FROM benchbase.item
UNION ALL SELECT 'new_order',  COUNT(*) FROM benchbase.new_order
UNION ALL SELECT 'oorder',     COUNT(*) FROM benchbase.oorder
UNION ALL SELECT 'order_line', COUNT(*) FROM benchbase.order_line
UNION ALL SELECT 'stock',      COUNT(*) FROM benchbase.stock
UNION ALL SELECT 'warehouse',  COUNT(*) FROM benchbase.warehouse;

-- Sizes (InnoDB estimates)
SELECT table_name,
       ROUND(data_length / 1024 / 1024)  AS data_mib,
       ROUND(index_length / 1024 / 1024) AS index_mib
FROM information_schema.tables
WHERE table_schema = 'benchbase'
ORDER BY data_length + index_length DESC;

-- Redo log written since server start, i.e. mostly by the load
SHOW GLOBAL STATUS WHERE Variable_name IN ('Innodb_os_log_written', 'Innodb_data_written', 'Innodb_lsn_current');

-- Configuration that differs from the compiled defaults
SELECT VARIABLE_NAME, GLOBAL_VALUE, GLOBAL_VALUE_ORIGIN
FROM information_schema.SYSTEM_VARIABLES
WHERE GLOBAL_VALUE_ORIGIN <> 'COMPILE-TIME'
ORDER BY VARIABLE_NAME;
