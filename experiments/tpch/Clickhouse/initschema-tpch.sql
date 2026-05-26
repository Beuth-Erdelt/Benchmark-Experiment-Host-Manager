-- Benchmark-Experiment-Host-Manager | experiments/tpch/Clickhouse
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create the tpch database and TPC-H tables for ClickHouse.
--          Uses Int32 for key columns (ClickHouse native integer type) and
--          MergeTree engine with an ORDER BY clause per table instead of
--          a primary key constraint. No constraints or secondary indexes.

CREATE DATABASE tpch;

CREATE TABLE tpch.nation (
    n_nationkey  Int32         NOT NULL,
    n_name       CHAR(25)      NOT NULL,
    n_regionkey  Int32         NOT NULL,
    n_comment    VARCHAR(152)
) ENGINE = MergeTree() ORDER BY n_nationkey;

CREATE TABLE tpch.region (
    r_regionkey  Int32         NOT NULL,
    r_name       CHAR(25)      NOT NULL,
    r_comment    VARCHAR(152)
) ENGINE = MergeTree() ORDER BY r_regionkey;

CREATE TABLE tpch.part (
    p_partkey      Int32         NOT NULL,
    p_name         VARCHAR(55)   NOT NULL,
    p_mfgr         CHAR(25)      NOT NULL,
    p_brand        CHAR(10)      NOT NULL,
    p_type         VARCHAR(25)   NOT NULL,
    p_size         INTEGER       NOT NULL,
    p_container    CHAR(10)      NOT NULL,
    p_retailprice  DECIMAL(15,2) NOT NULL,
    p_comment      VARCHAR(23)   NOT NULL
) ENGINE = MergeTree() ORDER BY p_partkey;

CREATE TABLE tpch.supplier (
    s_suppkey    Int32         NOT NULL,
    s_name       CHAR(25)      NOT NULL,
    s_address    VARCHAR(40)   NOT NULL,
    s_nationkey  Int32         NOT NULL,
    s_phone      CHAR(15)      NOT NULL,
    s_acctbal    DECIMAL(15,2) NOT NULL,
    s_comment    VARCHAR(101)  NOT NULL
) ENGINE = MergeTree() ORDER BY s_suppkey;

CREATE TABLE tpch.partsupp (
    ps_partkey     Int32         NOT NULL,
    ps_suppkey     Int32         NOT NULL,
    ps_availqty    INTEGER       NOT NULL,
    ps_supplycost  DECIMAL(15,2) NOT NULL,
    ps_comment     VARCHAR(199)  NOT NULL
) ENGINE = MergeTree() ORDER BY (ps_partkey, ps_suppkey);

CREATE TABLE tpch.customer (
    c_custkey     Int32         NOT NULL,
    c_name        VARCHAR(25)   NOT NULL,
    c_address     VARCHAR(40)   NOT NULL,
    c_nationkey   Int32         NOT NULL,
    c_phone       CHAR(15)      NOT NULL,
    c_acctbal     DECIMAL(15,2) NOT NULL,
    c_mktsegment  CHAR(10)      NOT NULL,
    c_comment     VARCHAR(117)  NOT NULL
) ENGINE = MergeTree() ORDER BY c_custkey;

CREATE TABLE tpch.orders (
    o_orderkey       Int32         NOT NULL,
    o_custkey        Int32         NOT NULL,
    o_orderstatus    CHAR(1)       NOT NULL,
    o_totalprice     DECIMAL(15,2) NOT NULL,
    o_orderdate      DATE          NOT NULL,
    o_orderpriority  CHAR(15)      NOT NULL,
    o_clerk          CHAR(15)      NOT NULL,
    o_shippriority   INTEGER       NOT NULL,
    o_comment        VARCHAR(79)   NOT NULL
) ENGINE = MergeTree() ORDER BY o_orderkey;

CREATE TABLE tpch.lineitem (
    l_orderkey       Int32         NOT NULL,
    l_partkey        Int32         NOT NULL,
    l_suppkey        Int32         NOT NULL,
    l_linenumber     INTEGER       NOT NULL,
    l_quantity       DECIMAL(15,2) NOT NULL,
    l_extendedprice  DECIMAL(15,2) NOT NULL,
    l_discount       DECIMAL(15,2) NOT NULL,
    l_tax            DECIMAL(15,2) NOT NULL,
    l_returnflag     CHAR(1)       NOT NULL,
    l_linestatus     CHAR(1)       NOT NULL,
    l_shipdate       DATE          NOT NULL,
    l_commitdate     DATE          NOT NULL,
    l_receiptdate    DATE          NOT NULL,
    l_shipinstruct   CHAR(25)      NOT NULL,
    l_shipmode       CHAR(10)      NOT NULL,
    l_comment        VARCHAR(44)   NOT NULL
) ENGINE = MergeTree() ORDER BY (l_orderkey, l_partkey, l_suppkey);
