COPY INTO customer FROM '/data/tpch/SF10/customer.tbl' DELIMITERS '|';
COPY INTO lineitem FROM '/data/tpch/SF10/lineitem.tbl' DELIMITERS '|';
COPY INTO nation FROM '/data/tpch/SF10/nation.tbl' DELIMITERS '|';
COPY INTO orders FROM '/data/tpch/SF10/orders.tbl' DELIMITERS '|';
COPY INTO part FROM '/data/tpch/SF10/part.tbl' DELIMITERS '|';
COPY INTO partsupp FROM '/data/tpch/SF10/partsupp.tbl' DELIMITERS '|';
COPY INTO region FROM '/data/tpch/SF10/region.tbl' DELIMITERS '|';
COPY INTO supplier FROM '/data/tpch/SF10/supplier.tbl' DELIMITERS '|';
