-- Benchmark-Experiment-Host-Manager | experiments/tpcc/OracleDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Post-load checks for TPC-C (HammerDB) on Oracle Database Free (initscripts key
--          'Checks'). Runs last after loading: reports the version and logging
--          mode, writes a checkpoint (dirty blocks of the load to disk), and
--          reports row counts, sizes, the redo written so far and the parameters
--          that differ from the defaults.
--          Load settings (-xld) are restored before, by restoredurability-*.sql.
--          The schema is the current one (CURRENT_SCHEMA of /tmp/bexhoma-session.sql).
--          No curly braces in this file: bexhoma may fill it with str.format().

-- Version and logging mode
SELECT banner_full FROM v$version;
SELECT log_mode, force_logging FROM v$database;

-- Persist: write the dirty blocks of the load
ALTER SYSTEM CHECKPOINT;

-- Row counts per table (exact) and sizes of tables and indexes
DECLARE
    n NUMBER;
BEGIN
    FOR t IN (SELECT table_name FROM dba_tables
              WHERE owner = SYS_CONTEXT('USERENV', 'CURRENT_SCHEMA') ORDER BY table_name) LOOP
        EXECUTE IMMEDIATE 'SELECT COUNT(*) FROM "' || t.table_name || '"' INTO n;
        DBMS_OUTPUT.PUT_LINE(RPAD(t.table_name, 30) || ' rows ' || n);
    END LOOP;
END;
/

COLUMN segment_name FORMAT A30
SELECT segment_type, segment_name, ROUND(SUM(bytes) / 1024 / 1024) AS size_mib
FROM dba_segments
WHERE owner = SYS_CONTEXT('USERENV', 'CURRENT_SCHEMA')
GROUP BY segment_type, segment_name
ORDER BY size_mib DESC;

SELECT ROUND(SUM(bytes) / 1024 / 1024) AS user_data_mib
FROM dba_segments
WHERE owner = SYS_CONTEXT('USERENV', 'CURRENT_SCHEMA');

-- Redo written since the start of the instance, i.e. mostly by the load
SELECT name, ROUND(value / 1024 / 1024) AS mib
FROM v$sysstat
WHERE name IN ('redo size', 'physical write total bytes');

-- Parameters that differ from the defaults
COLUMN name FORMAT A40
COLUMN value FORMAT A60
SELECT name, value
FROM v$parameter
WHERE isdefault = 'FALSE'
ORDER BY name;
