-- Benchmark-Experiment-Host-Manager | experiments/tpch/CockroachDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load TPC-H data at scale factor 1 (SF1 ≈ 1 GB) into the public schema
--          using CockroachDB's IMPORT INTO command. Source files must be BOM-free
--          UTF-8 (-nobom suffix) and accessible via the nodelocal file store.

IMPORT INTO public.customer CSV DATA ('nodelocal://self/data/tpch/SF1/customer-nobom.tbl') WITH delimiter = '|', nullif = '';
IMPORT INTO public.lineitem CSV DATA ('nodelocal://self/data/tpch/SF1/lineitem-nobom.tbl') WITH delimiter = '|', nullif = '';
IMPORT INTO public.nation   CSV DATA ('nodelocal://self/data/tpch/SF1/nation-nobom.tbl')   WITH delimiter = '|', nullif = '';
IMPORT INTO public.orders   CSV DATA ('nodelocal://self/data/tpch/SF1/orders-nobom.tbl')   WITH delimiter = '|', nullif = '';
IMPORT INTO public.part     CSV DATA ('nodelocal://self/data/tpch/SF1/part-nobom.tbl')     WITH delimiter = '|', nullif = '';
IMPORT INTO public.partsupp CSV DATA ('nodelocal://self/data/tpch/SF1/partsupp-nobom.tbl') WITH delimiter = '|', nullif = '';
IMPORT INTO public.region   CSV DATA ('nodelocal://self/data/tpch/SF1/region-nobom.tbl')   WITH delimiter = '|', nullif = '';
IMPORT INTO public.supplier CSV DATA ('nodelocal://self/data/tpch/SF1/supplier-nobom.tbl') WITH delimiter = '|', nullif = '';
