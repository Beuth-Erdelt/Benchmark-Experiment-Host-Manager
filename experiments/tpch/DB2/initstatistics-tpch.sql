-- Benchmark-Experiment-Host-Manager | experiments/tpch/DB2
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Optimizer statistics of the TPC-H tables (-xis): RUNSTATS collects
--          table, column (with distribution: frequent values and quantiles) and
--          detailed index statistics of every table of the schema DB2INST1,
--          reading all rows (no sampling).
--          No curly braces in this file: bexhoma may fill it with str.format().

RUNSTATS ON TABLE nation   WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE region   WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE part     WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE supplier WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE partsupp WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE customer WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE orders   WITH DISTRIBUTION AND DETAILED INDEXES ALL;
RUNSTATS ON TABLE lineitem WITH DISTRIBUTION AND DETAILED INDEXES ALL;

SELECT CAST(tabname AS VARCHAR(20)) AS tabname, card, npages, stats_time
FROM syscat.tables
WHERE tabschema = CURRENT SCHEMA
ORDER BY tabname;
