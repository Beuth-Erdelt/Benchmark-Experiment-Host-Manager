-- sccsid:     @(#)dss.ri	2.1.8.1
-- tpcd benchmark version 8.0

-- for table nation
alter table nation
add foreign key (n_regionkey) references region(r_regionkey);

-- for table supplier
alter table supplier
add foreign key (s_nationkey) references nation(n_nationkey);

-- for table customer
alter table customer
add foreign key (c_nationkey) references nation(n_nationkey);

-- for table partsupp
alter table partsupp
add foreign key (ps_suppkey) references supplier(s_suppkey);

alter table partsupp
add foreign key (ps_partkey) references part(p_partkey);

-- for table orders
alter table orders
add foreign key (o_custkey) references customer(c_custkey);

-- for table lineitem
alter table lineitem
add foreign key (l_orderkey)  references orders(o_orderkey);

alter table lineitem
add foreign key (l_partkey,l_suppkey) references 
        partsupp(ps_partkey,ps_suppkey);



