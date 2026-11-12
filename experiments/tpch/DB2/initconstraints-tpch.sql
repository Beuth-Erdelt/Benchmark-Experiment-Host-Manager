-- Benchmark-Experiment-Host-Manager | experiments/tpch/DB2
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Foreign keys of the TPC-H tables (TPC-H spec section 1.4.2.3), the
--          same as for SQL Server and Oracle. They are enforced and checked
--          against the loaded rows (ENFORCED, the default), so the optimizer may
--          trust them. Runs in the schema DB2INST1 (default schema of the CLP
--          session of /tmp/bexhoma-run.sh).
--          No curly braces in this file: bexhoma may fill it with str.format().

ALTER TABLE nation
    ADD CONSTRAINT fk_n_r FOREIGN KEY (n_regionkey) REFERENCES region (r_regionkey);

ALTER TABLE partsupp
    ADD CONSTRAINT fk_ps_s FOREIGN KEY (ps_suppkey) REFERENCES supplier (s_suppkey)
    ADD CONSTRAINT fk_ps_p FOREIGN KEY (ps_partkey) REFERENCES part (p_partkey);

ALTER TABLE supplier
    ADD CONSTRAINT fk_s_n FOREIGN KEY (s_nationkey) REFERENCES nation (n_nationkey);

ALTER TABLE customer
    ADD CONSTRAINT fk_c_n FOREIGN KEY (c_nationkey) REFERENCES nation (n_nationkey);

ALTER TABLE orders
    ADD CONSTRAINT fk_o_c FOREIGN KEY (o_custkey) REFERENCES customer (c_custkey);

ALTER TABLE lineitem
    ADD CONSTRAINT fk_l_o  FOREIGN KEY (l_orderkey)           REFERENCES orders (o_orderkey)
    ADD CONSTRAINT fk_l_p  FOREIGN KEY (l_partkey)            REFERENCES part (p_partkey)
    ADD CONSTRAINT fk_l_s  FOREIGN KEY (l_suppkey)            REFERENCES supplier (s_suppkey)
    ADD CONSTRAINT fk_l_ps FOREIGN KEY (l_partkey, l_suppkey) REFERENCES partsupp (ps_partkey, ps_suppkey);
