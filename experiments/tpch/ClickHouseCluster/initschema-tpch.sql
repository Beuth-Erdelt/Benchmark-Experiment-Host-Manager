-- Benchmark-Experiment-Host-Manager | experiments/tpch/ClickHouseCluster
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create the TPC-H tables on a ClickHouse cluster (cluster bexhoma of
--          deploymenttemplate-ClickHouseCluster.yml): per table a MergeTree
--          table <name>_local on every shard (ON CLUSTER), and a Distributed
--          table <name> that the loader writes to and the queries read: on the
--          coordinator, which is not a shard, and on every shard, where the
--          parts of a distributed query that name a table resolve it.
--          Rows are spread by the first column of the sorting key; joins of
--          Distributed tables are correct for any sharding
--          (distributed_product_mode = global in the template).
--          Columns and sorting keys as in experiments/tpch/ClickHouse.
--          No curly braces in this file: bexhoma may fill it with str.format().

CREATE TABLE nation_local ON CLUSTER bexhoma (
    n_nationkey  Int32,
    n_name       String,
    n_regionkey  Int32,
    n_comment    String
) ENGINE = MergeTree ORDER BY n_nationkey;

CREATE TABLE nation ON CLUSTER bexhoma (
    n_nationkey  Int32,
    n_name       String,
    n_regionkey  Int32,
    n_comment    String
) ENGINE = Distributed(bexhoma, currentDatabase(), nation_local, n_nationkey);

CREATE TABLE nation (
    n_nationkey  Int32,
    n_name       String,
    n_regionkey  Int32,
    n_comment    String
) ENGINE = Distributed(bexhoma, currentDatabase(), nation_local, n_nationkey);

CREATE TABLE region_local ON CLUSTER bexhoma (
    r_regionkey  Int32,
    r_name       String,
    r_comment    String
) ENGINE = MergeTree ORDER BY r_regionkey;

CREATE TABLE region ON CLUSTER bexhoma (
    r_regionkey  Int32,
    r_name       String,
    r_comment    String
) ENGINE = Distributed(bexhoma, currentDatabase(), region_local, r_regionkey);

CREATE TABLE region (
    r_regionkey  Int32,
    r_name       String,
    r_comment    String
) ENGINE = Distributed(bexhoma, currentDatabase(), region_local, r_regionkey);

CREATE TABLE part_local ON CLUSTER bexhoma (
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

CREATE TABLE part ON CLUSTER bexhoma (
    p_partkey      Int32,
    p_name         String,
    p_mfgr         String,
    p_brand        String,
    p_type         String,
    p_size         Int32,
    p_container    String,
    p_retailprice  Decimal(15,2),
    p_comment      String
) ENGINE = Distributed(bexhoma, currentDatabase(), part_local, p_partkey);

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
) ENGINE = Distributed(bexhoma, currentDatabase(), part_local, p_partkey);

CREATE TABLE supplier_local ON CLUSTER bexhoma (
    s_suppkey    Int32,
    s_name       String,
    s_address    String,
    s_nationkey  Int32,
    s_phone      String,
    s_acctbal    Decimal(15,2),
    s_comment    String
) ENGINE = MergeTree ORDER BY s_suppkey;

CREATE TABLE supplier ON CLUSTER bexhoma (
    s_suppkey    Int32,
    s_name       String,
    s_address    String,
    s_nationkey  Int32,
    s_phone      String,
    s_acctbal    Decimal(15,2),
    s_comment    String
) ENGINE = Distributed(bexhoma, currentDatabase(), supplier_local, s_suppkey);

CREATE TABLE supplier (
    s_suppkey    Int32,
    s_name       String,
    s_address    String,
    s_nationkey  Int32,
    s_phone      String,
    s_acctbal    Decimal(15,2),
    s_comment    String
) ENGINE = Distributed(bexhoma, currentDatabase(), supplier_local, s_suppkey);

CREATE TABLE partsupp_local ON CLUSTER bexhoma (
    ps_partkey     Int32,
    ps_suppkey     Int32,
    ps_availqty    Int32,
    ps_supplycost  Decimal(15,2),
    ps_comment     String
) ENGINE = MergeTree ORDER BY (ps_partkey, ps_suppkey);

CREATE TABLE partsupp ON CLUSTER bexhoma (
    ps_partkey     Int32,
    ps_suppkey     Int32,
    ps_availqty    Int32,
    ps_supplycost  Decimal(15,2),
    ps_comment     String
) ENGINE = Distributed(bexhoma, currentDatabase(), partsupp_local, ps_partkey);

CREATE TABLE partsupp (
    ps_partkey     Int32,
    ps_suppkey     Int32,
    ps_availqty    Int32,
    ps_supplycost  Decimal(15,2),
    ps_comment     String
) ENGINE = Distributed(bexhoma, currentDatabase(), partsupp_local, ps_partkey);

CREATE TABLE customer_local ON CLUSTER bexhoma (
    c_custkey     Int32,
    c_name        String,
    c_address     String,
    c_nationkey   Int32,
    c_phone       String,
    c_acctbal     Decimal(15,2),
    c_mktsegment  String,
    c_comment     String
) ENGINE = MergeTree ORDER BY c_custkey;

CREATE TABLE customer ON CLUSTER bexhoma (
    c_custkey     Int32,
    c_name        String,
    c_address     String,
    c_nationkey   Int32,
    c_phone       String,
    c_acctbal     Decimal(15,2),
    c_mktsegment  String,
    c_comment     String
) ENGINE = Distributed(bexhoma, currentDatabase(), customer_local, c_custkey);

CREATE TABLE customer (
    c_custkey     Int32,
    c_name        String,
    c_address     String,
    c_nationkey   Int32,
    c_phone       String,
    c_acctbal     Decimal(15,2),
    c_mktsegment  String,
    c_comment     String
) ENGINE = Distributed(bexhoma, currentDatabase(), customer_local, c_custkey);

CREATE TABLE orders_local ON CLUSTER bexhoma (
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

CREATE TABLE orders ON CLUSTER bexhoma (
    o_orderkey       Int64,
    o_custkey        Int32,
    o_orderstatus    String,
    o_totalprice     Decimal(15,2),
    o_orderdate      Date,
    o_orderpriority  String,
    o_clerk          String,
    o_shippriority   Int32,
    o_comment        String
) ENGINE = Distributed(bexhoma, currentDatabase(), orders_local, o_orderkey);

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
) ENGINE = Distributed(bexhoma, currentDatabase(), orders_local, o_orderkey);

CREATE TABLE lineitem_local ON CLUSTER bexhoma (
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

CREATE TABLE lineitem ON CLUSTER bexhoma (
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
) ENGINE = Distributed(bexhoma, currentDatabase(), lineitem_local, l_orderkey);

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
) ENGINE = Distributed(bexhoma, currentDatabase(), lineitem_local, l_orderkey);
