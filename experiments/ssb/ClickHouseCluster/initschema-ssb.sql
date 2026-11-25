-- Benchmark-Experiment-Host-Manager | experiments/ssb/ClickHouseCluster
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create the SSB star schema on a ClickHouse cluster (cluster bexhoma of
--          deploymenttemplate-ClickHouseCluster.yml) with replicated dimensions
--          (-xdim replicated, default).
--          - customer, supplier, part, dates: ReplicatedMergeTree on every shard
--            (ON CLUSTER) and on the coordinator, all replicas of one table (the
--            template's default replica path has no shard). The loader inserts on
--            the coordinator, Keeper copies the parts to the shards, so a join with
--            lineorder runs on each shard against its local copy.
--          - lineorder: MergeTree lineorder_local on every shard and a Distributed
--            table lineorder on the shards and the coordinator, rows spread by
--            lo_orderkey (all lines of an order on one shard).
--          Columns and sorting keys as in experiments/ssb/ClickHouse.

CREATE TABLE customer ON CLUSTER bexhoma (
    c_custkey     Int32,
    c_name        String,
    c_address     String,
    c_city        {low_cardinality},
    c_nation      {low_cardinality},
    c_region      {low_cardinality},
    c_phone       String,
    c_mktsegment  {low_cardinality}
) ENGINE = ReplicatedMergeTree ORDER BY c_custkey;

CREATE TABLE customer (
    c_custkey     Int32,
    c_name        String,
    c_address     String,
    c_city        {low_cardinality},
    c_nation      {low_cardinality},
    c_region      {low_cardinality},
    c_phone       String,
    c_mktsegment  {low_cardinality}
) ENGINE = ReplicatedMergeTree ORDER BY c_custkey;

CREATE TABLE supplier ON CLUSTER bexhoma (
    s_suppkey  Int32,
    s_name     String,
    s_address  String,
    s_city     {low_cardinality},
    s_nation   {low_cardinality},
    s_region   {low_cardinality},
    s_phone    String
) ENGINE = ReplicatedMergeTree ORDER BY s_suppkey;

CREATE TABLE supplier (
    s_suppkey  Int32,
    s_name     String,
    s_address  String,
    s_city     {low_cardinality},
    s_nation   {low_cardinality},
    s_region   {low_cardinality},
    s_phone    String
) ENGINE = ReplicatedMergeTree ORDER BY s_suppkey;

CREATE TABLE part ON CLUSTER bexhoma (
    p_partkey    Int32,
    p_name       String,
    p_mfgr       {low_cardinality},
    p_category   {low_cardinality},
    p_brand1     {low_cardinality},
    p_color      {low_cardinality},
    p_type       {low_cardinality},
    p_size       Int32,
    p_container  {low_cardinality}
) ENGINE = ReplicatedMergeTree ORDER BY p_partkey;

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
) ENGINE = ReplicatedMergeTree ORDER BY p_partkey;

CREATE TABLE dates ON CLUSTER bexhoma (
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
) ENGINE = ReplicatedMergeTree ORDER BY d_datekey;

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
) ENGINE = ReplicatedMergeTree ORDER BY d_datekey;

CREATE TABLE lineorder_local ON CLUSTER bexhoma (
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

CREATE TABLE lineorder ON CLUSTER bexhoma (
    lo_orderkey         Int64,
    lo_linenumber       Int32,
    lo_custkey          Int32,
    lo_partkey          Int32,
    lo_suppkey          Int32,
    lo_orderdate        Int32,
    lo_orderpriority    {low_cardinality},
    lo_shippriority     {low_cardinality},
    lo_quantity         Int32,
    lo_extendedprice    Int32,
    lo_ordtotalprice    Int32,
    lo_discount         Int32,
    lo_revenue          Int32,
    lo_supplycost       Int32,
    lo_tax              Int32,
    lo_commitdate       Int32,
    lo_shipmode         {low_cardinality}
) ENGINE = Distributed(bexhoma, currentDatabase(), lineorder_local, lo_orderkey);

CREATE TABLE lineorder (
    lo_orderkey         Int64,
    lo_linenumber       Int32,
    lo_custkey          Int32,
    lo_partkey          Int32,
    lo_suppkey          Int32,
    lo_orderdate        Int32,
    lo_orderpriority    {low_cardinality},
    lo_shippriority     {low_cardinality},
    lo_quantity         Int32,
    lo_extendedprice    Int32,
    lo_ordtotalprice    Int32,
    lo_discount         Int32,
    lo_revenue          Int32,
    lo_supplycost       Int32,
    lo_tax              Int32,
    lo_commitdate       Int32,
    lo_shipmode         {low_cardinality}
) ENGINE = Distributed(bexhoma, currentDatabase(), lineorder_local, lo_orderkey);
