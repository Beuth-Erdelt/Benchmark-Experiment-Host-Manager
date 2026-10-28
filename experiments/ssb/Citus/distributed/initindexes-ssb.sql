-- Benchmark-Experiment-Host-Manager | experiments/ssb/Citus/distributed
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create indexes after data loading (-xii), as for PostgreSQL: the
--          foreign key columns of lineorder for the joins, and the dimension
--          columns the 13 SSB queries filter on. Citus creates each index on
--          every shard (and every copy of a reference table).
--          No curly braces in this file: bexhoma may fill it with str.format().

CREATE INDEX idx_lineorder_orderdate ON public.lineorder (lo_orderdate);
CREATE INDEX idx_lineorder_custkey   ON public.lineorder (lo_custkey);
CREATE INDEX idx_lineorder_suppkey   ON public.lineorder (lo_suppkey);
CREATE INDEX idx_lineorder_partkey   ON public.lineorder (lo_partkey);
CREATE INDEX idx_customer_region     ON public.customer  (c_region);
CREATE INDEX idx_customer_nation     ON public.customer  (c_nation);
CREATE INDEX idx_customer_city       ON public.customer  (c_city);
CREATE INDEX idx_supplier_region     ON public.supplier  (s_region);
CREATE INDEX idx_supplier_nation     ON public.supplier  (s_nation);
CREATE INDEX idx_supplier_city       ON public.supplier  (s_city);
CREATE INDEX idx_part_mfgr           ON public.part      (p_mfgr);
CREATE INDEX idx_part_category       ON public.part      (p_category);
CREATE INDEX idx_part_brand1         ON public.part      (p_brand1);
CREATE INDEX idx_dates_year          ON public.dates     (d_year);
CREATE INDEX idx_dates_yearmonthnum  ON public.dates     (d_yearmonthnum);
CREATE INDEX idx_dates_yearmonth     ON public.dates     (d_yearmonth);
CREATE INDEX idx_dates_weeknuminyear ON public.dates     (d_weeknuminyear);
