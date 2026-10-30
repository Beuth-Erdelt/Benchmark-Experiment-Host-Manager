-- Benchmark-Experiment-Host-Manager | experiments/ssb/MariaDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Collect statistics of lineorder_flat after data loading (-xis, -xsv flat).

-- Histograms (PERSISTENT FOR ALL) are the DDL parameter histograms (ddl-parameters.config)
ANALYZE TABLE ssb.lineorder_flat {histograms};
