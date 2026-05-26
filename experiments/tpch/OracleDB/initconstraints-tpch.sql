-- Benchmark-Experiment-Host-Manager | experiments/tpch/OracleDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Add CHECK constraints to TPC-H tables in OracleDB per TPC-H spec
--          sections 1.4.2.4-1 (non-negative key columns), 1.4.2.4-2 (non-negative
--          quantity/price columns), and 1.4.2.4-3 (discount range).
--          Primary key and foreign key constraints are added in initindexes-tpch.sql.

-- TPC-H spec 1.4.2.4-1: non-negative key columns
ALTER TABLE tpch.part
    ADD CONSTRAINT chk_part_partkey CHECK (p_partkey >= 0);

ALTER TABLE tpch.supplier
    ADD CONSTRAINT chk_supplier_suppkey CHECK (s_suppkey >= 0);

ALTER TABLE tpch.customer
    ADD CONSTRAINT chk_customer_custkey CHECK (c_custkey >= 0);

ALTER TABLE tpch.partsupp
    ADD CONSTRAINT chk_partsupp_partkey CHECK (ps_partkey >= 0);

ALTER TABLE tpch.region
    ADD CONSTRAINT chk_region_regionkey CHECK (r_regionkey >= 0);

ALTER TABLE tpch.nation
    ADD CONSTRAINT chk_nation_nationkey CHECK (n_nationkey >= 0);

-- TPC-H spec 1.4.2.4-2: non-negative quantity and price columns
ALTER TABLE tpch.part
    ADD (CONSTRAINT chk_part_size        CHECK (p_size >= 0),
         CONSTRAINT chk_part_retailprice CHECK (p_retailprice >= 0));

ALTER TABLE tpch.partsupp
    ADD (CONSTRAINT chk_partsupp_availqty   CHECK (ps_availqty >= 0),
         CONSTRAINT chk_partsupp_supplycost CHECK (ps_supplycost >= 0));

ALTER TABLE tpch.orders
    ADD CONSTRAINT chk_orders_totalprice CHECK (o_totalprice >= 0);

ALTER TABLE tpch.lineitem
    ADD (CONSTRAINT chk_lineitem_quantity       CHECK (l_quantity >= 0),
         CONSTRAINT chk_lineitem_extendedprice  CHECK (l_extendedprice >= 0),
         CONSTRAINT chk_lineitem_tax            CHECK (l_tax >= 0));

-- TPC-H spec 1.4.2.4-3: discount bounded to [0.00, 1.00]
ALTER TABLE tpch.lineitem
    ADD CONSTRAINT chk_lineitem_discount CHECK (l_discount >= 0.00 AND l_discount <= 1.00);
