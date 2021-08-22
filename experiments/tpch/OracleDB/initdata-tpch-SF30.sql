COPY public.customer FROM '/data/tpch/SF30/customer.tbl' DELIMITER '|';
COPY public.lineitem FROM '/data/tpch/SF30/lineitem.tbl' DELIMITER '|';
COPY public.nation FROM '/data/tpch/SF30/nation.tbl' DELIMITER '|';
COPY public.orders FROM '/data/tpch/SF30/orders.tbl' DELIMITER '|';
COPY public.part FROM '/data/tpch/SF30/part.tbl' DELIMITER '|';
COPY public.partsupp FROM '/data/tpch/SF30/partsupp.tbl' DELIMITER '|';
COPY public.region FROM '/data/tpch/SF30/region.tbl' DELIMITER '|';
COPY public.supplier FROM '/data/tpch/SF30/supplier.tbl' DELIMITER '|';
