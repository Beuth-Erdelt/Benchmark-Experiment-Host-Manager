-- Benchmark-Experiment-Host-Manager | experiments/tpch/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create indexes on foreign key columns to support join operations
--          in TPC-H queries. Run after data loading.
--          Separate indexes on lineitem(l_partkey) and lineitem(l_suppkey) are
--          omitted: l_partkey is already covered as the leading column of the
--          compound index (l_partkey, l_suppkey), and l_suppkey alone is not
--          selective enough to benefit queries in the TPC-H workload.

CREATE INDEX ON public.nation   (n_regionkey);
CREATE INDEX ON public.customer (c_nationkey);
CREATE INDEX ON public.partsupp (ps_suppkey);
CREATE INDEX ON public.partsupp (ps_partkey);
CREATE INDEX ON public.orders   (o_custkey);
CREATE INDEX ON public.lineitem (l_orderkey);
CREATE INDEX ON public.lineitem (l_partkey, l_suppkey);
