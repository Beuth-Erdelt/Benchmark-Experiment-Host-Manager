-- Benchmark-Experiment-Host-Manager | experiments/tpch/Citus
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Bexhoma template variant of the Citus TPC-H schema.
--          The placeholders {shard_count} and {replication_count} are substituted
--          at runtime by the Bexhoma framework before execution.
--          In this variant all dimension tables AND orders are reference tables;
--          only lineitem is distributed (maximises co-location for fact queries).
--          No PKs are added here; they are handled separately.
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


ALTER SYSTEM SET citus.max_intermediate_result_size TO -1;
ALTER SYSTEM SET citus.shard_count              TO {shard_count};
ALTER SYSTEM SET citus.shard_replication_factor TO {replication_count};
ALTER SYSTEM SET citus.enable_repartition_joins TO 1;

SELECT pg_reload_conf();


-- All tables except lineitem are reference tables so every worker has a full
-- local copy, eliminating network round-trips for dimension lookups.
SELECT create_reference_table('supplier');
SELECT create_reference_table('nation');
SELECT create_reference_table('region');
SELECT create_reference_table('part');
SELECT create_reference_table('partsupp');
SELECT create_reference_table('customer');
SELECT create_reference_table('orders');
SELECT create_distributed_table('lineitem', 'l_orderkey');
