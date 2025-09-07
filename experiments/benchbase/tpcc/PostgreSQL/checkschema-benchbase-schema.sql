CHECKPOINT;

SELECT * FROM pg_stat_bgwriter;


VACUUM ANALYZE {BEXHOMA_SCHEMA}.customer;
VACUUM ANALYZE {BEXHOMA_SCHEMA}.district;
VACUUM ANALYZE {BEXHOMA_SCHEMA}.history;
VACUUM ANALYZE {BEXHOMA_SCHEMA}.warehouse;
VACUUM ANALYZE {BEXHOMA_SCHEMA}.stock;
VACUUM ANALYZE {BEXHOMA_SCHEMA}.new_order;
VACUUM ANALYZE {BEXHOMA_SCHEMA}.oorder;
VACUUM ANALYZE {BEXHOMA_SCHEMA}.order_line;
VACUUM ANALYZE {BEXHOMA_SCHEMA}.item;

SELECT COUNT(*) AS "count warehouses" FROM {BEXHOMA_SCHEMA}.warehouse;


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



