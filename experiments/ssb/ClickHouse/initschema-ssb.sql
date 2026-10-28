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
--          No curly braces in this file: bexhoma may fill it with str.format().

CREATE TABLE customer (
    c_custkey     Int32,
    c_name        String,
    c_address     String,
    c_city        String,
    c_nation      String,
    c_region      String,
    c_phone       String,
    c_mktsegment  String
) ENGINE = MergeTree ORDER BY c_custkey;

CREATE TABLE supplier (
    s_suppkey  Int32,
    s_name     String,
    s_address  String,
    s_city     String,
    s_nation   String,
    s_region   String,
    s_phone    String
) ENGINE = MergeTree ORDER BY s_suppkey;

CREATE TABLE part (
    p_partkey    Int32,
    p_name       String,
    p_mfgr       String,
    p_category   String,
    p_brand1     String,
    p_color      String,
    p_type       String,
    p_size       Int32,
    p_container  String
) ENGINE = MergeTree ORDER BY p_partkey;

CREATE TABLE dates (
    d_datekey           Int32,
    d_date              String,
    d_dayofweek         String,
    d_month             String,
    d_year              Int32,
    d_yearmonthnum      Int32,
    d_yearmonth         String,
    d_daynuminweek      Int32,
    d_daynuminmonth     Int32,
    d_daynuminyear      Int32,
    d_monthnuminyear    Int32,
    d_weeknuminyear     Int32,
    d_sellingseason     String,
    d_lastdayinweekfl   String,
    d_lastdayinmonthfl  String,
    d_holidayfl         String,
    d_weekdayfl         String
) ENGINE = MergeTree ORDER BY d_datekey;

CREATE TABLE lineorder (
    lo_orderkey         Int64,
    lo_linenumber       Int32,
    lo_custkey          Int32,
    lo_partkey          Int32,
    lo_suppkey          Int32,
    lo_orderdate        Int32,
    lo_orderpriority    String,
    lo_shippriority     String,
    lo_quantity         Int32,
    lo_extendedprice    Int32,
    lo_ordtotalprice    Int32,
    lo_discount         Int32,
    lo_revenue          Int32,
    lo_supplycost       Int32,
    lo_tax              Int32,
    lo_commitdate       Int32,
    lo_shipmode         String
) ENGINE = MergeTree ORDER BY (lo_orderdate, lo_orderkey);
