-- indexes for foreign keys

-- for table region
-- alter table {BEXHOMA_SCHEMA}.region
-- add primary key (r_regionkey);

-- for table nation
-- alter table {BEXHOMA_SCHEMA}.nation
-- add primary key (n_nationkey);

create index on {BEXHOMA_SCHEMA}.nation (n_regionkey);

-- for table part
-- alter table {BEXHOMA_SCHEMA}.part
-- add primary key (p_partkey);

-- for table supplier
-- alter table {BEXHOMA_SCHEMA}.supplier
-- add primary key (s_suppkey);

-- create index on {BEXHOMA_SCHEMA}.supplier (s_nationkey);

-- for table partsupp
-- alter table {BEXHOMA_SCHEMA}.partsupp
-- add primary key (ps_partkey,ps_suppkey);

-- for table customer
-- alter table {BEXHOMA_SCHEMA}.customer
-- add primary key (c_custkey);

create index on {BEXHOMA_SCHEMA}.customer (c_nationkey);

-- for table partsupp
create index on {BEXHOMA_SCHEMA}.partsupp (ps_suppkey);

create index on {BEXHOMA_SCHEMA}.partsupp (ps_partkey);

-- for table lineitem
-- alter table {BEXHOMA_SCHEMA}.lineitem
-- add primary key (l_orderkey,l_linenumber);

-- for table orders
-- alter table {BEXHOMA_SCHEMA}.orders
-- add primary key (o_orderkey);

create index on {BEXHOMA_SCHEMA}.orders (o_custkey);

-- for table lineitem
create index on {BEXHOMA_SCHEMA}.lineitem (l_orderkey);

-- create index on {BEXHOMA_SCHEMA}.lineitem (l_partkey);

-- create index on {BEXHOMA_SCHEMA}.lineitem (l_suppkey);

create index on {BEXHOMA_SCHEMA}.lineitem (l_partkey,l_suppkey);

