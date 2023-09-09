-- https://github.com/cockroachdb/cockroach/blob/master/pkg/workload/tpch/tpch.go

ALTER TABLE nation ADD CONSTRAINT nation_fkey_region FOREIGN KEY (n_regionkey) REFERENCES region (r_regionkey) NOT VALID;

ALTER TABLE supplier ADD CONSTRAINT supplier_fkey_nation FOREIGN KEY (s_nationkey) REFERENCES nation (n_nationkey) NOT VALID;

ALTER TABLE partsupp ADD CONSTRAINT partsupp_fkey_part FOREIGN KEY (ps_partkey) REFERENCES part (p_partkey) NOT VALID;

ALTER TABLE partsupp ADD CONSTRAINT partsupp_fkey_supplier FOREIGN KEY (ps_suppkey) REFERENCES supplier (s_suppkey) NOT VALID;

ALTER TABLE customer ADD CONSTRAINT customer_fkey_nation FOREIGN KEY (c_nationkey) REFERENCES nation (n_nationkey) NOT VALID;

ALTER TABLE orders ADD CONSTRAINT orders_fkey_customer FOREIGN KEY (o_custkey) REFERENCES customer (c_custkey) NOT VALID;

ALTER TABLE lineitem ADD CONSTRAINT lineitem_fkey_orders FOREIGN KEY (l_orderkey) REFERENCES orders (o_orderkey) NOT VALID;

ALTER TABLE lineitem ADD CONSTRAINT lineitem_fkey_part FOREIGN KEY (l_partkey) REFERENCES part (p_partkey) NOT VALID;

ALTER TABLE lineitem ADD CONSTRAINT lineitem_fkey_supplier FOREIGN KEY (l_suppkey) REFERENCES supplier (s_suppkey) NOT VALID;
