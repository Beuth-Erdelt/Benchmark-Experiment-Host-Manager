-- Benchmark-Experiment-Host-Manager | experiments/tpch/MonetDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load TPC-H data at scale factor 30 (SF30 ~ 30 GB) using MonetDB's
--          COPY INTO command. DELIMITERS '|' matches dbgen's pipe output.

COPY INTO customer FROM '/data/tpch/SF30/customer.tbl' DELIMITERS '|';
COPY INTO lineitem FROM '/data/tpch/SF30/lineitem.tbl' DELIMITERS '|';
COPY INTO nation   FROM '/data/tpch/SF30/nation.tbl'   DELIMITERS '|';
COPY INTO orders   FROM '/data/tpch/SF30/orders.tbl'   DELIMITERS '|';
COPY INTO part     FROM '/data/tpch/SF30/part.tbl'     DELIMITERS '|';
COPY INTO partsupp FROM '/data/tpch/SF30/partsupp.tbl' DELIMITERS '|';
COPY INTO region   FROM '/data/tpch/SF30/region.tbl'   DELIMITERS '|';
COPY INTO supplier FROM '/data/tpch/SF30/supplier.tbl' DELIMITERS '|';
