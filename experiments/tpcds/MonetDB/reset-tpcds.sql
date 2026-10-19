-- Benchmark-Experiment-Host-Manager | experiments/tpcds/MonetDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for TPC-DS on MonetDB, run before each
--          benchmarking round with -ar. Steps of the reset contract
--          (docs/DBMS.md): 1 statistics, 2 persist, 3 counters. ANALYZE
--          refreshes the column statistics; sys.flush_log() moves the changes
--          in the write-ahead log into the persistent BATs, so that work does
--          not fall into the measured round. Tables are in schema sys.

-- step 1 (statistics)
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

-- step 2 (persist)
CALL sys.flush_log();

-- step 3 (counters): n/a - MonetDB has no resettable cumulative activity counters
