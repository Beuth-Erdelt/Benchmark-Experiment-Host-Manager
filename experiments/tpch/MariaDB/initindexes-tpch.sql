-- indexes for foreign keys

-- for table region
alter table tpch.region
add primary key (r_regionkey);

-- for table nation
alter table tpch.nation
add primary key (n_nationkey);

create index n_r on tpch.nation (n_regionkey);

-- for table part
alter table tpch.part
add primary key (p_partkey);

-- for table supplier
alter table tpch.supplier
add primary key (s_suppkey);

create index s_n on tpch.supplier (s_nationkey);

-- for table partsupp
alter table tpch.partsupp
add primary key (ps_partkey,ps_suppkey);

-- for table customer
alter table tpch.customer
add primary key (c_custkey);

create index c_n on tpch.customer (c_nationkey);

-- for table partsupp
create index ps_s on tpch.partsupp (ps_suppkey);

create index ps_p on tpch.partsupp (ps_partkey);

-- for table lineitem
alter table tpch.lineitem
add primary key (l_orderkey,l_linenumber);

-- for table orders
alter table tpch.orders
add primary key (o_orderkey);

create index o_c on tpch.orders (o_custkey);

-- for table lineitem
create index l_o on tpch.lineitem (l_orderkey);

create index l_ps on tpch.lineitem (l_partkey,l_suppkey);

