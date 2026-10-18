-- Benchmark-Experiment-Host-Manager | experiments/tpch/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Last post-load script for schema-per-tenant TPC-H, run once per
--          tenant. Writes a checkpoint and reports row counts and sizes of
--          this tenant's schema.
--          {BEXHOMA_SCHEMA} is substituted at runtime by the Bexhoma framework.

CHECKPOINT;

-- Row counts per table of this tenant (exact counts)
SELECT table_schema,
       table_name,
       (xpath('/row/c/text()',
              query_to_xml(format('SELECT count(*) AS c FROM %I.%I', table_schema, table_name),
                           false, true, '')))[1]::text::bigint AS row_count
FROM information_schema.tables
WHERE table_type = 'BASE TABLE'
  AND table_schema = '{BEXHOMA_SCHEMA}'
ORDER BY table_name;

-- Sizes of this tenant's tables
SELECT schemaname, relname,
       pg_size_pretty(pg_table_size(relid))          AS table_size,
       pg_size_pretty(pg_indexes_size(relid))        AS indexes_size,
       pg_size_pretty(pg_total_relation_size(relid)) AS total_size
FROM pg_stat_user_tables
WHERE schemaname = '{BEXHOMA_SCHEMA}'
ORDER BY pg_total_relation_size(relid) DESC;
