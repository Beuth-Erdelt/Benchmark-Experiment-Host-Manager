-- Benchmark-Experiment-Host-Manager | experiments/tpch/MariaDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Collect table statistics after data loading.
--          Run after initdata-tpch-SF*.sql (and optionally after initindexes).

-- Histograms (PERSISTENT FOR ALL) are the DDL parameter histograms (ddl-parameters.config)
ANALYZE TABLE tpch.customer {histograms};
ANALYZE TABLE tpch.lineitem {histograms};
ANALYZE TABLE tpch.nation {histograms};
ANALYZE TABLE tpch.orders {histograms};
ANALYZE TABLE tpch.part {histograms};
ANALYZE TABLE tpch.partsupp {histograms};
ANALYZE TABLE tpch.region {histograms};
ANALYZE TABLE tpch.supplier {histograms};
