COPY call_center FROM '/data/tpcds/SF30/call_center.dat' delimiter '|' null '';
COPY catalog_page FROM '/data/tpcds/SF30/catalog_page.dat' delimiter '|' null '';
COPY catalog_returns FROM '/data/tpcds/SF30/catalog_returns.dat' delimiter '|' null '';
COPY catalog_sales FROM '/data/tpcds/SF30/catalog_sales.dat' delimiter '|' null '';
COPY customer FROM '/data/tpcds/SF30/customer.dat' delimiter '|' null '';
COPY customer_address FROM '/data/tpcds/SF30/customer_address.dat' delimiter '|' null '';
COPY customer_demographics FROM '/data/tpcds/SF30/customer_demographics.dat' delimiter '|' null '';
COPY date_dim FROM '/data/tpcds/SF30/date_dim.dat' delimiter '|' null '';
COPY dbgen_version FROM '/data/tpcds/SF30/dbgen_version.dat' delimiter '|' null '';
COPY household_demographics FROM '/data/tpcds/SF30/household_demographics.dat' delimiter '|' null '';
COPY income_band FROM '/data/tpcds/SF30/income_band.dat' delimiter '|' null '';
COPY inventory FROM '/data/tpcds/SF30/inventory.dat' delimiter '|' null '';
COPY item FROM '/data/tpcds/SF30/item.dat' delimiter '|' null '';
COPY promotion FROM '/data/tpcds/SF30/promotion.dat' delimiter '|' null '';
COPY reason FROM '/data/tpcds/SF30/reason.dat' delimiter '|' null '';
COPY ship_mode FROM '/data/tpcds/SF30/ship_mode.dat' delimiter '|' null '';
COPY store FROM '/data/tpcds/SF30/store.dat' delimiter '|' null '';
COPY store_returns FROM '/data/tpcds/SF30/store_returns.dat' delimiter '|' null '';
COPY store_sales FROM '/data/tpcds/SF30/store_sales.dat' delimiter '|' null '';
COPY time_dim FROM '/data/tpcds/SF30/time_dim.dat' delimiter '|' null '';
COPY warehouse FROM '/data/tpcds/SF30/warehouse.dat' delimiter '|' null '';
COPY web_page FROM '/data/tpcds/SF30/web_page.dat' delimiter '|' null '';
COPY web_returns FROM '/data/tpcds/SF30/web_returns.dat' delimiter '|' null '';
COPY web_sales FROM '/data/tpcds/SF30/web_sales.dat' delimiter '|' null '';
COPY web_site FROM '/data/tpcds/SF30/web_site.dat' delimiter '|' null '';


-- rebalance the shards over the new worker nodes
SELECT get_rebalance_table_shards_plan();
SELECT rebalance_table_shards();

SELECT * FROM pg_dist_shard_placement;
