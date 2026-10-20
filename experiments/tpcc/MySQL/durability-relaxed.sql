-- Benchmark-Experiment-Host-Manager | experiments/tpcc/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load durability 'relaxed' for TPC-C (-xld relaxed, the default).
--          No redo log flush at commit and a large log buffer for the HammerDB
--          build. restoredurability-relaxed.sql restores both.
--          No curly braces in this file: bexhoma may fill it with str.format().

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

SELECT @@GLOBAL.innodb_flush_log_at_trx_commit, @@GLOBAL.innodb_log_buffer_size;
