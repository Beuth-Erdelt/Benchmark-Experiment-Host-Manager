-- Benchmark-Experiment-Host-Manager | experiments/ssb/MariaDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Collect table statistics after data loading (-xis).
--          No curly braces in this file: bexhoma may fill it with str.format().

ANALYZE TABLE ssb.customer;
ANALYZE TABLE ssb.supplier;
ANALYZE TABLE ssb.part;
ANALYZE TABLE ssb.dates;
ANALYZE TABLE ssb.lineorder;
