-- Benchmark-Experiment-Host-Manager | experiments/tpcds/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Collect planner statistics for all TPC-DS tables and re-enable
--          synchronous_commit (disabled during bulk loading in initschema).

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
SELECT pg_reload_conf();
