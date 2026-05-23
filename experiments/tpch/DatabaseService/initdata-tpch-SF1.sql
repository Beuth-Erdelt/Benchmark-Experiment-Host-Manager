-- Benchmark-Experiment-Host-Manager | experiments/tpch/DatabaseService
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load TPC-H data at scale factor 1 (SF1 ≈ 1 GB) into DatabaseService.
--          COPY reads pipe-delimited .tbl files; NULL '' maps empty fields to SQL NULL.

COPY public.customer FROM '/data/tpch/SF1/customer.tbl' DELIMITER '|' NULL '';
COPY public.lineitem FROM '/data/tpch/SF1/lineitem.tbl' DELIMITER '|' NULL '';
COPY public.nation   FROM '/data/tpch/SF1/nation.tbl'   DELIMITER '|' NULL '';
COPY public.orders   FROM '/data/tpch/SF1/orders.tbl'   DELIMITER '|' NULL '';
COPY public.part     FROM '/data/tpch/SF1/part.tbl'     DELIMITER '|' NULL '';
COPY public.partsupp FROM '/data/tpch/SF1/partsupp.tbl' DELIMITER '|' NULL '';
COPY public.region   FROM '/data/tpch/SF1/region.tbl'   DELIMITER '|' NULL '';
COPY public.supplier FROM '/data/tpch/SF1/supplier.tbl' DELIMITER '|' NULL '';
