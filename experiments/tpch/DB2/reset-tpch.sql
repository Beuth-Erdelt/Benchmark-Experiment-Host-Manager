-- Benchmark-Experiment-Host-Manager | experiments/tpch/DB2
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Reset contract (docs/DBMS.md) for TPC-H on IBM Db2, run before each
--          benchmarking round with -ar, in the schema DB2INST1 (default schema
--          of the CLP session of /tmp/bexhoma-run.sh).
--          Step 1 (statistics): RUNSTATS on every TPC-H table.
--          Step 2 (persist): FLUSH BUFFERPOOLS ALL writes the dirty pages of all
--          buffer pools to disk; it comes after step 1, as RUNSTATS writes the
--          catalog again.
--          No curly braces in this file: bexhoma may fill it with str.format().

-- step 1 (statistics)
RUNSTATS ON TABLE nation   WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE region   WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE part     WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE supplier WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE partsupp WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE customer WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE orders   WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE lineitem WITH DISTRIBUTION AND DETAILED INDEXES ALL;

-- step 2 (persist)
FLUSH BUFFERPOOLS ALL;

-- step 3 (counters): n/a - the monitor table functions of Db2 (MON_GET_*) count from the activation of the database and cannot be reset
