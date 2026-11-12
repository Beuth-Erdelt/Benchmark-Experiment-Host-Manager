-- Benchmark-Experiment-Host-Manager | experiments/tpcds/DB2
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Optimizer statistics of the TPC-DS tables (-xis): RUNSTATS collects
--          table, column (with distribution: frequent values and quantiles) and
--          detailed index statistics of every table of the schema DB2INST1,
--          reading all rows (no sampling).
--          No curly braces in this file: bexhoma may fill it with str.format().

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

SELECT CAST(tabname AS VARCHAR(30)) AS tabname, card, npages, stats_time
FROM syscat.tables
WHERE tabschema = CURRENT SCHEMA
ORDER BY tabname;
