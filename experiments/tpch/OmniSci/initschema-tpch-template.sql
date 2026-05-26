-- Benchmark-Experiment-Host-Manager | experiments/tpch/OmniSci
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Bexhoma template for the OmniSci TPC-H schema.
--          The placeholders {fragment_size} and {shard_count} are substituted
--          at runtime by the Bexhoma framework before execution.
--          Dimension tables (all except orders and lineitem) are replicated
--          across all nodes. orders is sharded on o_custkey; lineitem is
--          sharded on l_orderkey for efficient order-key joins.
--          Key columns use TEXT ENCODING DICT(32); string data TEXT ENCODING DICT.

DROP TABLE IF EXISTS NATION;
CREATE TABLE NATION (
    N_NATIONKEY  TEXT ENCODING DICT(32),
    N_NAME       TEXT ENCODING DICT,
    N_REGIONKEY  TEXT ENCODING DICT(32),
    N_COMMENT    TEXT ENCODING DICT
) WITH (fragment_size = {fragment_size}, partitions = 'replicated');

DROP TABLE IF EXISTS REGION;
CREATE TABLE REGION (
    R_REGIONKEY  TEXT ENCODING DICT(32),
    R_NAME       TEXT ENCODING DICT,
    R_COMMENT    TEXT ENCODING DICT
) WITH (fragment_size = {fragment_size}, partitions = 'replicated');

DROP TABLE IF EXISTS PART;
CREATE TABLE PART (
    P_PARTKEY      TEXT ENCODING DICT(32),
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
    S_SUPPKEY    TEXT ENCODING DICT(32),
    S_NAME       TEXT ENCODING DICT,
    S_ADDRESS    TEXT ENCODING DICT,
    S_NATIONKEY  TEXT ENCODING DICT(32),
    S_PHONE      TEXT ENCODING DICT,
    S_ACCTBAL    DOUBLE,
    S_COMMENT    TEXT ENCODING DICT
) WITH (fragment_size = {fragment_size}, partitions = 'replicated');

DROP TABLE IF EXISTS PARTSUPP;
CREATE TABLE PARTSUPP (
    PS_PARTKEY     TEXT ENCODING DICT(32),
    PS_SUPPKEY     TEXT ENCODING DICT(32),
    PS_AVAILQTY    INTEGER,
    PS_SUPPLYCOST  DOUBLE,
    PS_COMMENT     TEXT ENCODING DICT
) WITH (fragment_size = {fragment_size}, partitions = 'replicated');

DROP TABLE IF EXISTS CUSTOMER;
CREATE TABLE CUSTOMER (
    C_CUSTKEY     TEXT ENCODING DICT(32),
    C_NAME        TEXT ENCODING DICT,
    C_ADDRESS     TEXT ENCODING DICT,
    C_NATIONKEY   TEXT ENCODING DICT(32),
    C_PHONE       TEXT ENCODING DICT,
    C_ACCTBAL     DOUBLE,
    C_MKTSEGMENT  TEXT ENCODING DICT,
    C_COMMENT     TEXT ENCODING DICT
) WITH (fragment_size = {fragment_size}, partitions = 'replicated');

-- orders sharded on o_custkey to co-locate with customer rows.
DROP TABLE IF EXISTS ORDERS;
CREATE TABLE ORDERS (
    O_ORDERKEY       TEXT ENCODING DICT(32),
    O_CUSTKEY        TEXT ENCODING DICT(32),
    O_ORDERSTATUS    TEXT ENCODING DICT,
    O_TOTALPRICE     DOUBLE,
    O_ORDERDATE      DATE,
    O_ORDERPRIORITY  TEXT ENCODING DICT,
    O_CLERK          TEXT ENCODING DICT,
    O_SHIPPRIORITY   INTEGER,
    O_COMMENT        TEXT ENCODING DICT,
    SHARD KEY (O_CUSTKEY)
) WITH (fragment_size = {fragment_size}, shard_count = {shard_count}, partitions = 'sharded');

-- lineitem sharded on l_orderkey to co-locate with orders rows.
DROP TABLE IF EXISTS LINEITEM;
CREATE TABLE LINEITEM (
    L_ORDERKEY       TEXT ENCODING DICT(32),
    L_PARTKEY        TEXT ENCODING DICT(32),
    L_SUPPKEY        TEXT ENCODING DICT(32),
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
