LOAD DATA INFILE '/data/tpch/SF10/customer.tbl' INTO TABLE tpch.customer
FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF10/lineitem.tbl' INTO TABLE tpch.lineitem
FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF10/nation.tbl' INTO TABLE tpch.nation
FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF10/orders.tbl' INTO TABLE tpch.orders
FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF10/part.tbl' INTO TABLE tpch.part
FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF10/partsupp.tbl' INTO TABLE tpch.partsupp
FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF10/region.tbl' INTO TABLE tpch.region
FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF10/supplier.tbl' INTO TABLE tpch.supplier
FIELDS TERMINATED BY '|';

