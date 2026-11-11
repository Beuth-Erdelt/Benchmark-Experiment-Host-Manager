-- Benchmark-Experiment-Host-Manager | experiments/ycsb/SQLServer
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load durability 'durable' (-xld) on SQL Server:
--          every commit waits for the log flush (delayed durability DISABLED,
--          the value of a new database). Nothing to restore.
--          No curly braces in this file: bexhoma may fill it with str.format().

ALTER DATABASE CURRENT SET DELAYED_DURABILITY = DISABLED;
GO

SELECT name, recovery_model_desc, delayed_durability_desc
FROM sys.databases
WHERE name = DB_NAME();
GO
