-- Benchmark-Experiment-Host-Manager | experiments/ycsb/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Post-load maintenance and statistics collection for the YCSB
--          usertable on PostgreSQL. Runs a checkpoint, collects vacuum and
--          table statistics, and reports database session metadata.

CHECKPOINT;

SELECT * FROM pg_stat_bgwriter;

VACUUM ANALYZE usertable;

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

SELECT current_database(), current_user, current_schema();

SHOW search_path;
