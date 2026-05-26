-- Benchmark-Experiment-Host-Manager | experiments/tpch/SingleStore
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load TPC-H data at scale factor 1 (SF1 ≈ 1 GB) into SingleStore.
--          LOAD DATA INFILE reads pipe-delimited .tbl files from the server
--          filesystem. The trailing '|' dbgen appends is silently consumed
--          because SingleStore reads exactly as many fields as the table has columns.

LOAD DATA INFILE '/data/tpch/SF1/customer.tbl' INTO TABLE tpch.customer FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF1/lineitem.tbl' INTO TABLE tpch.lineitem FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF1/nation.tbl'   INTO TABLE tpch.nation   FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF1/orders.tbl'   INTO TABLE tpch.orders   FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF1/part.tbl'     INTO TABLE tpch.part     FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF1/partsupp.tbl' INTO TABLE tpch.partsupp FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF1/region.tbl'   INTO TABLE tpch.region   FIELDS TERMINATED BY '|';
LOAD DATA INFILE '/data/tpch/SF1/supplier.tbl' INTO TABLE tpch.supplier FIELDS TERMINATED BY '|';
