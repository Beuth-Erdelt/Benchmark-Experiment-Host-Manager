-- Benchmark-Experiment-Host-Manager | experiments/tpch/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Collect table statistics and verify row counts after data loading.
--          {BEXHOMA_SCHEMA} is substituted at runtime by the Bexhoma framework.

ANALYZE VERBOSE {BEXHOMA_SCHEMA}.customer;
ANALYZE VERBOSE {BEXHOMA_SCHEMA}.lineitem;
ANALYZE VERBOSE {BEXHOMA_SCHEMA}.nation;
ANALYZE VERBOSE {BEXHOMA_SCHEMA}.orders;
ANALYZE VERBOSE {BEXHOMA_SCHEMA}.part;
ANALYZE VERBOSE {BEXHOMA_SCHEMA}.partsupp;
ANALYZE VERBOSE {BEXHOMA_SCHEMA}.region;
ANALYZE VERBOSE {BEXHOMA_SCHEMA}.supplier;

-- Verify that reference tables loaded correctly
SELECT COUNT(*) AS count_nation FROM {BEXHOMA_SCHEMA}.nation;
SELECT COUNT(*) AS count_region FROM {BEXHOMA_SCHEMA}.region;
