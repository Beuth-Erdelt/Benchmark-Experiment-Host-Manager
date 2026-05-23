-- Benchmark-Experiment-Host-Manager | experiments/tpch/MemSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create hash indexes on key columns in MemSQL. MemSQL maintains a
--          columnar store (declared in initschema-tpch.sql via CLUSTERED COLUMNSTORE)
--          alongside an optional row-store layer; hash indexes accelerate
--          point-lookup joins on the row-store side. Hash indexes on PK columns
--          and FK columns are both useful because MemSQL cannot use the columnar
--          key for row-level point lookups.

ALTER TABLE tpch.region
    ADD INDEX USING HASH (r_regionkey);

ALTER TABLE tpch.nation
    ADD INDEX USING HASH (n_nationkey),
    ADD INDEX USING HASH (n_regionkey);

ALTER TABLE tpch.part
    ADD INDEX USING HASH (p_partkey);

ALTER TABLE tpch.supplier
    ADD INDEX USING HASH (s_suppkey),
    ADD INDEX USING HASH (s_nationkey);

ALTER TABLE tpch.partsupp
    ADD INDEX USING HASH (ps_suppkey),
    ADD INDEX USING HASH (ps_partkey);

ALTER TABLE tpch.customer
    ADD INDEX USING HASH (c_custkey),
    ADD INDEX USING HASH (c_nationkey);

ALTER TABLE tpch.orders
    ADD INDEX USING HASH (o_orderkey),
    ADD INDEX USING HASH (o_custkey);

ALTER TABLE tpch.lineitem
    ADD INDEX USING HASH (l_orderkey);
