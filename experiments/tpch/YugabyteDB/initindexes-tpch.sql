-- indexes for foreign keys

-- for table region
-- alter table public.region
-- add primary key (r_regionkey);

-- for table nation
-- alter table public.nation
-- add primary key (n_nationkey);

create index on public.nation (n_regionkey);

-- for table part
-- alter table public.part
-- add primary key (p_partkey);

-- for table supplier
-- alter table public.supplier
-- add primary key (s_suppkey);

-- create index on public.supplier (s_nationkey);

-- for table partsupp
-- alter table public.partsupp
-- add primary key (ps_partkey,ps_suppkey);

-- for table customer
-- alter table public.customer
-- add primary key (c_custkey);

create index on public.customer (c_nationkey);

-- for table partsupp
create index on public.partsupp (ps_suppkey);

create index on public.partsupp (ps_partkey);

-- for table lineitem
-- alter table public.lineitem
-- add primary key (l_orderkey,l_linenumber);

-- for table orders
-- alter table public.orders
-- add primary key (o_orderkey);

create index on public.orders (o_custkey);

-- for table lineitem
create index on public.lineitem (l_orderkey);

-- create index on public.lineitem (l_partkey);

-- create index on public.lineitem (l_suppkey);

create index on public.lineitem (l_partkey,l_suppkey);

