-- Benchmark-Experiment-Host-Manager | experiments/tpch/SingleStore
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Collect optimizer statistics after data loading in SingleStore.
--          ANALYZE TABLE updates SingleStore's statistics for all TPC-H tables.

ANALYZE TABLE tpch.customer;
ANALYZE TABLE tpch.lineitem;
ANALYZE TABLE tpch.nation;
ANALYZE TABLE tpch.orders;
ANALYZE TABLE tpch.part;
ANALYZE TABLE tpch.partsupp;
ANALYZE TABLE tpch.region;
ANALYZE TABLE tpch.supplier;
