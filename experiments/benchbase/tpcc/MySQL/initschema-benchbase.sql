-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Configure the MySQL server for benchbase TPC-C loading and create
--          the benchbase database. Benchbase creates the TPC-C tables at runtime.

-- Show current database and user
SELECT
    DATABASE() AS `current_database`,
    USER() AS `current_user`;

DROP USER 'root'@'%';
FLUSH PRIVILEGES;

CREATE USER 'root'@'%';
ALTER USER 'root'@'%' IDENTIFIED BY 'root';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

-- allow load local in file
SET GLOBAL local_infile = 1;

-- allow zero date
SET sql_mode = '';
SET GLOBAL sql_mode = '';

CREATE DATABASE IF NOT EXISTS benchbase;
