-- Benchmark-Experiment-Host-Manager | experiments/ssb/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Collect statistics of lineorder_flat after data loading (-xis, -xsv flat).

ANALYZE TABLE ssb.lineorder_flat;

-- Histograms are the DDL parameter histograms (ddl-parameters.config): with off, the lines
-- below start with a comment mark
{histograms}ANALYZE TABLE ssb.lineorder_flat UPDATE HISTOGRAM ON lo_custkey, lo_partkey, lo_suppkey, lo_orderdate, lo_orderpriority, lo_shippriority, lo_quantity, lo_extendedprice, lo_ordtotalprice, lo_discount, lo_revenue, lo_supplycost, lo_tax, lo_commitdate, lo_shipmode, c_name, c_address, c_city, c_nation, c_region, c_phone, c_mktsegment, s_name, s_address, s_city, s_nation, s_region, s_phone, p_name, p_mfgr, p_category, p_brand1, p_color, p_type, p_size, p_container WITH 100 BUCKETS;
