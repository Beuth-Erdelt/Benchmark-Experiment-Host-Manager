-- Benchmark-Experiment-Host-Manager | experiments/tpch/DB2
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Secondary indexes on the foreign key columns of the TPC-H tables
--          (the same as for MySQL, SQL Server and Oracle). The primary keys are
--          declared in initschema-tpch.sql. Runs in the schema DB2INST1 (default
--          schema of the CLP session of /tmp/bexhoma-run.sh).
--          No curly braces in this file: bexhoma may fill it with str.format().

CREATE INDEX n_r  ON nation   (n_regionkey);
CREATE INDEX c_n  ON customer (c_nationkey);
CREATE INDEX ps_s ON partsupp (ps_suppkey);
CREATE INDEX ps_p ON partsupp (ps_partkey);
CREATE INDEX o_c  ON orders   (o_custkey);
CREATE INDEX l_o  ON lineitem (l_orderkey);
CREATE INDEX l_ps ON lineitem (l_partkey, l_suppkey);
