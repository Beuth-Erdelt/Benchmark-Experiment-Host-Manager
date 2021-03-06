COPY public.customer FROM '/data/tpch/SF100/customer.tbl' DELIMITER '|' null '';
COPY public.lineitem FROM '/data/tpch/SF100/lineitem.tbl' DELIMITER '|' null '';
COPY public.nation FROM '/data/tpch/SF100/nation.tbl' DELIMITER '|' null '';
COPY public.orders FROM '/data/tpch/SF100/orders.tbl' DELIMITER '|' null '';
COPY public.part FROM '/data/tpch/SF100/part.tbl' DELIMITER '|' null '';
COPY public.partsupp FROM '/data/tpch/SF100/partsupp.tbl' DELIMITER '|' null '';
COPY public.region FROM '/data/tpch/SF100/region.tbl' DELIMITER '|' null '';
COPY public.supplier FROM '/data/tpch/SF100/supplier.tbl' DELIMITER '|' null '';
