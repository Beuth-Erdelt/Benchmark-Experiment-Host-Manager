-- Benchmark-Experiment-Host-Manager | experiments/tpch/CockroachDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Collect table statistics after data loading.
--          Run after initdata-tpch-SF*.sql (and optionally after initindexes).

ANALYZE public.customer;
ANALYZE public.lineitem;
ANALYZE public.nation;
ANALYZE public.orders;
ANALYZE public.part;
ANALYZE public.partsupp;
ANALYZE public.region;
ANALYZE public.supplier;
