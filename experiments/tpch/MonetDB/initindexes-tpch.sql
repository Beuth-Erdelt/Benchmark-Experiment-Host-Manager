-- Benchmark-Experiment-Host-Manager | experiments/tpch/MonetDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create indexes on foreign key columns to support join operations
--          in TPC-H queries. Run after data loading.
--          Unlike other DBMS variants, individual indexes on lineitem(l_partkey)
--          and lineitem(l_suppkey) are created here in addition to the compound
--          index — MonetDB's columnar storage benefits from per-column access
--          paths and does not make individual indexes redundant.
--          The index on supplier(s_nationkey) is omitted because the
--          supplier→nation FK is not applied in this configuration.

CREATE INDEX n_r  ON nation   (n_regionkey);
CREATE INDEX c_n  ON customer (c_nationkey);
CREATE INDEX ps_s ON partsupp (ps_suppkey);
CREATE INDEX ps_p ON partsupp (ps_partkey);
CREATE INDEX o_c  ON orders   (o_custkey);
CREATE INDEX l_o  ON lineitem (l_orderkey);
CREATE INDEX l_p  ON lineitem (l_partkey);
CREATE INDEX l_s  ON lineitem (l_suppkey);
CREATE INDEX l_ps ON lineitem (l_partkey, l_suppkey);
