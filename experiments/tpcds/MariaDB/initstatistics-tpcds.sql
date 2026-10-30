-- Benchmark-Experiment-Host-Manager | experiments/tpcds/MariaDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Collect optimizer statistics for all TPC-DS tables in MariaDB.
--          Run after initindexes-tpcds.sql.

-- Histograms (PERSISTENT FOR ALL) are the DDL parameter histograms (ddl-parameters.config)
ANALYZE TABLE tpcds.call_center {histograms};
ANALYZE TABLE tpcds.catalog_page {histograms};
ANALYZE TABLE tpcds.catalog_returns {histograms};
ANALYZE TABLE tpcds.catalog_sales {histograms};
ANALYZE TABLE tpcds.customer {histograms};
ANALYZE TABLE tpcds.customer_address {histograms};
ANALYZE TABLE tpcds.customer_demographics {histograms};
ANALYZE TABLE tpcds.date_dim {histograms};
ANALYZE TABLE tpcds.dbgen_version {histograms};
ANALYZE TABLE tpcds.household_demographics {histograms};
ANALYZE TABLE tpcds.income_band {histograms};
ANALYZE TABLE tpcds.inventory {histograms};
ANALYZE TABLE tpcds.item {histograms};
ANALYZE TABLE tpcds.promotion {histograms};
ANALYZE TABLE tpcds.reason {histograms};
ANALYZE TABLE tpcds.ship_mode {histograms};
ANALYZE TABLE tpcds.store {histograms};
ANALYZE TABLE tpcds.store_returns {histograms};
ANALYZE TABLE tpcds.store_sales {histograms};
ANALYZE TABLE tpcds.time_dim {histograms};
ANALYZE TABLE tpcds.warehouse {histograms};
ANALYZE TABLE tpcds.web_page {histograms};
ANALYZE TABLE tpcds.web_returns {histograms};
ANALYZE TABLE tpcds.web_sales {histograms};
ANALYZE TABLE tpcds.web_site {histograms};
