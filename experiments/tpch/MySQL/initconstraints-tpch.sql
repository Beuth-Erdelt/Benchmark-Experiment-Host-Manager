-- Benchmark-Experiment-Host-Manager | experiments/tpch/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Add primary key and foreign key constraints to TPC-H tables.
--          Run after data loading (initdata-tpch-SF*.sql).
--          Each ALTER TABLE combines all actions for that table so it is
--          locked only once. Statements are ordered by FK dependency.

ALTER TABLE tpch.region
    ADD PRIMARY KEY (r_regionkey);

ALTER TABLE tpch.nation
    ADD PRIMARY KEY (n_nationkey),
    ADD FOREIGN KEY (n_regionkey) REFERENCES tpch.region(r_regionkey);

ALTER TABLE tpch.part
    ADD PRIMARY KEY (p_partkey);

ALTER TABLE tpch.supplier
    ADD PRIMARY KEY (s_suppkey);
-- supplier→nation FK not applied: not required by the TPC-H query workload

ALTER TABLE tpch.partsupp
    ADD PRIMARY KEY (ps_partkey, ps_suppkey),
    ADD FOREIGN KEY (ps_suppkey) REFERENCES tpch.supplier(s_suppkey),
    ADD FOREIGN KEY (ps_partkey) REFERENCES tpch.part(p_partkey);

ALTER TABLE tpch.customer
    ADD PRIMARY KEY (c_custkey),
    ADD FOREIGN KEY (c_nationkey) REFERENCES tpch.nation(n_nationkey);

ALTER TABLE tpch.orders
    ADD PRIMARY KEY (o_orderkey),
    ADD FOREIGN KEY (o_custkey)   REFERENCES tpch.customer(c_custkey);

ALTER TABLE tpch.lineitem
    ADD PRIMARY KEY (l_orderkey, l_linenumber),
    ADD FOREIGN KEY (l_orderkey)           REFERENCES tpch.orders(o_orderkey),
    ADD FOREIGN KEY (l_partkey)            REFERENCES tpch.part(p_partkey),
    ADD FOREIGN KEY (l_suppkey)            REFERENCES tpch.supplier(s_suppkey),
    ADD FOREIGN KEY (l_partkey, l_suppkey) REFERENCES tpch.partsupp(ps_partkey, ps_suppkey);
