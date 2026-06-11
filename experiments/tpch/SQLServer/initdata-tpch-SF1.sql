-- Benchmark-Experiment-Host-Manager | experiments/tpch/SQLServer
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load TPC-H data at scale factor 1 (SF1 ~ 1 GB) into SQL Server.
--          BULK INSERT reads pipe-delimited .tbl files from the server filesystem.
--          LASTROW caps the read at the expected row count, preventing BULK INSERT
--          from treating the trailing '|' delimiter as an extra empty row.
--          BULK_LOGGED recovery minimises transaction log growth during the load;
--          FULL recovery is restored afterwards.
--          Data files reside in SF1_sqlserver/ (SQL Server-compatible variant).

USE [tpch]
GO

ALTER DATABASE tpch SET RECOVERY BULK_LOGGED;
GO

BULK INSERT customer
    FROM '/data/tpch/SF1_sqlserver/customer.tbl'
    WITH
    (
        FIRSTROW        = 1,
        FIELDTERMINATOR = '|',
        ROWTERMINATOR   = '\n',
        LASTROW         = 150000,
        TABLOCK
    )
GO

BULK INSERT lineitem
    FROM '/data/tpch/SF1_sqlserver/lineitem.tbl'
    WITH
    (
        FIRSTROW        = 1,
        FIELDTERMINATOR = '|',
        ROWTERMINATOR   = '\n',
        LASTROW         = 6001215,
        TABLOCK
    )
GO

BULK INSERT nation
    FROM '/data/tpch/SF1_sqlserver/nation.tbl'
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
    FROM '/data/tpch/SF1_sqlserver/orders.tbl'
    WITH
    (
        FIRSTROW        = 1,
        FIELDTERMINATOR = '|',
        ROWTERMINATOR   = '\n',
        LASTROW         = 1500000,
        TABLOCK
    )
GO

BULK INSERT part
    FROM '/data/tpch/SF1_sqlserver/part.tbl'
    WITH
    (
        FIRSTROW        = 1,
        FIELDTERMINATOR = '|',
        ROWTERMINATOR   = '\n',
        LASTROW         = 200000,
        TABLOCK
    )
GO

BULK INSERT partsupp
    FROM '/data/tpch/SF1_sqlserver/partsupp.tbl'
    WITH
    (
        FIRSTROW        = 1,
        FIELDTERMINATOR = '|',
        ROWTERMINATOR   = '\n',
        LASTROW         = 800000,
        TABLOCK
    )
GO

BULK INSERT region
    FROM '/data/tpch/SF1_sqlserver/region.tbl'
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
    FROM '/data/tpch/SF1_sqlserver/supplier.tbl'
    WITH
    (
        FIRSTROW        = 1,
        FIELDTERMINATOR = '|',
        ROWTERMINATOR   = '\n',
        LASTROW         = 10000,
        TABLOCK
    )
GO

ALTER DATABASE tpch SET RECOVERY FULL;
GO
