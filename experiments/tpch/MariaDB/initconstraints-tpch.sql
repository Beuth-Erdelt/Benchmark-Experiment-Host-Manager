-- sccsid:     @(#)dss.ri	2.1.8.1
-- tpcd benchmark version 8.0


-- for table region
alter table tpch.region
add primary key (r_regionkey);

-- for table nation
alter table tpch.nation
add primary key (n_nationkey);

-- for table part
alter table tpch.part
add primary key (p_partkey);

-- for table supplier
alter table tpch.supplier
add primary key (s_suppkey);

-- for table partsupp
alter table tpch.partsupp
add primary key (ps_partkey,ps_suppkey);

-- for table customer
alter table tpch.customer
add primary key (c_custkey);

-- for table lineitem
alter table tpch.lineitem
add primary key (l_orderkey,l_linenumber);

-- for table orders
alter table tpch.orders
add primary key (o_orderkey);



-- for table nation
alter table tpch.nation
add foreign key (n_regionkey) references tpch.region(r_regionkey);

-- for table supplier
-- alter table tpch.supplier
-- add foreign key (s_nationkey) references tpch.nation(n_nationkey);

-- for table customer
alter table tpch.customer
add foreign key (c_nationkey) references tpch.nation(n_nationkey);

-- for table partsupp
alter table tpch.partsupp
add foreign key (ps_suppkey) references tpch.supplier(s_suppkey);

alter table tpch.partsupp
add foreign key (ps_partkey) references tpch.part(p_partkey);

-- for table orders
alter table tpch.orders
add foreign key (o_custkey) references tpch.customer(c_custkey);

-- for table lineitem
alter table tpch.lineitem
add foreign key (l_orderkey)  references tpch.orders(o_orderkey);

alter table tpch.lineitem
add foreign key (l_partkey) references 
        tpch.part(p_partkey);

alter table tpch.lineitem
add foreign key (l_suppkey) references 
        tpch.supplier(s_suppkey);

alter table tpch.lineitem
add foreign key (l_partkey,l_suppkey) references 
        tpch.partsupp(ps_partkey,ps_suppkey);



