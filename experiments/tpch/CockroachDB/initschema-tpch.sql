-- https://github.com/cockroachdb/cockroach/blob/master/pkg/workload/tpch/tpch.go

SHOW ZONE CONFIGURATION FROM DATABASE defaultdb;

ALTER DATABASE defaultdb CONFIGURE ZONE USING num_replicas = {num_replicas};

SHOW ZONE CONFIGURATION FROM DATABASE defaultdb;

create table public.nation  ( n_nationkey  integer not null,
                            n_name       char(25) not null,
                            n_regionkey  integer not null,
                            n_comment    varchar(152));

create table public.region  ( r_regionkey  integer not null,
                            r_name       char(25) not null,
                            r_comment    varchar(152));

create table public.part  ( p_partkey     integer not null,
                          p_name        varchar(55) not null,
                          p_mfgr        char(25) not null,
                          p_brand       char(10) not null,
                          p_type        varchar(25) not null,
                          p_size        integer not null,
                          p_container   char(10) not null,
                          p_retailprice decimal(15,2) not null,
                          p_comment     varchar(23) not null );

create table public.supplier ( s_suppkey     integer not null,
                             s_name        char(25) not null,
                             s_address     varchar(40) not null,
                             s_nationkey   integer not null,
                             s_phone       char(15) not null,
                             s_acctbal     decimal(15,2) not null,
                             s_comment     varchar(101) not null);

create table public.partsupp ( ps_partkey     integer not null,
                             ps_suppkey     integer not null,
                             ps_availqty    integer not null,
                             ps_supplycost  decimal(15,2)  not null,
                             ps_comment     varchar(199) not null );

create table public.customer ( c_custkey     integer not null,
                             c_name        varchar(25) not null,
                             c_address     varchar(40) not null,
                             c_nationkey   integer not null,
                             c_phone       char(15) not null,
                             c_acctbal     decimal(15,2)   not null,
                             c_mktsegment  char(10) not null,
                             c_comment     varchar(117) not null);

create table public.orders  ( o_orderkey       integer not null,
                           o_custkey        integer not null,
                           o_orderstatus    char(1) not null,
                           o_totalprice     decimal(15,2) not null,
                           o_orderdate      date not null,
                           o_orderpriority  char(15) not null,  
                           o_clerk          char(15) not null, 
                           o_shippriority   integer not null,
                           o_comment        varchar(79) not null);

create table public.lineitem ( l_orderkey    integer not null,
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

-- for table region
alter table public.region
add primary key (r_regionkey);

-- for table nation
alter table public.nation
add primary key (n_nationkey);

-- for table part
alter table public.part
add primary key (p_partkey);

-- for table supplier
alter table public.supplier
add primary key (s_suppkey);

-- for table partsupp
alter table public.partsupp
add primary key (ps_partkey,ps_suppkey);

-- for table customer
alter table public.customer
add primary key (c_custkey);

-- for table lineitem
alter table public.lineitem
add primary key (l_orderkey,l_linenumber);

-- for table orders
alter table public.orders
add primary key (o_orderkey);

