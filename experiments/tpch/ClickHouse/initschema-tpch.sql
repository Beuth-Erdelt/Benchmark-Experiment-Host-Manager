-- Benchmark-Experiment-Host-Manager | experiments/tpch/ClickHouse
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create TPC-H tables in ClickHouse (database default).
--          MergeTree needs a sorting key at creation; it is the TPC-H primary
--          key of each table, which also is ClickHouse's sparse primary index.
--          There are no secondary indexes or constraints (-xii/-xic have no
--          scripts). CHAR/VARCHAR are String: FixedString pads with \0, not
--          with blanks. Order keys are Int64 (SF 1000 exceeds Int32).
--          No curly braces in this file: bexhoma may fill it with str.format().

CREATE TABLE nation (
    n_nationkey  Int32,
    n_name       String,
    n_regionkey  Int32,
    n_comment    String
) ENGINE = MergeTree ORDER BY n_nationkey;

CREATE TABLE region (
    r_regionkey  Int32,
    r_name       String,
    r_comment    String
) ENGINE = MergeTree ORDER BY r_regionkey;

CREATE TABLE part (
    p_partkey      Int32,
    p_name         String,
    p_mfgr         String,
    p_brand        String,
    p_type         String,
    p_size         Int32,
    p_container    String,
    p_retailprice  Decimal(15,2),
    p_comment      String
) ENGINE = MergeTree ORDER BY p_partkey;

CREATE TABLE supplier (
    s_suppkey    Int32,
    s_name       String,
    s_address    String,
    s_nationkey  Int32,
    s_phone      String,
    s_acctbal    Decimal(15,2),
    s_comment    String
) ENGINE = MergeTree ORDER BY s_suppkey;

CREATE TABLE partsupp (
    ps_partkey     Int32,
    ps_suppkey     Int32,
    ps_availqty    Int32,
    ps_supplycost  Decimal(15,2),
    ps_comment     String
) ENGINE = MergeTree ORDER BY (ps_partkey, ps_suppkey);

CREATE TABLE customer (
    c_custkey     Int32,
    c_name        String,
    c_address     String,
    c_nationkey   Int32,
    c_phone       String,
    c_acctbal     Decimal(15,2),
    c_mktsegment  String,
    c_comment     String
) ENGINE = MergeTree ORDER BY c_custkey;

CREATE TABLE orders (
    o_orderkey       Int64,
    o_custkey        Int32,
    o_orderstatus    String,
    o_totalprice     Decimal(15,2),
    o_orderdate      Date,
    o_orderpriority  String,
    o_clerk          String,
    o_shippriority   Int32,
    o_comment        String
) ENGINE = MergeTree ORDER BY o_orderkey;

CREATE TABLE lineitem (
    l_orderkey       Int64,
    l_partkey        Int32,
    l_suppkey        Int32,
    l_linenumber     Int32,
    l_quantity       Decimal(15,2),
    l_extendedprice  Decimal(15,2),
    l_discount       Decimal(15,2),
    l_tax            Decimal(15,2),
    l_returnflag     String,
    l_linestatus     String,
    l_shipdate       Date,
    l_commitdate     Date,
    l_receiptdate    Date,
    l_shipinstruct   String,
    l_shipmode       String,
    l_comment        String
) ENGINE = MergeTree ORDER BY (l_orderkey, l_linenumber);
