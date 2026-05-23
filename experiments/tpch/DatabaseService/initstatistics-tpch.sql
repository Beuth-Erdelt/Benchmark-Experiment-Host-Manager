-- Benchmark-Experiment-Host-Manager | experiments/tpch/DatabaseService
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Collect optimizer statistics after data loading in DatabaseService.
--          ANALYZE VERBOSE updates the planner's statistics for all TPC-H tables.

ANALYZE VERBOSE public.customer;
ANALYZE VERBOSE public.lineitem;
ANALYZE VERBOSE public.nation;
ANALYZE VERBOSE public.orders;
ANALYZE VERBOSE public.part;
ANALYZE VERBOSE public.partsupp;
ANALYZE VERBOSE public.region;
ANALYZE VERBOSE public.supplier;
