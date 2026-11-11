-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/OracleDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Prepare Oracle Database Free for TPC-C (Benchbase). Benchbase creates
--          its tables itself, in the schema of the user it logs in as (BEXHOMA,
--          created by the template). This script only reports the container,
--          the schema and the users.
--          No curly braces in this file: bexhoma may fill it with str.format().

SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS container,
       SYS_CONTEXT('USERENV', 'CURRENT_SCHEMA') AS current_schema
FROM dual;

SELECT username, default_tablespace, created
FROM dba_users
WHERE oracle_maintained = 'N'
ORDER BY username;
