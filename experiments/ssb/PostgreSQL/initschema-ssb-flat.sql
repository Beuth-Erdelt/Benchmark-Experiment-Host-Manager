-- Benchmark-Experiment-Host-Manager | experiments/ssb/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create the denormalized SSB table lineorder_flat (-xsv flat) in the
--          public schema: the 17 lineorder columns, then all customer, supplier
--          and part columns without their keys (same column set as ClickHouse's
--          lineorder_flat). The generator writes the file in this column order
--          (images/ssb/generator/flat.awk); lo_orderdate and lo_commitdate are
--          dates. The date dimension is not joined: the queries take year, month
--          and week from lo_orderdate.
--          Import settings (load durability, -xld) are in durability-*.sql.
--          No curly braces in this file: bexhoma may fill it with str.format().

CREATE TABLE public.lineorder_flat (
    lo_orderkey         BIGINT       NOT NULL,
    lo_linenumber       INTEGER      NOT NULL,
    lo_custkey          INTEGER      NOT NULL,
    lo_partkey          INTEGER      NOT NULL,
    lo_suppkey          INTEGER      NOT NULL,
    lo_orderdate        DATE         NOT NULL,
    lo_orderpriority    VARCHAR(15)  NOT NULL,
    lo_shippriority     CHAR(1)      NOT NULL,
    lo_quantity         INTEGER      NOT NULL,
    lo_extendedprice    INTEGER      NOT NULL,
    lo_ordtotalprice    INTEGER      NOT NULL,
    lo_discount         INTEGER      NOT NULL,
    lo_revenue          INTEGER      NOT NULL,
    lo_supplycost       INTEGER      NOT NULL,
    lo_tax              INTEGER      NOT NULL,
    lo_commitdate       DATE         NOT NULL,
    lo_shipmode         VARCHAR(10)  NOT NULL,
    c_name              VARCHAR(25)  NOT NULL,
    c_address           VARCHAR(25)  NOT NULL,
    c_city              CHAR(10)     NOT NULL,
    c_nation            VARCHAR(15)  NOT NULL,
    c_region            VARCHAR(12)  NOT NULL,
    c_phone             CHAR(15)     NOT NULL,
    c_mktsegment        VARCHAR(10)  NOT NULL,
    s_name              VARCHAR(25)  NOT NULL,
    s_address           VARCHAR(25)  NOT NULL,
    s_city              CHAR(10)     NOT NULL,
    s_nation            VARCHAR(15)  NOT NULL,
    s_region            VARCHAR(12)  NOT NULL,
    s_phone             CHAR(15)     NOT NULL,
    p_name              VARCHAR(22)  NOT NULL,
    p_mfgr              VARCHAR(6)   NOT NULL,
    p_category          VARCHAR(7)   NOT NULL,
    p_brand1            VARCHAR(9)   NOT NULL,
    p_color             VARCHAR(11)  NOT NULL,
    p_type              VARCHAR(25)  NOT NULL,
    p_size              INTEGER      NOT NULL,
    p_container         VARCHAR(10)  NOT NULL
);
