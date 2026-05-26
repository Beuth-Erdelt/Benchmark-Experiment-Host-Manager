-- Benchmark-Experiment-Host-Manager | experiments/tpch/DB2
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load TPC-H data at scale factor 1 (SF1 ≈ 1 GB) into the tpch schema.
--          Uses DB2 IMPORT with DEL (delimited) format and pipe as column delimiter.

CONNECT TO testdb USER db2inst1 USING root1234ROOT;
IMPORT FROM "/data/tpch/SF1/nation.tbl"   OF DEL MODIFIED BY COLDEL| INSERT INTO tpch.nation;
IMPORT FROM "/data/tpch/SF1/region.tbl"   OF DEL MODIFIED BY COLDEL| INSERT INTO tpch.region;
IMPORT FROM "/data/tpch/SF1/part.tbl"     OF DEL MODIFIED BY COLDEL| INSERT INTO tpch.part;
IMPORT FROM "/data/tpch/SF1/supplier.tbl" OF DEL MODIFIED BY COLDEL| INSERT INTO tpch.supplier;
IMPORT FROM "/data/tpch/SF1/partsupp.tbl" OF DEL MODIFIED BY COLDEL| INSERT INTO tpch.partsupp;
IMPORT FROM "/data/tpch/SF1/customer.tbl" OF DEL MODIFIED BY COLDEL| INSERT INTO tpch.customer;
IMPORT FROM "/data/tpch/SF1/orders.tbl"   OF DEL MODIFIED BY COLDEL| INSERT INTO tpch.orders;
IMPORT FROM "/data/tpch/SF1/lineitem.tbl" OF DEL MODIFIED BY COLDEL| INSERT INTO tpch.lineitem;
