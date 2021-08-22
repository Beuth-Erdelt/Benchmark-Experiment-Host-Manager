-- 1.4.2.4 - 1

ALTER TABLE tpch.part
    ADD CONSTRAINT chk_part_partkey CHECK(p_partkey >= 0);

ALTER TABLE tpch.supplier
    ADD CONSTRAINT chk_supplier_suppkey CHECK(s_suppkey >= 0);

ALTER TABLE tpch.customer
    ADD CONSTRAINT chk_customer_custkey CHECK(c_custkey >= 0);

ALTER TABLE tpch.partsupp
    ADD CONSTRAINT chk_partsupp_partkey CHECK(ps_partkey >= 0);

ALTER TABLE tpch.region
    ADD CONSTRAINT chk_region_regionkey CHECK(r_regionkey >= 0);

ALTER TABLE tpch.nation
    ADD CONSTRAINT chk_nation_nationkey CHECK(n_nationkey >= 0);

-- 1.4.2.4 - 2

ALTER TABLE tpch.part
    ADD CONSTRAINT chk_part_size CHECK(p_size >= 0);

ALTER TABLE tpch.part
    ADD CONSTRAINT chk_part_retailprice CHECK(p_retailprice >= 0);

ALTER TABLE tpch.partsupp
    ADD CONSTRAINT chk_partsupp_availqty CHECK(ps_availqty >= 0);

ALTER TABLE tpch.partsupp
    ADD CONSTRAINT chk_partsupp_supplycost CHECK(ps_supplycost >= 0);

ALTER TABLE tpch.orders
    ADD CONSTRAINT chk_orders_totalprice CHECK(o_totalprice >= 0);

ALTER TABLE tpch.lineitem
    ADD CONSTRAINT chk_lineitem_quantity CHECK(l_quantity >= 0);

ALTER TABLE tpch.lineitem
    ADD CONSTRAINT chk_lineitem_extendedprice CHECK(l_extendedprice >= 0);

ALTER TABLE tpch.lineitem
    ADD CONSTRAINT chk_lineitem_tax CHECK(l_tax >= 0);

-- 1.4.2.4 - 3

ALTER TABLE tpch.lineitem
    ADD CONSTRAINT chk_lineitem_discount CHECK(l_discount >= 0.00 AND l_discount <= 1.00);

