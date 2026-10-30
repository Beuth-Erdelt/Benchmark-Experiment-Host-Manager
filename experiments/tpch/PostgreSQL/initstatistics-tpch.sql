-- Benchmark-Experiment-Host-Manager | experiments/tpch/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Collect table statistics and verify row counts after data loading.

-- Statistics target and extended statistics are DDL parameters (ddl-parameters.config).
-- ALTER DATABASE: the ANALYZE of a reset script (-ar) keeps the target.
ALTER DATABASE postgres SET default_statistics_target = {statistics_target};
SET default_statistics_target = {statistics_target};
{extended_statistics}

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
