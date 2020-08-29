-- sccsid:     @(#)dss.ri	2.1.8.1
-- tpcd benchmark version 8.0

-- for table region
alter table tpch.region
add index using hash (r_regionkey);

-- for table nation
alter table tpch.nation
add index using hash (n_nationkey);

alter table tpch.nation
add index using hash (n_regionkey);

-- for table part
alter table tpch.part
add index using hash (p_partkey);

-- for table supplier
alter table tpch.supplier
add index using hash (s_suppkey);

alter table tpch.supplier
add index using hash (s_nationkey);

-- for table partsupp
-- alter table tpch.partsupp
-- add index using hash (ps_partkey,ps_suppkey);

-- for table customer
alter table tpch.customer
add index using hash (c_custkey);

alter table tpch.customer
add index using hash (c_nationkey);

-- for table lineitem
-- alter table tpch.lineitem
-- add index using hash (l_orderkey,l_linenumber);

-- for table orders
alter table tpch.orders
add index using hash (o_orderkey);

-- for table partsupp
alter table tpch.partsupp
add index using hash (ps_suppkey);

alter table tpch.partsupp
add index using hash (ps_partkey);

-- for table orders
alter table tpch.orders
add index using hash (o_custkey);


-- for table lineitem
alter table tpch.lineitem
add index using hash (l_orderkey);


-- alter table tpch.lineitem
-- add index using hash (l_partkey,l_suppkey) references 
--        partsupp(ps_partkey,ps_suppkey);



