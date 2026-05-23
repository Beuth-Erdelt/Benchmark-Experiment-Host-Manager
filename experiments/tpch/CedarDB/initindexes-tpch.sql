-- Benchmark-Experiment-Host-Manager | experiments/tpch/CedarDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create indexes on foreign key columns to accelerate TPC-H join queries
--          in CedarDB. Indexes on lineitem(l_partkey) and lineitem(l_suppkey) are
--          omitted: l_partkey is covered as the leading column of the compound index
--          (l_partkey, l_suppkey); l_suppkey alone is not selective enough for the
--          TPC-H workload.

CREATE INDEX n_r  ON public.nation   (n_regionkey);
CREATE INDEX c_n  ON public.customer (c_nationkey);
CREATE INDEX ps_p ON public.partsupp (ps_partkey);
CREATE INDEX ps_s ON public.partsupp (ps_suppkey);
CREATE INDEX o_c  ON public.orders   (o_custkey);
CREATE INDEX l_o  ON public.lineitem (l_orderkey);
CREATE INDEX l_ps ON public.lineitem (l_partkey, l_suppkey);
