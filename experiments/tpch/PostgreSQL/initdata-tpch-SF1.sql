COPY public.customer FROM '/data/tpch/SF1/customer.tbl' DELIMITER '|' null '';
COPY public.lineitem FROM '/data/tpch/SF1/lineitem.tbl' DELIMITER '|' null '';
COPY public.nation FROM '/data/tpch/SF1/nation.tbl' DELIMITER '|' null '';
COPY public.orders FROM '/data/tpch/SF1/orders.tbl' DELIMITER '|' null '';
COPY public.part FROM '/data/tpch/SF1/part.tbl' DELIMITER '|' null '';
COPY public.partsupp FROM '/data/tpch/SF1/partsupp.tbl' DELIMITER '|' null '';
COPY public.region FROM '/data/tpch/SF1/region.tbl' DELIMITER '|' null '';
COPY public.supplier FROM '/data/tpch/SF1/supplier.tbl' DELIMITER '|' null '';
