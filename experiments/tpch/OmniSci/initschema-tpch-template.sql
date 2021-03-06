DROP TABLE IF EXISTS PART;
CREATE TABLE PART (
 P_PARTKEY INTEGER NOT NULL,
 P_NAME TEXT NOT NULL ENCODING DICT(32),
 P_MFGR TEXT NOT NULL ENCODING DICT(32),
 P_BRAND TEXT NOT NULL ENCODING DICT(32),
 P_TYPE TEXT NOT NULL ENCODING DICT(32),
 P_SIZE INTEGER NOT NULL,
 P_CONTAINER TEXT NOT NULL ENCODING DICT(32),
 P_RETAILPRICE DECIMAL(16,2),
 P_COMMENT TEXT NOT NULL ENCODING DICT(32)
) with (fragment_size={fragment_size}, partitions='replicated');

DROP TABLE IF EXISTS SUPPLIER;
CREATE TABLE SUPPLIER (
 S_SUPPKEY INTEGER NOT NULL,
 S_NAME TEXT NOT NULL ENCODING DICT(32),
 S_ADDRESS TEXT NOT NULL ENCODING DICT(32),
 S_NATIONKEY INTEGER NOT NULL,
 S_PHONE TEXT NOT NULL ENCODING DICT(32),
 S_ACCTBAL DECIMAL(16,2) NOT NULL,
 S_COMMENT TEXT NOT NULL ENCODING DICT(32)
) with (fragment_size={fragment_size}, partitions='replicated');

DROP TABLE IF EXISTS PARTSUPP ;
CREATE TABLE PARTSUPP (
 PS_PARTKEY INTEGER NOT NULL,
 PS_SUPPKEY INTEGER NOT NULL,
 PS_AVAILQTY INTEGER NOT NULL,
 PS_SUPPLYCOST DECIMAL(16,2) NOT NULL,
 PS_COMMENT TEXT NOT NULL ENCODING DICT(32)
) with (fragment_size={fragment_size}, partitions='replicated');

DROP TABLE IF EXISTS CUSTOMER;
CREATE TABLE CUSTOMER (
 C_CUSTKEY INTEGER NOT NULL,
 C_NAME TEXT NOT NULL ENCODING DICT(32),
 C_ADDRESS TEXT NOT NULL ENCODING DICT(32),
 C_NATIONKEY INTEGER NOT NULL,
 C_PHONE TEXT NOT NULL ENCODING DICT(32),
 C_ACCTBAL DECIMAL(16,2) NOT NULL,
 C_MKTSEGMENT TEXT NOT NULL ENCODING DICT(32),
 C_COMMENT TEXT NOT NULL ENCODING DICT(32)
) with (fragment_size={fragment_size}, partitions='replicated');

DROP TABLE IF EXISTS ORDERS ;
CREATE TABLE ORDERS (
  O_ORDERKEY INTEGER NOT NULL,
  O_CUSTKEY INTEGER NOT NULL,
  O_ORDERSTATUS TEXT NOT NULL ENCODING DICT(8),
  O_TOTALPRICE DECIMAL(18,2) NOT NULL,
  O_ORDERDATE DATE NOT NULL ENCODING DAYS(16),
  O_ORDERPRIORITY TEXT NOT NULL ENCODING DICT(32),
  O_CLERK TEXT NOT NULL ENCODING DICT(32),
  O_SHIPPRIORITY INTEGER NOT NULL,
  O_COMMENT TEXT NOT NULL ENCODING DICT(32),
 SHARD KEY (O_ORDERKEY)
) with (fragment_size={fragment_size}, shard_count = {shard_count}, partitions='sharded');

DROP TABLE IF EXISTS LINEITEM ;
CREATE TABLE LINEITEM (
  L_ORDERKEY INTEGER NOT NULL,
  L_PARTKEY INTEGER NOT NULL,
  L_SUPPKEY INTEGER NOT NULL,
  L_LINENUMBER INTEGER NOT NULL,
  L_QUANTITY DECIMAL(10,2) NOT NULL,
  L_EXTENDEDPRICE DECIMAL(16,2) NOT NULL,
  L_DISCOUNT DECIMAL(16,2) NOT NULL,
  L_TAX DECIMAL(16,2) NOT NULL,
  L_RETURNFLAG TEXT NOT NULL ENCODING DICT(8),
  L_LINESTATUS TEXT NOT NULL ENCODING DICT(8),
  L_SHIPDATE DATE NOT NULL ENCODING DAYS(16),
  L_COMMITDATE DATE NOT NULL ENCODING DAYS(16),
  L_RECEIPTDATE DATE NOT NULL ENCODING DAYS(16),
  L_SHIPINSTRUCT TEXT NOT NULL ENCODING DICT(8),
  L_SHIPMODE TEXT NOT NULL ENCODING DICT(8),
  L_COMMENT TEXT NOT NULL ENCODING DICT(32),
 SHARD KEY (L_ORDERKEY)
) with (fragment_size={fragment_size}, shard_count = {shard_count}, partitions='sharded');

DROP TABLE IF EXISTS NATION ;
CREATE TABLE NATION (
 N_NATIONKEY INTEGER NOT NULL,
 N_NAME TEXT NOT NULL ENCODING DICT(32),
 N_REGIONKEY INTEGER NOT NULL,
 N_COMMENT TEXT NOT NULL ENCODING DICT(32)
) with (fragment_size={fragment_size}, partitions='replicated');

DROP TABLE IF EXISTS REGION ;
CREATE TABLE REGION (
 R_REGIONKEY INTEGER NOT NULL,
 R_NAME TEXT NOT NULL ENCODING DICT(32),
 R_COMMENT TEXT NOT NULL ENCODING DICT(32)
) with (fragment_size={fragment_size}, partitions='replicated');
