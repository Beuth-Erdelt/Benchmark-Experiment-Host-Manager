LOAD DATA INFILE '/data/tpch/SF1/customer.tbl' IGNORE INTO TABLE tpch.customer
FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF1/lineitem.tbl' IGNORE INTO TABLE tpch.lineitem
FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF1/nation.tbl' IGNORE INTO TABLE tpch.nation
FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF1/orders.tbl' IGNORE INTO TABLE tpch.orders
FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF1/part.tbl' IGNORE INTO TABLE tpch.part
FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF1/partsupp.tbl' IGNORE INTO TABLE tpch.partsupp
FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF1/region.tbl' IGNORE INTO TABLE tpch.region
FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF1/supplier.tbl' IGNORE INTO TABLE tpch.supplier
FIELDS TERMINATED BY '|';

