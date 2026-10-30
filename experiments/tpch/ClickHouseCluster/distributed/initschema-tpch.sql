-- Benchmark-Experiment-Host-Manager | experiments/tpch/ClickHouseCluster/distributed
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create the TPC-H tables on a ClickHouse cluster (cluster bexhoma of
--          deploymenttemplate-ClickHouseCluster.yml) with distributed dimensions
--          (-xdim distributed):
--          - part, partsupp, supplier, customer, orders, lineitem: a MergeTree
--            table <name>_local on every shard (ON CLUSTER), and a Distributed
--            table <name> that the loader writes to and the queries read: on the
--            coordinator, which is not a shard, and on every shard, where the
--            parts of a distributed query that name a table resolve it.
--            Rows are spread by the first column of the sorting key; joins of
--            Distributed tables are correct for any sharding
--            (distributed_product_mode = global in the template).
--          - nation, region (25 and 5 rows): ReplicatedMergeTree on every shard
--            and on the coordinator, as in the default (-xdim replicated).
--          Columns and sorting keys as in experiments/tpch/ClickHouse.
--          Sort keys, partitions and part settings of orders and lineitem, and
--          LowCardinality string columns are DDL parameters
--          (ddl-parameters.config of the parent folder).

CREATE TABLE nation ON CLUSTER bexhoma (
    n_nationkey  Int32,
    n_name       {low_cardinality},
    n_regionkey  Int32,
    n_comment    String
) ENGINE = ReplicatedMergeTree ORDER BY n_nationkey;

CREATE TABLE nation (
    n_nationkey  Int32,
    n_name       {low_cardinality},
    n_regionkey  Int32,
    n_comment    String
) ENGINE = ReplicatedMergeTree ORDER BY n_nationkey;

CREATE TABLE region ON CLUSTER bexhoma (
    r_regionkey  Int32,
    r_name       {low_cardinality},
    r_comment    String
) ENGINE = ReplicatedMergeTree ORDER BY r_regionkey;

CREATE TABLE region (
    r_regionkey  Int32,
    r_name       {low_cardinality},
    r_comment    String
) ENGINE = ReplicatedMergeTree ORDER BY r_regionkey;

CREATE TABLE part_local ON CLUSTER bexhoma (
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

CREATE TABLE part ON CLUSTER bexhoma (
    p_partkey      Int32,
    p_name         String,
    p_mfgr         {low_cardinality},
    p_brand        {low_cardinality},
    p_type         {low_cardinality},
    p_size         Int32,
    p_container    {low_cardinality},
    p_retailprice  Decimal(15,2),
    p_comment      String
) ENGINE = Distributed(bexhoma, currentDatabase(), part_local, p_partkey);

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
    c_mktsegment  {low_cardinality},
    c_comment     String
) ENGINE = MergeTree ORDER BY c_custkey;

CREATE TABLE customer ON CLUSTER bexhoma (
    c_custkey     Int32,
    c_name        String,
    c_address     String,
    c_nationkey   Int32,
    c_phone       String,
    c_acctbal     Decimal(15,2),
    c_mktsegment  {low_cardinality},
    c_comment     String
) ENGINE = Distributed(bexhoma, currentDatabase(), customer_local, c_custkey);

CREATE TABLE customer (
    c_custkey     Int32,
    c_name        String,
    c_address     String,
    c_nationkey   Int32,
    c_phone       String,
    c_acctbal     Decimal(15,2),
    c_mktsegment  {low_cardinality},
    c_comment     String
) ENGINE = Distributed(bexhoma, currentDatabase(), customer_local, c_custkey);

CREATE TABLE orders_local ON CLUSTER bexhoma (
    o_orderkey       Int64,
    o_custkey        Int32,
    o_orderstatus    {low_cardinality},
    o_totalprice     Decimal(15,2),
    o_orderdate      Date,
    o_orderpriority  {low_cardinality},
    o_clerk          String,
    o_shippriority   Int32,
    o_comment        String
) ENGINE = MergeTree{partition_orders} ORDER BY {order_orders}
    SETTINGS index_granularity = {index_granularity}, min_bytes_for_wide_part = {wide_parts};

CREATE TABLE orders ON CLUSTER bexhoma (
    o_orderkey       Int64,
    o_custkey        Int32,
    o_orderstatus    {low_cardinality},
    o_totalprice     Decimal(15,2),
    o_orderdate      Date,
    o_orderpriority  {low_cardinality},
    o_clerk          String,
    o_shippriority   Int32,
    o_comment        String
) ENGINE = Distributed(bexhoma, currentDatabase(), orders_local, o_orderkey);

CREATE TABLE orders (
    o_orderkey       Int64,
    o_custkey        Int32,
    o_orderstatus    {low_cardinality},
    o_totalprice     Decimal(15,2),
    o_orderdate      Date,
    o_orderpriority  {low_cardinality},
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
    l_returnflag     {low_cardinality},
    l_linestatus     {low_cardinality},
    l_shipdate       Date,
    l_commitdate     Date,
    l_receiptdate    Date,
    l_shipinstruct   {low_cardinality},
    l_shipmode       {low_cardinality},
    l_comment        String
) ENGINE = MergeTree{partition_lineitem} ORDER BY {order_lineitem}
    SETTINGS index_granularity = {index_granularity}, min_bytes_for_wide_part = {wide_parts};

CREATE TABLE lineitem ON CLUSTER bexhoma (
    l_orderkey       Int64,
    l_partkey        Int32,
    l_suppkey        Int32,
    l_linenumber     Int32,
    l_quantity       Decimal(15,2),
    l_extendedprice  Decimal(15,2),
    l_discount       Decimal(15,2),
    l_tax            Decimal(15,2),
    l_returnflag     {low_cardinality},
    l_linestatus     {low_cardinality},
    l_shipdate       Date,
    l_commitdate     Date,
    l_receiptdate    Date,
    l_shipinstruct   {low_cardinality},
    l_shipmode       {low_cardinality},
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
    l_returnflag     {low_cardinality},
    l_linestatus     {low_cardinality},
    l_shipdate       Date,
    l_commitdate     Date,
    l_receiptdate    Date,
    l_shipinstruct   {low_cardinality},
    l_shipmode       {low_cardinality},
    l_comment        String
) ENGINE = Distributed(bexhoma, currentDatabase(), lineitem_local, l_orderkey);
