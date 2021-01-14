USE [tpch]
GO

ALTER DATABASE tpch SET RECOVERY BULK_LOGGED;

GO

BULK INSERT customer
    FROM '/data/tpch/SF1/customer.tbl'
    WITH
    (
    FIRSTROW = 1,
    FIELDTERMINATOR = '|',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    TABLOCK
    )

GO

BULK INSERT lineitem
    FROM '/data/tpch/SF1/lineitem.tbl'
    WITH
    (
    FIRSTROW = 1,
    FIELDTERMINATOR = '|',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    TABLOCK
    )

GO

BULK INSERT nation
    FROM '/data/tpch/SF1/nation.tbl'
    WITH
    (
    FIRSTROW = 1,
    FIELDTERMINATOR = '|',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    TABLOCK
    )

GO

BULK INSERT orders
    FROM '/data/tpch/SF1/orders.tbl'
    WITH
    (
    FIRSTROW = 1,
    FIELDTERMINATOR = '|',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    TABLOCK
    )

GO

BULK INSERT part
    FROM '/data/tpch/SF1/part.tbl'
    WITH
    (
    FIRSTROW = 1,
    FIELDTERMINATOR = '|',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    TABLOCK
    )

GO

BULK INSERT partsupp
    FROM '/data/tpch/SF1/partsupp.tbl'
    WITH
    (
    FIRSTROW = 1,
    FIELDTERMINATOR = '|',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    TABLOCK
    )

GO

BULK INSERT region
    FROM '/data/tpch/SF1/region.tbl'
    WITH
    (
    FIRSTROW = 1,
    FIELDTERMINATOR = '|',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    TABLOCK
    )

GO

BULK INSERT supplier
    FROM '/data/tpch/SF1/supplier.tbl'
    WITH
    (
    FIRSTROW = 1,
    FIELDTERMINATOR = '|',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    TABLOCK
    )

GO

ALTER DATABASE tpch SET RECOVERY FULL;

GO

