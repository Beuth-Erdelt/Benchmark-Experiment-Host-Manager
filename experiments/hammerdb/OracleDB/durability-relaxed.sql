-- Benchmark-Experiment-Host-Manager | experiments/hammerdb/OracleDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load durability relaxed (-xld relaxed, the default): a commit does not
--          wait for the redo to be written (COMMIT_WAIT = NOWAIT) and the redo
--          of several commits is written together (COMMIT_LOGGING = BATCH).
--          A crash during the load may lose the last commits, not corrupt data.
--          Set in the pluggable database, in memory only;
--          restoredurability-relaxed.sql sets the defaults again.
--          Runs before initschema (pre-load list), as SYSDBA in FREEPDB1.
--          No curly braces in this file: bexhoma may fill it with str.format().

ALTER SYSTEM SET commit_wait = 'NOWAIT' SCOPE = MEMORY;
ALTER SYSTEM SET commit_logging = 'BATCH' SCOPE = MEMORY;

SELECT name, SUBSTR(value, 1, 20) AS value FROM v$parameter WHERE name IN ('commit_wait', 'commit_logging') ORDER BY name;
