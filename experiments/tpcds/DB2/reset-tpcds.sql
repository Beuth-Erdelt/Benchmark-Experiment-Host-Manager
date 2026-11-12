-- Benchmark-Experiment-Host-Manager | experiments/tpcds/DB2
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Reset contract (docs/DBMS.md) for TPC-DS on IBM Db2, run before each
--          benchmarking round with -ar, in the schema DB2INST1 (default schema
--          of the CLP session of /tmp/bexhoma-run.sh).
--          Step 1 (statistics): RUNSTATS on every TPC-DS table.
--          Step 2 (persist): FLUSH BUFFERPOOLS ALL writes the dirty pages of all
--          buffer pools to disk; it comes after step 1, as RUNSTATS writes the
--          catalog again.
--          No curly braces in this file: bexhoma may fill it with str.format().

-- step 1 (statistics)
RUNSTATS ON TABLE dbgen_version          WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE customer_address       WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE customer_demographics  WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE date_dim               WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE warehouse              WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE ship_mode              WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE time_dim               WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE reason                 WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE income_band            WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE item                   WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE store                  WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE call_center            WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE customer               WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE web_site               WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE store_returns          WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE household_demographics WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE web_page               WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE promotion              WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE catalog_page           WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE inventory              WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE catalog_returns        WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE web_returns            WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE web_sales              WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE catalog_sales          WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE store_sales            WITH DISTRIBUTION AND DETAILED INDEXES ALL;

-- step 2 (persist)
FLUSH BUFFERPOOLS ALL;

-- step 3 (counters): n/a - the monitor table functions of Db2 (MON_GET_*) count from the activation of the database and cannot be reset
