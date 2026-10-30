-- Benchmark-Experiment-Host-Manager | experiments/ssb/CedarDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create indexes after data loading (-xii): the foreign key columns of
--          lineorder for the joins, and the dimension columns the 13 SSB queries
--          filter on (region/nation/city, mfgr/category/brand, year/month/week).
--          No curly braces in this file: bexhoma may fill it with str.format().

CREATE INDEX ON public.lineorder (lo_orderdate);
CREATE INDEX ON public.lineorder (lo_custkey);
CREATE INDEX ON public.lineorder (lo_suppkey);
CREATE INDEX ON public.lineorder (lo_partkey);
CREATE INDEX ON public.customer  (c_region);
CREATE INDEX ON public.customer  (c_nation);
CREATE INDEX ON public.customer  (c_city);
CREATE INDEX ON public.supplier  (s_region);
CREATE INDEX ON public.supplier  (s_nation);
CREATE INDEX ON public.supplier  (s_city);
CREATE INDEX ON public.part      (p_mfgr);
CREATE INDEX ON public.part      (p_category);
CREATE INDEX ON public.part      (p_brand1);
CREATE INDEX ON public.dates     (d_year);
CREATE INDEX ON public.dates     (d_yearmonthnum);
CREATE INDEX ON public.dates     (d_yearmonth);
CREATE INDEX ON public.dates     (d_weeknuminyear);
