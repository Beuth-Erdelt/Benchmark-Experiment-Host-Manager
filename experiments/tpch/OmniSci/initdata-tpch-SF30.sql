
COPY customer FROM '/data/tpch/SF30/customer.tbl'
WITH (delimiter='|', header='false', quoted='false');
COPY lineitem FROM '/data/tpch/SF30/lineitem.tbl'
WITH (delimiter='|', header='false', quoted='false');
COPY nation FROM '/data/tpch/SF30/nation.tbl'
WITH (delimiter='|', header='false', quoted='false');
COPY orders FROM '/data/tpch/SF30/orders.tbl'
WITH (delimiter='|', header='false', quoted='false');
COPY part FROM '/data/tpch/SF30/part.tbl'
WITH (delimiter='|', header='false', quoted='false');
COPY partsupp FROM '/data/tpch/SF30/partsupp.tbl'
WITH (delimiter='|', header='false', quoted='false');
COPY region FROM '/data/tpch/SF30/region.tbl'
WITH (delimiter='|', header='false', quoted='false');
COPY supplier FROM '/data/tpch/SF30/supplier.tbl'
WITH (delimiter='|', header='false', quoted='false');
