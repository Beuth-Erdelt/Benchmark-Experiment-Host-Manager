-- Benchmark-Experiment-Host-Manager | experiments/tpch/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Add primary key and foreign key constraints to TPC-H tables.
--          Run after data loading (initdata-tpch-SF*.sql).
--          Each ALTER TABLE combines all actions for that table so it is
--          locked only once. Statements are ordered by FK dependency.
--          Note: the supplier→nation FK is part of the TPC-H DDL standard
--          but is not required by any query in the TPC-H workload and is
--          therefore not applied here.

ALTER TABLE public.region
    ADD PRIMARY KEY (r_regionkey);

ALTER TABLE public.nation
    ADD PRIMARY KEY (n_nationkey),
    ADD FOREIGN KEY (n_regionkey)          REFERENCES public.region(r_regionkey);

ALTER TABLE public.part
    ADD PRIMARY KEY (p_partkey);

ALTER TABLE public.supplier
    ADD PRIMARY KEY (s_suppkey);

ALTER TABLE public.partsupp
    ADD PRIMARY KEY (ps_partkey, ps_suppkey),
    ADD FOREIGN KEY (ps_suppkey)           REFERENCES public.supplier(s_suppkey),
    ADD FOREIGN KEY (ps_partkey)           REFERENCES public.part(p_partkey);

ALTER TABLE public.customer
    ADD PRIMARY KEY (c_custkey),
    ADD FOREIGN KEY (c_nationkey)          REFERENCES public.nation(n_nationkey);

ALTER TABLE public.orders
    ADD PRIMARY KEY (o_orderkey),
    ADD FOREIGN KEY (o_custkey)            REFERENCES public.customer(c_custkey);

ALTER TABLE public.lineitem
    ADD PRIMARY KEY (l_orderkey, l_linenumber),
    ADD FOREIGN KEY (l_orderkey)           REFERENCES public.orders(o_orderkey),
    ADD FOREIGN KEY (l_partkey)            REFERENCES public.part(p_partkey),
    ADD FOREIGN KEY (l_suppkey)            REFERENCES public.supplier(s_suppkey),
    ADD FOREIGN KEY (l_partkey, l_suppkey) REFERENCES public.partsupp(ps_partkey, ps_suppkey);
