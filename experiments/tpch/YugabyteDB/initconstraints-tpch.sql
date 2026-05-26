-- Benchmark-Experiment-Host-Manager | experiments/tpch/YugabyteDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Add foreign key constraints to TPC-H tables. Run after data loading.
--          Statements are ordered by FK dependency; each ALTER TABLE combines
--          all FK actions for that table. Table references are unqualified
--          (YugabyteDB resolves them in the default public schema).

ALTER TABLE public.nation
    ADD FOREIGN KEY (n_regionkey) REFERENCES region(r_regionkey);
-- supplier→nation FK not applied: not required by the TPC-H query workload

ALTER TABLE public.partsupp
    ADD FOREIGN KEY (ps_suppkey) REFERENCES supplier(s_suppkey),
    ADD FOREIGN KEY (ps_partkey) REFERENCES part(p_partkey);

ALTER TABLE public.customer
    ADD FOREIGN KEY (c_nationkey) REFERENCES nation(n_nationkey);

ALTER TABLE public.orders
    ADD FOREIGN KEY (o_custkey)   REFERENCES customer(c_custkey);

ALTER TABLE public.lineitem
    ADD FOREIGN KEY (l_orderkey)           REFERENCES orders(o_orderkey),
    ADD FOREIGN KEY (l_partkey)            REFERENCES part(p_partkey),
    ADD FOREIGN KEY (l_suppkey)            REFERENCES supplier(s_suppkey),
    ADD FOREIGN KEY (l_partkey, l_suppkey) REFERENCES partsupp(ps_partkey, ps_suppkey);
