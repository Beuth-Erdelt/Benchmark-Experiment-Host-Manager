-- Benchmark-Experiment-Host-Manager | experiments/benchbase/ycsb/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Report table, index, and total sizes for all user tables in the
--          YCSB schema on PostgreSQL.

SELECT
    schemaname || '.' || relname AS table_name,
    pg_size_pretty(pg_relation_size(schemaname || '.' || relname)) AS table_size,
    pg_size_pretty(pg_indexes_size(schemaname || '.' || relname)) AS index_size,
    pg_size_pretty(pg_total_relation_size(schemaname || '.' || relname)) AS total_size
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(schemaname || '.' || relname) DESC;
