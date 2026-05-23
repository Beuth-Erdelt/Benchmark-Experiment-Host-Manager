-- Benchmark-Experiment-Host-Manager | experiments/tpch/Kinetica
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Add foreign key constraints to TPC-H tables in Kinetica.
--          Statements are ordered by FK dependency. Table names are unqualified
--          because Kinetica places tables in the schema of the connected user.
--          supplier→nation FK not applied: not required by the TPC-H query workload.
--          Kinetica shard key caveats for lineitem:
--            l_suppkey → supplier: lineitem and supplier have different shard key counts.
--            (l_partkey, l_suppkey) → partsupp: shard keys exist but 0 were equated.

ALTER TABLE nation
    ADD FOREIGN KEY (n_regionkey) REFERENCES region (r_regionkey);

ALTER TABLE customer
    ADD FOREIGN KEY (c_nationkey) REFERENCES nation (n_nationkey);

ALTER TABLE partsupp
    ADD FOREIGN KEY (ps_suppkey) REFERENCES supplier (s_suppkey),
    ADD FOREIGN KEY (ps_partkey) REFERENCES part     (p_partkey);

ALTER TABLE orders
    ADD FOREIGN KEY (o_custkey) REFERENCES customer (c_custkey);

ALTER TABLE lineitem
    ADD FOREIGN KEY (l_orderkey)           REFERENCES orders   (o_orderkey),
    ADD FOREIGN KEY (l_partkey)            REFERENCES part     (p_partkey),
    ADD FOREIGN KEY (l_suppkey)            REFERENCES supplier (s_suppkey),
    ADD FOREIGN KEY (l_partkey, l_suppkey) REFERENCES partsupp (ps_partkey, ps_suppkey);
