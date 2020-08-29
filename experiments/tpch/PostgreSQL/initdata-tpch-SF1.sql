COPY public.customer FROM '/data/tpch/SF1/customer.tbl' DELIMITER '|';
COPY public.lineitem FROM '/data/tpch/SF1/lineitem.tbl' DELIMITER '|';
COPY public.nation FROM '/data/tpch/SF1/nation.tbl' DELIMITER '|';
COPY public.orders FROM '/data/tpch/SF1/orders.tbl' DELIMITER '|';
COPY public.part FROM '/data/tpch/SF1/part.tbl' DELIMITER '|';
COPY public.partsupp FROM '/data/tpch/SF1/partsupp.tbl' DELIMITER '|';
COPY public.region FROM '/data/tpch/SF1/region.tbl' DELIMITER '|';
COPY public.supplier FROM '/data/tpch/SF1/supplier.tbl' DELIMITER '|';
