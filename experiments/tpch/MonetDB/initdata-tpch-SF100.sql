COPY 15000000 RECORDS INTO customer FROM '/data/tpch/SF100/customer.tbl' DELIMITERS '|';
COPY 610000000 RECORDS INTO lineitem FROM '/data/tpch/SF100/lineitem.tbl' DELIMITERS '|';
COPY 25 RECORDS INTO nation FROM '/data/tpch/SF100/nation.tbl' DELIMITERS '|';
COPY 150000000 RECORDS INTO orders FROM '/data/tpch/SF100/orders.tbl' DELIMITERS '|';
COPY 20000000 RECORDS INTO part FROM '/data/tpch/SF100/part.tbl' DELIMITERS '|';
COPY 80000000 RECORDS INTO partsupp FROM '/data/tpch/SF100/partsupp.tbl' DELIMITERS '|';
COPY 5 RECORDS INTO region FROM '/data/tpch/SF100/region.tbl' DELIMITERS '|';
COPY 1000000 RECORDS INTO supplier FROM '/data/tpch/SF100/supplier.tbl' DELIMITERS '|';
