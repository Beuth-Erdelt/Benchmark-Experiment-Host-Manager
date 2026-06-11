-- Benchmark-Experiment-Host-Manager | experiments/tpch/CockroachDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Add foreign key constraints to TPC-H tables. Run after data loading.
--          NOT VALID skips validation of existing rows, which is safe after a
--          bulk load from trusted dbgen data. Statements are ordered by FK
--          dependency. Note: the supplier->nation FK is applied here (unlike
--          most other DBMS variants) following the full TPC-H DDL standard.
--          CockroachDB automatically creates a backing index for each FK.
-- Reference: https://github.com/cockroachdb/cockroach/blob/master/pkg/workload/tpch/tpch.go

ALTER TABLE nation
    ADD CONSTRAINT nation_fkey_region   FOREIGN KEY (n_regionkey) REFERENCES region (r_regionkey) NOT VALID;

ALTER TABLE supplier
    ADD CONSTRAINT supplier_fkey_nation FOREIGN KEY (s_nationkey) REFERENCES nation (n_nationkey) NOT VALID;

ALTER TABLE partsupp
    ADD CONSTRAINT partsupp_fkey_part     FOREIGN KEY (ps_partkey) REFERENCES part     (p_partkey) NOT VALID,
    ADD CONSTRAINT partsupp_fkey_supplier FOREIGN KEY (ps_suppkey) REFERENCES supplier (s_suppkey) NOT VALID;

ALTER TABLE customer
    ADD CONSTRAINT customer_fkey_nation  FOREIGN KEY (c_nationkey) REFERENCES nation   (n_nationkey) NOT VALID;

ALTER TABLE orders
    ADD CONSTRAINT orders_fkey_customer  FOREIGN KEY (o_custkey)   REFERENCES customer (c_custkey)   NOT VALID;

ALTER TABLE lineitem
    ADD CONSTRAINT lineitem_fkey_orders   FOREIGN KEY (l_orderkey) REFERENCES orders   (o_orderkey) NOT VALID,
    ADD CONSTRAINT lineitem_fkey_part     FOREIGN KEY (l_partkey)  REFERENCES part     (p_partkey)  NOT VALID,
    ADD CONSTRAINT lineitem_fkey_supplier FOREIGN KEY (l_suppkey)  REFERENCES supplier (s_suppkey)  NOT VALID;
