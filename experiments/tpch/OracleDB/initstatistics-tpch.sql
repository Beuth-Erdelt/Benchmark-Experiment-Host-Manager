-- Benchmark-Experiment-Host-Manager | experiments/tpch/OracleDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Optimizer statistics of the TPC-H tables (-xis): DBMS_STATS gathers
--          table, column and index statistics of the current schema (BEXHOMA)
--          with a full scan (estimate_percent 100, as SQL Server WITH FULLSCAN)
--          and the default histograms (FOR ALL COLUMNS SIZE AUTO).
--          No curly braces in this file: bexhoma may fill it with str.format().

BEGIN
    DBMS_STATS.GATHER_SCHEMA_STATS(
        ownname          => SYS_CONTEXT('USERENV', 'CURRENT_SCHEMA'),
        estimate_percent => 100,
        cascade          => TRUE);
END;
/

SELECT table_name, num_rows, blocks, last_analyzed
FROM dba_tables
WHERE owner = SYS_CONTEXT('USERENV', 'CURRENT_SCHEMA')
ORDER BY table_name;
