-- Benchmark-Experiment-Host-Manager | experiments/ssb/Citus/distributed
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create the SSB star schema on Citus with distributed dimensions
--          (-xdim distributed): every table is distributed, the dimensions by
--          their key, lineorder by lo_orderkey. A join of lineorder with a
--          dimension is not co-located, so Citus runs it as a repartition join
--          (citus.enable_repartition_joins). Columns as in experiments/ssb/PostgreSQL.
--          Import settings (load durability, -xld) are in durability-*.sql.
--          No curly braces in this file: bexhoma may fill it with str.format().

SELECT * FROM master_get_active_worker_nodes();

CREATE TABLE public.customer (
    c_custkey     INTEGER      NOT NULL,
    c_name        VARCHAR(25)  NOT NULL,
    c_address     VARCHAR(25)  NOT NULL,
    c_city        CHAR(10)     NOT NULL,
    c_nation      VARCHAR(15)  NOT NULL,
    c_region      VARCHAR(12)  NOT NULL,
    c_phone       CHAR(15)     NOT NULL,
    c_mktsegment  VARCHAR(10)  NOT NULL
);

CREATE TABLE public.supplier (
    s_suppkey  INTEGER      NOT NULL,
    s_name     VARCHAR(25)  NOT NULL,
    s_address  VARCHAR(25)  NOT NULL,
    s_city     CHAR(10)     NOT NULL,
    s_nation   VARCHAR(15)  NOT NULL,
    s_region   VARCHAR(12)  NOT NULL,
    s_phone    CHAR(15)     NOT NULL
);

CREATE TABLE public.part (
    p_partkey    INTEGER      NOT NULL,
    p_name       VARCHAR(22)  NOT NULL,
    p_mfgr       VARCHAR(6)   NOT NULL,
    p_category   VARCHAR(7)   NOT NULL,
    p_brand1     VARCHAR(9)   NOT NULL,
    p_color      VARCHAR(11)  NOT NULL,
    p_type       VARCHAR(25)  NOT NULL,
    p_size       INTEGER      NOT NULL,
    p_container  VARCHAR(10)  NOT NULL
);

CREATE TABLE public.dates (
    d_datekey           INTEGER      NOT NULL,
    d_date              VARCHAR(19)  NOT NULL,
    d_dayofweek         VARCHAR(10)  NOT NULL,
    d_month             VARCHAR(10)  NOT NULL,
    d_year              INTEGER      NOT NULL,
    d_yearmonthnum      INTEGER      NOT NULL,
    d_yearmonth         VARCHAR(8)   NOT NULL,
    d_daynuminweek      INTEGER      NOT NULL,
    d_daynuminmonth     INTEGER      NOT NULL,
    d_daynuminyear      INTEGER      NOT NULL,
    d_monthnuminyear    INTEGER      NOT NULL,
    d_weeknuminyear     INTEGER      NOT NULL,
    d_sellingseason     VARCHAR(13)  NOT NULL,
    d_lastdayinweekfl   CHAR(1)      NOT NULL,
    d_lastdayinmonthfl  CHAR(1)      NOT NULL,
    d_holidayfl         CHAR(1)      NOT NULL,
    d_weekdayfl         CHAR(1)      NOT NULL
);

CREATE TABLE public.lineorder (
    lo_orderkey         BIGINT       NOT NULL,
    lo_linenumber       INTEGER      NOT NULL,
    lo_custkey          INTEGER      NOT NULL,
    lo_partkey          INTEGER      NOT NULL,
    lo_suppkey          INTEGER      NOT NULL,
    lo_orderdate        INTEGER      NOT NULL,
    lo_orderpriority    VARCHAR(15)  NOT NULL,
    lo_shippriority     CHAR(1)      NOT NULL,
    lo_quantity         INTEGER      NOT NULL,
    lo_extendedprice    INTEGER      NOT NULL,
    lo_ordtotalprice    INTEGER      NOT NULL,
    lo_discount         INTEGER      NOT NULL,
    lo_revenue          INTEGER      NOT NULL,
    lo_supplycost       INTEGER      NOT NULL,
    lo_tax              INTEGER      NOT NULL,
    lo_commitdate       INTEGER      NOT NULL,
    lo_shipmode         VARCHAR(10)  NOT NULL
);

-- Citus settings as for TPC-H: no limit on intermediate results, repartition joins allowed
ALTER SYSTEM SET citus.max_intermediate_result_size TO -1;
ALTER SYSTEM SET citus.enable_repartition_joins TO 1;
SELECT pg_reload_conf();

SELECT create_distributed_table('public.customer', 'c_custkey');
SELECT create_distributed_table('public.supplier', 's_suppkey');
SELECT create_distributed_table('public.part', 'p_partkey');
SELECT create_distributed_table('public.dates', 'd_datekey');
SELECT create_distributed_table('public.lineorder', 'lo_orderkey');
