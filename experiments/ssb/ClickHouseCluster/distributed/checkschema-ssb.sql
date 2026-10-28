-- Benchmark-Experiment-Host-Manager | experiments/ssb/ClickHouseCluster/distributed
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Last post-load script, always run (also without -xii/-xic/-xis), for
--          Distributed dimensions (-xdim distributed). Reports row counts and
--          storage per table summed over all shards, then per shard (active parts
--          of the <name>_local tables; a high part count means merges are still
--          running). ClickHouse's init scripts relax no setting, so nothing is restored.
--          No curly braces in this file: bexhoma may fill it with str.format().

SYSTEM FLUSH DISTRIBUTED customer;
SYSTEM FLUSH DISTRIBUTED supplier;
SYSTEM FLUSH DISTRIBUTED part;
SYSTEM FLUSH DISTRIBUTED dates;
SYSTEM FLUSH DISTRIBUTED lineorder;

SELECT replaceRegexpOne(table, '_local$', '') AS table_name,
       sum(rows) AS rows,
       count() AS parts,
       intDiv(sum(bytes_on_disk), 1048576) AS size_mib,
       intDiv(sum(data_uncompressed_bytes), 1048576) AS uncompressed_mib
FROM clusterAllReplicas(bexhoma, system.parts)
WHERE active AND database = currentDatabase()
GROUP BY table_name
ORDER BY table_name
FORMAT TSVWithNames;

SELECT hostName() AS shard,
       sum(rows) AS rows,
       count() AS parts,
       intDiv(sum(bytes_on_disk), 1048576) AS size_mib
FROM clusterAllReplicas(bexhoma, system.parts)
WHERE active AND database = currentDatabase()
GROUP BY shard
ORDER BY shard
FORMAT TSVWithNames;
