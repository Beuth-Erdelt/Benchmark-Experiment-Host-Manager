-- Benchmark-Experiment-Host-Manager | experiments/tpch/OracleDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Add primary key and foreign key constraints to TPC-H tables in OracleDB.
--          This file is named initindexes because Oracle creates a unique index
--          automatically for each PRIMARY KEY constraint; both structures are added
--          in one step. Foreign keys per TPC-H spec section 1.4.2.3 are included
--          here rather than in initconstraints-tpch.sql (which holds CHECK constraints).
--          Note: nation→region and supplier→nation FKs are not applied; lineitem→part
--          and lineitem→supplier FKs are applied (all per TPC-H spec 1.4.2.3).

ALTER TABLE tpch.region
    ADD CONSTRAINT pk_region PRIMARY KEY (r_regionkey);

ALTER TABLE tpch.nation
    ADD CONSTRAINT pk_nation PRIMARY KEY (n_nationkey);

ALTER TABLE tpch.part
    ADD CONSTRAINT pk_part PRIMARY KEY (p_partkey);

ALTER TABLE tpch.supplier
    ADD CONSTRAINT pk_supplier PRIMARY KEY (s_suppkey);

ALTER TABLE tpch.partsupp
    ADD (CONSTRAINT pk_partsupp          PRIMARY KEY (ps_partkey, ps_suppkey),
         CONSTRAINT fk_partsupp_part     FOREIGN KEY (ps_partkey) REFERENCES tpch.part     (p_partkey),
         CONSTRAINT fk_partsupp_supplier FOREIGN KEY (ps_suppkey) REFERENCES tpch.supplier (s_suppkey));

ALTER TABLE tpch.customer
    ADD (CONSTRAINT pk_customer       PRIMARY KEY (c_custkey),
         CONSTRAINT fk_customer_nation FOREIGN KEY (c_nationkey) REFERENCES tpch.nation (n_nationkey));

ALTER TABLE tpch.orders
    ADD (CONSTRAINT pk_orders          PRIMARY KEY (o_orderkey),
         CONSTRAINT fk_orders_customer FOREIGN KEY (o_custkey) REFERENCES tpch.customer (c_custkey));

ALTER TABLE tpch.lineitem
    ADD (CONSTRAINT pk_lineitem            PRIMARY KEY (l_linenumber, l_orderkey),
         CONSTRAINT fk_lineitem_order      FOREIGN KEY (l_orderkey)           REFERENCES tpch.orders   (o_orderkey),
         CONSTRAINT fk_lineitem_part       FOREIGN KEY (l_partkey)            REFERENCES tpch.part     (p_partkey),
         CONSTRAINT fk_lineitem_supplier   FOREIGN KEY (l_suppkey)            REFERENCES tpch.supplier (s_suppkey),
         CONSTRAINT fk_lineitem_partsupp   FOREIGN KEY (l_partkey, l_suppkey) REFERENCES tpch.partsupp (ps_partkey, ps_suppkey));
