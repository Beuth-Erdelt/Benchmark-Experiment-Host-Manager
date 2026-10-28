-- Benchmark-Experiment-Host-Manager | experiments/ssb/ClickHouseCluster/distributed
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create the SSB star schema on a ClickHouse cluster (cluster bexhoma of
--          deploymenttemplate-ClickHouseCluster.yml) with Distributed dimensions
--          (-xdim distributed), as for TPC-H: per table a MergeTree table
--          <name>_local on every shard (ON CLUSTER), and a Distributed table <name>
--          on the shards and the coordinator. Rows are spread by the table's key
--          (lineorder by lo_orderkey); a join with a dimension reads the dimension
--          once and sends it to all shards (distributed_product_mode = global in
--          the template).
--          Columns and sorting keys as in experiments/ssb/ClickHouse.
--          No curly braces in this file: bexhoma may fill it with str.format().

CREATE TABLE customer_local ON CLUSTER bexhoma (
    c_custkey     Int32,
    c_name        String,
    c_address     String,
    c_city        String,
    c_nation      String,
    c_region      String,
    c_phone       String,
    c_mktsegment  String
) ENGINE = MergeTree ORDER BY c_custkey;

CREATE TABLE customer ON CLUSTER bexhoma (
    c_custkey     Int32,
    c_name        String,
    c_address     String,
    c_city        String,
    c_nation      String,
    c_region      String,
    c_phone       String,
    c_mktsegment  String
) ENGINE = Distributed(bexhoma, currentDatabase(), customer_local, c_custkey);

CREATE TABLE customer (
    c_custkey     Int32,
    c_name        String,
    c_address     String,
    c_city        String,
    c_nation      String,
    c_region      String,
    c_phone       String,
    c_mktsegment  String
) ENGINE = Distributed(bexhoma, currentDatabase(), customer_local, c_custkey);

CREATE TABLE supplier_local ON CLUSTER bexhoma (
    s_suppkey  Int32,
    s_name     String,
    s_address  String,
    s_city     String,
    s_nation   String,
    s_region   String,
    s_phone    String
) ENGINE = MergeTree ORDER BY s_suppkey;

CREATE TABLE supplier ON CLUSTER bexhoma (
    s_suppkey  Int32,
    s_name     String,
    s_address  String,
    s_city     String,
    s_nation   String,
    s_region   String,
    s_phone    String
) ENGINE = Distributed(bexhoma, currentDatabase(), supplier_local, s_suppkey);

CREATE TABLE supplier (
    s_suppkey  Int32,
    s_name     String,
    s_address  String,
    s_city     String,
    s_nation   String,
    s_region   String,
    s_phone    String
) ENGINE = Distributed(bexhoma, currentDatabase(), supplier_local, s_suppkey);

CREATE TABLE part_local ON CLUSTER bexhoma (
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

CREATE TABLE part ON CLUSTER bexhoma (
    p_partkey    Int32,
    p_name       String,
    p_mfgr       String,
    p_category   String,
    p_brand1     String,
    p_color      String,
    p_type       String,
    p_size       Int32,
    p_container  String
) ENGINE = Distributed(bexhoma, currentDatabase(), part_local, p_partkey);

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
) ENGINE = Distributed(bexhoma, currentDatabase(), part_local, p_partkey);

CREATE TABLE dates_local ON CLUSTER bexhoma (
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

CREATE TABLE dates ON CLUSTER bexhoma (
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
) ENGINE = Distributed(bexhoma, currentDatabase(), dates_local, d_datekey);

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
) ENGINE = Distributed(bexhoma, currentDatabase(), dates_local, d_datekey);

CREATE TABLE lineorder_local ON CLUSTER bexhoma (
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

CREATE TABLE lineorder ON CLUSTER bexhoma (
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
) ENGINE = Distributed(bexhoma, currentDatabase(), lineorder_local, lo_orderkey);

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
) ENGINE = Distributed(bexhoma, currentDatabase(), lineorder_local, lo_orderkey);
