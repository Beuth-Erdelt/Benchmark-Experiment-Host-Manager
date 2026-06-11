-- Benchmark-Experiment-Host-Manager | experiments/tpch/Kinetica
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load TPC-H data at scale factor 10 (SF10 ~ 10 GB) into Kinetica.
--          COPY reads pipe-delimited .tbl files; NULL '' maps empty fields to SQL NULL.

COPY public.customer FROM '/data/tpch/SF10/customer.tbl' DELIMITER '|' NULL '';
COPY public.lineitem FROM '/data/tpch/SF10/lineitem.tbl' DELIMITER '|' NULL '';
COPY public.nation   FROM '/data/tpch/SF10/nation.tbl'   DELIMITER '|' NULL '';
COPY public.orders   FROM '/data/tpch/SF10/orders.tbl'   DELIMITER '|' NULL '';
COPY public.part     FROM '/data/tpch/SF10/part.tbl'     DELIMITER '|' NULL '';
COPY public.partsupp FROM '/data/tpch/SF10/partsupp.tbl' DELIMITER '|' NULL '';
COPY public.region   FROM '/data/tpch/SF10/region.tbl'   DELIMITER '|' NULL '';
COPY public.supplier FROM '/data/tpch/SF10/supplier.tbl' DELIMITER '|' NULL '';
