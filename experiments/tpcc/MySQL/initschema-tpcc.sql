-- Benchmark-Experiment-Host-Manager | experiments/tpcc/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-load setup for TPC-C on MySQL. Configures the root user,
--          enables local infile loading and sets session modes.
--          Import settings (load durability, -xld) are in durability-relaxed.sql.
--          Memory sizes (buffer pool, tmp tables) come from the template or --set.

DROP USER 'root'@'%';
FLUSH PRIVILEGES;

CREATE USER 'root'@'%';
-- MySQL 9 has no mysql_native_password: default plugin (caching_sha2_password)
ALTER USER 'root'@'%' IDENTIFIED BY 'root';

ALTER USER 'root'@'%' REQUIRE NONE;

GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

-- allow load local in file
SET GLOBAL local_infile = 1;

-- allow zero date
SET sql_mode='';
SET GLOBAL sql_mode='';
