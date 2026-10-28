-- Benchmark-Experiment-Host-Manager | experiments/ssb/Citus
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create indexes on lineorder_flat after data loading (-xii, -xsv flat),
--          as for PostgreSQL: the order date and the dimension columns the 13
--          SSB queries filter on. Citus creates each index on every shard.
--          No curly braces in this file: bexhoma may fill it with str.format().

CREATE INDEX idx_lineorder_flat_orderdate ON public.lineorder_flat (lo_orderdate);
CREATE INDEX idx_lineorder_flat_c_region  ON public.lineorder_flat (c_region);
CREATE INDEX idx_lineorder_flat_c_nation  ON public.lineorder_flat (c_nation);
CREATE INDEX idx_lineorder_flat_c_city    ON public.lineorder_flat (c_city);
CREATE INDEX idx_lineorder_flat_s_region  ON public.lineorder_flat (s_region);
CREATE INDEX idx_lineorder_flat_s_nation  ON public.lineorder_flat (s_nation);
CREATE INDEX idx_lineorder_flat_s_city    ON public.lineorder_flat (s_city);
CREATE INDEX idx_lineorder_flat_p_mfgr    ON public.lineorder_flat (p_mfgr);
CREATE INDEX idx_lineorder_flat_category  ON public.lineorder_flat (p_category);
CREATE INDEX idx_lineorder_flat_brand1    ON public.lineorder_flat (p_brand1);
