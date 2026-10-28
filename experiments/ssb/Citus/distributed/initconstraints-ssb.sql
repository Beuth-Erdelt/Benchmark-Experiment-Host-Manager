-- Benchmark-Experiment-Host-Manager | experiments/ssb/Citus/distributed
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Add constraints after data loading (-xic), for distributed dimensions
--          (-xdim distributed): the primary keys of the SSB specification, each
--          including its table's distribution column. No foreign keys: Citus
--          allows a foreign key between distributed tables only when they are
--          co-located and the key includes the distribution column, and
--          lineorder is distributed by lo_orderkey, not by a dimension key.
--          No curly braces in this file: bexhoma may fill it with str.format().

ALTER TABLE public.customer  ADD PRIMARY KEY (c_custkey);
ALTER TABLE public.supplier  ADD PRIMARY KEY (s_suppkey);
ALTER TABLE public.part      ADD PRIMARY KEY (p_partkey);
ALTER TABLE public.dates     ADD PRIMARY KEY (d_datekey);
ALTER TABLE public.lineorder ADD PRIMARY KEY (lo_orderkey, lo_linenumber);
