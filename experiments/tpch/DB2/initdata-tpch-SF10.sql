connect to testdb user db2inst1 using root1234ROOT;
IMPORT FROM "/data/tpch/SF10/nation.tbl" OF DEL modified by coldel| INSERT INTO tpch.nation;
IMPORT FROM "/data/tpch/SF10/region.tbl" OF DEL modified by coldel| INSERT INTO tpch.region;
IMPORT FROM "/data/tpch/SF10/part.tbl" OF DEL modified by coldel| INSERT INTO tpch.part;
IMPORT FROM "/data/tpch/SF10/supplier.tbl" OF DEL modified by coldel| INSERT INTO tpch.supplier;
IMPORT FROM "/data/tpch/SF10/partsupp.tbl" OF DEL modified by coldel| INSERT INTO tpch.partsupp;
IMPORT FROM "/data/tpch/SF10/customer.tbl" OF DEL modified by coldel| INSERT INTO tpch.customer;
IMPORT FROM "/data/tpch/SF10/orders.tbl" OF DEL modified by coldel| INSERT INTO tpch.orders;
IMPORT FROM "/data/tpch/SF10/lineitem.tbl" OF DEL modified by coldel| INSERT INTO tpch.lineitem;
