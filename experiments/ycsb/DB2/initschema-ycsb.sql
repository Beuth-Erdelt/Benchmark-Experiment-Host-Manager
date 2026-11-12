-- Benchmark-Experiment-Host-Manager | experiments/ycsb/DB2
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create the YCSB table usertable in IBM Db2, for the YCSB JDBC
--          binding. loadData runs this file with /tmp/bexhoma-run.sh of the
--          template, connected to the database BEXHOMA as db2inst1, the user
--          YCSB logs in as, so the table is in its default schema DB2INST1 and
--          the binding finds it without a schema name.
--          The database has 4 KiB pages, which hold rows of about 4 KB: the
--          table is in a table space of 32 KiB pages (with its own buffer pool,
--          sized by the self-tuning memory manager), so the ten fields of
--          VARCHAR(3000) fit into one row; the field length is set by the
--          workload (default 100).
--          No curly braces in this file: bexhoma may fill it with str.format().

CREATE BUFFERPOOL bp32k SIZE AUTOMATIC PAGESIZE 32K;

CREATE TABLESPACE ts32k PAGESIZE 32K BUFFERPOOL bp32k;

CREATE TABLE usertable (
    YCSB_KEY    VARCHAR(255)    NOT NULL,
    FIELD0      VARCHAR(3000),
    FIELD1      VARCHAR(3000),
    FIELD2      VARCHAR(3000),
    FIELD3      VARCHAR(3000),
    FIELD4      VARCHAR(3000),
    FIELD5      VARCHAR(3000),
    FIELD6      VARCHAR(3000),
    FIELD7      VARCHAR(3000),
    FIELD8      VARCHAR(3000),
    FIELD9      VARCHAR(3000),
    CONSTRAINT pk_usertable PRIMARY KEY (YCSB_KEY)
) IN ts32k;

-- Database and schema the table is in
VALUES (CURRENT SERVER, CURRENT SCHEMA);
