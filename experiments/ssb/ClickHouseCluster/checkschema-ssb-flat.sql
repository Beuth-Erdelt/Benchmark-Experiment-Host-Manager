-- Benchmark-Experiment-Host-Manager | experiments/ssb/ClickHouseCluster
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Last post-load script of -xsv flat, always run (also without
--          -xii/-xis). Reports the row count of lineorder_flat summed over all
--          shards, then rows and storage per shard (active parts of
--          lineorder_flat_local; a high part count means merges are still running).
--          ClickHouse's init scripts relax no setting, so nothing is restored.
--          No curly braces in this file: bexhoma may fill it with str.format().

SYSTEM FLUSH DISTRIBUTED lineorder_flat;

SELECT 'lineorder_flat' AS table_name, count() AS row_count FROM lineorder_flat
FORMAT TSVWithNames;

SELECT hostName() AS shard,
       sum(rows) AS rows,
       count() AS parts,
       intDiv(sum(bytes_on_disk), 1048576) AS size_mib,
       intDiv(sum(data_uncompressed_bytes), 1048576) AS uncompressed_mib
FROM clusterAllReplicas(bexhoma, system.parts)
WHERE active AND database = currentDatabase() AND table = 'lineorder_flat_local'
GROUP BY shard
ORDER BY shard
FORMAT TSVWithNames;
