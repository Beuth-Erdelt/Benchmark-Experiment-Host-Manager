-- SQL*Loader control file of TPC-H table nation (loader_oracle); BEXHOMA_TABLE is replaced by <schema>.nation
LOAD DATA
CHARACTERSET AL32UTF8
APPEND
INTO TABLE BEXHOMA_TABLE
FIELDS TERMINATED BY '|'
TRAILING NULLCOLS
(
    n_nationkey,
    n_name,
    n_regionkey,
    n_comment CHAR(152)
)
