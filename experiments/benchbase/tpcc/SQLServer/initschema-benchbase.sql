-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/SQLServer
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Prepare SQL Server for Benchbase TPC-C. The database benchbase is
--          created by loadData (/tmp/bexhoma-database.sql of the template,
--          recovery model SIMPLE), which also switches to it; Benchbase creates
--          the tables itself (--create=true of the loading job).
--          This script only reports the database it runs in.
--          No curly braces in this file: bexhoma may fill it with str.format().

SELECT DB_NAME() AS current_database, SUSER_SNAME() AS current_user_name;

SELECT name, recovery_model_desc, delayed_durability_desc, compatibility_level, collation_name
FROM sys.databases
WHERE name = DB_NAME();
GO
