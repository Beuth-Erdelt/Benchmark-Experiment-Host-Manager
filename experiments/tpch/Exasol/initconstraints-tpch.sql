-- Benchmark-Experiment-Host-Manager | experiments/tpch/Exasol
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Add foreign key constraints to TPC-H tables in Exasol.
--          Primary keys are added separately in initindexes-tpch.sql; Exasol
--          treats PKs primarily as optimizer hints rather than enforcement.
--          The supplier→nation FK is applied here; it is part of the TPC-H DDL
--          standard and Exasol can use it as a join-elimination hint.
--          Statements are ordered by FK dependency.

ALTER TABLE public.nation
    ADD FOREIGN KEY (n_regionkey) REFERENCES public.region (r_regionkey);

ALTER TABLE public.supplier
    ADD FOREIGN KEY (s_nationkey) REFERENCES public.nation (n_nationkey);

ALTER TABLE public.customer
    ADD FOREIGN KEY (c_nationkey) REFERENCES public.nation (n_nationkey);

ALTER TABLE public.partsupp
    ADD FOREIGN KEY (ps_suppkey) REFERENCES public.supplier (s_suppkey),
    ADD FOREIGN KEY (ps_partkey) REFERENCES public.part     (p_partkey);

ALTER TABLE public.orders
    ADD FOREIGN KEY (o_custkey) REFERENCES public.customer (c_custkey);

ALTER TABLE public.lineitem
    ADD FOREIGN KEY (l_orderkey)           REFERENCES public.orders   (o_orderkey),
    ADD FOREIGN KEY (l_partkey, l_suppkey) REFERENCES public.partsupp (ps_partkey, ps_suppkey);
