-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/OracleDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Restore the durability after a relaxed load (-xld relaxed): a commit
--          waits for its redo again (COMMIT_WAIT = WAIT, COMMIT_LOGGING =
--          IMMEDIATE, the behaviour of the unset parameters, which the template
--          does not set). Ends with an ERROR if a value is not back.
--          Runs in the post-load list before checkschema, as SYSDBA in FREEPDB1.
--          No curly braces in this file: bexhoma may fill it with str.format().

ALTER SYSTEM SET commit_wait = 'WAIT' SCOPE = MEMORY;
ALTER SYSTEM SET commit_logging = 'IMMEDIATE' SCOPE = MEMORY;

SELECT name, SUBSTR(value, 1, 20) AS value FROM v$parameter WHERE name IN ('commit_wait', 'commit_logging') ORDER BY name;

DECLARE
    n NUMBER;
BEGIN
    SELECT COUNT(*) INTO n FROM v$parameter
    WHERE (name = 'commit_wait' AND UPPER(value) <> 'WAIT')
       OR (name = 'commit_logging' AND UPPER(value) <> 'IMMEDIATE');
    IF n > 0 THEN
        RAISE_APPLICATION_ERROR(-20001, 'ERROR: commit_wait or commit_logging not restored');
    END IF;
END;
/
