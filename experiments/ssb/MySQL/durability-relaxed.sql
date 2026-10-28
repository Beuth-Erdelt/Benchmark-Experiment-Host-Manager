-- Benchmark-Experiment-Host-Manager | experiments/ssb/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load durability 'relaxed' for SSB (-xld relaxed, the default).
--          Flush 2, key checks off, autocommit off (the SSB loader commits).
--          restoredurability-relaxed.sql restores all of it.
--          No curly braces in this file: bexhoma may fill it with str.format().

-- Save the startup values of the settings relaxed below (first save wins)
CREATE DATABASE IF NOT EXISTS bexhoma;
CREATE TABLE IF NOT EXISTS bexhoma.saved_settings (name VARCHAR(64) PRIMARY KEY, value VARCHAR(255));
INSERT IGNORE INTO bexhoma.saved_settings VALUES
  ('innodb_flush_log_at_trx_commit', @@GLOBAL.innodb_flush_log_at_trx_commit),
  ('foreign_key_checks', @@GLOBAL.foreign_key_checks),
  ('unique_checks', @@GLOBAL.unique_checks),
  ('autocommit', @@GLOBAL.autocommit);
SELECT * FROM bexhoma.saved_settings;

-- write the redo log at commit, flush it once per second (binlog is off, see --skip-log-bin)
SET GLOBAL innodb_flush_log_at_trx_commit = 2;

-- disable checks globally because loaders use separate sessions
SET GLOBAL foreign_key_checks = 0;
SET GLOBAL unique_checks = 0;
SET GLOBAL autocommit = 0;

SELECT @@GLOBAL.innodb_flush_log_at_trx_commit, @@GLOBAL.foreign_key_checks,
       @@GLOBAL.unique_checks, @@GLOBAL.autocommit;
