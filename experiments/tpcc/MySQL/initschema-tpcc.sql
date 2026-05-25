-- Benchmark-Experiment-Host-Manager | experiments/tpcc/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-load setup for TPC-C on MySQL. Configures the root user,
--          enables local infile loading, sets session modes, and tunes
--          InnoDB and MEMORY engine parameters to accelerate bulk import.

DROP USER 'root'@'%';
FLUSH PRIVILEGES;

CREATE USER 'root'@'%';
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'root';

ALTER USER 'root'@'%' REQUIRE NONE;

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

-- set max MEMORY engine size
SET GLOBAL tmp_table_size = 1024 * 1024 * 1024 * 32;
SET GLOBAL max_heap_table_size = 1024 * 1024 * 1024 * 32;
