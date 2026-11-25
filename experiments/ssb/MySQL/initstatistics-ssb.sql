-- Benchmark-Experiment-Host-Manager | experiments/ssb/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Collect table statistics after data loading (-xis).

ANALYZE TABLE ssb.customer;
ANALYZE TABLE ssb.supplier;
ANALYZE TABLE ssb.part;
ANALYZE TABLE ssb.dates;
ANALYZE TABLE ssb.lineorder;

-- Histograms are the DDL parameter histograms (ddl-parameters.config): with off, the lines
-- below start with a comment mark
{histograms}ANALYZE TABLE ssb.customer UPDATE HISTOGRAM ON c_name, c_address, c_city, c_nation, c_region, c_phone, c_mktsegment WITH 100 BUCKETS;
{histograms}ANALYZE TABLE ssb.supplier UPDATE HISTOGRAM ON s_name, s_address, s_city, s_nation, s_region, s_phone WITH 100 BUCKETS;
{histograms}ANALYZE TABLE ssb.part UPDATE HISTOGRAM ON p_name, p_mfgr, p_category, p_brand1, p_color, p_type, p_size, p_container WITH 100 BUCKETS;
{histograms}ANALYZE TABLE ssb.dates UPDATE HISTOGRAM ON d_date, d_dayofweek, d_month, d_year, d_yearmonthnum, d_yearmonth, d_daynuminweek, d_daynuminmonth, d_daynuminyear, d_monthnuminyear, d_weeknuminyear, d_sellingseason, d_lastdayinweekfl, d_lastdayinmonthfl, d_holidayfl, d_weekdayfl WITH 100 BUCKETS;
{histograms}ANALYZE TABLE ssb.lineorder UPDATE HISTOGRAM ON lo_custkey, lo_partkey, lo_suppkey, lo_orderdate, lo_orderpriority, lo_shippriority, lo_quantity, lo_extendedprice, lo_ordtotalprice, lo_discount, lo_revenue, lo_supplycost, lo_tax, lo_commitdate, lo_shipmode WITH 100 BUCKETS;
