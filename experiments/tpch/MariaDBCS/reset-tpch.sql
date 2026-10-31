-- Benchmark-Experiment-Host-Manager | experiments/tpch/MariaDBCS
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for TPCH on MariaDB ColumnStore, run before each
--          benchmarking round with -ar. Steps of the reset contract
--          (docs/DBMS.md): 1 statistics, 2 persist, 3 counters.
--          No curly braces in this file: bexhoma may fill it with str.format().

-- step 1 (statistics)
ANALYZE TABLE tpch.customer;
ANALYZE TABLE tpch.lineitem;
ANALYZE TABLE tpch.nation;
ANALYZE TABLE tpch.orders;
ANALYZE TABLE tpch.part;
ANALYZE TABLE tpch.partsupp;
ANALYZE TABLE tpch.region;
ANALYZE TABLE tpch.supplier;

-- step 2 (persist): n/a - ColumnStore writes loads to its files, no dirty pages to flush

-- step 3 (counters): n/a - the check scripts read no ColumnStore counter
