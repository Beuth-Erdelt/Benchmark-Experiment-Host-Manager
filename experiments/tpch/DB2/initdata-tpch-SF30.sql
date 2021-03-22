connect to testdb user db2inst1 using root1234ROOT;
IMPORT FROM "/data/tpch/SF30/nation.tbl" OF DEL modified by coldel| INSERT INTO tpch.nation;
IMPORT FROM "/data/tpch/SF30/region.tbl" OF DEL modified by coldel| INSERT INTO tpch.region;
IMPORT FROM "/data/tpch/SF30/part.tbl" OF DEL modified by coldel| INSERT INTO tpch.part;
IMPORT FROM "/data/tpch/SF30/supplier.tbl" OF DEL modified by coldel| INSERT INTO tpch.supplier;
IMPORT FROM "/data/tpch/SF30/partsupp.tbl" OF DEL modified by coldel| INSERT INTO tpch.partsupp;
IMPORT FROM "/data/tpch/SF30/customer.tbl" OF DEL modified by coldel| INSERT INTO tpch.customer;
IMPORT FROM "/data/tpch/SF30/orders.tbl" OF DEL modified by coldel| INSERT INTO tpch.orders;
IMPORT FROM "/data/tpch/SF30/lineitem.tbl" OF DEL modified by coldel| INSERT INTO tpch.lineitem;
