COPY INTO call_center FROM '/data/tpcds/SF10/call_center.dat' DELIMITERS '|' NULL AS '';
COPY INTO catalog_page FROM '/data/tpcds/SF10/catalog_page.dat' DELIMITERS '|' NULL AS '';
COPY INTO catalog_returns FROM '/data/tpcds/SF10/catalog_returns.dat' DELIMITERS '|' NULL AS '';
COPY INTO catalog_sales FROM '/data/tpcds/SF10/catalog_sales.dat' DELIMITERS '|' NULL AS '';
COPY INTO customer FROM '/data/tpcds/SF10/customer.dat' DELIMITERS '|' NULL AS '';
COPY INTO customer_address FROM '/data/tpcds/SF10/customer_address.dat' DELIMITERS '|' NULL AS '';
COPY INTO customer_demographics FROM '/data/tpcds/SF10/customer_demographics.dat' DELIMITERS '|' NULL AS '';
COPY INTO date_dim FROM '/data/tpcds/SF10/date_dim.dat' DELIMITERS '|' NULL AS '';
COPY INTO dbgen_version FROM '/data/tpcds/SF10/dbgen_version.dat' DELIMITERS '|' NULL AS '';
COPY INTO household_demographics FROM '/data/tpcds/SF10/household_demographics.dat' DELIMITERS '|' NULL AS '';
COPY INTO income_band FROM '/data/tpcds/SF10/income_band.dat' DELIMITERS '|' NULL AS '';
COPY INTO inventory FROM '/data/tpcds/SF10/inventory.dat' DELIMITERS '|' NULL AS '';
COPY INTO item FROM '/data/tpcds/SF10/item.dat' DELIMITERS '|' NULL AS '';
COPY INTO promotion FROM '/data/tpcds/SF10/promotion.dat' DELIMITERS '|' NULL AS '';
COPY INTO reason FROM '/data/tpcds/SF10/reason.dat' DELIMITERS '|' NULL AS '';
COPY INTO ship_mode FROM '/data/tpcds/SF10/ship_mode.dat' DELIMITERS '|' NULL AS '';
COPY INTO store FROM '/data/tpcds/SF10/store.dat' DELIMITERS '|' NULL AS '';
COPY INTO store_returns FROM '/data/tpcds/SF10/store_returns.dat' DELIMITERS '|' NULL AS '';
COPY INTO store_sales FROM '/data/tpcds/SF10/store_sales.dat' DELIMITERS '|' NULL AS '';
COPY INTO time_dim FROM '/data/tpcds/SF10/time_dim.dat' DELIMITERS '|' NULL AS '';
COPY INTO warehouse FROM '/data/tpcds/SF10/warehouse.dat' DELIMITERS '|' NULL AS '';
COPY INTO web_page FROM '/data/tpcds/SF10/web_page.dat' DELIMITERS '|' NULL AS '';
COPY INTO web_returns FROM '/data/tpcds/SF10/web_returns.dat' DELIMITERS '|' NULL AS '';
COPY INTO web_sales FROM '/data/tpcds/SF10/web_sales.dat' DELIMITERS '|' NULL AS '';
COPY INTO web_site FROM '/data/tpcds/SF10/web_site.dat' DELIMITERS '|' NULL AS '';
