-- ANALYZE: Update table statistics for the optimizer
ANALYZE TABLE customer;
ANALYZE TABLE district;
ANALYZE TABLE history;
ANALYZE TABLE warehouse;
ANALYZE TABLE stock;
ANALYZE TABLE new_order;
ANALYZE TABLE oorder;
ANALYZE TABLE order_line;
ANALYZE TABLE item;

-- OPTIMIZE (Optional): Reclaim disk space and defragment InnoDB tables
-- Uncomment if you suspect high fragmentation or heavy deletes
-- OPTIMIZE TABLE customer;
-- OPTIMIZE TABLE district;
-- OPTIMIZE TABLE history;
-- OPTIMIZE TABLE warehouse;
-- OPTIMIZE TABLE stock;
-- OPTIMIZE TABLE new_order;
-- OPTIMIZE TABLE oorder;
-- OPTIMIZE TABLE order_line;
-- OPTIMIZE TABLE item;

-- Count number of warehouses
SELECT COUNT(*) AS `count warehouses` FROM warehouse;

-- Show non-default global MySQL configuration variables (approximate)
-- NOTE: MySQL does not track source of values like PostgreSQL
SHOW GLOBAL VARIABLES;

-- Table statistics: estimated row counts and last update time
SELECT 
  TABLE_NAME AS table_name,
  ENGINE,
  TABLE_ROWS AS approx_row_count,
  UPDATE_TIME AS last_update
FROM information_schema.tables
-- WHERE table_schema = 'BEXHOMA_SCHEMA'
ORDER BY TABLE_ROWS DESC
LIMIT 10;

-- Show current database and user
SELECT 
  DATABASE() AS current_database,
  USER() AS current_user;

-- Optional: show table status for deeper insights (includes size info)
SHOW TABLE STATUS -- FROM BEXHOMA_SCHEMA
;
