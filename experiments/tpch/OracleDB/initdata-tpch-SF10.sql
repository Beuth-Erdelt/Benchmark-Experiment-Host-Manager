COPY public.customer FROM '/data/tpch/SF10/customer.tbl' DELIMITER '|';
COPY public.lineitem FROM '/data/tpch/SF10/lineitem.tbl' DELIMITER '|';
COPY public.nation FROM '/data/tpch/SF10/nation.tbl' DELIMITER '|';
COPY public.orders FROM '/data/tpch/SF10/orders.tbl' DELIMITER '|';
COPY public.part FROM '/data/tpch/SF10/part.tbl' DELIMITER '|';
COPY public.partsupp FROM '/data/tpch/SF10/partsupp.tbl' DELIMITER '|';
COPY public.region FROM '/data/tpch/SF10/region.tbl' DELIMITER '|';
COPY public.supplier FROM '/data/tpch/SF10/supplier.tbl' DELIMITER '|';
