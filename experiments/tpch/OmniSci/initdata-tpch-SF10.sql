
COPY customer FROM '/data/tpch/SF10/customer.tbl'
WITH (delimiter='|', header='false', quoted='false');
COPY lineitem FROM '/data/tpch/SF10/lineitem.tbl'
WITH (delimiter='|', header='false', quoted='false');
COPY nation FROM '/data/tpch/SF10/nation.tbl'
WITH (delimiter='|', header='false', quoted='false');
COPY orders FROM '/data/tpch/SF10/orders.tbl'
WITH (delimiter='|', header='false', quoted='false');
COPY part FROM '/data/tpch/SF10/part.tbl'
WITH (delimiter='|', header='false', quoted='false');
COPY partsupp FROM '/data/tpch/SF10/partsupp.tbl'
WITH (delimiter='|', header='false', quoted='false');
COPY region FROM '/data/tpch/SF10/region.tbl'
WITH (delimiter='|', header='false', quoted='false');
COPY supplier FROM '/data/tpch/SF10/supplier.tbl'
WITH (delimiter='|', header='false', quoted='false');
