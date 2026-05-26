-- Benchmark-Experiment-Host-Manager | experiments/tpcds/Citus
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load TPC-DS scale factor 10 data into Citus tables using COPY FROM
--          with pipe delimiter. Run after initschema-tpcds.sql.

COPY call_center FROM '/data/tpcds/SF10/call_center.dat' DELIMITER '|' NULL '';
COPY catalog_page FROM '/data/tpcds/SF10/catalog_page.dat' DELIMITER '|' NULL '';
COPY catalog_returns FROM '/data/tpcds/SF10/catalog_returns.dat' DELIMITER '|' NULL '';
COPY catalog_sales FROM '/data/tpcds/SF10/catalog_sales.dat' DELIMITER '|' NULL '';
COPY customer FROM '/data/tpcds/SF10/customer.dat' DELIMITER '|' NULL '';
COPY customer_address FROM '/data/tpcds/SF10/customer_address.dat' DELIMITER '|' NULL '';
COPY customer_demographics FROM '/data/tpcds/SF10/customer_demographics.dat' DELIMITER '|' NULL '';
COPY date_dim FROM '/data/tpcds/SF10/date_dim.dat' DELIMITER '|' NULL '';
COPY dbgen_version FROM '/data/tpcds/SF10/dbgen_version.dat' DELIMITER '|' NULL '';
COPY household_demographics FROM '/data/tpcds/SF10/household_demographics.dat' DELIMITER '|' NULL '';
COPY income_band FROM '/data/tpcds/SF10/income_band.dat' DELIMITER '|' NULL '';
COPY inventory FROM '/data/tpcds/SF10/inventory.dat' DELIMITER '|' NULL '';
COPY item FROM '/data/tpcds/SF10/item.dat' DELIMITER '|' NULL '';
COPY promotion FROM '/data/tpcds/SF10/promotion.dat' DELIMITER '|' NULL '';
COPY reason FROM '/data/tpcds/SF10/reason.dat' DELIMITER '|' NULL '';
COPY ship_mode FROM '/data/tpcds/SF10/ship_mode.dat' DELIMITER '|' NULL '';
COPY store FROM '/data/tpcds/SF10/store.dat' DELIMITER '|' NULL '';
COPY store_returns FROM '/data/tpcds/SF10/store_returns.dat' DELIMITER '|' NULL '';
COPY store_sales FROM '/data/tpcds/SF10/store_sales.dat' DELIMITER '|' NULL '';
COPY time_dim FROM '/data/tpcds/SF10/time_dim.dat' DELIMITER '|' NULL '';
COPY warehouse FROM '/data/tpcds/SF10/warehouse.dat' DELIMITER '|' NULL '';
COPY web_page FROM '/data/tpcds/SF10/web_page.dat' DELIMITER '|' NULL '';
COPY web_returns FROM '/data/tpcds/SF10/web_returns.dat' DELIMITER '|' NULL '';
COPY web_sales FROM '/data/tpcds/SF10/web_sales.dat' DELIMITER '|' NULL '';
COPY web_site FROM '/data/tpcds/SF10/web_site.dat' DELIMITER '|' NULL '';

-- rebalance the shards over the new worker nodes
SELECT get_rebalance_table_shards_plan();
SELECT rebalance_table_shards();

SELECT * FROM pg_dist_shard_placement;
