-- SQL*Loader control file of TPC-H table supplier (loader_oracle); BEXHOMA_TABLE is replaced by <schema>.supplier
LOAD DATA
CHARACTERSET AL32UTF8
APPEND
INTO TABLE BEXHOMA_TABLE
FIELDS TERMINATED BY '|'
TRAILING NULLCOLS
(
    s_suppkey,
    s_name,
    s_address,
    s_nationkey,
    s_phone,
    s_acctbal,
    s_comment CHAR(101)
)
