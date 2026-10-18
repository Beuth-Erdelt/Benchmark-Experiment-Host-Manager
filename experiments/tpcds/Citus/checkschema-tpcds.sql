-- Benchmark-Experiment-Host-Manager | experiments/tpcds/Citus
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Last post-load script, always run (also without -xii/-xic/-xis).
--          Writes a checkpoint on the coordinator and all workers, and reports
--          row counts, sizes, the distribution, the WAL written so far and the
--          non-default configuration. The citus.* settings of initschema-tpcds.sql
--          are meant for the queries and stay.
--          No curly braces in this file: bexhoma may fill it with str.format().

-- Persist the loaded data now, not during the first queries
CHECKPOINT;
SELECT nodename, success, result FROM run_command_on_workers('CHECKPOINT');

-- Row counts per table (exact counts)
SELECT table_schema,
       table_name,
       (xpath('/row/c/text()',
              query_to_xml(format('SELECT count(*) AS c FROM %I.%I', table_schema, table_name),
                           false, true, '')))[1]::text::bigint AS row_count
FROM information_schema.tables
WHERE table_type = 'BASE TABLE'
  AND table_schema NOT IN ('pg_catalog', 'information_schema', 'citus', 'citus_internal',
                           'columnar', 'columnar_internal')
ORDER BY table_schema, table_name;

-- Sizes and distribution
SELECT table_name, citus_table_type, distribution_column, shard_count, table_size
FROM citus_tables
ORDER BY table_name;

SELECT nodename, nodeport, count(*) AS shards, pg_size_pretty(sum(shard_size)) AS size
FROM citus_shards
GROUP BY nodename, nodeport
ORDER BY nodename, nodeport;

-- WAL written since the statistics reset (server start), i.e. mostly by the load
SELECT wal_records, wal_fpi, pg_size_pretty(wal_bytes) AS wal_bytes, stats_reset FROM pg_stat_wal;
SELECT nodename, success, result AS wal_bytes
FROM run_command_on_workers('SELECT pg_size_pretty(wal_bytes) FROM pg_stat_wal');

-- Configuration that differs from the compiled defaults (coordinator)
SELECT name, setting, unit, source FROM pg_settings
WHERE source NOT IN ('default', 'override')
ORDER BY name;
