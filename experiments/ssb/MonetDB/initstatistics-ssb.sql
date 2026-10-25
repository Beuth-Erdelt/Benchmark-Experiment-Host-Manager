-- Benchmark-Experiment-Host-Manager | experiments/ssb/MonetDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Collect table statistics after data loading (-xis). Tables are
--          referenced with the sys schema prefix as that is where they reside.
--          No curly braces in this file: bexhoma may fill it with str.format().

ANALYZE sys.customer;
ANALYZE sys.supplier;
ANALYZE sys.part;
ANALYZE sys.dates;
ANALYZE sys.lineorder;
