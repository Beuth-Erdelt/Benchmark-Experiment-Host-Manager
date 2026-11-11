-- Benchmark-Experiment-Host-Manager | experiments/tpch/SQLServer
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create the TPC-H tables in SQL Server, schema dbo.
--          The database is created by loadData (/tmp/bexhoma-database.sql of the
--          template, recovery model SIMPLE), which also switches to it.
--          Primary keys are clustered and declared inline (as for MySQL); the
--          loader (bcp, TABLOCK) loads into them. Keys are INT, the order keys
--          BIGINT (more than 2^31 orders above SF 300); foreign keys have the
--          type of the key they reference (initconstraints-tpch.sql).
--          No curly braces in this file: bexhoma may fill it with str.format().

SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;
GO

CREATE TABLE dbo.nation (
    n_nationkey     INT             NOT NULL,
    n_name          CHAR(25)        NOT NULL,
    n_regionkey     INT             NOT NULL,
    n_comment       VARCHAR(152),
    CONSTRAINT pk_nation PRIMARY KEY CLUSTERED (n_nationkey)
);

CREATE TABLE dbo.region (
    r_regionkey     INT             NOT NULL,
    r_name          CHAR(25)        NOT NULL,
    r_comment       VARCHAR(152),
    CONSTRAINT pk_region PRIMARY KEY CLUSTERED (r_regionkey)
);

CREATE TABLE dbo.part (
    p_partkey       INT             NOT NULL,
    p_name          VARCHAR(55)     NOT NULL,
    p_mfgr          CHAR(25)        NOT NULL,
    p_brand         CHAR(10)        NOT NULL,
    p_type          VARCHAR(25)     NOT NULL,
    p_size          INT             NOT NULL,
    p_container     CHAR(10)        NOT NULL,
    p_retailprice   DECIMAL(15,2)   NOT NULL,
    p_comment       VARCHAR(23)     NOT NULL,
    CONSTRAINT pk_part PRIMARY KEY CLUSTERED (p_partkey)
);

CREATE TABLE dbo.supplier (
    s_suppkey       INT             NOT NULL,
    s_name          CHAR(25)        NOT NULL,
    s_address       VARCHAR(40)     NOT NULL,
    s_nationkey     INT             NOT NULL,
    s_phone         CHAR(15)        NOT NULL,
    s_acctbal       DECIMAL(15,2)   NOT NULL,
    s_comment       VARCHAR(101)    NOT NULL,
    CONSTRAINT pk_supplier PRIMARY KEY CLUSTERED (s_suppkey)
);

CREATE TABLE dbo.partsupp (
    ps_partkey      INT             NOT NULL,
    ps_suppkey      INT             NOT NULL,
    ps_availqty     INT             NOT NULL,
    ps_supplycost   DECIMAL(15,2)   NOT NULL,
    ps_comment      VARCHAR(199)    NOT NULL,
    CONSTRAINT pk_partsupp PRIMARY KEY CLUSTERED (ps_partkey, ps_suppkey)
);

CREATE TABLE dbo.customer (
    c_custkey       INT             NOT NULL,
    c_name          VARCHAR(25)     NOT NULL,
    c_address       VARCHAR(40)     NOT NULL,
    c_nationkey     INT             NOT NULL,
    c_phone         CHAR(15)        NOT NULL,
    c_acctbal       DECIMAL(15,2)   NOT NULL,
    c_mktsegment    CHAR(10)        NOT NULL,
    c_comment       VARCHAR(117)    NOT NULL,
    CONSTRAINT pk_customer PRIMARY KEY CLUSTERED (c_custkey)
);

CREATE TABLE dbo.orders (
    o_orderkey      BIGINT          NOT NULL,
    o_custkey       INT             NOT NULL,
    o_orderstatus   CHAR(1)         NOT NULL,
    o_totalprice    DECIMAL(15,2)   NOT NULL,
    o_orderdate     DATE            NOT NULL,
    o_orderpriority CHAR(15)        NOT NULL,
    o_clerk         CHAR(15)        NOT NULL,
    o_shippriority  INT             NOT NULL,
    o_comment       VARCHAR(79)     NOT NULL,
    CONSTRAINT pk_orders PRIMARY KEY CLUSTERED (o_orderkey)
);

CREATE TABLE dbo.lineitem (
    l_orderkey      BIGINT          NOT NULL,
    l_partkey       INT             NOT NULL,
    l_suppkey       INT             NOT NULL,
    l_linenumber    INT             NOT NULL,
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
    CONSTRAINT pk_lineitem PRIMARY KEY CLUSTERED (l_orderkey, l_linenumber)
);
GO

SELECT name, recovery_model_desc, delayed_durability_desc, compatibility_level, collation_name
FROM sys.databases
WHERE name = DB_NAME();
GO
