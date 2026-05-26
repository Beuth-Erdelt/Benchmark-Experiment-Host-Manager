-- Benchmark-Experiment-Host-Manager | experiments/tpch/Citus
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load TPC-H data at scale factor 100 (SF100 ≈ 100 GB) into Citus.
--          See initdata-tpch-SF1.sql for option descriptions.

COPY public.customer FROM '/data/tpch/SF100/customer.tbl' DELIMITER '|' NULL '';
COPY public.lineitem FROM '/data/tpch/SF100/lineitem.tbl' DELIMITER '|' NULL '';
COPY public.nation   FROM '/data/tpch/SF100/nation.tbl'   DELIMITER '|' NULL '';
COPY public.orders   FROM '/data/tpch/SF100/orders.tbl'   DELIMITER '|' NULL '';
COPY public.part     FROM '/data/tpch/SF100/part.tbl'     DELIMITER '|' NULL '';
COPY public.partsupp FROM '/data/tpch/SF100/partsupp.tbl' DELIMITER '|' NULL '';
COPY public.region   FROM '/data/tpch/SF100/region.tbl'   DELIMITER '|' NULL '';
COPY public.supplier FROM '/data/tpch/SF100/supplier.tbl' DELIMITER '|' NULL '';

SELECT get_rebalance_table_shards_plan();
SELECT rebalance_table_shards();
