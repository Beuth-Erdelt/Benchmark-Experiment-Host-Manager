-- Benchmark-Experiment-Host-Manager | experiments/tpch/OracleDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load TPC-H data at scale factor 10 (SF10 ≈ 10 GB) into OracleDB.
--          NOTE: This file uses PostgreSQL COPY syntax and will not execute
--          on a native Oracle instance. It may be used by a compatibility layer
--          or placeholder for an alternative loading path.

COPY public.customer FROM '/data/tpch/SF10/customer.tbl' DELIMITER '|';
COPY public.lineitem FROM '/data/tpch/SF10/lineitem.tbl' DELIMITER '|';
COPY public.nation   FROM '/data/tpch/SF10/nation.tbl'   DELIMITER '|';
COPY public.orders   FROM '/data/tpch/SF10/orders.tbl'   DELIMITER '|';
COPY public.part     FROM '/data/tpch/SF10/part.tbl'     DELIMITER '|';
COPY public.partsupp FROM '/data/tpch/SF10/partsupp.tbl' DELIMITER '|';
COPY public.region   FROM '/data/tpch/SF10/region.tbl'   DELIMITER '|';
COPY public.supplier FROM '/data/tpch/SF10/supplier.tbl' DELIMITER '|';
