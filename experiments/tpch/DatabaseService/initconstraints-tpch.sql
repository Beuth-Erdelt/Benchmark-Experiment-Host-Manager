-- sccsid:     @(#)dss.ri       2.1.8.1
-- tpcd benchmark version 8.0

-- for table region
alter table public.region
add primary key (r_regionkey);

-- for table nation
alter table public.nation
add primary key (n_nationkey);

-- for table part
alter table public.part
add primary key (p_partkey);

-- for table supplier
alter table public.supplier
add primary key (s_suppkey);

-- for table partsupp
alter table public.partsupp
add primary key (ps_partkey,ps_suppkey);

-- for table customer
alter table public.customer
add primary key (c_custkey);

-- for table lineitem
alter table public.lineitem
add primary key (l_orderkey,l_linenumber);

-- for table orders
alter table public.orders
add primary key (o_orderkey);




-- for table nation
alter table public.nation
add foreign key (n_regionkey) references region(r_regionkey);

-- for table supplier
-- alter table public.supplier
-- add foreign key (s_nationkey) references nation(n_nationkey);

-- for table customer
alter table public.customer
add foreign key (c_nationkey) references nation(n_nationkey);

-- for table partsupp
alter table public.partsupp
add foreign key (ps_suppkey) references supplier(s_suppkey);

alter table public.partsupp
add foreign key (ps_partkey) references part(p_partkey);

-- for table orders
alter table public.orders
add foreign key (o_custkey) references customer(c_custkey);

-- for table lineitem
alter table public.lineitem
add foreign key (l_orderkey)  references orders(o_orderkey);

alter table public.lineitem
add foreign key (l_partkey) references 
        part(p_partkey);

alter table public.lineitem
add foreign key (l_suppkey) references 
        supplier(s_suppkey);

alter table public.lineitem
add foreign key (l_partkey,l_suppkey) references 
        partsupp(ps_partkey,ps_suppkey);


