-- Benchmark-Experiment-Host-Manager | experiments/tpch/DB2
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create the TPC-H tables in IBM Db2 Community Edition.
--          loadData runs this file with /tmp/bexhoma-run.sh of the template: one
--          CLP session of db2inst1, connected to the database BEXHOMA, so the
--          tables are created in the schema DB2INST1, the default schema of the
--          user all clients log in as.
--          Row-organized tables in the default table space; primary keys are
--          declared inline (as for MySQL, SQL Server and Oracle), the loader
--          inserts into them. Keys are INTEGER, the order keys BIGINT; amounts
--          are DECIMAL(15,2). Foreign keys are added by initconstraints-tpch.sql.
--          Per TPC-H spec section 1.4.1/1.4.2.1 all columns may be NOT NULL.
--          No curly braces in this file: bexhoma may fill it with str.format().

CREATE TABLE nation (
    n_nationkey     INTEGER         NOT NULL,
    n_name          CHAR(25)        NOT NULL,
    n_regionkey     INTEGER         NOT NULL,
    n_comment       VARCHAR(152),
    CONSTRAINT pk_nation PRIMARY KEY (n_nationkey)
);

CREATE TABLE region (
    r_regionkey     INTEGER         NOT NULL,
    r_name          CHAR(25)        NOT NULL,
    r_comment       VARCHAR(152),
    CONSTRAINT pk_region PRIMARY KEY (r_regionkey)
);

CREATE TABLE part (
    p_partkey       INTEGER         NOT NULL,
    p_name          VARCHAR(55)     NOT NULL,
    p_mfgr          CHAR(25)        NOT NULL,
    p_brand         CHAR(10)        NOT NULL,
    p_type          VARCHAR(25)     NOT NULL,
    p_size          INTEGER         NOT NULL,
    p_container     CHAR(10)        NOT NULL,
    p_retailprice   DECIMAL(15,2)   NOT NULL,
    p_comment       VARCHAR(23)     NOT NULL,
    CONSTRAINT pk_part PRIMARY KEY (p_partkey)
);

CREATE TABLE supplier (
    s_suppkey       INTEGER         NOT NULL,
    s_name          CHAR(25)        NOT NULL,
    s_address       VARCHAR(40)     NOT NULL,
    s_nationkey     INTEGER         NOT NULL,
    s_phone         CHAR(15)        NOT NULL,
    s_acctbal       DECIMAL(15,2)   NOT NULL,
    s_comment       VARCHAR(101)    NOT NULL,
    CONSTRAINT pk_supplier PRIMARY KEY (s_suppkey)
);

CREATE TABLE partsupp (
    ps_partkey      INTEGER         NOT NULL,
    ps_suppkey      INTEGER         NOT NULL,
    ps_availqty     INTEGER         NOT NULL,
    ps_supplycost   DECIMAL(15,2)   NOT NULL,
    ps_comment      VARCHAR(199)    NOT NULL,
    CONSTRAINT pk_partsupp PRIMARY KEY (ps_partkey, ps_suppkey)
);

CREATE TABLE customer (
    c_custkey       INTEGER         NOT NULL,
    c_name          VARCHAR(25)     NOT NULL,
    c_address       VARCHAR(40)     NOT NULL,
    c_nationkey     INTEGER         NOT NULL,
    c_phone         CHAR(15)        NOT NULL,
    c_acctbal       DECIMAL(15,2)   NOT NULL,
    c_mktsegment    CHAR(10)        NOT NULL,
    c_comment       VARCHAR(117)    NOT NULL,
    CONSTRAINT pk_customer PRIMARY KEY (c_custkey)
);

CREATE TABLE orders (
    o_orderkey      BIGINT          NOT NULL,
    o_custkey       INTEGER         NOT NULL,
    o_orderstatus   CHAR(1)         NOT NULL,
    o_totalprice    DECIMAL(15,2)   NOT NULL,
    o_orderdate     DATE            NOT NULL,
    o_orderpriority CHAR(15)        NOT NULL,
    o_clerk         CHAR(15)        NOT NULL,
    o_shippriority  INTEGER         NOT NULL,
    o_comment       VARCHAR(79)     NOT NULL,
    CONSTRAINT pk_orders PRIMARY KEY (o_orderkey)
);

CREATE TABLE lineitem (
    l_orderkey      BIGINT          NOT NULL,
    l_partkey       INTEGER         NOT NULL,
    l_suppkey       INTEGER         NOT NULL,
    l_linenumber    INTEGER         NOT NULL,
    l_quantity      DECIMAL(15,2)   NOT NULL,
    l_extendedprice DECIMAL(15,2)   NOT NULL,
    l_discount      DECIMAL(15,2)   NOT NULL,
    l_tax           DECIMAL(15,2)   NOT NULL,
    l_returnflag    CHAR(1)         NOT NULL,
    l_linestatus    CHAR(1)         NOT NULL,
    l_shipdate      DATE            NOT NULL,
    l_commitdate    DATE            NOT NULL,
    l_receiptdate   DATE            NOT NULL,
    l_shipinstruct  CHAR(25)        NOT NULL,
    l_shipmode      CHAR(10)        NOT NULL,
    l_comment       VARCHAR(44)     NOT NULL,
    CONSTRAINT pk_lineitem PRIMARY KEY (l_orderkey, l_linenumber)
);

-- Database and schema the tables are in
VALUES (CURRENT SERVER, CURRENT SCHEMA);
