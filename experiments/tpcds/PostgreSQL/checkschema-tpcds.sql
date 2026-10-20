-- Benchmark-Experiment-Host-Manager | experiments/tpcds/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Last post-load script, always run (also without -xii/-xic/-xis).
--          Writes a checkpoint and reports row counts, sizes, the WAL written
--          so far and the non-default configuration. Load settings (-xld) are
--          restored before, by restoredurability-*.sql.
--          The planner settings of initschema-tpcds.sql are meant for the
--          queries and stay. No VACUUM/ANALYZE here (initstatistics-tpcds.sql).
--          No curly braces in this file: bexhoma may fill it with str.format().

SHOW synchronous_commit;

-- Persist the loaded data now, not during the first queries
CHECKPOINT;

-- Row counts per table (exact counts)
SELECT table_schema,
       table_name,
       (xpath('/row/c/text()',
              query_to_xml(format('SELECT count(*) AS c FROM %I.%I', table_schema, table_name),
                           false, true, '')))[1]::text::bigint AS row_count
FROM information_schema.tables
WHERE table_type = 'BASE TABLE'
  AND table_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY table_schema, table_name;

-- Sizes
SELECT schemaname, relname,
       pg_size_pretty(pg_table_size(relid))          AS table_size,
       pg_size_pretty(pg_indexes_size(relid))        AS indexes_size,
       pg_size_pretty(pg_total_relation_size(relid)) AS total_size
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(relid) DESC;

SELECT pg_size_pretty(pg_database_size(current_database())) AS database_size;

-- WAL written since the statistics reset (server start), i.e. mostly by the load
SELECT wal_records, wal_fpi, pg_size_pretty(wal_bytes) AS wal_bytes, stats_reset FROM pg_stat_wal;

-- Configuration that differs from the compiled defaults
SELECT name, setting, unit, source FROM pg_settings
WHERE source NOT IN ('default', 'override')
ORDER BY name;
