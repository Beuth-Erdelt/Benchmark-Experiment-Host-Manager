-- SQL*Loader control file of TPC-H table partsupp (loader_oracle); BEXHOMA_TABLE is replaced by <schema>.partsupp
LOAD DATA
CHARACTERSET AL32UTF8
APPEND
INTO TABLE BEXHOMA_TABLE
FIELDS TERMINATED BY '|'
TRAILING NULLCOLS
(
    ps_partkey,
    ps_suppkey,
    ps_availqty,
    ps_supplycost,
    ps_comment CHAR(199)
)
