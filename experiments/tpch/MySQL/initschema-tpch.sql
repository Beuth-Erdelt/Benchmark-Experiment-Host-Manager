DROP USER 'root'@'%';
FLUSH PRIVILEGES;

CREATE USER 'root'@'%';
ALTER USER 'root'@'%' IDENTIFIED BY 'root';

 -- SET PASSWORD FOR root@'172.17.0.3' = PASSWORD('root');

GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

-- allow load local in file
SET GLOBAL local_infile = 1;

-- allow zero date
SET sql_mode='';
SET GLOBAL sql_mode='';

-- speed up import
SET GLOBAL innodb_buffer_pool_size = 32*1024*1024*1024;
SET GLOBAL innodb_log_buffer_size = 16*1024*1024*1024;
SET GLOBAL innodb_flush_log_at_trx_commit =0;

-- the server performs a DNS lookup every time a client connects
-- SET GLOBAL host_cache_size=0

-- Defines the amount of disk space occupied by redo log files.
SET GLOBAL innodb_redo_log_capacity=1024*1024*1024;


CREATE DATABASE tpch;

-- sccsid:     @(#)dss.ddl  2.1.8.1
create table tpch.nation  ( n_nationkey  integer not null,
                            n_name       char(25) not null,
                            n_regionkey  integer not null,
                            n_comment    varchar(152));

create table tpch.region  ( r_regionkey  integer not null,
                            r_name       char(25) not null,
                            r_comment    varchar(152));

create table tpch.part  ( p_partkey     integer not null,
                          p_name        varchar(55) not null,
                          p_mfgr        char(25) not null,
                          p_brand       char(10) not null,
                          p_type        varchar(25) not null,
                          p_size        integer not null,
                          p_container   char(10) not null,
                          p_retailprice decimal(15,2) not null,
                          p_comment     varchar(23) not null );

create table tpch.supplier ( s_suppkey     integer not null,
                             s_name        char(25) not null,
                             s_address     varchar(40) not null,
                             s_nationkey   integer not null,
                             s_phone       char(15) not null,
                             s_acctbal     decimal(15,2) not null,
                             s_comment     varchar(101) not null);

create table tpch.partsupp ( ps_partkey     integer not null,
                             ps_suppkey     integer not null,
                             ps_availqty    integer not null,
                             ps_supplycost  decimal(15,2)  not null,
                             ps_comment     varchar(199) not null );

create table tpch.customer ( c_custkey     integer not null,
                             c_name        varchar(25) not null,
                             c_address     varchar(40) not null,
                             c_nationkey   integer not null,
                             c_phone       char(15) not null,
                             c_acctbal     decimal(15,2)   not null,
                             c_mktsegment  char(10) not null,
                             c_comment     varchar(117) not null);

create table tpch.orders  ( o_orderkey       integer not null,
                           o_custkey        integer not null,
                           o_orderstatus    char(1) not null,
                           o_totalprice     decimal(15,2) not null,
                           o_orderdate      date not null,
                           o_orderpriority  char(15) not null,  
                           o_clerk          char(15) not null, 
                           o_shippriority   integer not null,
                           o_comment        varchar(79) not null);

create table tpch.lineitem ( l_orderkey    integer not null,
                             l_partkey     integer not null,
                             l_suppkey     integer not null,
                             l_linenumber  integer not null,
                             l_quantity    decimal(15,2) not null,
                             l_extendedprice  decimal(15,2) not null,
                             l_discount    decimal(15,2) not null,
                             l_tax         decimal(15,2) not null,
                             l_returnflag  char(1) not null,
                             l_linestatus  char(1) not null,
                             l_shipdate    date not null,
                             l_commitdate  date not null,
                             l_receiptdate date not null,
                             l_shipinstruct char(25) not null,
                             l_shipmode     char(10) not null,
                             l_comment      varchar(44) not null);
