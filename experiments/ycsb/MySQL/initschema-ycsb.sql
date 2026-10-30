-- Benchmark-Experiment-Host-Manager | experiments/ycsb/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-load setup for YCSB on MySQL. Configures the root user,
--          enables local infile loading, sets session modes, and creates the
--          ycsb database and usertable.
--          Import settings (load durability, -xld) are in durability-relaxed.sql.
--          Memory sizes (buffer pool) come from the template or --set.

DROP USER 'root'@'%';
FLUSH PRIVILEGES;

CREATE USER 'root'@'%';
ALTER USER 'root'@'%' IDENTIFIED BY 'root';

GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

-- allow load local in file
SET GLOBAL local_infile = 1;

-- allow zero date
SET sql_mode='';
SET GLOBAL sql_mode='';

CREATE DATABASE ycsb;

CREATE TABLE ycsb.usertable (
    `YCSB_KEY`  VARCHAR(255)  NOT NULL,
    `FIELD0`    TEXT,
    `FIELD1`    TEXT,
    `FIELD2`    TEXT,
    `FIELD3`    TEXT,
    `FIELD4`    TEXT,
    `FIELD5`    TEXT,
    `FIELD6`    TEXT,
    `FIELD7`    TEXT,
    `FIELD8`    TEXT,
    `FIELD9`    TEXT,
    PRIMARY KEY (`YCSB_KEY`)
) ENGINE=InnoDB {collation} ROW_FORMAT={row_format};
-- Collation and row format are DDL parameters (ddl-parameters.config)

SHOW CREATE TABLE ycsb.usertable;
