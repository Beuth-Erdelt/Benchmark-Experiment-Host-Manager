-- Benchmark-Experiment-Host-Manager | experiments/tpch/MariaDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Step 1 (statistics) of the reset contract (docs/DBMS.md) for
--          TPC-H on MariaDB, run before each benchmarking round with -ar.
--          ANALYZE TABLE refreshes optimizer statistics on every TPC-H table.
--          Steps 2 (persist) and 3 (counters) follow in reset-flush.sh.

ANALYZE TABLE tpch.customer;
ANALYZE TABLE tpch.lineitem;
ANALYZE TABLE tpch.nation;
ANALYZE TABLE tpch.orders;
ANALYZE TABLE tpch.part;
ANALYZE TABLE tpch.partsupp;
ANALYZE TABLE tpch.region;
ANALYZE TABLE tpch.supplier;
