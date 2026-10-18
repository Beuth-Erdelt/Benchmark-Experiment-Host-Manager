-- Benchmark-Experiment-Host-Manager | experiments/tpch/MariaDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Last post-load script, always run (also without -xii/-xic/-xis).
--          Reports row counts, sizes, the redo log written so far and the
--          non-default configuration. initschema-tpch.sql relaxes no
--          durability setting, so nothing is restored here.
--          No curly braces in this file: bexhoma may fill it with str.format().

-- Row counts per table (exact counts; for reference: lineitem SF 10 = 59,986,052)
SELECT 'customer' AS table_name, COUNT(*) AS row_count FROM tpch.customer
UNION ALL SELECT 'lineitem', COUNT(*) FROM tpch.lineitem
UNION ALL SELECT 'nation',   COUNT(*) FROM tpch.nation
UNION ALL SELECT 'orders',   COUNT(*) FROM tpch.orders
UNION ALL SELECT 'part',     COUNT(*) FROM tpch.part
UNION ALL SELECT 'partsupp', COUNT(*) FROM tpch.partsupp
UNION ALL SELECT 'region',   COUNT(*) FROM tpch.region
UNION ALL SELECT 'supplier', COUNT(*) FROM tpch.supplier;

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
SHOW GLOBAL STATUS WHERE Variable_name IN ('Innodb_os_log_written', 'Innodb_data_written', 'Innodb_lsn_current');

-- Configuration that differs from the compiled defaults
SELECT VARIABLE_NAME, GLOBAL_VALUE, GLOBAL_VALUE_ORIGIN
FROM information_schema.SYSTEM_VARIABLES
WHERE GLOBAL_VALUE_ORIGIN <> 'COMPILE-TIME'
ORDER BY VARIABLE_NAME;
