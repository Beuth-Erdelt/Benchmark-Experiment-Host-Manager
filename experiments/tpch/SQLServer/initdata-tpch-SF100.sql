USE [tpch]
GO

ALTER DATABASE tpch SET RECOVERY BULK_LOGGED;

GO

BULK INSERT customer
    FROM '/data/tpch/SF100/customer.tbl'
    WITH
    (
    FIRSTROW = 1,
    FIELDTERMINATOR = '|',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    LASTROW = 15000000,
    TABLOCK
    )

GO

BULK INSERT lineitem
    FROM '/data/tpch/SF100/lineitem.tbl'
    WITH
    (
    FIRSTROW = 1,
    FIELDTERMINATOR = '|',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    LASTROW = 600037902,
    TABLOCK
    )

GO

BULK INSERT nation
    FROM '/data/tpch/SF100/nation.tbl'
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
    FROM '/data/tpch/SF100/orders.tbl'
    WITH
    (
    FIRSTROW = 1,
    FIELDTERMINATOR = '|',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    LASTROW = 150000000,
    TABLOCK
    )

GO

BULK INSERT part
    FROM '/data/tpch/SF100/part.tbl'
    WITH
    (
    FIRSTROW = 1,
    FIELDTERMINATOR = '|',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    LASTROW = 20000000,
    TABLOCK
    )

GO

BULK INSERT partsupp
    FROM '/data/tpch/SF100/partsupp.tbl'
    WITH
    (
    FIRSTROW = 1,
    FIELDTERMINATOR = '|',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    LASTROW = 80000000,
    TABLOCK
    )

GO

BULK INSERT region
    FROM '/data/tpch/SF100/region.tbl'
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
    FROM '/data/tpch/SF100/supplier.tbl'
    WITH
    (
    FIRSTROW = 1,
    FIELDTERMINATOR = '|',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    LASTROW = 1000000,
    TABLOCK
    )

GO

ALTER DATABASE tpch SET RECOVERY FULL;

GO

