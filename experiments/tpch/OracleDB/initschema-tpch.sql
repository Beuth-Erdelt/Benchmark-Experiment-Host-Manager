-- Benchmark-Experiment-Host-Manager | experiments/tpch/OracleDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create the TPC-H tables in Oracle Database Free.
--          loadData runs this file as SYSDBA in the pluggable database FREEPDB1
--          with CURRENT_SCHEMA = BEXHOMA (/tmp/bexhoma-session.sql of the template),
--          so the tables are created in the schema of the user bexhoma, which
--          the template creates at every start and which all clients log in as.
--          Primary keys are declared inline (as for MySQL and SQL Server); the
--          loader (SQL*Loader, conventional path) loads into them. Keys are
--          NUMBER(10), the order keys NUMBER(12); amounts are NUMBER(15,2).
--          Foreign keys are added by initconstraints-tpch.sql.
--          Per TPC-H spec section 1.4.1/1.4.2.1 all columns may be NOT NULL.
--          No curly braces in this file: bexhoma may fill it with str.format().

CREATE TABLE nation (
    n_nationkey     NUMBER(10)      NOT NULL,
    n_name          CHAR(25)        NOT NULL,
    n_regionkey     NUMBER(10)      NOT NULL,
    n_comment       VARCHAR2(152),
    CONSTRAINT pk_nation PRIMARY KEY (n_nationkey)
);

CREATE TABLE region (
    r_regionkey     NUMBER(10)      NOT NULL,
    r_name          CHAR(25)        NOT NULL,
    r_comment       VARCHAR2(152),
    CONSTRAINT pk_region PRIMARY KEY (r_regionkey)
);

CREATE TABLE part (
    p_partkey       NUMBER(10)      NOT NULL,
    p_name          VARCHAR2(55)    NOT NULL,
    p_mfgr          CHAR(25)        NOT NULL,
    p_brand         CHAR(10)        NOT NULL,
    p_type          VARCHAR2(25)    NOT NULL,
    p_size          NUMBER(10)      NOT NULL,
    p_container     CHAR(10)        NOT NULL,
    p_retailprice   NUMBER(15,2)    NOT NULL,
    p_comment       VARCHAR2(23)    NOT NULL,
    CONSTRAINT pk_part PRIMARY KEY (p_partkey)
);

CREATE TABLE supplier (
    s_suppkey       NUMBER(10)      NOT NULL,
    s_name          CHAR(25)        NOT NULL,
    s_address       VARCHAR2(40)    NOT NULL,
    s_nationkey     NUMBER(10)      NOT NULL,
    s_phone         CHAR(15)        NOT NULL,
    s_acctbal       NUMBER(15,2)    NOT NULL,
    s_comment       VARCHAR2(101)   NOT NULL,
    CONSTRAINT pk_supplier PRIMARY KEY (s_suppkey)
);

CREATE TABLE partsupp (
    ps_partkey      NUMBER(10)      NOT NULL,
    ps_suppkey      NUMBER(10)      NOT NULL,
    ps_availqty     NUMBER(10)      NOT NULL,
    ps_supplycost   NUMBER(15,2)    NOT NULL,
    ps_comment      VARCHAR2(199)   NOT NULL,
    CONSTRAINT pk_partsupp PRIMARY KEY (ps_partkey, ps_suppkey)
);

CREATE TABLE customer (
    c_custkey       NUMBER(10)      NOT NULL,
    c_name          VARCHAR2(25)    NOT NULL,
    c_address       VARCHAR2(40)    NOT NULL,
    c_nationkey     NUMBER(10)      NOT NULL,
    c_phone         CHAR(15)        NOT NULL,
    c_acctbal       NUMBER(15,2)    NOT NULL,
    c_mktsegment    CHAR(10)        NOT NULL,
    c_comment       VARCHAR2(117)   NOT NULL,
    CONSTRAINT pk_customer PRIMARY KEY (c_custkey)
);

CREATE TABLE orders (
    o_orderkey      NUMBER(12)      NOT NULL,
    o_custkey       NUMBER(10)      NOT NULL,
    o_orderstatus   CHAR(1)         NOT NULL,
    o_totalprice    NUMBER(15,2)    NOT NULL,
    o_orderdate     DATE            NOT NULL,
    o_orderpriority CHAR(15)        NOT NULL,
    o_clerk         CHAR(15)        NOT NULL,
    o_shippriority  NUMBER(10)      NOT NULL,
    o_comment       VARCHAR2(79)    NOT NULL,
    CONSTRAINT pk_orders PRIMARY KEY (o_orderkey)
);

CREATE TABLE lineitem (
    l_orderkey      NUMBER(12)      NOT NULL,
    l_partkey       NUMBER(10)      NOT NULL,
    l_suppkey       NUMBER(10)      NOT NULL,
    l_linenumber    NUMBER(10)      NOT NULL,
    l_quantity      NUMBER(15,2)    NOT NULL,
    l_extendedprice NUMBER(15,2)    NOT NULL,
    l_discount      NUMBER(15,2)    NOT NULL,
    l_tax           NUMBER(15,2)    NOT NULL,
    l_returnflag    CHAR(1)         NOT NULL,
    l_linestatus    CHAR(1)         NOT NULL,
    l_shipdate      DATE            NOT NULL,
    l_commitdate    DATE            NOT NULL,
    l_receiptdate   DATE            NOT NULL,
    l_shipinstruct  CHAR(25)        NOT NULL,
    l_shipmode      CHAR(10)        NOT NULL,
    l_comment       VARCHAR2(44)    NOT NULL,
    CONSTRAINT pk_lineitem PRIMARY KEY (l_orderkey, l_linenumber)
);

-- Container and schema the tables are in
SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS container,
       SYS_CONTEXT('USERENV', 'CURRENT_SCHEMA') AS current_schema
FROM dual;
