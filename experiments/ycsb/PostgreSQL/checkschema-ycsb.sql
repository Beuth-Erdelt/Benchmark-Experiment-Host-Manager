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



