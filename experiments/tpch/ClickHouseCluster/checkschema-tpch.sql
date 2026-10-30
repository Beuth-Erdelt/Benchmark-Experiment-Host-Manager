-- Benchmark-Experiment-Host-Manager | experiments/tpch/ClickHouseCluster
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Last post-load script, always run (also without -xii/-xic/-xis), for
--          replicated dimensions (-xdim replicated). Sends the rows the
--          Distributed tables still hold, waits until every shard has fetched
--          the dimension parts from the coordinator, fails if a node holds other
--          rows of a dimension than the coordinator, then reports row counts and
--          storage per table and node. ClickHouse's init scripts relax no
--          setting, so nothing is restored.
--          No curly braces in this file: bexhoma may fill it with str.format().

SYSTEM FLUSH DISTRIBUTED orders;
SYSTEM FLUSH DISTRIBUTED lineitem;
SYSTEM SYNC REPLICA ON CLUSTER bexhoma nation;
SYSTEM SYNC REPLICA ON CLUSTER bexhoma region;
SYSTEM SYNC REPLICA ON CLUSTER bexhoma part;
SYSTEM SYNC REPLICA ON CLUSTER bexhoma supplier;
SYSTEM SYNC REPLICA ON CLUSTER bexhoma partsupp;
SYSTEM SYNC REPLICA ON CLUSTER bexhoma customer;

-- Row counts per table (orders, lineitem summed over the shards, dimensions: the coordinator's copy)
SELECT 'customer' AS table_name, count() AS row_count FROM customer
UNION ALL SELECT 'lineitem', count() FROM lineitem
UNION ALL SELECT 'nation',   count() FROM nation
UNION ALL SELECT 'orders',   count() FROM orders
UNION ALL SELECT 'part',     count() FROM part
UNION ALL SELECT 'partsupp', count() FROM partsupp
UNION ALL SELECT 'region',   count() FROM region
UNION ALL SELECT 'supplier', count() FROM supplier
FORMAT TSVWithNames;

-- Storage per table and node (active parts; a high part count means merges are still running)
SELECT table, node, rows, parts, size_mib
FROM (
    SELECT table, hostName() AS node, sum(rows) AS rows, count() AS parts,
           intDiv(sum(bytes_on_disk), 1048576) AS size_mib
    FROM clusterAllReplicas(bexhoma, system.parts)
    WHERE active AND database = currentDatabase()
    GROUP BY table, node
    UNION ALL
    SELECT table, 'coordinator', sum(rows), count(), intDiv(sum(bytes_on_disk), 1048576)
    FROM system.parts
    WHERE active AND database = currentDatabase()
    GROUP BY table
)
ORDER BY table, node
FORMAT TSVWithNames;

-- Every node (all shards and the coordinator) holds the same rows of each dimension (else: error)
SELECT table, count() AS nodes,
       throwIf(count() != (SELECT count() FROM system.clusters WHERE cluster = 'bexhoma') + 1
               OR min(rows) != max(rows), 'a replica of a dimension is missing or differs') AS replicas_differ
FROM (
    SELECT table, hostName() AS node, sum(rows) AS rows
    FROM clusterAllReplicas(bexhoma, system.parts)
    WHERE active AND database = currentDatabase()
      AND table IN ('nation', 'region', 'part', 'supplier', 'partsupp', 'customer')
    GROUP BY table, node
    UNION ALL
    SELECT table, 'coordinator', sum(rows)
    FROM system.parts
    WHERE active AND database = currentDatabase()
      AND table IN ('nation', 'region', 'part', 'supplier', 'partsupp', 'customer')
    GROUP BY table
)
GROUP BY table
ORDER BY table
FORMAT TSVWithNames;
