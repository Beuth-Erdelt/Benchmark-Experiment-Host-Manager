-- Benchmark-Experiment-Host-Manager | experiments/tpch/SAPHANA
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load TPC-H data at scale factor 1 (SF1 ~ 1 GB) into SAP HANA.
--          IMPORT FROM CSV FILE reads pipe-delimited .tbl files; THREADS 10 runs
--          parallel ingest workers; NO TYPE CHECK skips column-type validation
--          to maximise throughput; BATCH 1000 commits every 1000 rows.
--          The path filter in indexserver.ini is disabled first so HANA can
--          read files from arbitrary paths.

ALTER SYSTEM ALTER CONFIGURATION ('indexserver.ini', 'system')
    SET ('import_export', 'enable_csv_import_path_filter') = 'false'
    WITH RECONFIGURE;

IMPORT FROM CSV FILE '/data/tpch/SF1/region.tbl'
    INTO TPCH.REGION
    WITH
        RECORD DELIMITED BY '\n'
        FIELD DELIMITED BY '|'
        THREADS 10
        NO TYPE CHECK
        ERROR LOG '/data/tpch/SF1/error_log.txt'
        BATCH 1000;

IMPORT FROM CSV FILE '/data/tpch/SF1/nation.tbl'
    INTO TPCH.NATION
    WITH
        RECORD DELIMITED BY '\n'
        FIELD DELIMITED BY '|'
        THREADS 10
        NO TYPE CHECK
        ERROR LOG '/data/tpch/SF1/error_log.txt'
        BATCH 1000;

IMPORT FROM CSV FILE '/data/tpch/SF1/customer.tbl'
    INTO TPCH.CUSTOMER
    WITH
        RECORD DELIMITED BY '\n'
        FIELD DELIMITED BY '|'
        THREADS 10
        NO TYPE CHECK
        ERROR LOG '/data/tpch/SF1/error_log.txt'
        BATCH 1000;

IMPORT FROM CSV FILE '/data/tpch/SF1/part.tbl'
    INTO TPCH.PART
    WITH
        RECORD DELIMITED BY '\n'
        FIELD DELIMITED BY '|'
        THREADS 10
        NO TYPE CHECK
        ERROR LOG '/data/tpch/SF1/error_log.txt'
        BATCH 1000;

IMPORT FROM CSV FILE '/data/tpch/SF1/supplier.tbl'
    INTO TPCH.SUPPLIER
    WITH
        RECORD DELIMITED BY '\n'
        FIELD DELIMITED BY '|'
        THREADS 10
        NO TYPE CHECK
        ERROR LOG '/data/tpch/SF1/error_log.txt'
        BATCH 1000;

IMPORT FROM CSV FILE '/data/tpch/SF1/partsupp.tbl'
    INTO TPCH.PARTSUPP
    WITH
        RECORD DELIMITED BY '\n'
        FIELD DELIMITED BY '|'
        THREADS 10
        NO TYPE CHECK
        ERROR LOG '/data/tpch/SF1/error_log.txt'
        BATCH 1000;

IMPORT FROM CSV FILE '/data/tpch/SF1/orders.tbl'
    INTO TPCH.ORDERS
    WITH
        RECORD DELIMITED BY '\n'
        FIELD DELIMITED BY '|'
        THREADS 10
        NO TYPE CHECK
        ERROR LOG '/data/tpch/SF1/error_log.txt'
        BATCH 1000;

IMPORT FROM CSV FILE '/data/tpch/SF1/lineitem.tbl'
    INTO TPCH.LINEITEM
    WITH
        RECORD DELIMITED BY '\n'
        FIELD DELIMITED BY '|'
        THREADS 10
        NO TYPE CHECK
        ERROR LOG '/data/tpch/SF1/error_log.txt'
        BATCH 1000;
