
COPY customer FROM '/data/tpch/SF100/customer.tbl'
WITH (delimiter='|', header='false', quoted='false');
COPY lineitem FROM '/data/tpch/SF100/lineitem.tbl'
WITH (delimiter='|', header='false', quoted='false');
COPY nation FROM '/data/tpch/SF100/nation.tbl'
WITH (delimiter='|', header='false', quoted='false');
COPY orders FROM '/data/tpch/SF100/orders.tbl'
WITH (delimiter='|', header='false', quoted='false');
COPY part FROM '/data/tpch/SF100/part.tbl'
WITH (delimiter='|', header='false', quoted='false');
COPY partsupp FROM '/data/tpch/SF100/partsupp.tbl'
WITH (delimiter='|', header='false', quoted='false');
COPY region FROM '/data/tpch/SF100/region.tbl'
WITH (delimiter='|', header='false', quoted='false');
COPY supplier FROM '/data/tpch/SF100/supplier.tbl'
WITH (delimiter='|', header='false', quoted='false');
