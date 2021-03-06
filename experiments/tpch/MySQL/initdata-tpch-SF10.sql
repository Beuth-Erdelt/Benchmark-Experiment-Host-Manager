LOAD DATA INFILE '/data/tpch/SF10/customer.tbl' IGNORE INTO TABLE tpch.customer
FIELDS TERMINATED BY '|'
(@c_custkey, @c_name, @c_address, @c_nationkey, @c_phone, @c_acctbal, @c_mktsegment, @c_comment) SET c_custkey=NULLIF(@c_custkey,''), c_name=NULLIF(@c_name,''), c_address=NULLIF(@c_address,''), c_nationkey=NULLIF(@c_nationkey,''), c_phone=NULLIF(@c_phone,''), c_acctbal=NULLIF(@c_acctbal,''), c_mktsegment=NULLIF(@c_mktsegment,''), c_comment=NULLIF(@c_comment,'');

LOAD DATA INFILE '/data/tpch/SF10/lineitem.tbl' IGNORE INTO TABLE tpch.lineitem
FIELDS TERMINATED BY '|'
(@l_orderkey, @l_partkey, @l_suppkey, @l_linenumber, @l_quantity, @l_extendedprice, @l_discount, @l_tax, @l_returnflag, @l_linestatus, @l_shipdate, @l_commitdate, @l_receiptdate, @l_shipinstruct, @l_shipmode, @l_comment) SET l_orderkey=NULLIF(@l_orderkey,''), l_partkey=NULLIF(@l_partkey,''), l_suppkey=NULLIF(@l_suppkey,''), l_linenumber=NULLIF(@l_linenumber,''), l_quantity=NULLIF(@l_quantity,''), l_extendedprice=NULLIF(@l_extendedprice,''), l_discount=NULLIF(@l_discount,''), l_tax=NULLIF(@l_tax,''), l_returnflag=NULLIF(@l_returnflag,''), l_linestatus=NULLIF(@l_linestatus,''), l_shipdate=NULLIF(@l_shipdate,''), l_commitdate=NULLIF(@l_commitdate,''), l_receiptdate=NULLIF(@l_receiptdate,''), l_shipinstruct=NULLIF(@l_shipinstruct,''), l_shipmode=NULLIF(@l_shipmode,''), l_comment=NULLIF(@l_comment,'');

LOAD DATA INFILE '/data/tpch/SF10/nation.tbl' IGNORE INTO TABLE tpch.nation
FIELDS TERMINATED BY '|'
(@n_nationkey, @n_name, @n_regionkey, @n_comment) SET n_nationkey=NULLIF(@n_nationkey,''), n_name=NULLIF(@n_name,''), n_regionkey=NULLIF(@n_regionkey,''), n_comment=NULLIF(@n_comment,'');

LOAD DATA INFILE '/data/tpch/SF10/orders.tbl' IGNORE INTO TABLE tpch.orders
FIELDS TERMINATED BY '|'
(@o_orderkey, @o_custkey, @o_orderstatus, @o_totalprice, @o_orderdate, @o_orderpriority, @o_clerk, @o_shippriority, @o_comment) SET o_orderkey=NULLIF(@o_orderkey,''), o_custkey=NULLIF(@o_custkey,''), o_orderstatus=NULLIF(@o_orderstatus,''), o_totalprice=NULLIF(@o_totalprice,''), o_orderdate=NULLIF(@o_orderdate,''), o_orderpriority=NULLIF(@o_orderpriority,''), o_clerk=NULLIF(@o_clerk,''), o_shippriority=NULLIF(@o_shippriority,''), o_comment=NULLIF(@o_comment,'');

LOAD DATA INFILE '/data/tpch/SF10/part.tbl' IGNORE INTO TABLE tpch.part
FIELDS TERMINATED BY '|'
(@p_partkey, @p_name, @p_mfgr, @p_brand, @p_type, @p_size, @p_container, @p_retailprice, @p_comment) SET p_partkey=NULLIF(@p_partkey,''), p_name=NULLIF(@p_name,''), p_mfgr=NULLIF(@p_mfgr,''), p_brand=NULLIF(@p_brand,''), p_type=NULLIF(@p_type,''), p_size=NULLIF(@p_size,''), p_container=NULLIF(@p_container,''), p_retailprice=NULLIF(@p_retailprice,''), p_comment=NULLIF(@p_comment,'');

LOAD DATA INFILE '/data/tpch/SF10/partsupp.tbl' IGNORE INTO TABLE tpch.partsupp
FIELDS TERMINATED BY '|'
(@ps_partkey, @ps_suppkey, @ps_availqty, @ps_supplycost, @ps_comment) SET ps_partkey=NULLIF(@ps_partkey,''), ps_suppkey=NULLIF(@ps_suppkey,''), ps_availqty=NULLIF(@ps_availqty,''), ps_supplycost=NULLIF(@ps_supplycost,''), ps_comment=NULLIF(@ps_comment,'');

LOAD DATA INFILE '/data/tpch/SF10/region.tbl' IGNORE INTO TABLE tpch.region
FIELDS TERMINATED BY '|'
(@r_regionkey, @r_name, @r_comment) SET r_regionkey=NULLIF(@r_regionkey,''), r_name=NULLIF(@r_name,''), r_comment=NULLIF(@r_comment,'');

LOAD DATA INFILE '/data/tpch/SF10/supplier.tbl' IGNORE INTO TABLE tpch.supplier
FIELDS TERMINATED BY '|'
(@s_suppkey, @s_name, @s_address, @s_nationkey, @s_phone, @s_acctbal, @s_comment) SET s_suppkey=NULLIF(@s_suppkey,''), s_name=NULLIF(@s_name,''), s_address=NULLIF(@s_address,''), s_nationkey=NULLIF(@s_nationkey,''), s_phone=NULLIF(@s_phone,''), s_acctbal=NULLIF(@s_acctbal,''), s_comment=NULLIF(@s_comment,'');


