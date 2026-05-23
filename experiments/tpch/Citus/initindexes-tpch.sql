-- Benchmark-Experiment-Host-Manager | experiments/tpch/Citus
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create secondary indexes for TPC-H on Citus.
--          Indexes on FK columns speed up FK enforcement and lookup joins.
--          Individual indexes on lineitem(l_partkey) and lineitem(l_suppkey)
--          are omitted: l_partkey is the leading column of the compound index
--          IDX_LINEITEM_PART_SUPP, and l_suppkey alone is not selective enough
--          for the TPC-H workload.
--          Additional indexes on l_shipdate and o_orderdate accelerate the
--          date-range filters that appear in several TPC-H queries.

CREATE INDEX idx_nation_regionkey    ON nation   (n_regionkey);
CREATE INDEX idx_supplier_nationkey  ON supplier (s_nationkey);
CREATE INDEX idx_partsupp_partkey    ON partsupp (ps_partkey);
CREATE INDEX idx_partsupp_suppkey    ON partsupp (ps_suppkey);
CREATE INDEX idx_customer_nationkey  ON customer (c_nationkey);
CREATE INDEX idx_orders_custkey      ON orders   (o_custkey);
CREATE INDEX idx_lineitem_orderkey   ON lineitem (l_orderkey);
CREATE INDEX idx_lineitem_part_supp  ON lineitem (l_partkey, l_suppkey);

-- Additional indexes for date-range predicates in TPC-H queries.
CREATE INDEX idx_lineitem_shipdate   ON lineitem (l_shipdate, l_discount, l_quantity);
CREATE INDEX idx_orders_orderdate    ON orders   (o_orderdate);
