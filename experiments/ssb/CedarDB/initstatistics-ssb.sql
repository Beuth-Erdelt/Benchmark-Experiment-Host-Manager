-- Benchmark-Experiment-Host-Manager | experiments/ssb/CedarDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Collect table statistics after data loading (-xis).
--          No curly braces in this file: bexhoma may fill it with str.format().

ANALYZE VERBOSE public.customer;
ANALYZE VERBOSE public.supplier;
ANALYZE VERBOSE public.part;
ANALYZE VERBOSE public.dates;
ANALYZE VERBOSE public.lineorder;
