-- Benchmark-Experiment-Host-Manager | experiments/ssb/ClickHouse
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create the denormalized SSB table lineorder_flat (-xsv flat) in
--          ClickHouse (database default): the 17 lineorder columns, then all
--          customer, supplier and part columns without their keys, in the column
--          order the generator writes (images/ssb/generator/flat.awk). Sorting
--          key and partitioning by year as in the ClickHouse SSB docs.
--          No curly braces in this file: bexhoma may fill it with str.format().

CREATE TABLE lineorder_flat (
    lo_orderkey         Int64,
    lo_linenumber       Int32,
    lo_custkey          Int32,
    lo_partkey          Int32,
    lo_suppkey          Int32,
    lo_orderdate        Date,
    lo_orderpriority    String,
    lo_shippriority     String,
    lo_quantity         Int32,
    lo_extendedprice    Int32,
    lo_ordtotalprice    Int32,
    lo_discount         Int32,
    lo_revenue          Int32,
    lo_supplycost       Int32,
    lo_tax              Int32,
    lo_commitdate       Date,
    lo_shipmode         String,
    c_name              String,
    c_address           String,
    c_city              String,
    c_nation            String,
    c_region            String,
    c_phone             String,
    c_mktsegment        String,
    s_name              String,
    s_address           String,
    s_city              String,
    s_nation            String,
    s_region            String,
    s_phone             String,
    p_name              String,
    p_mfgr              String,
    p_category          String,
    p_brand1            String,
    p_color             String,
    p_type              String,
    p_size              Int32,
    p_container         String
) ENGINE = MergeTree
PARTITION BY toYear(lo_orderdate)
ORDER BY (lo_orderdate, lo_orderkey);
