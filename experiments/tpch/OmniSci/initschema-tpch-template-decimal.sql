-- Benchmark-Experiment-Host-Manager | experiments/tpch/OmniSci
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Bexhoma template for OmniSci TPC-H using INTEGER keys and DOUBLE
--          for monetary/quantity values (avoids DECIMAL overhead for GPU queries).
--          The placeholders {fragment_size} and {shard_count} are substituted
--          at runtime by the Bexhoma framework.
--          Dimension tables are replicated; orders/lineitem are sharded.
--          Contrast with initschema-tpch-decimal.sql (same keys, DECIMAL(16,2)).

DROP TABLE IF EXISTS NATION;
CREATE TABLE NATION (
    N_NATIONKEY  INTEGER,
    N_NAME       TEXT ENCODING DICT,
    N_REGIONKEY  INTEGER,
    N_COMMENT    TEXT ENCODING DICT
) WITH (fragment_size = {fragment_size}, partitions = 'replicated');

DROP TABLE IF EXISTS REGION;
CREATE TABLE REGION (
    R_REGIONKEY  INTEGER,
    R_NAME       TEXT ENCODING DICT,
    R_COMMENT    TEXT ENCODING DICT
) WITH (fragment_size = {fragment_size}, partitions = 'replicated');

DROP TABLE IF EXISTS PART;
CREATE TABLE PART (
    P_PARTKEY      INTEGER,
    P_NAME         TEXT ENCODING DICT,
    P_MFGR         TEXT ENCODING DICT,
    P_BRAND        TEXT ENCODING DICT,
    P_TYPE         TEXT ENCODING DICT,
    P_SIZE         INTEGER,
    P_CONTAINER    TEXT ENCODING DICT,
    P_RETAILPRICE  DOUBLE,
    P_COMMENT      TEXT ENCODING DICT
) WITH (fragment_size = {fragment_size}, partitions = 'replicated');

DROP TABLE IF EXISTS SUPPLIER;
CREATE TABLE SUPPLIER (
    S_SUPPKEY    INTEGER,
    S_NAME       TEXT ENCODING DICT,
    S_ADDRESS    TEXT ENCODING DICT,
    S_NATIONKEY  INTEGER,
    S_PHONE      TEXT ENCODING DICT,
    S_ACCTBAL    DOUBLE,
    S_COMMENT    TEXT ENCODING DICT
) WITH (fragment_size = {fragment_size}, partitions = 'replicated');

DROP TABLE IF EXISTS PARTSUPP;
CREATE TABLE PARTSUPP (
    PS_PARTKEY     INTEGER,
    PS_SUPPKEY     INTEGER,
    PS_AVAILQTY    INTEGER,
    PS_SUPPLYCOST  DOUBLE,
    PS_COMMENT     TEXT ENCODING DICT
) WITH (fragment_size = {fragment_size}, partitions = 'replicated');

DROP TABLE IF EXISTS CUSTOMER;
CREATE TABLE CUSTOMER (
    C_CUSTKEY     INTEGER,
    C_NAME        TEXT ENCODING DICT,
    C_ADDRESS     TEXT ENCODING DICT,
    C_NATIONKEY   INTEGER,
    C_PHONE       TEXT ENCODING DICT,
    C_ACCTBAL     DOUBLE,
    C_MKTSEGMENT  TEXT ENCODING DICT,
    C_COMMENT     TEXT ENCODING DICT
) WITH (fragment_size = {fragment_size}, partitions = 'replicated');

DROP TABLE IF EXISTS ORDERS;
CREATE TABLE ORDERS (
    O_ORDERKEY       INTEGER,
    O_CUSTKEY        INTEGER,
    O_ORDERSTATUS    TEXT ENCODING DICT,
    O_TOTALPRICE     DOUBLE,
    O_ORDERDATE      DATE,
    O_ORDERPRIORITY  TEXT ENCODING DICT,
    O_CLERK          TEXT ENCODING DICT,
    O_SHIPPRIORITY   INTEGER,
    O_COMMENT        TEXT ENCODING DICT,
    SHARD KEY (O_CUSTKEY)
) WITH (fragment_size = {fragment_size}, shard_count = {shard_count}, partitions = 'sharded');

DROP TABLE IF EXISTS LINEITEM;
CREATE TABLE LINEITEM (
    L_ORDERKEY       INTEGER,
    L_PARTKEY        INTEGER,
    L_SUPPKEY        INTEGER,
    L_LINENUMBER     INTEGER,
    L_QUANTITY       INTEGER,
    L_EXTENDEDPRICE  DOUBLE,
    L_DISCOUNT       DOUBLE,
    L_TAX            DOUBLE,
    L_RETURNFLAG     TEXT ENCODING DICT,
    L_LINESTATUS     TEXT ENCODING DICT,
    L_SHIPDATE       DATE,
    L_COMMITDATE     DATE,
    L_RECEIPTDATE    DATE,
    L_SHIPINSTRUCT   TEXT ENCODING DICT,
    L_SHIPMODE       TEXT ENCODING DICT,
    L_COMMENT        TEXT ENCODING DICT,
    SHARD KEY (L_ORDERKEY)
) WITH (fragment_size = {fragment_size}, shard_count = {shard_count}, partitions = 'sharded');
