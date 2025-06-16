-- sccsid:     @(#)dss.ri       2.1.8.1
-- tpcd benchmark version 8.0

-- for table region
alter table {BEXHOMA_SCHEMA}.region
add primary key (r_regionkey);

-- for table nation
alter table {BEXHOMA_SCHEMA}.nation
add primary key (n_nationkey);

-- for table part
alter table {BEXHOMA_SCHEMA}.part
add primary key (p_partkey);

-- for table supplier
alter table {BEXHOMA_SCHEMA}.supplier
add primary key (s_suppkey);

-- for table partsupp
alter table {BEXHOMA_SCHEMA}.partsupp
add primary key (ps_partkey,ps_suppkey);

-- for table customer
alter table {BEXHOMA_SCHEMA}.customer
add primary key (c_custkey);

-- for table lineitem
alter table {BEXHOMA_SCHEMA}.lineitem
add primary key (l_orderkey,l_linenumber);

-- for table orders
alter table {BEXHOMA_SCHEMA}.orders
add primary key (o_orderkey);




-- for table nation
alter table {BEXHOMA_SCHEMA}.nation
add foreign key (n_regionkey) references {BEXHOMA_SCHEMA}.region(r_regionkey);

-- for table supplier
-- alter table {BEXHOMA_SCHEMA}.supplier
-- add foreign key (s_nationkey) references nation(n_nationkey);

-- for table customer
alter table {BEXHOMA_SCHEMA}.customer
add foreign key (c_nationkey) references {BEXHOMA_SCHEMA}.nation(n_nationkey);

-- for table partsupp
alter table {BEXHOMA_SCHEMA}.partsupp
add foreign key (ps_suppkey) references {BEXHOMA_SCHEMA}.supplier(s_suppkey);

alter table {BEXHOMA_SCHEMA}.partsupp
add foreign key (ps_partkey) references {BEXHOMA_SCHEMA}.part(p_partkey);

-- for table orders
alter table {BEXHOMA_SCHEMA}.orders
add foreign key (o_custkey) references {BEXHOMA_SCHEMA}.customer(c_custkey);

-- for table lineitem
alter table {BEXHOMA_SCHEMA}.lineitem
add foreign key (l_orderkey)  references {BEXHOMA_SCHEMA}.orders(o_orderkey);

alter table {BEXHOMA_SCHEMA}.lineitem
add foreign key (l_partkey) references 
        {BEXHOMA_SCHEMA}.part(p_partkey);

alter table {BEXHOMA_SCHEMA}.lineitem
add foreign key (l_suppkey) references 
        {BEXHOMA_SCHEMA}.supplier(s_suppkey);

alter table {BEXHOMA_SCHEMA}.lineitem
add foreign key (l_partkey,l_suppkey) references 
        {BEXHOMA_SCHEMA}.partsupp(ps_partkey,ps_suppkey);


