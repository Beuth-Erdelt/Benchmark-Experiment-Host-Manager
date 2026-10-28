-- Benchmark-Experiment-Host-Manager | experiments/ssb/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Prepare the MySQL server as for TPC-H (root account for the loader,
--          LOAD DATA LOCAL), then create the denormalized SSB table lineorder_flat
--          (-xsv flat) in the database ssb. Columns as in experiments/ssb/PostgreSQL;
--          the primary key (lo_orderkey, lo_linenumber) is part of the table, as
--          for lineorder.
--          Import settings (load durability, -xld) are in durability-*.sql.
--          No curly braces in this file: bexhoma may fill it with str.format().

-- Create a passworded root account accessible from any host (the loader connects as root)
DROP USER 'root'@'%';
FLUSH PRIVILEGES;
CREATE USER 'root'@'%';
ALTER USER 'root'@'%' IDENTIFIED BY 'root';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

-- Enable LOAD DATA LOCAL INFILE (the loader sends the files)
SET GLOBAL local_infile = 1;
SHOW GLOBAL VARIABLES LIKE 'local_infile';

CREATE DATABASE ssb;

CREATE TABLE ssb.lineorder_flat (
    lo_orderkey         BIGINT       NOT NULL,
    lo_linenumber       INTEGER      NOT NULL,
    lo_custkey          INTEGER      NOT NULL,
    lo_partkey          INTEGER      NOT NULL,
    lo_suppkey          INTEGER      NOT NULL,
    lo_orderdate        DATE         NOT NULL,
    lo_orderpriority    VARCHAR(15)  NOT NULL,
    lo_shippriority     CHAR(1)      NOT NULL,
    lo_quantity         INTEGER      NOT NULL,
    lo_extendedprice    INTEGER      NOT NULL,
    lo_ordtotalprice    INTEGER      NOT NULL,
    lo_discount         INTEGER      NOT NULL,
    lo_revenue          INTEGER      NOT NULL,
    lo_supplycost       INTEGER      NOT NULL,
    lo_tax              INTEGER      NOT NULL,
    lo_commitdate       DATE         NOT NULL,
    lo_shipmode         VARCHAR(10)  NOT NULL,
    c_name              VARCHAR(25)  NOT NULL,
    c_address           VARCHAR(25)  NOT NULL,
    c_city              CHAR(10)     NOT NULL,
    c_nation            VARCHAR(15)  NOT NULL,
    c_region            VARCHAR(12)  NOT NULL,
    c_phone             CHAR(15)     NOT NULL,
    c_mktsegment        VARCHAR(10)  NOT NULL,
    s_name              VARCHAR(25)  NOT NULL,
    s_address           VARCHAR(25)  NOT NULL,
    s_city              CHAR(10)     NOT NULL,
    s_nation            VARCHAR(15)  NOT NULL,
    s_region            VARCHAR(12)  NOT NULL,
    s_phone             CHAR(15)     NOT NULL,
    p_name              VARCHAR(22)  NOT NULL,
    p_mfgr              VARCHAR(6)   NOT NULL,
    p_category          VARCHAR(7)   NOT NULL,
    p_brand1            VARCHAR(9)   NOT NULL,
    p_color             VARCHAR(11)  NOT NULL,
    p_type              VARCHAR(25)  NOT NULL,
    p_size              INTEGER      NOT NULL,
    p_container         VARCHAR(10)  NOT NULL,
    PRIMARY KEY (lo_orderkey, lo_linenumber)
);
