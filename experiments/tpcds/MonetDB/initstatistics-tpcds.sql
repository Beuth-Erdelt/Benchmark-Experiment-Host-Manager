-- Analyzing all TPC-DS tables

ANALYZE sys.call_center;
ANALYZE sys.catalog_page;
ANALYZE sys.catalog_returns;
ANALYZE sys.catalog_sales;
ANALYZE sys.customer;
ANALYZE sys.customer_address;
ANALYZE sys.customer_demographics;
ANALYZE sys.date_dim;
ANALYZE sys.dbgen_version;
ANALYZE sys.household_demographics;
ANALYZE sys.income_band;
ANALYZE sys.inventory;
ANALYZE sys.item;
ANALYZE sys.promotion;
ANALYZE sys.reason;
ANALYZE sys.ship_mode;
ANALYZE sys.store;
ANALYZE sys.store_returns;
ANALYZE sys.store_sales;
ANALYZE sys.time_dim;
ANALYZE sys.warehouse;
ANALYZE sys.web_page;
ANALYZE sys.web_returns;
ANALYZE sys.web_sales;
ANALYZE sys.web_site;

SELECT CURRENT_SCHEMA;
