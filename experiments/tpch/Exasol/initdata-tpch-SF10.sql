-- Benchmark-Experiment-Host-Manager | experiments/tpch/Exasol
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load TPC-H data at scale factor 10 (SF10 ~ 10 GB) into Exasol.
--          IMPORT INTO reads pipe-delimited .tbl files from the local filesystem;
--          SKIP = 0 means no header row to skip.

IMPORT INTO public.customer FROM LOCAL CSV FILE '/data/tpch/SF10/customer.tbl' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.lineitem FROM LOCAL CSV FILE '/data/tpch/SF10/lineitem.tbl' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.nation   FROM LOCAL CSV FILE '/data/tpch/SF10/nation.tbl'   COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.orders   FROM LOCAL CSV FILE '/data/tpch/SF10/orders.tbl'   COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.part     FROM LOCAL CSV FILE '/data/tpch/SF10/part.tbl'     COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.partsupp FROM LOCAL CSV FILE '/data/tpch/SF10/partsupp.tbl' COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.region   FROM LOCAL CSV FILE '/data/tpch/SF10/region.tbl'   COLUMN SEPARATOR = '|' SKIP = 0;
IMPORT INTO public.supplier FROM LOCAL CSV FILE '/data/tpch/SF10/supplier.tbl' COLUMN SEPARATOR = '|' SKIP = 0;
