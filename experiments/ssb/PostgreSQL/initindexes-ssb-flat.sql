-- Benchmark-Experiment-Host-Manager | experiments/ssb/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create indexes on lineorder_flat after data loading (-xii, -xsv flat):
--          the order date (every query restricts it or groups by it) and the
--          dimension columns the 13 SSB queries filter on.
--          No curly braces in this file: bexhoma may fill it with str.format().

CREATE INDEX ON public.lineorder_flat (lo_orderdate);
CREATE INDEX ON public.lineorder_flat (c_region);
CREATE INDEX ON public.lineorder_flat (c_nation);
CREATE INDEX ON public.lineorder_flat (c_city);
CREATE INDEX ON public.lineorder_flat (s_region);
CREATE INDEX ON public.lineorder_flat (s_nation);
CREATE INDEX ON public.lineorder_flat (s_city);
CREATE INDEX ON public.lineorder_flat (p_mfgr);
CREATE INDEX ON public.lineorder_flat (p_category);
CREATE INDEX ON public.lineorder_flat (p_brand1);
