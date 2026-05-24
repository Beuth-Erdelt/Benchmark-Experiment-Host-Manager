-- Benchmark-Experiment-Host-Manager | experiments/tpch/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Collect table statistics after data loading.
--          Run after initdata-tpch-SF*.sql (and optionally after initindexes).

-- after import + indexes + constraints
SET GLOBAL autocommit = 1;
SET GLOBAL foreign_key_checks = 1;
SET GLOBAL unique_checks = 1;

SET GLOBAL innodb_flush_log_at_trx_commit = 1;
SET GLOBAL sync_binlog = 1;

SET GLOBAL innodb_io_capacity = 200;
SET GLOBAL innodb_io_capacity_max = 2000;

SET GLOBAL innodb_ddl_threads = 4;
SET GLOBAL innodb_parallel_read_threads = 4;

ANALYZE TABLE tpch.customer;
ANALYZE TABLE tpch.lineitem;
ANALYZE TABLE tpch.nation;
ANALYZE TABLE tpch.orders;
ANALYZE TABLE tpch.part;
ANALYZE TABLE tpch.partsupp;
ANALYZE TABLE tpch.region;
ANALYZE TABLE tpch.supplier;
