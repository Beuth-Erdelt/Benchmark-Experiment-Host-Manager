-- Benchmark-Experiment-Host-Manager | experiments/tpch/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Collect table statistics after data loading.
--          Run after initdata-tpch-SF*.sql (and optionally after initindexes).

SET GLOBAL autocommit = 1;
SET GLOBAL foreign_key_checks = 1;
SET GLOBAL unique_checks = 1;
SET GLOBAL innodb_flush_log_at_trx_commit = 1;
SET GLOBAL innodb_io_capacity = 200;        -- zurück auf Default
SET GLOBAL innodb_io_capacity_max = 2000;

ANALYZE TABLE tpch.customer;
ANALYZE TABLE tpch.lineitem;
ANALYZE TABLE tpch.nation;
ANALYZE TABLE tpch.orders;
ANALYZE TABLE tpch.part;
ANALYZE TABLE tpch.partsupp;
ANALYZE TABLE tpch.region;
ANALYZE TABLE tpch.supplier;
