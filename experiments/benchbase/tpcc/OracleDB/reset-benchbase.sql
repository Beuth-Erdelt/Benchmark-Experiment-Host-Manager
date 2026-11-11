-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/OracleDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Reset contract (docs/DBMS.md) for TPC-C (Benchbase) on Oracle Database Free, run
--          before each benchmarking round with -ar, in the schema of the
--          benchmark (CURRENT_SCHEMA of /tmp/bexhoma-session.sql).
--          Step 1 (statistics): DBMS_STATS gathers the statistics of every table
--          of the schema that has none or stale ones (GATHER AUTO).
--          Step 2 (persist): ALTER SYSTEM CHECKPOINT writes the dirty blocks of
--          the pluggable database; it comes after step 1, as gathering
--          statistics writes blocks again.
--          No curly braces in this file: bexhoma may fill it with str.format().

-- step 1 (statistics)
BEGIN
    DBMS_STATS.GATHER_SCHEMA_STATS(
        ownname => SYS_CONTEXT('USERENV', 'CURRENT_SCHEMA'),
        options => 'GATHER AUTO');
END;
/

-- step 2 (persist)
ALTER SYSTEM CHECKPOINT;

-- step 3 (counters): n/a - the statistics views of Oracle (v$sysstat, v$system_event) cannot be reset
