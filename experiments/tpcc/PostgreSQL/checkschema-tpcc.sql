-- Benchmark-Experiment-Host-Manager | experiments/tpcc/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Post-load maintenance and statistics collection for the TPC-C
--          schema on PostgreSQL. Runs a checkpoint, VACUUM ANALYZE on all
--          TPC-C tables, and reports settings, vacuum/table statistics,
--          table sizes and database session metadata.
--          bexhoma runs this script against the default database (postgres),
--          but HammerDB loads TPC-C into database tpcc (pg_dbase in
--          images/hammerdb/generator/generator.sh), so switch there first.

\connect tpcc

CHECKPOINT;

SELECT * FROM pg_stat_bgwriter;

VACUUM ANALYZE customer;
VACUUM ANALYZE district;
VACUUM ANALYZE history;
VACUUM ANALYZE warehouse;
VACUUM ANALYZE stock;
VACUUM ANALYZE new_order;
VACUUM ANALYZE orders;
VACUUM ANALYZE order_line;
VACUUM ANALYZE item;

SELECT name, setting FROM pg_settings WHERE source != 'default';

SELECT relname, last_autovacuum, n_dead_tup
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC
LIMIT 10;

SELECT relname, last_analyze, n_live_tup
FROM pg_stat_user_tables
ORDER BY last_analyze NULLS FIRST;

SELECT relname, n_dead_tup, n_live_tup
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;

SELECT relname,
       pg_size_pretty(pg_table_size(relid))          AS table_size,
       pg_size_pretty(pg_indexes_size(relid))        AS indexes_size,
       pg_size_pretty(pg_total_relation_size(relid)) AS total_size
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(relid) DESC;

SELECT pg_size_pretty(pg_database_size(current_database())) AS database_size;

SELECT current_database(), current_user, current_schema();

SHOW search_path;
