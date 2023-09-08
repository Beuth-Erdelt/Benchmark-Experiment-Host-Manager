COPY INTO customer FROM '/data/tpch/SF3/customer.tbl' DELIMITERS '|' NULL AS '';
COPY INTO lineitem FROM '/data/tpch/SF3/lineitem.tbl' DELIMITERS '|' NULL AS '';
COPY INTO nation FROM '/data/tpch/SF3/nation.tbl' DELIMITERS '|' NULL AS '';
COPY INTO orders FROM '/data/tpch/SF3/orders.tbl' DELIMITERS '|' NULL AS '';
COPY INTO part FROM '/data/tpch/SF3/part.tbl' DELIMITERS '|' NULL AS '';
COPY INTO partsupp FROM '/data/tpch/SF3/partsupp.tbl' DELIMITERS '|' NULL AS '';
COPY INTO region FROM '/data/tpch/SF3/region.tbl' DELIMITERS '|' NULL AS '';
COPY INTO supplier FROM '/data/tpch/SF3/supplier.tbl' DELIMITERS '|' NULL AS '';
