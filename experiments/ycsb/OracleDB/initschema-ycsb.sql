-- Benchmark-Experiment-Host-Manager | experiments/ycsb/OracleDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create the YCSB table usertable in Oracle Database Free, for the YCSB
--          JDBC binding. loadData runs this file as SYSDBA in FREEPDB1 with
--          CURRENT_SCHEMA = BEXHOMA, the user YCSB logs in as, so the binding
--          finds the table without a schema name.
--          The fields are VARCHAR2(4000), the largest VARCHAR2 with the default
--          MAX_STRING_SIZE: the field length is set by the workload (default 100).
--          The JDBC binding of YCSB 0.17 scans with LIMIT, which Oracle does not
--          have: workload E (scans) fails, the other workloads run.
--          No curly braces in this file: bexhoma may fill it with str.format().

CREATE TABLE usertable (
    YCSB_KEY    VARCHAR2(255)   NOT NULL,
    FIELD0      VARCHAR2(4000),
    FIELD1      VARCHAR2(4000),
    FIELD2      VARCHAR2(4000),
    FIELD3      VARCHAR2(4000),
    FIELD4      VARCHAR2(4000),
    FIELD5      VARCHAR2(4000),
    FIELD6      VARCHAR2(4000),
    FIELD7      VARCHAR2(4000),
    FIELD8      VARCHAR2(4000),
    FIELD9      VARCHAR2(4000),
    CONSTRAINT pk_usertable PRIMARY KEY (YCSB_KEY)
);

-- Container and schema the table is in
SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS container,
       SYS_CONTEXT('USERENV', 'CURRENT_SCHEMA') AS current_schema
FROM dual;
