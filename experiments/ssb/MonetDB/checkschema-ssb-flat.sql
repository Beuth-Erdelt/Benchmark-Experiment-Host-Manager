-- Benchmark-Experiment-Host-Manager | experiments/ssb/MonetDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Last post-load script of the flat variant (-xsv flat), always run.
--          Reports row count and storage size of lineorder_flat.
--          No curly braces in this file: bexhoma may fill it with str.format().

-- Row count (exact; for reference: SF 10 = 59,986,052)
SELECT 'lineorder_flat' AS table_name, COUNT(*) AS row_count FROM sys.lineorder_flat;

-- Storage (columns, heaps and auxiliary structures)
SELECT s."table",
       CAST(SUM(s.columnsize + s.heapsize + s.hashes + s.imprints + s.orderidx) / 1024 / 1024 AS BIGINT) AS size_mib
FROM sys."storage" s
JOIN sys.tables t ON t.name = s."table" AND t.system = false
WHERE s."schema" = 'sys'
GROUP BY s."table"
ORDER BY size_mib DESC;
