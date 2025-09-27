-- Analyzing all TPC-DS tables

ANALYZE VERBOSE public.call_center;
ANALYZE VERBOSE public.catalog_page;
ANALYZE VERBOSE public.catalog_returns;
ANALYZE VERBOSE public.catalog_sales;
ANALYZE VERBOSE public.customer;
ANALYZE VERBOSE public.customer_address;
ANALYZE VERBOSE public.customer_demographics;
ANALYZE VERBOSE public.date_dim;
ANALYZE VERBOSE public.dbgen_version;
ANALYZE VERBOSE public.household_demographics;
ANALYZE VERBOSE public.income_band;
ANALYZE VERBOSE public.inventory;
ANALYZE VERBOSE public.item;
ANALYZE VERBOSE public.promotion;
ANALYZE VERBOSE public.reason;
ANALYZE VERBOSE public.ship_mode;
ANALYZE VERBOSE public.store;
ANALYZE VERBOSE public.store_returns;
ANALYZE VERBOSE public.store_sales;
ANALYZE VERBOSE public.time_dim;
ANALYZE VERBOSE public.warehouse;
ANALYZE VERBOSE public.web_page;
ANALYZE VERBOSE public.web_returns;
ANALYZE VERBOSE public.web_sales;
ANALYZE VERBOSE public.web_site;

ALTER SYSTEM SET synchronous_commit = on;
-- ALTER SYSTEM SET fsync = on;
SELECT pg_reload_conf();
