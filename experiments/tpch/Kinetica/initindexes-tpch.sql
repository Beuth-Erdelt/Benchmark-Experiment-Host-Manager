-- Benchmark-Experiment-Host-Manager | experiments/tpch/Kinetica
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create indexes on foreign key columns in Kinetica using ALTER TABLE
--          ADD INDEX. Kinetica's ADD INDEX builds a chained hash index that
--          accelerates point-lookup joins. Individual indexes on l_partkey and
--          l_suppkey are kept because Kinetica does not automatically benefit
--          from leading-column coverage the way a B-tree engine would.

ALTER TABLE nation   ADD INDEX (n_regionkey);
ALTER TABLE customer ADD INDEX (c_nationkey);
ALTER TABLE partsupp ADD INDEX (ps_suppkey);
ALTER TABLE partsupp ADD INDEX (ps_partkey);
ALTER TABLE orders   ADD INDEX (o_custkey);
ALTER TABLE lineitem ADD INDEX (l_orderkey);
ALTER TABLE lineitem ADD INDEX (l_partkey);
ALTER TABLE lineitem ADD INDEX (l_suppkey);
