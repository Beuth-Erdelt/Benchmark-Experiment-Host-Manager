-- Benchmark-Experiment-Host-Manager | experiments/tpch/CockroachDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load TPC-H data at scale factor 30 (SF30 ~ 30 GB) into the public schema
--          using the COPY command (pipe-delimited .tbl files from /data/tpch/SF30/).

COPY public.customer FROM '/data/tpch/SF30/customer.tbl' DELIMITER '|' NULL '';
COPY public.lineitem FROM '/data/tpch/SF30/lineitem.tbl' DELIMITER '|' NULL '';
COPY public.nation   FROM '/data/tpch/SF30/nation.tbl'   DELIMITER '|' NULL '';
COPY public.orders   FROM '/data/tpch/SF30/orders.tbl'   DELIMITER '|' NULL '';
COPY public.part     FROM '/data/tpch/SF30/part.tbl'     DELIMITER '|' NULL '';
COPY public.partsupp FROM '/data/tpch/SF30/partsupp.tbl' DELIMITER '|' NULL '';
COPY public.region   FROM '/data/tpch/SF30/region.tbl'   DELIMITER '|' NULL '';
COPY public.supplier FROM '/data/tpch/SF30/supplier.tbl' DELIMITER '|' NULL '';
