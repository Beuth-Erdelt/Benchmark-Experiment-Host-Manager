ANALYZE VERBOSE customer;
ANALYZE VERBOSE lineitem;
ANALYZE VERBOSE nation;
ANALYZE VERBOSE orders;
ANALYZE VERBOSE part;
ANALYZE VERBOSE partsupp;
ANALYZE VERBOSE region;
ANALYZE VERBOSE supplier;

SELECT COUNT(*) AS "count nation" FROM nation;
SELECT COUNT(*) AS "count region" FROM region;

SELECT logicalrelid AS name,
       pg_size_pretty(citus_table_size(logicalrelid)) AS size
FROM pg_dist_partition;
