-- Benchmark-Experiment-Host-Manager | experiments/tpch/Citus
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load TPC-H data at scale factor 1 (SF1 ~ 1 GB) into Citus.
--          Pipe-delimited .tbl files are loaded via COPY; NULL '' handles the
--          empty string that dbgen writes for nullable columns.
--          After loading, shards are rebalanced across all active workers.

COPY public.customer FROM '/data/tpch/SF1/customer.tbl' DELIMITER '|' NULL '';
COPY public.lineitem FROM '/data/tpch/SF1/lineitem.tbl' DELIMITER '|' NULL '';
COPY public.nation   FROM '/data/tpch/SF1/nation.tbl'   DELIMITER '|' NULL '';
COPY public.orders   FROM '/data/tpch/SF1/orders.tbl'   DELIMITER '|' NULL '';
COPY public.part     FROM '/data/tpch/SF1/part.tbl'     DELIMITER '|' NULL '';
COPY public.partsupp FROM '/data/tpch/SF1/partsupp.tbl' DELIMITER '|' NULL '';
COPY public.region   FROM '/data/tpch/SF1/region.tbl'   DELIMITER '|' NULL '';
COPY public.supplier FROM '/data/tpch/SF1/supplier.tbl' DELIMITER '|' NULL '';

-- Rebalance shards after bulk load so every worker carries an equal share.
SELECT get_rebalance_table_shards_plan();
SELECT rebalance_table_shards();
