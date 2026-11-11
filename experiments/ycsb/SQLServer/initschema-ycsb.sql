-- Benchmark-Experiment-Host-Manager | experiments/ycsb/SQLServer
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create the YCSB table usertable in SQL Server, schema dbo, for the
--          YCSB JDBC binding (which uses SELECT TOP for scans when the driver
--          is the one of SQL Server). The database is created by loadData
--          (/tmp/bexhoma-database.sql of the template), which also switches to it.
--          The fields are VARCHAR(MAX): the field length is set by the workload;
--          values up to 8000 bytes stay in the row.
--          The JDBC binding of YCSB splits db.url at ';' into shard URLs, so the
--          URL cannot name the database: the database (sqlcmd variable database)
--          becomes the default database of the login sa. The SUT runs only this
--          benchmark, and the setting is kept in master on the volume.
--          No curly braces in this file: bexhoma may fill it with str.format().

ALTER LOGIN sa WITH DEFAULT_DATABASE = [$(database)];
GO

CREATE TABLE dbo.usertable (
    YCSB_KEY    VARCHAR(255)    NOT NULL,
    FIELD0      VARCHAR(MAX),
    FIELD1      VARCHAR(MAX),
    FIELD2      VARCHAR(MAX),
    FIELD3      VARCHAR(MAX),
    FIELD4      VARCHAR(MAX),
    FIELD5      VARCHAR(MAX),
    FIELD6      VARCHAR(MAX),
    FIELD7      VARCHAR(MAX),
    FIELD8      VARCHAR(MAX),
    FIELD9      VARCHAR(MAX),
    CONSTRAINT pk_usertable PRIMARY KEY CLUSTERED (YCSB_KEY)
);
GO

SELECT name, recovery_model_desc, delayed_durability_desc, compatibility_level, collation_name
FROM sys.databases
WHERE name = DB_NAME();
GO
