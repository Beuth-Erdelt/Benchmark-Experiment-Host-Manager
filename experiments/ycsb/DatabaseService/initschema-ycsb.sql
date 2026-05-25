-- Benchmark-Experiment-Host-Manager | experiments/ycsb/DatabaseService
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Creates the YCSB usertable for DatabaseService and reports the
--          creation timestamp and initial row count.

CREATE TABLE IF NOT EXISTS usertable (
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

SELECT current_timestamp AS "Time after creation";

SELECT COUNT(*) AS "Number of rows in usertable" FROM usertable;
