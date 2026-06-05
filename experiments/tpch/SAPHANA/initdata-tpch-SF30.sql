-- Benchmark-Experiment-Host-Manager | experiments/tpch/SAPHANA
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load TPC-H data at scale factor 30 (SF30 ~ 30 GB) into SAP HANA.
--          See initdata-tpch-SF1.sql for option descriptions.
--          Note: the ORDERS error log path retains the original SF1 path.

ALTER SYSTEM ALTER CONFIGURATION ('indexserver.ini', 'system')
    SET ('import_export', 'enable_csv_import_path_filter') = 'false'
    WITH RECONFIGURE;

IMPORT FROM CSV FILE '/data/tpch/SF30/region.tbl'
    INTO TPCH.REGION
    WITH
        RECORD DELIMITED BY '\n'
        FIELD DELIMITED BY '|'
        THREADS 10
        NO TYPE CHECK
        ERROR LOG '/data/tpch/SF30/error_log.txt'
        BATCH 1000;

IMPORT FROM CSV FILE '/data/tpch/SF30/nation.tbl'
    INTO TPCH.NATION
    WITH
        RECORD DELIMITED BY '\n'
        FIELD DELIMITED BY '|'
        THREADS 10
        NO TYPE CHECK
        ERROR LOG '/data/tpch/SF30/error_log.txt'
        BATCH 1000;

IMPORT FROM CSV FILE '/data/tpch/SF30/customer.tbl'
    INTO TPCH.CUSTOMER
    WITH
        RECORD DELIMITED BY '\n'
        FIELD DELIMITED BY '|'
        THREADS 10
        NO TYPE CHECK
        ERROR LOG '/data/tpch/SF30/error_log.txt'
        BATCH 1000;

IMPORT FROM CSV FILE '/data/tpch/SF30/part.tbl'
    INTO TPCH.PART
    WITH
        RECORD DELIMITED BY '\n'
        FIELD DELIMITED BY '|'
        THREADS 10
        NO TYPE CHECK
        ERROR LOG '/data/tpch/SF30/error_log.txt'
        BATCH 1000;

IMPORT FROM CSV FILE '/data/tpch/SF30/supplier.tbl'
    INTO TPCH.SUPPLIER
    WITH
        RECORD DELIMITED BY '\n'
        FIELD DELIMITED BY '|'
        THREADS 10
        NO TYPE CHECK
        ERROR LOG '/data/tpch/SF30/error_log.txt'
        BATCH 1000;

IMPORT FROM CSV FILE '/data/tpch/SF30/partsupp.tbl'
    INTO TPCH.PARTSUPP
    WITH
        RECORD DELIMITED BY '\n'
        FIELD DELIMITED BY '|'
        THREADS 10
        NO TYPE CHECK
        ERROR LOG '/data/tpch/SF30/error_log.txt'
        BATCH 1000;

IMPORT FROM CSV FILE '/data/tpch/SF30/lineitem.tbl'
    INTO TPCH.LINEITEM
    WITH
        RECORD DELIMITED BY '\n'
        FIELD DELIMITED BY '|'
        THREADS 10
        NO TYPE CHECK
        ERROR LOG '/data/tpch/SF30/error_log.txt'
        BATCH 1000;

IMPORT FROM CSV FILE '/data/tpch/SF30/orders.tbl'
    INTO TPCH.ORDERS
    WITH
        RECORD DELIMITED BY '\n'
        FIELD DELIMITED BY '|'
        THREADS 10
        NO TYPE CHECK
        ERROR LOG '/data/tpch/SF1/error_log.txt'
        BATCH 1000;
