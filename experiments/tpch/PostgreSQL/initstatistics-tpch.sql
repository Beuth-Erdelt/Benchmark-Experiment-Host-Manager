-- Benchmark-Experiment-Host-Manager | experiments/tpch/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Collect table statistics and verify row counts after data loading.
--          Re-enables synchronous commit that was disabled in initschema-tpch.sql.

ANALYZE VERBOSE public.customer;
ANALYZE VERBOSE public.lineitem;
ANALYZE VERBOSE public.nation;
ANALYZE VERBOSE public.orders;
ANALYZE VERBOSE public.part;
ANALYZE VERBOSE public.partsupp;
ANALYZE VERBOSE public.region;
ANALYZE VERBOSE public.supplier;

-- Verify that reference tables loaded correctly
SELECT COUNT(*) AS count_nation FROM public.nation;
SELECT COUNT(*) AS count_region FROM public.region;

-- Restore synchronous commit after bulk loading
ALTER SYSTEM SET synchronous_commit = on;
SELECT pg_reload_conf();
