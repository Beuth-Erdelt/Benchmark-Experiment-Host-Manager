-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load durability 'durable' (-xld durable), first pre-load script.
--          The redo log is flushed at every commit during the load, whatever the
--          server was started with (e.g. --set ...innodb_flush_log_at_trx_commit=2).
--          Doublewrite cannot be switched on at runtime (MySQL 9.7: "cannot change
--          doublewrite mode to ON if doublewrite is disabled"), so it stays as
--          started (ON by default, unless --set ...innodb_doublewrite=OFF).
--          The startup value is saved in bexhoma.saved_settings;
--          restoredurability-durable.sql restores it after the load.
--          No curly braces in this file: bexhoma may fill it with str.format().

-- Save the startup values of the settings changed below (first save wins)
CREATE DATABASE IF NOT EXISTS bexhoma;
CREATE TABLE IF NOT EXISTS bexhoma.saved_settings (name VARCHAR(64) PRIMARY KEY, value VARCHAR(255));
INSERT IGNORE INTO bexhoma.saved_settings VALUES
  ('innodb_flush_log_at_trx_commit', @@GLOBAL.innodb_flush_log_at_trx_commit);
SELECT * FROM bexhoma.saved_settings;

SET GLOBAL innodb_flush_log_at_trx_commit = 1;

SELECT @@GLOBAL.innodb_flush_log_at_trx_commit, @@GLOBAL.innodb_doublewrite;
