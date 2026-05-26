-- Benchmark-Experiment-Host-Manager | experiments/tpch/MemSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load TPC-H data at scale factor 10 (SF10 ≈ 10 GB) into MemSQL.
--          LOAD DATA INFILE reads pipe-delimited .tbl files from the server
--          filesystem. The trailing '|' dbgen appends is silently consumed
--          because MemSQL reads exactly as many fields as the table has columns.

LOAD DATA INFILE '/data/tpch/SF10/customer.tbl' INTO TABLE tpch.customer FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF10/lineitem.tbl' INTO TABLE tpch.lineitem FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF10/nation.tbl'   INTO TABLE tpch.nation   FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF10/orders.tbl'   INTO TABLE tpch.orders   FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF10/part.tbl'     INTO TABLE tpch.part     FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF10/partsupp.tbl' INTO TABLE tpch.partsupp FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF10/region.tbl'   INTO TABLE tpch.region   FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF10/supplier.tbl' INTO TABLE tpch.supplier FIELDS TERMINATED BY '|';
