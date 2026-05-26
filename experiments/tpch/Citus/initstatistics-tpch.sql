-- Benchmark-Experiment-Host-Manager | experiments/tpch/Citus
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Collect planner statistics for all TPC-H tables on Citus and verify
--          row counts. The citus_table_size query reports logical shard sizes
--          for all distributed and reference tables via pg_dist_partition.

ANALYZE VERBOSE customer;
ANALYZE VERBOSE lineitem;
ANALYZE VERBOSE nation;
ANALYZE VERBOSE orders;
ANALYZE VERBOSE part;
ANALYZE VERBOSE partsupp;
ANALYZE VERBOSE region;
ANALYZE VERBOSE supplier;

SELECT COUNT(*) AS count_nation FROM nation;
SELECT COUNT(*) AS count_region FROM region;

SELECT logicalrelid                                    AS name,
       pg_size_pretty(citus_table_size(logicalrelid)) AS size
FROM   pg_dist_partition;
