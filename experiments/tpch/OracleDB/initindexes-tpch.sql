ALTER TABLE tpch.part
    ADD CONSTRAINT pk_part PRIMARY KEY(p_partkey);

ALTER TABLE tpch.supplier
    ADD CONSTRAINT pk_supplier PRIMARY KEY(s_suppkey);

ALTER TABLE tpch.partsupp
    ADD CONSTRAINT pk_partsupp PRIMARY KEY(ps_partkey, ps_suppkey);

ALTER TABLE tpch.customer
    ADD CONSTRAINT pk_customer PRIMARY KEY(c_custkey);

ALTER TABLE tpch.orders
    ADD CONSTRAINT pk_orders PRIMARY KEY(o_orderkey);

ALTER TABLE tpch.lineitem
    ADD CONSTRAINT pk_lineitem PRIMARY KEY(l_linenumber, l_orderkey);

ALTER TABLE tpch.nation
    ADD CONSTRAINT pk_nation PRIMARY KEY(n_nationkey);

ALTER TABLE tpch.region
    ADD CONSTRAINT pk_region PRIMARY KEY(r_regionkey);

-- 1.4.2.3

ALTER TABLE tpch.partsupp
    ADD CONSTRAINT fk_partsupp_part FOREIGN KEY(ps_partkey) REFERENCES tpch.part(p_partkey);

ALTER TABLE tpch.partsupp
    ADD CONSTRAINT fk_partsupp_supplier FOREIGN KEY(ps_suppkey) REFERENCES tpch.supplier(s_suppkey);

ALTER TABLE tpch.customer
    ADD CONSTRAINT fk_customer_nation FOREIGN KEY(c_nationkey) REFERENCES tpch.nation(n_nationkey);

ALTER TABLE tpch.orders
    ADD CONSTRAINT fk_orders_customer FOREIGN KEY(o_custkey) REFERENCES tpch.customer(c_custkey);

ALTER TABLE tpch.lineitem
    ADD CONSTRAINT fk_lineitem_order FOREIGN KEY(l_orderkey) REFERENCES tpch.orders(o_orderkey);

ALTER TABLE tpch.lineitem
    ADD CONSTRAINT fk_lineitem_part FOREIGN KEY(l_partkey) REFERENCES tpch.part(p_partkey);

ALTER TABLE tpch.lineitem
    ADD CONSTRAINT fk_lineitem_supplier FOREIGN KEY(l_suppkey) REFERENCES tpch.supplier(s_suppkey);

ALTER TABLE tpch.lineitem
    ADD CONSTRAINT fk_lineitem_partsupp FOREIGN KEY(l_partkey, l_suppkey)
        REFERENCES tpch.partsupp(ps_partkey, ps_suppkey);

