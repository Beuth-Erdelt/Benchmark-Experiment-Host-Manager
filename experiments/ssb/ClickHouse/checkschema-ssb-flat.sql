-- Benchmark-Experiment-Host-Manager | experiments/ssb/ClickHouse
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Last post-load script of the flat variant (-xsv flat), always run.
--          Reports row count and storage size of lineorder_flat.
--          No curly braces in this file: bexhoma may fill it with str.format().

-- Row count (exact; for reference: SF 10 = 59,986,052)
SELECT 'lineorder_flat' AS table_name, count() AS row_count FROM lineorder_flat
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
