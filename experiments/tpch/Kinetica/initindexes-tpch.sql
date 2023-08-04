-- indexes for foreign keys

-- for table region
-- alter table region
-- add primary key (r_regionkey);

-- for table nation
-- alter table nation
-- add primary key (n_nationkey);

alter table nation ADD INDEX (n_regionkey);

-- for table part
-- alter table part
-- add primary key (p_partkey);

-- for table supplier
-- alter table supplier
-- add primary key (s_suppkey);

-- alter table supplier (s_nationkey);

-- for table partsupp
-- alter table partsupp
-- add primary key (ps_partkey,ps_suppkey);

-- for table customer
-- alter table customer
-- add primary key (c_custkey);

alter table customer ADD INDEX (c_nationkey);

-- for table partsupp
alter table partsupp ADD INDEX (ps_suppkey);

alter table partsupp ADD INDEX (ps_partkey);

-- for table lineitem
-- alter table lineitem
-- add primary key (l_orderkey,l_linenumber);

-- for table orders
-- alter table orders
-- add primary key (o_orderkey);

alter table orders ADD INDEX (o_custkey);

-- for table lineitem
alter table lineitem ADD INDEX (l_orderkey);

-- alter table lineitem (l_partkey);

-- alter table lineitem (l_suppkey);

-- alter table lineitem ADD INDEX (l_partkey,l_suppkey);
alter table lineitem ADD INDEX (l_partkey);
alter table lineitem ADD INDEX (l_suppkey);

