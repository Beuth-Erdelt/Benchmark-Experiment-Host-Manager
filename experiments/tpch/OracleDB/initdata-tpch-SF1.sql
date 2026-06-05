-- Benchmark-Experiment-Host-Manager | experiments/tpch/OracleDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load TPC-H data at scale factor 1 (SF1 ~ 1 GB) into OracleDB.
--          Each INSERT reads from the corresponding external table (ext_<name>)
--          created in initschema-tpch.sql; the /*+ APPEND */ hint uses direct-path
--          insert to bypass the buffer cache and speed up bulk loading.
--          NLS_DATE_FORMAT ensures that CHAR(10) date strings in the .tbl files
--          are correctly parsed into Oracle DATE values.

ALTER SESSION SET nls_date_format = 'YYYY-MM-DD';

INSERT /*+ APPEND */ INTO tpch.part     SELECT * FROM tpch.ext_part;
INSERT /*+ APPEND */ INTO tpch.supplier SELECT * FROM tpch.ext_supplier;
INSERT /*+ APPEND */ INTO tpch.partsupp SELECT * FROM tpch.ext_partsupp;
INSERT /*+ APPEND */ INTO tpch.customer SELECT * FROM tpch.ext_customer;
INSERT /*+ APPEND */ INTO tpch.orders   SELECT * FROM tpch.ext_orders;
INSERT /*+ APPEND */ INTO tpch.lineitem SELECT * FROM tpch.ext_lineitem;
INSERT /*+ APPEND */ INTO tpch.nation   SELECT * FROM tpch.ext_nation;
INSERT /*+ APPEND */ INTO tpch.region   SELECT * FROM tpch.ext_region;
