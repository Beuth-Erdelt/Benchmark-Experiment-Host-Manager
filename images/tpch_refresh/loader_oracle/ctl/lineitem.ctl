-- SQL*Loader control file of TPC-H table lineitem (tpch_refresh/loader_oracle, RF1); BEXHOMA_TABLE is replaced by <schema>.lineitem
LOAD DATA
CHARACTERSET AL32UTF8
APPEND
INTO TABLE BEXHOMA_TABLE
FIELDS TERMINATED BY '|'
TRAILING NULLCOLS
(
    l_orderkey,
    l_partkey,
    l_suppkey,
    l_linenumber,
    l_quantity,
    l_extendedprice,
    l_discount,
    l_tax,
    l_returnflag,
    l_linestatus,
    l_shipdate DATE "YYYY-MM-DD",
    l_commitdate DATE "YYYY-MM-DD",
    l_receiptdate DATE "YYYY-MM-DD",
    l_shipinstruct,
    l_shipmode,
    l_comment CHAR(44)
)
