-- Benchmark-Experiment-Host-Manager | experiments/tpch/Exasol
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Add primary key constraints to TPC-H tables in Exasol.
--          In Exasol primary keys are not enforced at insert time; they serve
--          as optimizer hints that enable join elimination and filter push-down.
--          No secondary indexes are created: Exasol's columnar storage and
--          zone maps make traditional B-tree indexes unnecessary for the TPC-H
--          analytical workload.

ALTER TABLE public.region
    ADD PRIMARY KEY (r_regionkey);

ALTER TABLE public.nation
    ADD PRIMARY KEY (n_nationkey);

ALTER TABLE public.part
    ADD PRIMARY KEY (p_partkey);

ALTER TABLE public.supplier
    ADD PRIMARY KEY (s_suppkey);

ALTER TABLE public.partsupp
    ADD PRIMARY KEY (ps_partkey, ps_suppkey);

ALTER TABLE public.customer
    ADD PRIMARY KEY (c_custkey);

ALTER TABLE public.orders
    ADD PRIMARY KEY (o_orderkey);

ALTER TABLE public.lineitem
    ADD PRIMARY KEY (l_orderkey, l_linenumber);
