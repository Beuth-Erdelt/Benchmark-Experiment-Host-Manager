-- Benchmark-Experiment-Host-Manager | experiments/ssb/ClickHouse
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create the SSB star schema (4 dimensions + lineorder) in ClickHouse
--          (database default). MergeTree needs a sorting key at creation: the
--          dimensions are sorted by their key, lineorder by (lo_orderdate,
--          lo_orderkey) as in the ClickHouse SSB docs. There are no secondary
--          indexes or constraints (-xii/-xic have no scripts). CHAR/VARCHAR are
--          String. lo_orderkey is Int64. The date dimension is named dates, as
--          for the other DBMS.

CREATE TABLE customer (
    c_custkey     Int32,
    c_name        String,
    c_address     String,
    c_city        {low_cardinality},
    c_nation      {low_cardinality},
    c_region      {low_cardinality},
    c_phone       String,
    c_mktsegment  {low_cardinality}
) ENGINE = MergeTree ORDER BY c_custkey;

CREATE TABLE supplier (
    s_suppkey  Int32,
    s_name     String,
    s_address  String,
    s_city     {low_cardinality},
    s_nation   {low_cardinality},
    s_region   {low_cardinality},
    s_phone    String
) ENGINE = MergeTree ORDER BY s_suppkey;

CREATE TABLE part (
    p_partkey    Int32,
    p_name       String,
    p_mfgr       {low_cardinality},
    p_category   {low_cardinality},
    p_brand1     {low_cardinality},
    p_color      {low_cardinality},
    p_type       {low_cardinality},
    p_size       Int32,
    p_container  {low_cardinality}
) ENGINE = MergeTree ORDER BY p_partkey;

CREATE TABLE dates (
    d_datekey           Int32,
    d_date              String,
    d_dayofweek         {low_cardinality},
    d_month             {low_cardinality},
    d_year              Int32,
    d_yearmonthnum      Int32,
    d_yearmonth         {low_cardinality},
    d_daynuminweek      Int32,
    d_daynuminmonth     Int32,
    d_daynuminyear      Int32,
    d_monthnuminyear    Int32,
    d_weeknuminyear     Int32,
    d_sellingseason     {low_cardinality},
    d_lastdayinweekfl   {low_cardinality},
    d_lastdayinmonthfl  {low_cardinality},
    d_holidayfl         {low_cardinality},
    d_weekdayfl         {low_cardinality}
) ENGINE = MergeTree ORDER BY d_datekey;

CREATE TABLE lineorder (
    lo_orderkey         Int64{codec},
    lo_linenumber       Int32{codec},
    lo_custkey          Int32{codec},
    lo_partkey          Int32{codec},
    lo_suppkey          Int32{codec},
    lo_orderdate        Int32{codec},
    lo_orderpriority    {low_cardinality}{codec},
    lo_shippriority     {low_cardinality}{codec},
    lo_quantity         Int32{codec},
    lo_extendedprice    Int32{codec},
    lo_ordtotalprice    Int32{codec},
    lo_discount         Int32{codec},
    lo_revenue          Int32{codec},
    lo_supplycost       Int32{codec},
    lo_tax              Int32{codec},
    lo_commitdate       Int32{codec},
    lo_shipmode         {low_cardinality}{codec}
) ENGINE = MergeTree ORDER BY {order_lineorder}
    SETTINGS index_granularity = {index_granularity}, min_bytes_for_wide_part = {wide_parts};
