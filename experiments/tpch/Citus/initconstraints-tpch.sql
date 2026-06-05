-- Benchmark-Experiment-Host-Manager | experiments/tpch/Citus
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Add TPC-H foreign key constraints for Citus.
--          All 8 FK relationships from the TPC-H DDL are applied, including
--          nation->region and supplier->nation. Citus enforces FKs between
--          distributed and reference tables at the coordinator.
--          Statements are ordered by FK dependency: referenced tables first.

ALTER TABLE nation
    ADD CONSTRAINT nation_region_fkey
        FOREIGN KEY (n_regionkey) REFERENCES region (r_regionkey);

ALTER TABLE supplier
    ADD CONSTRAINT supplier_nation_fkey
        FOREIGN KEY (s_nationkey) REFERENCES nation (n_nationkey);

ALTER TABLE partsupp
    ADD CONSTRAINT partsupp_part_fkey
        FOREIGN KEY (ps_partkey) REFERENCES part (p_partkey),
    ADD CONSTRAINT partsupp_supplier_fkey
        FOREIGN KEY (ps_suppkey) REFERENCES supplier (s_suppkey);

ALTER TABLE customer
    ADD CONSTRAINT customer_nation_fkey
        FOREIGN KEY (c_nationkey) REFERENCES nation (n_nationkey);

ALTER TABLE orders
    ADD CONSTRAINT orders_customer_fkey
        FOREIGN KEY (o_custkey) REFERENCES customer (c_custkey);

ALTER TABLE lineitem
    ADD CONSTRAINT lineitem_orders_fkey
        FOREIGN KEY (l_orderkey) REFERENCES orders (o_orderkey),
    ADD CONSTRAINT lineitem_partsupp_fkey
        FOREIGN KEY (l_partkey, l_suppkey) REFERENCES partsupp (ps_partkey, ps_suppkey);
