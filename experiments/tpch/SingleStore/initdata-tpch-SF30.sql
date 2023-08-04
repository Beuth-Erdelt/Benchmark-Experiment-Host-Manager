LOAD DATA INFILE '/data/tpch/SF30/customer.tbl' INTO TABLE tpch.customer
FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF30/lineitem.tbl' INTO TABLE tpch.lineitem
FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF30/nation.tbl' INTO TABLE tpch.nation
FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF30/orders.tbl' INTO TABLE tpch.orders
FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF30/part.tbl' INTO TABLE tpch.part
FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF30/partsupp.tbl' INTO TABLE tpch.partsupp
FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF30/region.tbl' INTO TABLE tpch.region
FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF30/supplier.tbl' INTO TABLE tpch.supplier
FIELDS TERMINATED BY '|';

