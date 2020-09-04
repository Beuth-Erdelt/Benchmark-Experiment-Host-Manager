-- sccsid:     @(#)dss.ri	2.1.8.1
-- tpcd benchmark version 8.0

-- for table nation
alter table public.nation
add foreign key (n_regionkey) references public.region(r_regionkey);

-- for table supplier
alter table public.supplier
add foreign key (s_nationkey) references public.nation(n_nationkey);

-- for table customer
alter table public.customer
add foreign key (c_nationkey) references public.nation(n_nationkey);

-- for table partsupp
alter table public.partsupp
add foreign key (ps_suppkey) references public.supplier(s_suppkey);

alter table public.partsupp
add foreign key (ps_partkey) references public.part(p_partkey);

-- for table orders
alter table public.orders
add foreign key (o_custkey) references public.customer(c_custkey);

-- for table lineitem
alter table public.lineitem
add foreign key (l_orderkey)  references public.orders(o_orderkey);

alter table public.lineitem
add foreign key (l_partkey,l_suppkey) references 
        public.partsupp(ps_partkey,ps_suppkey);



