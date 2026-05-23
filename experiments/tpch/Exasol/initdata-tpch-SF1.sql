-- Benchmark-Experiment-Host-Manager | experiments/tpch/Exasol
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load TPC-H data at scale factor 1 (SF1 ≈ 1 GB) into Exasol.
--          IMPORT INTO reads pipe-delimited .tbl files from the local filesystem;
--          SKIP = 0 means no header row to skip.

IMPORT INTO public.customer FROM LOCAL CSV FILE '/data/tpch/SF1/customer.tbl' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.lineitem FROM LOCAL CSV FILE '/data/tpch/SF1/lineitem.tbl' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.nation   FROM LOCAL CSV FILE '/data/tpch/SF1/nation.tbl'   COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.orders   FROM LOCAL CSV FILE '/data/tpch/SF1/orders.tbl'   COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.part     FROM LOCAL CSV FILE '/data/tpch/SF1/part.tbl'     COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.partsupp FROM LOCAL CSV FILE '/data/tpch/SF1/partsupp.tbl' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.region   FROM LOCAL CSV FILE '/data/tpch/SF1/region.tbl'   COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.supplier FROM LOCAL CSV FILE '/data/tpch/SF1/supplier.tbl' COLUMN SEPARATOR = '|' SKIP = 0;
