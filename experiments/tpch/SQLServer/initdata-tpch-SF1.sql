USE [tpch]
GO

ALTER DATABASE tpch SET RECOVERY BULK_LOGGED;

GO

BULK INSERT customer
    FROM '/data/tpch/SF1_sqlserver/customer.tbl'
    WITH
    (
    FIRSTROW = 1,
    FIELDTERMINATOR = '|',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    LASTROW = 150000,
    TABLOCK
    )

GO

BULK INSERT lineitem
    FROM '/data/tpch/SF1_sqlserver/lineitem.tbl'
    WITH
    (
    FIRSTROW = 1,
    FIELDTERMINATOR = '|',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    LASTROW = 6001215,
    TABLOCK
    )

GO

BULK INSERT nation
    FROM '/data/tpch/SF1_sqlserver/nation.tbl'
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
    FROM '/data/tpch/SF1_sqlserver/orders.tbl'
    WITH
    (
    FIRSTROW = 1,
    FIELDTERMINATOR = '|',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    LASTROW = 1500000,
    TABLOCK
    )

GO

BULK INSERT part
    FROM '/data/tpch/SF1_sqlserver/part.tbl'
    WITH
    (
    FIRSTROW = 1,
    FIELDTERMINATOR = '|',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    LASTROW = 200000,
    TABLOCK
    )

GO

BULK INSERT partsupp
    FROM '/data/tpch/SF1_sqlserver/partsupp.tbl'
    WITH
    (
    FIRSTROW = 1,
    FIELDTERMINATOR = '|',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    LASTROW = 800000,
    TABLOCK
    )

GO

BULK INSERT region
    FROM '/data/tpch/SF1_sqlserver/region.tbl'
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
    FROM '/data/tpch/SF1_sqlserver/supplier.tbl'
    WITH
    (
    FIRSTROW = 1,
    FIELDTERMINATOR = '|',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    LASTROW = 10000,
    TABLOCK
    )

GO

ALTER DATABASE tpch SET RECOVERY FULL;

GO

