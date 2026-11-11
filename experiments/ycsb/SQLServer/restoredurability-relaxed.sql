-- Benchmark-Experiment-Host-Manager | experiments/ycsb/SQLServer
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Restore the load durability 'relaxed' (-xld) on SQL Server
--          to the startup value of the database: delayed durability DISABLED
--          (the value of a new database; the template sets nothing else).
--          Ends with an ERROR (sqlcmd -b exits 1) if the value is not back.
--          No curly braces in this file: bexhoma may fill it with str.format().

ALTER DATABASE CURRENT SET DELAYED_DURABILITY = DISABLED;
GO

IF (SELECT delayed_durability_desc FROM sys.databases WHERE name = DB_NAME()) <> 'DISABLED'
    RAISERROR('ERROR: delayed durability of the database is not DISABLED after the load', 16, 1);
GO

SELECT name, recovery_model_desc, delayed_durability_desc
FROM sys.databases
WHERE name = DB_NAME();
GO
