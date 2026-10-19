-- Benchmark-Experiment-Host-Manager | experiments/tpcds/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Step 1 (statistics) of the reset contract (docs/DBMS.md) for
--          TPC-DS on MySQL, run before each benchmarking round with -ar.
--          ANALYZE TABLE refreshes optimizer statistics on every TPC-DS table.
--          Steps 2 (persist) and 3 (counters) follow in reset-flush.sh.

ANALYZE TABLE tpcds.call_center;
ANALYZE TABLE tpcds.catalog_page;
ANALYZE TABLE tpcds.catalog_returns;
ANALYZE TABLE tpcds.catalog_sales;
ANALYZE TABLE tpcds.customer;
ANALYZE TABLE tpcds.customer_address;
ANALYZE TABLE tpcds.customer_demographics;
ANALYZE TABLE tpcds.date_dim;
ANALYZE TABLE tpcds.dbgen_version;
ANALYZE TABLE tpcds.household_demographics;
ANALYZE TABLE tpcds.income_band;
ANALYZE TABLE tpcds.inventory;
ANALYZE TABLE tpcds.item;
ANALYZE TABLE tpcds.promotion;
ANALYZE TABLE tpcds.reason;
ANALYZE TABLE tpcds.ship_mode;
ANALYZE TABLE tpcds.store;
ANALYZE TABLE tpcds.store_returns;
ANALYZE TABLE tpcds.store_sales;
ANALYZE TABLE tpcds.time_dim;
ANALYZE TABLE tpcds.warehouse;
ANALYZE TABLE tpcds.web_page;
ANALYZE TABLE tpcds.web_returns;
ANALYZE TABLE tpcds.web_sales;
ANALYZE TABLE tpcds.web_site;
