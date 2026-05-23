-- Benchmark-Experiment-Host-Manager | experiments/tpch/OmniSci
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Older OmniSci TPC-H schema using BIGINT keys and DECIMAL(16,2) for
--          monetary values. A fixed fragment_size of 64 000 000 rows is set on
--          every table. customer and orders are sharded on the customer key
--          (shard_count = 1, effectively no distribution). lineitem has no
--          shard key in this variant. See initschema-tpch-Nshards.sql for
--          multi-shard variants.

DROP TABLE IF EXISTS NATION;
CREATE TABLE NATION (
    N_NATIONKEY  BIGINT,
    N_NAME       TEXT ENCODING DICT,
    N_REGIONKEY  BIGINT,
    N_COMMENT    TEXT ENCODING DICT
) WITH (fragment_size = 64000000);

DROP TABLE IF EXISTS REGION;
CREATE TABLE REGION (
    R_REGIONKEY  BIGINT,
    R_NAME       TEXT ENCODING DICT,
    R_COMMENT    TEXT ENCODING DICT
) WITH (fragment_size = 64000000);

DROP TABLE IF EXISTS PART;
CREATE TABLE PART (
    P_PARTKEY      BIGINT,
    P_NAME         TEXT ENCODING DICT,
    P_MFGR         TEXT ENCODING DICT,
    P_BRAND        TEXT ENCODING DICT,
    P_TYPE         TEXT ENCODING DICT,
    P_SIZE         INTEGER,
    P_CONTAINER    TEXT ENCODING DICT,
    P_RETAILPRICE  DECIMAL(16,2),
    P_COMMENT      TEXT ENCODING DICT
) WITH (fragment_size = 64000000);

DROP TABLE IF EXISTS SUPPLIER;
CREATE TABLE SUPPLIER (
    S_SUPPKEY    BIGINT,
    S_NAME       TEXT ENCODING DICT,
    S_ADDRESS    TEXT ENCODING DICT,
    S_NATIONKEY  BIGINT,
    S_PHONE      TEXT ENCODING DICT,
    S_ACCTBAL    DECIMAL(16,2),
    S_COMMENT    TEXT ENCODING DICT
) WITH (fragment_size = 64000000);

DROP TABLE IF EXISTS PARTSUPP;
CREATE TABLE PARTSUPP (
    PS_PARTKEY     BIGINT,
    PS_SUPPKEY     BIGINT,
    PS_AVAILQTY    INTEGER,
    PS_SUPPLYCOST  DECIMAL(16,2),
    PS_COMMENT     TEXT ENCODING DICT
) WITH (fragment_size = 64000000);

-- customer and orders are sharded together on the customer key so that
-- joins between them are co-located on the same shard.
DROP TABLE IF EXISTS CUSTOMER;
CREATE TABLE CUSTOMER (
    C_CUSTKEY     BIGINT,
    C_NAME        TEXT ENCODING DICT,
    C_ADDRESS     TEXT ENCODING DICT,
    C_NATIONKEY   BIGINT,
    C_PHONE       TEXT ENCODING DICT,
    C_ACCTBAL     DECIMAL(16,2),
    C_MKTSEGMENT  TEXT ENCODING DICT,
    C_COMMENT     TEXT ENCODING DICT,
    SHARD KEY (C_CUSTKEY)
) WITH (fragment_size = 64000000, shard_count = 1, partitions = 'sharded');

DROP TABLE IF EXISTS ORDERS;
CREATE TABLE ORDERS (
    O_ORDERKEY       BIGINT,
    O_CUSTKEY        BIGINT,
    O_ORDERSTATUS    TEXT ENCODING DICT,
    O_TOTALPRICE     DECIMAL(16,2),
    O_ORDERDATE      DATE,
    O_ORDERPRIORITY  TEXT ENCODING DICT,
    O_CLERK          TEXT ENCODING DICT,
    O_SHIPPRIORITY   INTEGER,
    O_COMMENT        TEXT ENCODING DICT,
    SHARD KEY (O_CUSTKEY)
) WITH (fragment_size = 64000000, shard_count = 1, partitions = 'sharded');

DROP TABLE IF EXISTS LINEITEM;
CREATE TABLE LINEITEM (
    L_ORDERKEY       BIGINT,
    L_PARTKEY        BIGINT,
    L_SUPPKEY        BIGINT,
    L_LINENUMBER     INTEGER,
    L_QUANTITY       INTEGER,
    L_EXTENDEDPRICE  DECIMAL(16,2),
    L_DISCOUNT       DECIMAL(16,2),
    L_TAX            DECIMAL(16,2),
    L_RETURNFLAG     TEXT ENCODING DICT,
    L_LINESTATUS     TEXT ENCODING DICT,
    L_SHIPDATE       DATE,
    L_COMMITDATE     DATE,
    L_RECEIPTDATE    DATE,
    L_SHIPINSTRUCT   TEXT ENCODING DICT,
    L_SHIPMODE       TEXT ENCODING DICT,
    L_COMMENT        TEXT ENCODING DICT
) WITH (fragment_size = 64000000);
