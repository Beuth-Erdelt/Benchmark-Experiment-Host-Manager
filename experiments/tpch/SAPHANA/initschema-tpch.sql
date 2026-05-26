-- Benchmark-Experiment-Host-Manager | experiments/tpch/SAPHANA
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create the TPCH schema and all TPC-H tables in SAP HANA.
--          CREATE COLUMN TABLE places each table in HANA's columnar storage
--          engine, which is optimal for analytical (TPC-H) workloads.
--          Identifiers follow the HANA convention of double-quoted uppercase names.
--          Primary keys are declared inline; foreign keys are added in
--          initconstraints-tpch.sql.

CREATE SCHEMA TPCH OWNED BY SYSTEM;

CREATE COLUMN TABLE "TPCH"."CUSTOMER" (
    C_CUSTKEY     INTEGER       NOT NULL,
    C_NAME        VARCHAR(25)   NOT NULL,
    C_ADDRESS     VARCHAR(40)   NOT NULL,
    C_NATIONKEY   INTEGER       NOT NULL,
    C_PHONE       CHAR(15)      NOT NULL,
    C_ACCTBAL     DECIMAL(15,2) NOT NULL,
    C_MKTSEGMENT  CHAR(10)      NOT NULL,
    C_COMMENT     VARCHAR(117)  NOT NULL,
    PRIMARY KEY (C_CUSTKEY)
);

CREATE COLUMN TABLE "TPCH"."LINEITEM" (
    L_ORDERKEY       INTEGER       NOT NULL,
    L_PARTKEY        INTEGER       NOT NULL,
    L_SUPPKEY        INTEGER       NOT NULL,
    L_LINENUMBER     INTEGER       NOT NULL,
    L_QUANTITY       DECIMAL(15,2) NOT NULL,
    L_EXTENDEDPRICE  DECIMAL(15,2) NOT NULL,
    L_DISCOUNT       DECIMAL(15,2) NOT NULL,
    L_TAX            DECIMAL(15,2) NOT NULL,
    L_RETURNFLAG     CHAR          NOT NULL,
    L_LINESTATUS     CHAR          NOT NULL,
    L_SHIPDATE       DATE          NOT NULL,
    L_COMMITDATE     DATE          NOT NULL,
    L_RECEIPTDATE    DATE          NOT NULL,
    L_SHIPINSTRUCT   CHAR(25)      NOT NULL,
    L_SHIPMODE       CHAR(10)      NOT NULL,
    L_COMMENT        VARCHAR(44)   NOT NULL,
    PRIMARY KEY (L_ORDERKEY, L_LINENUMBER)
);

CREATE COLUMN TABLE "TPCH"."NATION" (
    N_NATIONKEY  INTEGER      NOT NULL,
    N_NAME       CHAR(25)     NOT NULL,
    N_REGIONKEY  INTEGER      NOT NULL,
    N_COMMENT    VARCHAR(152) NOT NULL,
    PRIMARY KEY (N_NATIONKEY)
);

CREATE COLUMN TABLE "TPCH"."ORDERS" (
    O_ORDERKEY       INTEGER       NOT NULL,
    O_CUSTKEY        INTEGER       NOT NULL,
    O_ORDERSTATUS    CHAR          NOT NULL,
    O_TOTALPRICE     DECIMAL(15,2) NOT NULL,
    O_ORDERDATE      DATE          NOT NULL,
    O_ORDERPRIORITY  CHAR(15)      NOT NULL,
    O_CLERK          CHAR(15)      NOT NULL,
    O_SHIPPRIORITY   INTEGER       NOT NULL,
    O_COMMENT        VARCHAR(79)   NOT NULL,
    PRIMARY KEY (O_ORDERKEY)
);

CREATE COLUMN TABLE "TPCH"."PART" (
    P_PARTKEY      INTEGER       NOT NULL,
    P_NAME         VARCHAR(55)   NOT NULL,
    P_MFGR         CHAR(25)      NOT NULL,
    P_BRAND        CHAR(10)      NOT NULL,
    P_TYPE         VARCHAR(25)   NOT NULL,
    P_SIZE         INTEGER       NOT NULL,
    P_CONTAINER    CHAR(10)      NOT NULL,
    P_RETAILPRICE  DECIMAL(15,2) NOT NULL,
    P_COMMENT      VARCHAR(23)   NOT NULL,
    PRIMARY KEY (P_PARTKEY)
);

CREATE COLUMN TABLE "TPCH"."PARTSUPP" (
    PS_PARTKEY     INTEGER       NOT NULL,
    PS_SUPPKEY     INTEGER       NOT NULL,
    PS_AVAILQTY    INTEGER       NOT NULL,
    PS_SUPPLYCOST  DECIMAL(15,2) NOT NULL,
    PS_COMMENT     VARCHAR(199)  NOT NULL,
    PRIMARY KEY (PS_PARTKEY, PS_SUPPKEY)
);

CREATE COLUMN TABLE "TPCH"."REGION" (
    R_REGIONKEY  INTEGER      NOT NULL,
    R_NAME       CHAR(25)     NOT NULL,
    R_COMMENT    VARCHAR(152) NOT NULL,
    PRIMARY KEY (R_REGIONKEY)
);

CREATE COLUMN TABLE "TPCH"."SUPPLIER" (
    S_SUPPKEY    INTEGER       NOT NULL,
    S_NAME       CHAR(25)      NOT NULL,
    S_ADDRESS    VARCHAR(40)   NOT NULL,
    S_NATIONKEY  INTEGER       NOT NULL,
    S_PHONE      CHAR(15)      NOT NULL,
    S_ACCTBAL    DECIMAL(15,2) NOT NULL,
    S_COMMENT    VARCHAR(101)  NOT NULL,
    PRIMARY KEY (S_SUPPKEY)
);
