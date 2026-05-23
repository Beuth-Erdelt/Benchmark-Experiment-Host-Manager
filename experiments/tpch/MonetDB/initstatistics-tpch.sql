-- Benchmark-Experiment-Host-Manager | experiments/tpch/MonetDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Collect table statistics after data loading. Tables are referenced
--          with the sys schema prefix as that is where they reside in MonetDB.
--          SELECT CURRENT_SCHEMA confirms the active schema for diagnostics.

ANALYZE sys.customer;
ANALYZE sys.lineitem;
ANALYZE sys.nation;
ANALYZE sys.orders;
ANALYZE sys.part;
ANALYZE sys.partsupp;
ANALYZE sys.region;
ANALYZE sys.supplier;

SELECT CURRENT_SCHEMA;
