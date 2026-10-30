-- Benchmark-Experiment-Host-Manager | experiments/ssb/MariaDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Collect table statistics after data loading (-xis).

-- Histograms (PERSISTENT FOR ALL) are the DDL parameter histograms (ddl-parameters.config)
ANALYZE TABLE ssb.customer {histograms};
ANALYZE TABLE ssb.supplier {histograms};
ANALYZE TABLE ssb.part {histograms};
ANALYZE TABLE ssb.dates {histograms};
ANALYZE TABLE ssb.lineorder {histograms};
