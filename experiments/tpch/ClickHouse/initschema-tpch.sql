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
--          Sort keys, partitions and part settings of orders and lineitem, and
--          LowCardinality string columns are DDL parameters
--          (ddl-parameters.config).

CREATE TABLE nation (
    n_nationkey  Int32,
    n_name       {low_cardinality},
    n_regionkey  Int32,
    n_comment    String
) ENGINE = MergeTree ORDER BY n_nationkey;

CREATE TABLE region (
    r_regionkey  Int32,
    r_name       {low_cardinality},
    r_comment    String
) ENGINE = MergeTree ORDER BY r_regionkey;

CREATE TABLE part (
    p_partkey      Int32,
    p_name         String,
    p_mfgr         {low_cardinality},
    p_brand        {low_cardinality},
    p_type         {low_cardinality},
    p_size         Int32,
    p_container    {low_cardinality},
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
    c_mktsegment  {low_cardinality},
    c_comment     String
) ENGINE = MergeTree ORDER BY c_custkey;

CREATE TABLE orders (
    o_orderkey       Int64{codec},
    o_custkey        Int32{codec},
    o_orderstatus    {low_cardinality}{codec},
    o_totalprice     Decimal(15,2),
    o_orderdate      Date{codec},
    o_orderpriority  {low_cardinality}{codec},
    o_clerk          String{codec},
    o_shippriority   Int32{codec},
    o_comment        String{codec}
) ENGINE = MergeTree{partition_orders} ORDER BY {order_orders}
    SETTINGS index_granularity = {index_granularity}, min_bytes_for_wide_part = {wide_parts};

CREATE TABLE lineitem (
    l_orderkey       Int64{codec},
    l_partkey        Int32{codec},
    l_suppkey        Int32{codec},
    l_linenumber     Int32{codec},
    l_quantity       Decimal(15,2),
    l_extendedprice  Decimal(15,2),
    l_discount       Decimal(15,2),
    l_tax            Decimal(15,2),
    l_returnflag     {low_cardinality}{codec},
    l_linestatus     {low_cardinality}{codec},
    l_shipdate       Date{codec},
    l_commitdate     Date{codec},
    l_receiptdate    Date{codec},
    l_shipinstruct   {low_cardinality}{codec},
    l_shipmode       {low_cardinality}{codec},
    l_comment        String{codec}
) ENGINE = MergeTree{partition_lineitem} ORDER BY {order_lineitem}
    SETTINGS index_granularity = {index_granularity}, min_bytes_for_wide_part = {wide_parts};
