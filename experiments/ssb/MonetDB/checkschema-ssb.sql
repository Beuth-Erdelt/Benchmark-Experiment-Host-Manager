-- Benchmark-Experiment-Host-Manager | experiments/ssb/MonetDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Last post-load script, always run (also without -xii/-xic/-xis).
--          Reports row counts and storage sizes. MonetDB's init scripts relax
--          no setting, so nothing is restored here.
--          No curly braces in this file: bexhoma may fill it with str.format().

-- Row counts per table (exact counts; for reference: lineorder SF 10 = 59,986,052)
SELECT 'customer' AS table_name, COUNT(*) AS row_count FROM sys.customer
UNION ALL SELECT 'dates',     COUNT(*) FROM sys.dates
UNION ALL SELECT 'lineorder', COUNT(*) FROM sys.lineorder
UNION ALL SELECT 'part',      COUNT(*) FROM sys.part
UNION ALL SELECT 'supplier',  COUNT(*) FROM sys.supplier;

-- Storage per table (columns, heaps and auxiliary structures)
SELECT s."table",
       CAST(SUM(s.columnsize + s.heapsize + s.hashes + s.imprints + s.orderidx) / 1024 / 1024 AS BIGINT) AS size_mib
FROM sys."storage" s
JOIN sys.tables t ON t.name = s."table" AND t.system = false
WHERE s."schema" = 'sys'
GROUP BY s."table"
ORDER BY size_mib DESC;
