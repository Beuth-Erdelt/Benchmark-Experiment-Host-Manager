-- SQL*Loader control file of TPC-H table customer (loader_oracle); BEXHOMA_TABLE is replaced by <schema>.customer
LOAD DATA
CHARACTERSET AL32UTF8
APPEND
INTO TABLE BEXHOMA_TABLE
FIELDS TERMINATED BY '|'
TRAILING NULLCOLS
(
    c_custkey,
    c_name,
    c_address,
    c_nationkey,
    c_phone,
    c_acctbal,
    c_mktsegment,
    c_comment CHAR(117)
)
