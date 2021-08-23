COPY public.customer FROM '/data/tpch/SF100/customer.tbl' DELIMITER '|';
COPY public.lineitem FROM '/data/tpch/SF100/lineitem.tbl' DELIMITER '|';
COPY public.nation FROM '/data/tpch/SF100/nation.tbl' DELIMITER '|';
COPY public.orders FROM '/data/tpch/SF100/orders.tbl' DELIMITER '|';
COPY public.part FROM '/data/tpch/SF100/part.tbl' DELIMITER '|';
COPY public.partsupp FROM '/data/tpch/SF100/partsupp.tbl' DELIMITER '|';
COPY public.region FROM '/data/tpch/SF100/region.tbl' DELIMITER '|';
COPY public.supplier FROM '/data/tpch/SF100/supplier.tbl' DELIMITER '|';
