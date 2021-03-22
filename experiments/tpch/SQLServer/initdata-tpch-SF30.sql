USE [tpch]
GO

ALTER DATABASE tpch SET RECOVERY BULK_LOGGED;

GO

BULK INSERT customer
    FROM '/data/tpch/SF30/customer.tbl'
    WITH
    (
    FIRSTROW = 1,
    FIELDTERMINATOR = '|',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    LASTROW = 4500000,
    TABLOCK
    )

GO

BULK INSERT lineitem
    FROM '/data/tpch/SF30/lineitem.tbl'
    WITH
    (
    FIRSTROW = 1,
    FIELDTERMINATOR = '|',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    LASTROW = 179998372,
    TABLOCK
    )

GO

BULK INSERT nation
    FROM '/data/tpch/SF30/nation.tbl'
    WITH
    (
    FIRSTROW = 1,
    FIELDTERMINATOR = '|',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    LASTROW = 25,
    TABLOCK
    )

GO

BULK INSERT orders
    FROM '/data/tpch/SF30/orders.tbl'
    WITH
    (
    FIRSTROW = 1,
    FIELDTERMINATOR = '|',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    LASTROW = 45000000,
    TABLOCK
    )

GO

BULK INSERT part
    FROM '/data/tpch/SF30/part.tbl'
    WITH
    (
    FIRSTROW = 1,
    FIELDTERMINATOR = '|',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    LASTROW = 6000000,
    TABLOCK
    )

GO

BULK INSERT partsupp
    FROM '/data/tpch/SF30/partsupp.tbl'
    WITH
    (
    FIRSTROW = 1,
    FIELDTERMINATOR = '|',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    LASTROW = 24000000,
    TABLOCK
    )

GO

BULK INSERT region
    FROM '/data/tpch/SF30/region.tbl'
    WITH
    (
    FIRSTROW = 1,
    FIELDTERMINATOR = '|',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    LASTROW = 5,
    TABLOCK
    )

GO

BULK INSERT supplier
    FROM '/data/tpch/SF30/supplier.tbl'
    WITH
    (
    FIRSTROW = 1,
    FIELDTERMINATOR = '|',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    LASTROW = 300000,
    TABLOCK
    )

GO

ALTER DATABASE tpch SET RECOVERY FULL;

GO

