-- Benchmark-Experiment-Host-Manager | experiments/tpch/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Configure the MySQL server for TPC-H loading, then create the
--          TPC-H tables in the tpch database.

-- Create a passworded root account accessible from any host
DROP USER 'root'@'%';
FLUSH PRIVILEGES;
CREATE USER 'root'@'%';
ALTER USER 'root'@'%' IDENTIFIED BY 'root';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

-- durability relaxed for bulk load
SET GLOBAL innodb_flush_log_at_trx_commit = 2;
SET GLOBAL sync_binlog = 0;

-- io tuning
-- SET GLOBAL innodb_io_capacity = 4000;
-- SET GLOBAL innodb_io_capacity_max = 20000;

-- parallelism
-- SET GLOBAL innodb_ddl_threads = 32;
-- SET GLOBAL innodb_parallel_read_threads = 32;

-- redo log (requires restart if changed in config)
-- innodb_redo_log_capacity = 16G

-- buffer pool (config file / restart)
-- innodb_buffer_pool_size = 96G

-- disable checks globally because loaders use separate sessions
SET GLOBAL foreign_key_checks = 0;
SET GLOBAL unique_checks = 0;
SET GLOBAL autocommit = 0;

-- Enable server-side LOAD DATA INFILE (required for bulk loading from /data/)
SET GLOBAL local_infile = 1;
SHOW GLOBAL VARIABLES LIKE 'local_infile';

-- Permit zero dates in DATE columns (TPC-H data may contain '0000-00-00' values)
SET sql_mode = '';
SET GLOBAL sql_mode = '';

-- Report current InnoDB configuration for diagnostics
SHOW GLOBAL STATUS;
SELECT @@innodb_buffer_pool_size / 1024 / 1024 / 1024,
       @@innodb_buffer_pool_chunk_size / 1024 / 1024 / 1024,
       @@innodb_buffer_pool_instances;
SELECT @@innodb_redo_log_capacity / 1024 / 1024,
       @@innodb_log_buffer_size / 1024 / 1024;
SELECT @@innodb_ddl_threads,
       @@innodb_ddl_buffer_size / 1024 / 1024;

CREATE DATABASE tpch;

CREATE TABLE tpch.nation (
    n_nationkey  INTEGER       NOT NULL,
    n_name       CHAR(25)      NOT NULL,
    n_regionkey  INTEGER       NOT NULL,
    n_comment    VARCHAR(152)
);

CREATE TABLE tpch.region (
    r_regionkey  INTEGER       NOT NULL,
    r_name       CHAR(25)      NOT NULL,
    r_comment    VARCHAR(152)
);

CREATE TABLE tpch.part (
    p_partkey      INTEGER       NOT NULL,
    p_name         VARCHAR(55)   NOT NULL,
    p_mfgr         CHAR(25)      NOT NULL,
    p_brand        CHAR(10)      NOT NULL,
    p_type         VARCHAR(25)   NOT NULL,
    p_size         INTEGER       NOT NULL,
    p_container    CHAR(10)      NOT NULL,
    p_retailprice  DECIMAL(15,2) NOT NULL,
    p_comment      VARCHAR(23)   NOT NULL
);

CREATE TABLE tpch.supplier (
    s_suppkey    INTEGER       NOT NULL,
    s_name       CHAR(25)      NOT NULL,
    s_address    VARCHAR(40)   NOT NULL,
    s_nationkey  INTEGER       NOT NULL,
    s_phone      CHAR(15)      NOT NULL,
    s_acctbal    DECIMAL(15,2) NOT NULL,
    s_comment    VARCHAR(101)  NOT NULL
);

CREATE TABLE tpch.partsupp (
    ps_partkey     INTEGER       NOT NULL,
    ps_suppkey     INTEGER       NOT NULL,
    ps_availqty    INTEGER       NOT NULL,
    ps_supplycost  DECIMAL(15,2) NOT NULL,
    ps_comment     VARCHAR(199)  NOT NULL
);

CREATE TABLE tpch.customer (
    c_custkey     INTEGER       NOT NULL,
    c_name        VARCHAR(25)   NOT NULL,
    c_address     VARCHAR(40)   NOT NULL,
    c_nationkey   INTEGER       NOT NULL,
    c_phone       CHAR(15)      NOT NULL,
    c_acctbal     DECIMAL(15,2) NOT NULL,
    c_mktsegment  CHAR(10)      NOT NULL,
    c_comment     VARCHAR(117)  NOT NULL
);

CREATE TABLE tpch.orders (
    o_orderkey       INTEGER       NOT NULL,
    o_custkey        INTEGER       NOT NULL,
    o_orderstatus    CHAR(1)       NOT NULL,
    o_totalprice     DECIMAL(15,2) NOT NULL,
    o_orderdate      DATE          NOT NULL,
    o_orderpriority  CHAR(15)      NOT NULL,
    o_clerk          CHAR(15)      NOT NULL,
    o_shippriority   INTEGER       NOT NULL,
    o_comment        VARCHAR(79)   NOT NULL
);

CREATE TABLE tpch.lineitem (
    l_orderkey       INTEGER       NOT NULL,
    l_partkey        INTEGER       NOT NULL,
    l_suppkey        INTEGER       NOT NULL,
    l_linenumber     INTEGER       NOT NULL,
    l_quantity       DECIMAL(15,2) NOT NULL,
    l_extendedprice  DECIMAL(15,2) NOT NULL,
    l_discount       DECIMAL(15,2) NOT NULL,
    l_tax            DECIMAL(15,2) NOT NULL,
    l_returnflag     CHAR(1)       NOT NULL,
    l_linestatus     CHAR(1)       NOT NULL,
    l_shipdate       DATE          NOT NULL,
    l_commitdate     DATE          NOT NULL,
    l_receiptdate    DATE          NOT NULL,
    l_shipinstruct   CHAR(25)      NOT NULL,
    l_shipmode       CHAR(10)      NOT NULL,
    l_comment        VARCHAR(44)   NOT NULL
);

COMMIT;
