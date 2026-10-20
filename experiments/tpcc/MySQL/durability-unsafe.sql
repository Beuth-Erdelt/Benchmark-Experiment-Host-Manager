-- Benchmark-Experiment-Host-Manager | experiments/tpcc/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load durability 'unsafe' (-xld unsafe), runs after durability-relaxed.sql.
--          Disables the InnoDB redo log for the load: a server crash during the
--          load leaves the instance unusable. restoredurability-unsafe.sql
--          enables it again after the load.
--          No curly braces in this file: bexhoma may fill it with str.format().

ALTER INSTANCE DISABLE INNODB REDO_LOG;
SHOW GLOBAL STATUS LIKE 'Innodb_redo_log_enabled';
