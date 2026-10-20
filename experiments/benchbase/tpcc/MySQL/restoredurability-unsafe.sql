-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Undo load durability 'unsafe' after the load, before
--          restoredurability-relaxed.sql. Enables the InnoDB redo log again
--          (a no-op when it is enabled).
--          No curly braces in this file: bexhoma may fill it with str.format().

ALTER INSTANCE ENABLE INNODB REDO_LOG;
SHOW GLOBAL STATUS LIKE 'Innodb_redo_log_enabled';
