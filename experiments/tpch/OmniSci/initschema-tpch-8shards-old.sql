-- Benchmark-Experiment-Host-Manager | experiments/tpch/OmniSci
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Older OmniSci TPC-H schema variant with 8 shards, using
--          PostgreSQL-style types (BIGINT, DOUBLE PRECISION, CHAR, VARCHAR,
--          NOT NULL). orders and lineitem are sharded on the order key.
--          No fragment_size is specified.
--          See initschema-tpch-8shards.sql for the current OmniSci-native variant.

CREATE TABLE nation (
    n_nationkey  INTEGER      NOT NULL,
    n_name       CHAR(25)     NOT NULL,
    n_regionkey  INTEGER      NOT NULL,
    n_comment    VARCHAR(152)
);

CREATE TABLE region (
    r_regionkey  INTEGER      NOT NULL,
    r_name       CHAR(25)     NOT NULL,
    r_comment    VARCHAR(152)
);

CREATE TABLE part (
    p_partkey      BIGINT           NOT NULL,
    p_name         VARCHAR(55)      NOT NULL,
    p_mfgr         CHAR(25)         NOT NULL,
    p_brand        CHAR(10)         NOT NULL,
    p_type         VARCHAR(25)      NOT NULL,
    p_size         INTEGER          NOT NULL,
    p_container    CHAR(10)         NOT NULL,
    p_retailprice  DOUBLE PRECISION NOT NULL,
    p_comment      VARCHAR(23)      NOT NULL
);

CREATE TABLE supplier (
    s_suppkey    BIGINT           NOT NULL,
    s_name       CHAR(25)         NOT NULL,
    s_address    VARCHAR(40)      NOT NULL,
    s_nationkey  INTEGER          NOT NULL,
    s_phone      CHAR(15)         NOT NULL,
    s_acctbal    DOUBLE PRECISION NOT NULL,
    s_comment    VARCHAR(101)     NOT NULL
);

CREATE TABLE partsupp (
    ps_partkey     BIGINT           NOT NULL,
    ps_suppkey     BIGINT           NOT NULL,
    ps_availqty    BIGINT           NOT NULL,
    ps_supplycost  DOUBLE PRECISION NOT NULL,
    ps_comment     VARCHAR(199)     NOT NULL
);

CREATE TABLE customer (
    c_custkey     BIGINT           NOT NULL,
    c_name        VARCHAR(25)      NOT NULL,
    c_address     VARCHAR(40)      NOT NULL,
    c_nationkey   INTEGER          NOT NULL,
    c_phone       CHAR(15)         NOT NULL,
    c_acctbal     DOUBLE PRECISION NOT NULL,
    c_mktsegment  CHAR(10)         NOT NULL,
    c_comment     VARCHAR(117)     NOT NULL
);

CREATE TABLE orders (
    o_orderkey       BIGINT           NOT NULL,
    o_custkey        BIGINT           NOT NULL,
    o_orderstatus    CHAR(1)          NOT NULL,
    o_totalprice     DOUBLE PRECISION NOT NULL,
    o_orderdate      DATE             NOT NULL,
    o_orderpriority  CHAR(15)         NOT NULL,
    o_clerk          CHAR(15)         NOT NULL,
    o_shippriority   INTEGER          NOT NULL,
    o_comment        VARCHAR(79)      NOT NULL,
    SHARD KEY (o_orderkey)
) WITH (shard_count = 8, partitions = 'SHARDED');

CREATE TABLE lineitem (
    l_orderkey       BIGINT           NOT NULL,
    l_partkey        BIGINT           NOT NULL,
    l_suppkey        BIGINT           NOT NULL,
    l_linenumber     BIGINT           NOT NULL,
    l_quantity       DOUBLE PRECISION NOT NULL,
    l_extendedprice  DOUBLE PRECISION NOT NULL,
    l_discount       DOUBLE PRECISION NOT NULL,
    l_tax            DOUBLE PRECISION NOT NULL,
    l_returnflag     CHAR(1)          NOT NULL,
    l_linestatus     CHAR(1)          NOT NULL,
    l_shipdate       DATE             NOT NULL,
    l_commitdate     DATE             NOT NULL,
    l_receiptdate    DATE             NOT NULL,
    l_shipinstruct   CHAR(25)         NOT NULL,
    l_shipmode       CHAR(10)         NOT NULL,
    l_comment        VARCHAR(44)      NOT NULL,
    SHARD KEY (l_orderkey)
) WITH (shard_count = 8, partitions = 'SHARDED');
