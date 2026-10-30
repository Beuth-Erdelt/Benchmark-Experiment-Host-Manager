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
--          Access method and deduplication are DDL parameters (ddl-parameters.config);
--          the multicolumn index stays a B-tree (hash indexes have one column).

CREATE INDEX ON public.nation{index_method}   (n_regionkey){btree_dedup};
CREATE INDEX ON public.customer{index_method} (c_nationkey){btree_dedup};
CREATE INDEX ON public.partsupp{index_method} (ps_suppkey){btree_dedup};
CREATE INDEX ON public.partsupp{index_method} (ps_partkey){btree_dedup};
CREATE INDEX ON public.orders{index_method}   (o_custkey){btree_dedup};
CREATE INDEX ON public.lineitem{index_method} (l_orderkey){btree_dedup};
CREATE INDEX ON public.lineitem (l_partkey, l_suppkey){btree_dedup};
