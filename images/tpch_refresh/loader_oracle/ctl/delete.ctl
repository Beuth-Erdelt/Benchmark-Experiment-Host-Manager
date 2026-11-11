-- SQL*Loader control file of the order keys of RF2 (tpch_refresh/loader_oracle); BEXHOMA_TABLE is replaced by the staging table
LOAD DATA
CHARACTERSET AL32UTF8
APPEND
INTO TABLE BEXHOMA_TABLE
FIELDS TERMINATED BY '|'
TRAILING NULLCOLS
(
    orderkey
)
