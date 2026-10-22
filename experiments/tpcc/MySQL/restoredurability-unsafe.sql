-- Benchmark-Experiment-Host-Manager | experiments/tpcc/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Undo load durability 'unsafe' after the load, before
--          restoredurability-relaxed.sql (which clears the saved values).
--          Enables the InnoDB redo log again (a no-op when it is enabled) and
--          restores doublewrite to its saved startup value (a missing row
--          keeps the current value).
--          No curly braces in this file: bexhoma may fill it with str.format().

ALTER INSTANCE ENABLE INNODB REDO_LOG;
SHOW GLOBAL STATUS LIKE 'Innodb_redo_log_enabled';

SET @v = @@GLOBAL.innodb_doublewrite;
SELECT value INTO @v FROM bexhoma.saved_settings WHERE name = 'innodb_doublewrite';
SET GLOBAL innodb_doublewrite = @v;
SELECT @@GLOBAL.innodb_doublewrite;
