-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/SQLServer
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load durability 'relaxed' (-xld, default) on SQL Server:
--          delayed durability for every transaction of the database, so a
--          commit does not wait for the log flush. Restored by
--          restoredurability-relaxed.sql. 'unsafe' is the same (no other
--          setting of SQL Server trades crash safety for speed).
--          The database is the current one (loadData creates it and switches to it).
--          No curly braces in this file: bexhoma may fill it with str.format().

ALTER DATABASE CURRENT SET DELAYED_DURABILITY = FORCED;
GO

SELECT name, recovery_model_desc, delayed_durability_desc
FROM sys.databases
WHERE name = DB_NAME();
GO
