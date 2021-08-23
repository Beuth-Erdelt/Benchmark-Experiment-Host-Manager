alter session set "_oracle_script"=true;

CREATE USER tpch IDENTIFIED BY tpch;

GRANT CREATE SESSION,
      CREATE TABLE,
      CREATE VIEW,
      UNLIMITED TABLESPACE
    TO tpch;

CREATE OR REPLACE DIRECTORY tpch_dir AS '/tmp/SF1/';

GRANT READ, WRITE ON DIRECTORY tpch_dir TO tpch;

-- 1.4.1
--  per 1.4.2.1  all table columns may be defined NOT NULL

CREATE TABLE tpch.ext_part
(
    p_partkey       NUMBER(10, 0),
    p_name          VARCHAR2(55),
    p_mfgr          CHAR(25),
    p_brand         CHAR(10),
    p_type          VARCHAR2(25),
    p_size          INTEGER,
    p_container     CHAR(10),
    p_retailprice   NUMBER,
    p_comment       VARCHAR2(23)
)
ORGANIZATION EXTERNAL
    (TYPE oracle_loader
          DEFAULT DIRECTORY tpch_dir
              ACCESS PARAMETERS (
                  FIELDS
                      TERMINATED BY '|'
                  MISSING FIELD VALUES ARE NULL
              )
          LOCATION('part.tbl'));

CREATE TABLE tpch.part
(
    p_partkey       NUMBER(10, 0) NOT NULL,
    p_name          VARCHAR2(55) NOT NULL,
    p_mfgr          CHAR(25) NOT NULL,
    p_brand         CHAR(10) NOT NULL,
    p_type          VARCHAR2(25) NOT NULL,
    p_size          INTEGER NOT NULL,
    p_container     CHAR(10) NOT NULL,
    p_retailprice   NUMBER NOT NULL,
    p_comment       VARCHAR2(23) NOT NULL
);


CREATE TABLE tpch.ext_supplier
(
    s_suppkey     NUMBER(10, 0),
    s_name        CHAR(25),
    s_address     VARCHAR2(40),
    s_nationkey   NUMBER(10, 0),
    s_phone       CHAR(15),
    s_acctbal     NUMBER,
    s_comment     VARCHAR2(101)
)
ORGANIZATION EXTERNAL
    (TYPE oracle_loader
          DEFAULT DIRECTORY tpch_dir
              ACCESS PARAMETERS (
                  FIELDS
                      TERMINATED BY '|'
                  MISSING FIELD VALUES ARE NULL
              )
          LOCATION('supplier.tbl'));

CREATE TABLE tpch.supplier
(
    s_suppkey     NUMBER(10, 0) NOT NULL,
    s_name        CHAR(25) NOT NULL,
    s_address     VARCHAR2(40) NOT NULL,
    s_nationkey   NUMBER(10, 0) NOT NULL,
    s_phone       CHAR(15) NOT NULL,
    s_acctbal     NUMBER NOT NULL,
    s_comment     VARCHAR2(101) NOT NULL
);

CREATE TABLE tpch.ext_partsupp
(
    ps_partkey      NUMBER(10, 0),
    ps_suppkey      NUMBER(10, 0),
    ps_availqty     INTEGER,
    ps_supplycost   NUMBER,
    ps_comment      VARCHAR2(199)
)
ORGANIZATION EXTERNAL
    (TYPE oracle_loader
          DEFAULT DIRECTORY tpch_dir
              ACCESS PARAMETERS (
                  FIELDS
                      TERMINATED BY '|'
                  MISSING FIELD VALUES ARE NULL
              )
          LOCATION('partsupp.tbl'));

CREATE TABLE tpch.partsupp
(
    ps_partkey      NUMBER(10, 0) NOT NULL,
    ps_suppkey      NUMBER(10, 0) NOT NULL,
    ps_availqty     INTEGER NOT NULL,
    ps_supplycost   NUMBER NOT NULL,
    ps_comment      VARCHAR2(199) NOT NULL
);

CREATE TABLE tpch.ext_customer
(
    c_custkey      NUMBER(10, 0),
    c_name         VARCHAR2(25),
    c_address      VARCHAR2(40),
    c_nationkey    NUMBER(10, 0),
    c_phone        CHAR(15),
    c_acctbal      NUMBER,
    c_mktsegment   CHAR(10),
    c_comment      VARCHAR2(117)
)
ORGANIZATION EXTERNAL
    (TYPE oracle_loader
          DEFAULT DIRECTORY tpch_dir
              ACCESS PARAMETERS (
                  FIELDS
                      TERMINATED BY '|'
                  MISSING FIELD VALUES ARE NULL
              )
          LOCATION('customer.tbl'));

CREATE TABLE tpch.customer
(
    c_custkey      NUMBER(10, 0) NOT NULL,
    c_name         VARCHAR2(25) NOT NULL,
    c_address      VARCHAR2(40) NOT NULL,
    c_nationkey    NUMBER(10, 0) NOT NULL,
    c_phone        CHAR(15) NOT NULL,
    c_acctbal      NUMBER NOT NULL,
    c_mktsegment   CHAR(10) NOT NULL,
    c_comment      VARCHAR2(117) NOT NULL
);

