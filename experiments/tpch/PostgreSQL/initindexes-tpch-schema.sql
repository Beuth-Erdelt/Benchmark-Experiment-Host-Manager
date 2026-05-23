-- Benchmark-Experiment-Host-Manager | experiments/tpch/PostgreSQL
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
--          {BEXHOMA_SCHEMA} is substituted at runtime by the Bexhoma framework.

CREATE INDEX ON {BEXHOMA_SCHEMA}.nation   (n_regionkey);
CREATE INDEX ON {BEXHOMA_SCHEMA}.customer (c_nationkey);
CREATE INDEX ON {BEXHOMA_SCHEMA}.partsupp (ps_suppkey);
CREATE INDEX ON {BEXHOMA_SCHEMA}.partsupp (ps_partkey);
CREATE INDEX ON {BEXHOMA_SCHEMA}.orders   (o_custkey);
CREATE INDEX ON {BEXHOMA_SCHEMA}.lineitem (l_orderkey);
CREATE INDEX ON {BEXHOMA_SCHEMA}.lineitem (l_partkey, l_suppkey);
