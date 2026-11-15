-- Benchmark-Experiment-Host-Manager | experiments/hammerdb/OracleDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Prepare Oracle Database Free for TPC-C (HammerDB). HammerDB creates
--          the user TPCC (tpcc_user = BEXHOMA_DATABASE of the loading parameters)
--          as SYSTEM and builds the schema in it, so the user must not exist
--          before. This script only reports the container and the users.
--          The later scripts (checkschema, reset) run in the schema TPCC
--          (CURRENT_SCHEMA of /tmp/bexhoma-session.sql).
--          No curly braces in this file: bexhoma may fill it with str.format().

SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS container,
       SYS_CONTEXT('USERENV', 'CURRENT_SCHEMA') AS current_schema
FROM dual;

SELECT username, default_tablespace, created
FROM dba_users
WHERE oracle_maintained = 'N'
ORDER BY username;
