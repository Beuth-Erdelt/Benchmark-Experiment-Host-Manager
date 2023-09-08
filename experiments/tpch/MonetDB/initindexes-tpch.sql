-- indexes for foreign keys

-- for table region
-- alter table region
-- add primary key (r_regionkey);

-- for table nation
-- alter table nation
-- add primary key (n_nationkey);

create index n_r on nation (n_regionkey);

-- for table part
-- alter table part
-- add primary key (p_partkey);

-- for table supplier
-- alter table supplier
-- add primary key (s_suppkey);

-- create index s_n on supplier (s_nationkey);

-- for table partsupp
-- alter table partsupp
-- add primary key (ps_partkey,ps_suppkey);

-- for table customer
-- alter table customer
-- add primary key (c_custkey);

create index c_n on customer (c_nationkey);

-- for table partsupp
create index ps_s on partsupp (ps_suppkey);

create index ps_p on partsupp (ps_partkey);

-- for table lineitem
-- alter table lineitem
-- add primary key (l_orderkey,l_linenumber);

-- for table orders
-- alter table orders
-- add primary key (o_orderkey);

create index o_c on orders (o_custkey);

-- for table lineitem
create index l_o on lineitem (l_orderkey);

create index l_p on lineitem (l_partkey);

create index l_s on lineitem (l_suppkey);

create index l_ps on lineitem (l_partkey,l_suppkey);

