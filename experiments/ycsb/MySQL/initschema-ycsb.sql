-- Benchmark-Experiment-Host-Manager | experiments/ycsb/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-load setup for YCSB on MySQL. Configures the root user,
--          enables local infile loading, sets session modes, tunes InnoDB
--          parameters, and creates the ycsb database and usertable.

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

-- speed up import
SET GLOBAL innodb_buffer_pool_size = 32*1024*1024*1024;
SET GLOBAL innodb_log_buffer_size = 16*1024*1024*1024;
SET GLOBAL innodb_flush_log_at_trx_commit = 0;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
