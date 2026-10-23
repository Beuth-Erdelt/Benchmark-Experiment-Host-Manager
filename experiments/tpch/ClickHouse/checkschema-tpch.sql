-- Benchmark-Experiment-Host-Manager | experiments/tpch/ClickHouse
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Last post-load script, always run (also without -xii/-xic/-xis).
--          Reports row counts and storage sizes. ClickHouse's init scripts
--          relax no setting, so nothing is restored here.
--          No curly braces in this file: bexhoma may fill it with str.format().

-- Row counts per table (exact counts; for reference: lineitem SF 10 = 59,986,052)
SELECT 'customer' AS table_name, count() AS row_count FROM customer
UNION ALL SELECT 'lineitem', count() FROM lineitem
UNION ALL SELECT 'nation',   count() FROM nation
UNION ALL SELECT 'orders',   count() FROM orders
UNION ALL SELECT 'part',     count() FROM part
UNION ALL SELECT 'partsupp', count() FROM partsupp
UNION ALL SELECT 'region',   count() FROM region
UNION ALL SELECT 'supplier', count() FROM supplier
FORMAT TSVWithNames;

-- Storage per table (active parts; a high part count means merges are still running)
SELECT table,
       sum(rows) AS rows,
       count() AS parts,
       intDiv(sum(bytes_on_disk), 1048576) AS size_mib,
       intDiv(sum(data_uncompressed_bytes), 1048576) AS uncompressed_mib
FROM system.parts
WHERE active AND database = currentDatabase()
GROUP BY table
ORDER BY size_mib DESC
FORMAT TSVWithNames;
