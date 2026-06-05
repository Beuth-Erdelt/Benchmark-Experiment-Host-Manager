-- Benchmark-Experiment-Host-Manager | experiments/tpch/MonetDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load TPC-H data at scale factor 3 (SF3 ~ 3 GB) using MonetDB's
--          COPY INTO command. DELIMITERS '|' matches dbgen's pipe output;
--          NULL AS '' maps the trailing empty field to NULL.

COPY INTO customer FROM '/data/tpch/SF3/customer.tbl' DELIMITERS '|' NULL AS '';
COPY INTO lineitem FROM '/data/tpch/SF3/lineitem.tbl' DELIMITERS '|' NULL AS '';
COPY INTO nation   FROM '/data/tpch/SF3/nation.tbl'   DELIMITERS '|' NULL AS '';
COPY INTO orders   FROM '/data/tpch/SF3/orders.tbl'   DELIMITERS '|' NULL AS '';
COPY INTO part     FROM '/data/tpch/SF3/part.tbl'     DELIMITERS '|' NULL AS '';
COPY INTO partsupp FROM '/data/tpch/SF3/partsupp.tbl' DELIMITERS '|' NULL AS '';
COPY INTO region   FROM '/data/tpch/SF3/region.tbl'   DELIMITERS '|' NULL AS '';
COPY INTO supplier FROM '/data/tpch/SF3/supplier.tbl' DELIMITERS '|' NULL AS '';
