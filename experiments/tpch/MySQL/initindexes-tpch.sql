-- Benchmark-Experiment-Host-Manager | experiments/tpch/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create indexes on foreign key columns to support join operations
--          in TPC-H queries. Run after data loading.
--          Separate indexes on lineitem(l_partkey) and lineitem(l_suppkey) are
--          omitted: l_partkey is already covered as the leading column of the
--          compound index (l_partkey, l_suppkey), and l_suppkey alone is not
--          selective enough to benefit queries in the TPC-H workload.
--          The index on supplier(s_nationkey) is omitted because the
--          supplier->nation FK is not applied in this configuration.

CREATE INDEX n_r  ON tpch.nation   (n_regionkey);
CREATE INDEX c_n  ON tpch.customer (c_nationkey);
CREATE INDEX ps_s ON tpch.partsupp (ps_suppkey);
CREATE INDEX ps_p ON tpch.partsupp (ps_partkey);
CREATE INDEX o_c  ON tpch.orders   (o_custkey);
CREATE INDEX l_o  ON tpch.lineitem (l_orderkey);
CREATE INDEX l_ps ON tpch.lineitem (l_partkey, l_suppkey);

COMMIT;
