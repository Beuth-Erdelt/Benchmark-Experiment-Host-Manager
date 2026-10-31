-- Benchmark-Experiment-Host-Manager | experiments/benchbase/ycsb/CedarDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Post-load report for the benchbase YCSB schema on CedarDB:
--          statistics, table, index and total sizes of all user tables.
--          No CHECKPOINT in CedarDB.

ANALYZE;

-- Sizes
SELECT schemaname, relname,
       pg_size_pretty(pg_table_size(relid))          AS table_size,
       pg_size_pretty(pg_indexes_size(relid))        AS indexes_size,
       pg_size_pretty(pg_total_relation_size(relid)) AS total_size
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(relid) DESC;

SELECT pg_size_pretty(pg_database_size(current_database())) AS database_size;
