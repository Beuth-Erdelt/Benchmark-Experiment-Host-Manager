-- Benchmark-Experiment-Host-Manager | experiments/tpch/MonetDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Add primary key and foreign key constraints to TPC-H tables.
--          Run after data loading (initdata-tpch-SF*.sql).
--          MonetDB does not support multiple actions in a single ALTER TABLE
--          statement; each constraint is applied as a separate statement.
--          Statements are ordered by FK dependency.
--          Table names are unqualified (MonetDB resolves them in the sys schema).

ALTER TABLE region
    ADD PRIMARY KEY (r_regionkey);

ALTER TABLE nation
    ADD PRIMARY KEY (n_nationkey);
ALTER TABLE nation
    ADD FOREIGN KEY (n_regionkey) REFERENCES region(r_regionkey);

ALTER TABLE part
    ADD PRIMARY KEY (p_partkey);

ALTER TABLE supplier
    ADD PRIMARY KEY (s_suppkey);
-- supplier->nation FK not applied: not required by the TPC-H query workload

ALTER TABLE partsupp
    ADD PRIMARY KEY (ps_partkey, ps_suppkey);
ALTER TABLE partsupp
    ADD FOREIGN KEY (ps_suppkey) REFERENCES supplier(s_suppkey);
ALTER TABLE partsupp
    ADD FOREIGN KEY (ps_partkey) REFERENCES part(p_partkey);

ALTER TABLE customer
    ADD PRIMARY KEY (c_custkey);
ALTER TABLE customer
    ADD FOREIGN KEY (c_nationkey) REFERENCES nation(n_nationkey);

ALTER TABLE orders
    ADD PRIMARY KEY (o_orderkey);
ALTER TABLE orders
    ADD FOREIGN KEY (o_custkey)   REFERENCES customer(c_custkey);

ALTER TABLE lineitem
    ADD PRIMARY KEY (l_orderkey, l_linenumber);
ALTER TABLE lineitem
    ADD FOREIGN KEY (l_orderkey)           REFERENCES orders(o_orderkey);
ALTER TABLE lineitem
    ADD FOREIGN KEY (l_partkey)            REFERENCES part(p_partkey);
ALTER TABLE lineitem
    ADD FOREIGN KEY (l_suppkey)            REFERENCES supplier(s_suppkey);
ALTER TABLE lineitem
    ADD FOREIGN KEY (l_partkey, l_suppkey) REFERENCES partsupp(ps_partkey, ps_suppkey);
