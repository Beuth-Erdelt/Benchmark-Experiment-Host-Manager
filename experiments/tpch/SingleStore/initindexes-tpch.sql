-- Benchmark-Experiment-Host-Manager | experiments/tpch/SingleStore
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create hash indexes on foreign key columns in SingleStore.
--          Hash indexes complement the primary key for fast point-lookup joins.
--          Individual indexes on l_partkey and l_suppkey are kept; the compound
--          (l_partkey, l_suppkey) index is omitted because each column already
--          has a single-column hash index that covers the TPC-H join patterns.

ALTER TABLE tpch.nation   ADD INDEX USING HASH (n_regionkey);
ALTER TABLE tpch.customer ADD INDEX USING HASH (c_nationkey);

ALTER TABLE tpch.partsupp
    ADD INDEX USING HASH (ps_suppkey),
    ADD INDEX USING HASH (ps_partkey);

ALTER TABLE tpch.orders ADD INDEX USING HASH (o_custkey);

ALTER TABLE tpch.lineitem
    ADD INDEX USING HASH (l_orderkey),
    ADD INDEX USING HASH (l_partkey),
    ADD INDEX USING HASH (l_suppkey);
