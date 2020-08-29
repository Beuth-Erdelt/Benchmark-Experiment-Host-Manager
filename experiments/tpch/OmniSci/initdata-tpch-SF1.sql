
COPY customer FROM '/data/tpch/SF1/customer.tbl'
WITH (delimiter='|', header='false', quoted='false');
COPY lineitem FROM '/data/tpch/SF1/lineitem.tbl'
WITH (delimiter='|', header='false', quoted='false');
COPY nation FROM '/data/tpch/SF1/nation.tbl'
WITH (delimiter='|', header='false', quoted='false');
COPY orders FROM '/data/tpch/SF1/orders.tbl'
WITH (delimiter='|', header='false', quoted='false');
COPY part FROM '/data/tpch/SF1/part.tbl'
WITH (delimiter='|', header='false', quoted='false');
COPY partsupp FROM '/data/tpch/SF1/partsupp.tbl'
WITH (delimiter='|', header='false', quoted='false');
COPY region FROM '/data/tpch/SF1/region.tbl'
WITH (delimiter='|', header='false', quoted='false');
COPY supplier FROM '/data/tpch/SF1/supplier.tbl'
WITH (delimiter='|', header='false', quoted='false');
