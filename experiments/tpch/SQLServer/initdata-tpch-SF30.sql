-- Benchmark-Experiment-Host-Manager | experiments/tpch/SQLServer
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load TPC-H data at scale factor 30 (SF30 ~ 30 GB) into SQL Server.
--          See initdata-tpch-SF1.sql for option descriptions.

USE [tpch]
GO

ALTER DATABASE tpch SET RECOVERY BULK_LOGGED;
GO

BULK INSERT customer
    FROM '/data/tpch/SF30/customer.tbl'
    WITH
    (
        FIRSTROW        = 1,
        FIELDTERMINATOR = '|',
        ROWTERMINATOR   = '\n',
        LASTROW         = 4500000,
        TABLOCK
    )
GO

BULK INSERT lineitem
    FROM '/data/tpch/SF30/lineitem.tbl'
    WITH
    (
        FIRSTROW        = 1,
        FIELDTERMINATOR = '|',
        ROWTERMINATOR   = '\n',
        LASTROW         = 179998372,
        TABLOCK
    )
GO

BULK INSERT nation
    FROM '/data/tpch/SF30/nation.tbl'
    WITH
    (
        FIRSTROW        = 1,
        FIELDTERMINATOR = '|',
        ROWTERMINATOR   = '\n',
        LASTROW         = 25,
        TABLOCK
    )
GO

BULK INSERT orders
    FROM '/data/tpch/SF30/orders.tbl'
    WITH
    (
        FIRSTROW        = 1,
        FIELDTERMINATOR = '|',
        ROWTERMINATOR   = '\n',
        LASTROW         = 45000000,
        TABLOCK
    )
GO

BULK INSERT part
    FROM '/data/tpch/SF30/part.tbl'
    WITH
    (
        FIRSTROW        = 1,
        FIELDTERMINATOR = '|',
        ROWTERMINATOR   = '\n',
        LASTROW         = 6000000,
        TABLOCK
    )
GO

BULK INSERT partsupp
    FROM '/data/tpch/SF30/partsupp.tbl'
    WITH
    (
        FIRSTROW        = 1,
        FIELDTERMINATOR = '|',
        ROWTERMINATOR   = '\n',
        LASTROW         = 24000000,
        TABLOCK
    )
GO

BULK INSERT region
    FROM '/data/tpch/SF30/region.tbl'
    WITH
    (
        FIRSTROW        = 1,
        FIELDTERMINATOR = '|',
        ROWTERMINATOR   = '\n',
        LASTROW         = 5,
        TABLOCK
    )
GO

BULK INSERT supplier
    FROM '/data/tpch/SF30/supplier.tbl'
    WITH
    (
        FIRSTROW        = 1,
        FIELDTERMINATOR = '|',
        ROWTERMINATOR   = '\n',
        LASTROW         = 300000,
        TABLOCK
    )
GO

ALTER DATABASE tpch SET RECOVERY FULL;
GO
