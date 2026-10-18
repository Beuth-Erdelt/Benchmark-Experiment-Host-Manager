-- Benchmark-Experiment-Host-Manager | experiments/tpcc/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-load setup for TPC-C on MySQL. Configures the root user,
--          enables local infile loading, sets session modes, and relaxes
--          InnoDB settings to accelerate the bulk import. The relaxed settings
--          hold for the load only: their startup values are saved in
--          bexhoma.saved_settings and checkschema-tpcc.sql restores them.
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

-- Save the startup values of the settings relaxed below (first save wins)
CREATE DATABASE IF NOT EXISTS bexhoma;
CREATE TABLE IF NOT EXISTS bexhoma.saved_settings (name VARCHAR(64) PRIMARY KEY, value VARCHAR(255));
INSERT IGNORE INTO bexhoma.saved_settings VALUES
  ('innodb_flush_log_at_trx_commit', @@GLOBAL.innodb_flush_log_at_trx_commit),
  ('innodb_log_buffer_size', @@GLOBAL.innodb_log_buffer_size);
SELECT * FROM bexhoma.saved_settings;

-- speed up import (load phase only)
SET GLOBAL innodb_log_buffer_size = 1024*1024*1024;
SET GLOBAL innodb_flush_log_at_trx_commit = 0;
