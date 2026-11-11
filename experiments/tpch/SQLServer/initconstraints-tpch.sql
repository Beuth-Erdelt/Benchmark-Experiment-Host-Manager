-- Benchmark-Experiment-Host-Manager | experiments/tpch/SQLServer
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Add foreign key constraints to the TPC-H tables (the same as for
--          MySQL; supplier->nation is not applied). Run after loading; the
--          primary keys are declared in initschema-tpch.sql.
--          WITH CHECK validates the rows, so the constraints are trusted and
--          the optimizer may use them (WITH NOCHECK would be metadata only).
--          No curly braces in this file: bexhoma may fill it with str.format().

ALTER TABLE dbo.nation
    WITH CHECK ADD CONSTRAINT fk_n_r FOREIGN KEY (n_regionkey) REFERENCES dbo.region (r_regionkey);

ALTER TABLE dbo.partsupp
    WITH CHECK ADD CONSTRAINT fk_ps_s FOREIGN KEY (ps_suppkey) REFERENCES dbo.supplier (s_suppkey),
                   CONSTRAINT fk_ps_p FOREIGN KEY (ps_partkey) REFERENCES dbo.part (p_partkey);

ALTER TABLE dbo.customer
    WITH CHECK ADD CONSTRAINT fk_c_n FOREIGN KEY (c_nationkey) REFERENCES dbo.nation (n_nationkey);

ALTER TABLE dbo.orders
    WITH CHECK ADD CONSTRAINT fk_o_c FOREIGN KEY (o_custkey) REFERENCES dbo.customer (c_custkey);

ALTER TABLE dbo.lineitem
    WITH CHECK ADD CONSTRAINT fk_l_o  FOREIGN KEY (l_orderkey)           REFERENCES dbo.orders (o_orderkey),
                   CONSTRAINT fk_l_p  FOREIGN KEY (l_partkey)            REFERENCES dbo.part (p_partkey),
                   CONSTRAINT fk_l_s  FOREIGN KEY (l_suppkey)            REFERENCES dbo.supplier (s_suppkey),
                   CONSTRAINT fk_l_ps FOREIGN KEY (l_partkey, l_suppkey) REFERENCES dbo.partsupp (ps_partkey, ps_suppkey);
GO
