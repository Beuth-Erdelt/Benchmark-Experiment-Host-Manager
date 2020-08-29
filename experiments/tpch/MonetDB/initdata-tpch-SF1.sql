COPY INTO customer FROM '/data/tpch/SF1/customer.tbl' DELIMITERS '|';
COPY INTO lineitem FROM '/data/tpch/SF1/lineitem.tbl' DELIMITERS '|';
COPY INTO nation FROM '/data/tpch/SF1/nation.tbl' DELIMITERS '|';
COPY INTO orders FROM '/data/tpch/SF1/orders.tbl' DELIMITERS '|';
COPY INTO part FROM '/data/tpch/SF1/part.tbl' DELIMITERS '|';
COPY INTO partsupp FROM '/data/tpch/SF1/partsupp.tbl' DELIMITERS '|';
COPY INTO region FROM '/data/tpch/SF1/region.tbl' DELIMITERS '|';
COPY INTO supplier FROM '/data/tpch/SF1/supplier.tbl' DELIMITERS '|';
