CREATE SCHEMA TPCH OWNED BY SYSTEM;


CREATE COLUMN TABLE "TPCH"."CUSTOMER" (
   C_CUSTKEY            integer                        not null,
   C_NAME               varchar(25)                    not null,
   C_ADDRESS            varchar(40)                    not null,
   C_NATIONKEY          integer                        not null,
   C_PHONE              char(15)                       not null,
   C_ACCTBAL            decimal(15,2)                  not null,
   C_MKTSEGMENT         char(10)                       not null,
   C_COMMENT            varchar(117)                   not null,
   primary key (C_CUSTKEY)
);

CREATE COLUMN TABLE "TPCH"."LINEITEM" (
    L_ORDERKEY           integer                        not null,
    L_PARTKEY            integer                        not null,
    L_SUPPKEY            integer                        not null,
    L_LINENUMBER         integer                        not null,
    L_QUANTITY           decimal(15,2)                  not null,
    L_EXTENDEDPRICE      decimal(15,2)                  not null,
    L_DISCOUNT           decimal(15,2)                  not null,
    L_TAX                decimal(15,2)                  not null,
    L_RETURNFLAG         char                           not null,
    L_LINESTATUS         char                           not null,
    L_SHIPDATE           date                           not null,
    L_COMMITDATE         date                           not null,
    L_RECEIPTDATE        date                           not null,
    L_SHIPINSTRUCT       char(25)                       not null,
    L_SHIPMODE           char(10)                       not null,
    L_COMMENT            varchar(44)                    not null,
    primary key (L_ORDERKEY, L_LINENUMBER)
);

CREATE COLUMN TABLE "TPCH"."NATION" (
    N_NATIONKEY          integer                        not null,
    N_NAME               char(25)                       not null,
    N_REGIONKEY          integer                        not null,
    N_COMMENT            varchar(152)                   not null,
    primary key (N_NATIONKEY)
);

CREATE COLUMN TABLE "TPCH"."ORDERS" (
    O_ORDERKEY           integer                        not null,
    O_CUSTKEY            integer                        not null,
    O_ORDERSTATUS        char                           not null,
    O_TOTALPRICE         decimal(15,2)                  not null,
    O_ORDERDATE          date                           not null,
    O_ORDERPRIORITY      char(15)                       not null,
    O_CLERK              char(15)                       not null,
    O_SHIPPRIORITY       integer                        not null,
    O_COMMENT            varchar(79)                    not null,
    primary key (O_ORDERKEY)
);

CREATE COLUMN TABLE "TPCH"."PART" (
    P_PARTKEY            integer                        not null,
    P_NAME               varchar(55)                    not null,
    P_MFGR               char(25)                       not null,
    P_BRAND              char(10)                       not null,
    P_TYPE               varchar(25)                    not null,
    P_SIZE               integer                        not null,
    P_CONTAINER          char(10)                       not null,
    P_RETAILPRICE        decimal(15,2)                  not null,
    P_COMMENT            varchar(23)                    not null,
    primary key (P_PARTKEY)
);

CREATE COLUMN TABLE "TPCH"."PARTSUPP" (
    PS_PARTKEY           integer                        not null,
    PS_SUPPKEY           integer                        not null,
    PS_AVAILQTY          integer                        not null,
    PS_SUPPLYCOST        decimal(15,2)                  not null,
    PS_COMMENT           varchar(199)                   not null,
    primary key (PS_PARTKEY, PS_SUPPKEY)
);

CREATE COLUMN TABLE "TPCH"."REGION" (
    R_REGIONKEY          integer                        not null,
    R_NAME               char(25)                       not null,
    R_COMMENT            varchar(152)                   not null,
    primary key (R_REGIONKEY)
);

CREATE COLUMN TABLE "TPCH"."SUPPLIER" (
    S_SUPPKEY            integer                        not null,
    S_NAME               char(25)                       not null,
    S_ADDRESS            varchar(40)                    not null,
    S_NATIONKEY          integer                        not null,
    S_PHONE              char(15)                       not null,
    S_ACCTBAL            decimal(15,2)                  not null,
    S_COMMENT            varchar(101)                   not null,
    primary key (S_SUPPKEY)
);

