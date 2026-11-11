-- SQL*Loader control file of TPC-H table orders (loader_oracle); BEXHOMA_TABLE is replaced by <schema>.orders
LOAD DATA
CHARACTERSET AL32UTF8
APPEND
INTO TABLE BEXHOMA_TABLE
FIELDS TERMINATED BY '|'
TRAILING NULLCOLS
(
    o_orderkey,
    o_custkey,
    o_orderstatus,
    o_totalprice,
    o_orderdate DATE "YYYY-MM-DD",
    o_orderpriority,
    o_clerk,
    o_shippriority,
    o_comment CHAR(79)
)
