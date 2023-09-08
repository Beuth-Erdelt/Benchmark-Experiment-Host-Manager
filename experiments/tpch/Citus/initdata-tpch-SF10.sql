COPY public.customer FROM '/data/tpch/SF10/customer.tbl' DELIMITER '|' null '';
COPY public.lineitem FROM '/data/tpch/SF10/lineitem.tbl' DELIMITER '|' null '';
COPY public.nation FROM '/data/tpch/SF10/nation.tbl' DELIMITER '|' null '';
COPY public.orders FROM '/data/tpch/SF10/orders.tbl' DELIMITER '|' null '';
COPY public.part FROM '/data/tpch/SF10/part.tbl' DELIMITER '|' null '';
COPY public.partsupp FROM '/data/tpch/SF10/partsupp.tbl' DELIMITER '|' null '';
COPY public.region FROM '/data/tpch/SF10/region.tbl' DELIMITER '|' null '';
COPY public.supplier FROM '/data/tpch/SF10/supplier.tbl' DELIMITER '|' null '';

-- rebalance the shards over the new worker nodes
SELECT get_rebalance_table_shards_plan();
SELECT rebalance_table_shards();