-- read date values as yyyy-mm-dd text

CREATE TABLE tpch.ext_orders
(
    o_orderkey        NUMBER(10, 0),
    o_custkey         NUMBER(10, 0),
    o_orderstatus     CHAR(1),
    o_totalprice      NUMBER,
    o_orderdate       CHAR(10),
    o_orderpriority   CHAR(15),
    o_clerk           CHAR(15),
    o_shippriority    INTEGER,
    o_comment         VARCHAR2(79)
)
ORGANIZATION EXTERNAL
    (TYPE oracle_loader
          DEFAULT DIRECTORY tpch_dir
              ACCESS PARAMETERS (
                  FIELDS
                      TERMINATED BY '|'
                  MISSING FIELD VALUES ARE NULL
              )
          LOCATION('orders.tbl'));

CREATE TABLE tpch.orders
(
    o_orderkey        NUMBER(10, 0) NOT NULL,
    o_custkey         NUMBER(10, 0) NOT NULL,
    o_orderstatus     CHAR(1) NOT NULL,
    o_totalprice      NUMBER NOT NULL,
    o_orderdate       DATE NOT NULL,
    o_orderpriority   CHAR(15) NOT NULL,
    o_clerk           CHAR(15) NOT NULL,
    o_shippriority    INTEGER NOT NULL,
    o_comment         VARCHAR2(79) NOT NULL
);

-- read date values as yyyy-mm-dd text

CREATE TABLE tpch.ext_lineitem
(
    l_orderkey        NUMBER(10, 0),
    l_partkey         NUMBER(10, 0),
    l_suppkey         NUMBER(10, 0),
    l_linenumber      INTEGER,
    l_quantity        NUMBER,
    l_extendedprice   NUMBER,
    l_discount        NUMBER,
    l_tax             NUMBER,
    l_returnflag      CHAR(1),
    l_linestatus      CHAR(1),
    l_shipdate        CHAR(10),
    l_commitdate      CHAR(10),
    l_receiptdate     CHAR(10),
    l_shipinstruct    CHAR(25),
    l_shipmode        CHAR(10),
    l_comment         VARCHAR2(44)
)
ORGANIZATION EXTERNAL
    (TYPE oracle_loader
          DEFAULT DIRECTORY tpch_dir
              ACCESS PARAMETERS (
                  FIELDS
                      TERMINATED BY '|'
                  MISSING FIELD VALUES ARE NULL
              )
          LOCATION('lineitem.tbl'));

CREATE TABLE tpch.lineitem
(
    l_orderkey        NUMBER(10, 0),
    l_partkey         NUMBER(10, 0),
    l_suppkey         NUMBER(10, 0),
    l_linenumber      INTEGER,
    l_quantity        NUMBER,
    l_extendedprice   NUMBER,
    l_discount        NUMBER,
    l_tax             NUMBER,
    l_returnflag      CHAR(1),
    l_linestatus      CHAR(1),
    l_shipdate        DATE,
    l_commitdate      DATE,
    l_receiptdate     DATE,
    l_shipinstruct    CHAR(25),
    l_shipmode        CHAR(10),
    l_comment         VARCHAR2(44)
);

CREATE TABLE tpch.ext_nation
(
    n_nationkey   NUMBER(10, 0),
    n_name        CHAR(25),
    n_regionkey   NUMBER(10, 0),
    n_comment     VARCHAR(152)
)
ORGANIZATION EXTERNAL
    (TYPE oracle_loader
          DEFAULT DIRECTORY tpch_dir
              ACCESS PARAMETERS (
                  FIELDS
                      TERMINATED BY '|'
                  MISSING FIELD VALUES ARE NULL
              )
          LOCATION('nation.tbl'));

CREATE TABLE tpch.nation
(
    n_nationkey   NUMBER(10, 0),
    n_name        CHAR(25),
    n_regionkey   NUMBER(10, 0),
    n_comment     VARCHAR(152)
);

CREATE TABLE tpch.ext_region
(
    r_regionkey   NUMBER(10, 0),
    r_name        CHAR(25),
    r_comment     VARCHAR(152)
)
ORGANIZATION EXTERNAL
    (TYPE oracle_loader
          DEFAULT DIRECTORY tpch_dir
              ACCESS PARAMETERS (
                  FIELDS
                      TERMINATED BY '|'
                  MISSING FIELD VALUES ARE NULL
              )
          LOCATION('region.tbl'));

CREATE TABLE tpch.region
(
    r_regionkey   NUMBER(10, 0),
    r_name        CHAR(25),
    r_comment     VARCHAR(152)
);



TRUNCATE TABLE tpch.part;
TRUNCATE TABLE tpch.supplier;
TRUNCATE TABLE tpch.partsupp;
TRUNCATE TABLE tpch.customer;
TRUNCATE TABLE tpch.orders;
TRUNCATE TABLE tpch.lineitem;
TRUNCATE TABLE tpch.nation;
TRUNCATE TABLE tpch.region;



