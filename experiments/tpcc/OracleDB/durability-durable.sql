-- Benchmark-Experiment-Host-Manager | experiments/tpcc/OracleDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load durability durable (-xld durable): every commit waits until its
--          redo is written (COMMIT_WAIT = WAIT, COMMIT_LOGGING = IMMEDIATE, the
--          behaviour of the unset parameters, which the template does not set),
--          so the load is crash-safe. Nothing to restore afterwards.
--          Runs before initschema (pre-load list), as SYSDBA in FREEPDB1.
--          No curly braces in this file: bexhoma may fill it with str.format().

ALTER SYSTEM SET commit_wait = 'WAIT' SCOPE = MEMORY;
ALTER SYSTEM SET commit_logging = 'IMMEDIATE' SCOPE = MEMORY;

SELECT name, SUBSTR(value, 1, 20) AS value FROM v$parameter WHERE name IN ('commit_wait', 'commit_logging') ORDER BY name;
