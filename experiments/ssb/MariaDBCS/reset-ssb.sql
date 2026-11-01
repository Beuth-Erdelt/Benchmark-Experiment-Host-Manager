-- Benchmark-Experiment-Host-Manager | experiments/ssb/MariaDBCS
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for SSB on MariaDB ColumnStore, run before each
--          benchmarking round with -ar. Steps of the reset contract
--          (docs/DBMS.md): 1 statistics, 2 persist, 3 counters.
--          No curly braces in this file: bexhoma may fill it with str.format().

-- step 1 (statistics)
ANALYZE TABLE ssb.customer;
ANALYZE TABLE ssb.dates;
ANALYZE TABLE ssb.lineorder;
ANALYZE TABLE ssb.part;
ANALYZE TABLE ssb.supplier;

-- step 2 (persist): n/a - ColumnStore writes loads to its files, no dirty pages to flush

-- step 3 (counters): n/a - the check scripts read no ColumnStore counter
