-- Benchmark-Experiment-Host-Manager | experiments/tpch/SQLServer
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load TPC-H data at scale factor 100 (SF100 ~ 100 GB) into SQL Server.
--          See initdata-tpch-SF1.sql for option descriptions.

USE [tpch]
GO

ALTER DATABASE tpch SET RECOVERY BULK_LOGGED;
GO

BULK INSERT customer
    FROM '/data/tpch/SF100/customer.tbl'
    WITH
    (
        FIRSTROW        = 1,
        FIELDTERMINATOR = '|',
        ROWTERMINATOR   = '\n',
        LASTROW         = 15000000,
        TABLOCK
    )
GO

BULK INSERT lineitem
    FROM '/data/tpch/SF100/lineitem.tbl'
    WITH
    (
        FIRSTROW        = 1,
        FIELDTERMINATOR = '|',
        ROWTERMINATOR   = '\n',
        LASTROW         = 600037902,
        TABLOCK
    )
GO

BULK INSERT nation
    FROM '/data/tpch/SF100/nation.tbl'
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
    FROM '/data/tpch/SF100/orders.tbl'
    WITH
    (
        FIRSTROW        = 1,
        FIELDTERMINATOR = '|',
        ROWTERMINATOR   = '\n',
        LASTROW         = 150000000,
        TABLOCK
    )
GO

BULK INSERT part
    FROM '/data/tpch/SF100/part.tbl'
    WITH
    (
        FIRSTROW        = 1,
        FIELDTERMINATOR = '|',
        ROWTERMINATOR   = '\n',
        LASTROW         = 20000000,
        TABLOCK
    )
GO

BULK INSERT partsupp
    FROM '/data/tpch/SF100/partsupp.tbl'
    WITH
    (
        FIRSTROW        = 1,
        FIELDTERMINATOR = '|',
        ROWTERMINATOR   = '\n',
        LASTROW         = 80000000,
        TABLOCK
    )
GO

BULK INSERT region
    FROM '/data/tpch/SF100/region.tbl'
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
    FROM '/data/tpch/SF100/supplier.tbl'
    WITH
    (
        FIRSTROW        = 1,
        FIELDTERMINATOR = '|',
        ROWTERMINATOR   = '\n',
        LASTROW         = 1000000,
        TABLOCK
    )
GO

ALTER DATABASE tpch SET RECOVERY FULL;
GO
