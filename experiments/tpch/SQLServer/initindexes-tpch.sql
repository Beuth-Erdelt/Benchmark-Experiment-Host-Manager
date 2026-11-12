-- Benchmark-Experiment-Host-Manager | experiments/tpch/SQLServer
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create indexes on foreign key columns to support join operations
--          in TPC-H queries (the same indexes as for MySQL). Run after loading.
--          The primary keys are the clustered indexes of initschema-tpch.sql.
--          No curly braces in this file: bexhoma may fill it with str.format().

CREATE INDEX n_r  ON dbo.nation   (n_regionkey);
CREATE INDEX c_n  ON dbo.customer (c_nationkey);
CREATE INDEX ps_s ON dbo.partsupp (ps_suppkey);
CREATE INDEX ps_p ON dbo.partsupp (ps_partkey);
CREATE INDEX o_c  ON dbo.orders   (o_custkey);
CREATE INDEX l_o  ON dbo.lineitem (l_orderkey);
CREATE INDEX l_ps ON dbo.lineitem (l_partkey, l_suppkey);
GO
