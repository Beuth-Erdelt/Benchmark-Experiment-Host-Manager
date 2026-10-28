-- Benchmark-Experiment-Host-Manager | experiments/ssb/MariaDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Collect statistics of lineorder_flat after data loading (-xis, -xsv flat).
--          No curly braces in this file: bexhoma may fill it with str.format().

ANALYZE TABLE ssb.lineorder_flat;
