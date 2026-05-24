-- Benchmark-Experiment-Host-Manager | experiments/tpcds/DB2
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load TPC-DS scale factor 10 data into DB2. See
--          initdata-tpcds-SF1.sql for format details.

CONNECT TO testdb USER db2inst1 USING root1234ROOT;
IMPORT FROM "/data/tpcds/SF10/call_center.dat"           OF DEL MODIFIED BY coldel| INSERT INTO tpcds.call_center;
IMPORT FROM "/data/tpcds/SF10/catalog_page.dat"          OF DEL MODIFIED BY coldel| INSERT INTO tpcds.catalog_page;
IMPORT FROM "/data/tpcds/SF10/catalog_returns.dat"       OF DEL MODIFIED BY coldel| INSERT INTO tpcds.catalog_returns;
IMPORT FROM "/data/tpcds/SF10/catalog_sales.dat"         OF DEL MODIFIED BY coldel| INSERT INTO tpcds.catalog_sales;
IMPORT FROM "/data/tpcds/SF10/customer.dat"              OF DEL MODIFIED BY coldel| INSERT INTO tpcds.customer;
IMPORT FROM "/data/tpcds/SF10/customer_address.dat"      OF DEL MODIFIED BY coldel| INSERT INTO tpcds.customer_address;
IMPORT FROM "/data/tpcds/SF10/customer_demographics.dat" OF DEL MODIFIED BY coldel| INSERT INTO tpcds.customer_demographics;
IMPORT FROM "/data/tpcds/SF10/date_dim.dat"              OF DEL MODIFIED BY coldel| INSERT INTO tpcds.date_dim;
IMPORT FROM "/data/tpcds/SF10/dbgen_version.dat"         OF DEL MODIFIED BY coldel| INSERT INTO tpcds.dbgen_version;
IMPORT FROM "/data/tpcds/SF10/household_demographics.dat" OF DEL MODIFIED BY coldel| INSERT INTO tpcds.household_demographics;
IMPORT FROM "/data/tpcds/SF10/income_band.dat"           OF DEL MODIFIED BY coldel| INSERT INTO tpcds.income_band;
IMPORT FROM "/data/tpcds/SF10/inventory.dat"             OF DEL MODIFIED BY coldel| INSERT INTO tpcds.inventory;
IMPORT FROM "/data/tpcds/SF10/item.dat"                  OF DEL MODIFIED BY coldel| INSERT INTO tpcds.item;
IMPORT FROM "/data/tpcds/SF10/promotion.dat"             OF DEL MODIFIED BY coldel| INSERT INTO tpcds.promotion;
IMPORT FROM "/data/tpcds/SF10/reason.dat"                OF DEL MODIFIED BY coldel| INSERT INTO tpcds.reason;
IMPORT FROM "/data/tpcds/SF10/ship_mode.dat"             OF DEL MODIFIED BY coldel| INSERT INTO tpcds.ship_mode;
IMPORT FROM "/data/tpcds/SF10/store.dat"                 OF DEL MODIFIED BY coldel| INSERT INTO tpcds.store;
IMPORT FROM "/data/tpcds/SF10/store_returns.dat"         OF DEL MODIFIED BY coldel| INSERT INTO tpcds.store_returns;
IMPORT FROM "/data/tpcds/SF10/store_sales.dat"           OF DEL MODIFIED BY coldel| INSERT INTO tpcds.store_sales;
IMPORT FROM "/data/tpcds/SF10/time_dim.dat"              OF DEL MODIFIED BY coldel| INSERT INTO tpcds.time_dim;
IMPORT FROM "/data/tpcds/SF10/warehouse.dat"             OF DEL MODIFIED BY coldel| INSERT INTO tpcds.warehouse;
IMPORT FROM "/data/tpcds/SF10/web_page.dat"              OF DEL MODIFIED BY coldel| INSERT INTO tpcds.web_page;
IMPORT FROM "/data/tpcds/SF10/web_returns.dat"           OF DEL MODIFIED BY coldel| INSERT INTO tpcds.web_returns;
IMPORT FROM "/data/tpcds/SF10/web_sales.dat"             OF DEL MODIFIED BY coldel| INSERT INTO tpcds.web_sales;
IMPORT FROM "/data/tpcds/SF10/web_site.dat"              OF DEL MODIFIED BY coldel| INSERT INTO tpcds.web_site;
