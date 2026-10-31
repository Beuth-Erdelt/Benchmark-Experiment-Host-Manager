-- Benchmark-Experiment-Host-Manager | experiments/ssb/MariaDBCS
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Last post-load script, always run (also without -xii/-xic/-xis).
--          Reports row counts, the sizes on disk and the configuration of the server.
--          ColumnStore has no keys, so there are none to count.
--          No curly braces in this file: bexhoma may fill it with str.format().

-- Row counts per table (exact counts; for reference: lineorder SF 10 = 59,986,052)
SELECT 'customer' AS table_name, COUNT(*) AS row_count FROM ssb.customer
UNION ALL SELECT 'dates',     COUNT(*) FROM ssb.dates
UNION ALL SELECT 'lineorder', COUNT(*) FROM ssb.lineorder
UNION ALL SELECT 'part',      COUNT(*) FROM ssb.part
UNION ALL SELECT 'supplier',  COUNT(*) FROM ssb.supplier;

-- Sizes on disk per table
CALL columnstore_info.table_usage('ssb', NULL);

CALL columnstore_info.total_usage();

-- Configuration that differs from the compiled defaults
SELECT VARIABLE_NAME, GLOBAL_VALUE, GLOBAL_VALUE_ORIGIN
FROM information_schema.SYSTEM_VARIABLES
WHERE GLOBAL_VALUE_ORIGIN <> 'COMPILE-TIME'
ORDER BY VARIABLE_NAME;
