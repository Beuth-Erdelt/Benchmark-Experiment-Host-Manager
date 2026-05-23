-- Benchmark-Experiment-Host-Manager | experiments/tpch/Citus
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create TPC-H tables for Citus (PostgreSQL-based distributed DBMS).
--          Uses BIGINT for high-cardinality key columns and DOUBLE PRECISION
--          for monetary/quantity values, following the dimitri/tpch-citus schema.
--          After table creation, configures Citus settings and distributes tables:
--          dimension tables as reference tables, orders/lineitem as distributed.
--          PKs are added before distribution so Citus can use them as shard keys.
-- Reference: https://github.com/dimitri/tpch-citus/tree/master/schema

SELECT * FROM master_get_active_worker_nodes();


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
    c_custkey     INTEGER          NOT NULL,
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
    o_custkey        INTEGER          NOT NULL,
    o_orderstatus    CHAR(1)          NOT NULL,
    o_totalprice     DOUBLE PRECISION NOT NULL,
    o_orderdate      DATE             NOT NULL,
    o_orderpriority  CHAR(15)         NOT NULL,
    o_clerk          CHAR(15)         NOT NULL,
    o_shippriority   INTEGER          NOT NULL,
    o_comment        VARCHAR(79)      NOT NULL
);

CREATE TABLE lineitem (
    l_orderkey       BIGINT           NOT NULL,
    l_partkey        INTEGER          NOT NULL,
    l_suppkey        INTEGER          NOT NULL,
    l_linenumber     INTEGER          NOT NULL,
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
    l_comment        VARCHAR(44)      NOT NULL
);


-- Citus settings: unlimited intermediate result size and repartition joins
-- allow complex analytical queries to spill to workers instead of failing.
ALTER SYSTEM SET citus.max_intermediate_result_size TO -1;
ALTER SYSTEM SET citus.enable_repartition_joins TO 1;

SELECT pg_reload_conf();


-- PKs must exist before create_distributed_table so Citus can enforce uniqueness
-- across shards (PK must include the distribution column).
ALTER TABLE region   ADD CONSTRAINT region_pkey   PRIMARY KEY (r_regionkey);
ALTER TABLE nation   ADD CONSTRAINT nation_pkey   PRIMARY KEY (n_nationkey);
ALTER TABLE part     ADD CONSTRAINT part_pkey     PRIMARY KEY (p_partkey);
ALTER TABLE supplier ADD CONSTRAINT supplier_pkey PRIMARY KEY (s_suppkey);
ALTER TABLE partsupp ADD CONSTRAINT partsupp_pkey PRIMARY KEY (ps_partkey, ps_suppkey);
ALTER TABLE customer ADD CONSTRAINT customer_pkey PRIMARY KEY (c_custkey);
ALTER TABLE orders   ADD CONSTRAINT orders_pkey   PRIMARY KEY (o_orderkey);
ALTER TABLE lineitem ADD CONSTRAINT lineitem_pkey PRIMARY KEY (l_orderkey, l_linenumber);


-- Q22: correlated subqueries are not supported when FROM contains a reference table.
-- Dimension tables are reference tables (replicated to every worker for fast joins).
-- orders and lineitem are distributed by their order key for co-located joins.
SELECT create_reference_table('nation');
SELECT create_reference_table('region');
SELECT create_reference_table('part');
SELECT create_reference_table('supplier');
SELECT create_reference_table('partsupp');
SELECT create_reference_table('customer');
SELECT create_distributed_table('orders',   'o_orderkey');
SELECT create_distributed_table('lineitem', 'l_orderkey');
