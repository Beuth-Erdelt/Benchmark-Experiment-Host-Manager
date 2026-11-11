-- SQL*Loader control file of TPC-H table region (loader_oracle); BEXHOMA_TABLE is replaced by <schema>.region
LOAD DATA
CHARACTERSET AL32UTF8
APPEND
INTO TABLE BEXHOMA_TABLE
FIELDS TERMINATED BY '|'
TRAILING NULLCOLS
(
    r_regionkey,
    r_name,
    r_comment CHAR(152)
)
