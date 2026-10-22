-- Benchmark-Experiment-Host-Manager | experiments/tpcc/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Undo load durability 'relaxed' after the load (post-load phase, right
--          before the check script). Restores every setting saved in
--          bexhoma.saved_settings by durability-relaxed.sql (any of the MySQL
--          folders' variants), then clears the saved values, so a later load on
--          the same volume saves the server's values again.
--          No curly braces in this file: bexhoma may fill it with str.format().

-- Restore the settings saved before the load (SET GLOBAL x = DEFAULT would give
-- compiled defaults, not the server's startup values). @v starts at the current
-- value, so a setting without a saved row stays as it is.
SET @v = @@GLOBAL.innodb_flush_log_at_trx_commit;
SELECT CAST(value AS UNSIGNED) INTO @v FROM bexhoma.saved_settings WHERE name = 'innodb_flush_log_at_trx_commit';
SET GLOBAL innodb_flush_log_at_trx_commit = @v;
SET @v = @@GLOBAL.innodb_log_buffer_size;
SELECT CAST(value AS UNSIGNED) INTO @v FROM bexhoma.saved_settings WHERE name = 'innodb_log_buffer_size';
SET GLOBAL innodb_log_buffer_size = @v;
SET @v = @@GLOBAL.foreign_key_checks;
SELECT CAST(value AS UNSIGNED) INTO @v FROM bexhoma.saved_settings WHERE name = 'foreign_key_checks';
SET GLOBAL foreign_key_checks = @v;
SET @v = @@GLOBAL.unique_checks;
SELECT CAST(value AS UNSIGNED) INTO @v FROM bexhoma.saved_settings WHERE name = 'unique_checks';
SET GLOBAL unique_checks = @v;
SET @v = @@GLOBAL.autocommit;
SELECT CAST(value AS UNSIGNED) INTO @v FROM bexhoma.saved_settings WHERE name = 'autocommit';
SET GLOBAL autocommit = @v;

SELECT name, value AS saved_value FROM bexhoma.saved_settings ORDER BY name;
DELETE FROM bexhoma.saved_settings;
COMMIT;

SELECT @@GLOBAL.innodb_flush_log_at_trx_commit, @@GLOBAL.innodb_log_buffer_size,
       @@GLOBAL.foreign_key_checks, @@GLOBAL.unique_checks, @@GLOBAL.autocommit;
