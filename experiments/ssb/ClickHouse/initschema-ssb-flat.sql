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

CREATE TABLE lineorder_flat (
    lo_orderkey         Int64{codec},
    lo_linenumber       Int32{codec},
    lo_custkey          Int32{codec},
    lo_partkey          Int32{codec},
    lo_suppkey          Int32{codec},
    lo_orderdate        Date{codec},
    lo_orderpriority    {low_cardinality}{codec},
    lo_shippriority     {low_cardinality}{codec},
    lo_quantity         Int32{codec},
    lo_extendedprice    Int32{codec},
    lo_ordtotalprice    Int32{codec},
    lo_discount         Int32{codec},
    lo_revenue          Int32{codec},
    lo_supplycost       Int32{codec},
    lo_tax              Int32{codec},
    lo_commitdate       Date{codec},
    lo_shipmode         {low_cardinality}{codec},
    c_name              String{codec},
    c_address           String{codec},
    c_city              {low_cardinality}{codec},
    c_nation            {low_cardinality}{codec},
    c_region            {low_cardinality}{codec},
    c_phone             String{codec},
    c_mktsegment        {low_cardinality}{codec},
    s_name              String{codec},
    s_address           String{codec},
    s_city              {low_cardinality}{codec},
    s_nation            {low_cardinality}{codec},
    s_region            {low_cardinality}{codec},
    s_phone             String{codec},
    p_name              String{codec},
    p_mfgr              {low_cardinality}{codec},
    p_category          {low_cardinality}{codec},
    p_brand1            {low_cardinality}{codec},
    p_color             {low_cardinality}{codec},
    p_type              {low_cardinality}{codec},
    p_size              Int32{codec},
    p_container         {low_cardinality}{codec}
) ENGINE = MergeTree
PARTITION BY toYear(lo_orderdate)
ORDER BY {order_lineorder}
    SETTINGS index_granularity = {index_granularity}, min_bytes_for_wide_part = {wide_parts};
