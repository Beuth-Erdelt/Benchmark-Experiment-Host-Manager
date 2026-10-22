-- Benchmark-Experiment-Host-Manager | experiments/tpcc/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Post-load checks for TPC-C (HammerDB) on MySQL (initscripts key 'Checks').
--          Reports the settings in effect, row counts, sizes, the redo log
--          written so far and the non-default configuration. Load settings
--          (-xld) are restored before, by restoredurability-*.sql.
--          HammerDB loads into database tpcc.
--          No curly braces in this file: bexhoma may fill it with str.format().

SELECT @@GLOBAL.innodb_flush_log_at_trx_commit, @@GLOBAL.innodb_log_buffer_size;

-- Row counts per table (exact counts)
SELECT 'customer' AS table_name, COUNT(*) AS row_count FROM tpcc.customer
UNION ALL SELECT 'district',   COUNT(*) FROM tpcc.district
UNION ALL SELECT 'history',    COUNT(*) FROM tpcc.history
UNION ALL SELECT 'item',       COUNT(*) FROM tpcc.item
UNION ALL SELECT 'new_order',  COUNT(*) FROM tpcc.new_order
UNION ALL SELECT 'order_line', COUNT(*) FROM tpcc.order_line
UNION ALL SELECT 'orders',     COUNT(*) FROM tpcc.orders
UNION ALL SELECT 'stock',      COUNT(*) FROM tpcc.stock
UNION ALL SELECT 'warehouse',  COUNT(*) FROM tpcc.warehouse;

-- Sizes (InnoDB estimates)
SELECT table_name,
       ROUND(data_length / 1024 / 1024)  AS data_mib,
       ROUND(index_length / 1024 / 1024) AS index_mib
FROM information_schema.tables
WHERE table_schema = 'tpcc'
ORDER BY data_length + index_length DESC;

-- Redo log written since server start, i.e. mostly by the load
SHOW GLOBAL STATUS WHERE Variable_name IN ('Innodb_os_log_written', 'Innodb_data_written', 'Innodb_redo_log_enabled');

-- Configuration that differs from the compiled defaults
SELECT vi.VARIABLE_NAME, gv.VARIABLE_VALUE, vi.VARIABLE_SOURCE
FROM performance_schema.variables_info vi
JOIN performance_schema.global_variables gv ON gv.VARIABLE_NAME = vi.VARIABLE_NAME
WHERE vi.VARIABLE_SOURCE <> 'COMPILED'
ORDER BY vi.VARIABLE_NAME;
