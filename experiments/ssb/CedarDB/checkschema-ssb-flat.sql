-- Benchmark-Experiment-Host-Manager | experiments/ssb/CedarDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Last post-load script, always run (also without -xii/-xic/-xis).
--          Reports row counts and sizes. Not available in CedarDB, unlike the
--          PostgreSQL script: CHECKPOINT, query_to_xml (so the tables are
--          listed), pg_stat_wal, the source column of pg_settings. No
--          load settings to restore: -xld has no effect on CedarDB.
--          No curly braces in this file: bexhoma may fill it with str.format().

SHOW synchronous_commit;

-- Row counts per table (exact counts)
SELECT 'lineorder_flat' AS table_name, count(*) AS row_count FROM public.lineorder_flat;

-- Sizes
SELECT schemaname, relname,
       pg_size_pretty(pg_table_size(relid))          AS table_size,
       pg_size_pretty(pg_indexes_size(relid))        AS indexes_size,
       pg_size_pretty(pg_total_relation_size(relid)) AS total_size
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(relid) DESC;

SELECT pg_size_pretty(pg_database_size(current_database())) AS database_size;
