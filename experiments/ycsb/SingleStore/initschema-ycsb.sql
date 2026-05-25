-- Benchmark-Experiment-Host-Manager | experiments/ycsb/SingleStore
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Creates the ycsb database and the YCSB usertable as a rowstore
--          table in SingleStore, then verifies the schema.

CREATE DATABASE ycsb;

CREATE ROWSTORE TABLE ycsb.usertable (
    YCSB_KEY  VARCHAR(255) PRIMARY KEY,
    FIELD0    TEXT,
    FIELD1    TEXT,
    FIELD2    TEXT,
    FIELD3    TEXT,
    FIELD4    TEXT,
    FIELD5    TEXT,
    FIELD6    TEXT,
    FIELD7    TEXT,
    FIELD8    TEXT,
    FIELD9    TEXT
);

USE ycsb;

SHOW TABLES EXTENDED;

SHOW DATABASES EXTENDED;

SHOW TABLES IN ycsb EXTENDED;
