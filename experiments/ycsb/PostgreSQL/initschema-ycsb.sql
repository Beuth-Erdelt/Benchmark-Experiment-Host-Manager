-- Benchmark-Experiment-Host-Manager | experiments/ycsb/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Creates the YCSB usertable in the public schema for PostgreSQL.

CREATE TABLE public.usertable (
    YCSB_KEY  VARCHAR(255)  NOT NULL,
    FIELD0    TEXT,
    FIELD1    TEXT,
    FIELD2    TEXT,
    FIELD3    TEXT,
    FIELD4    TEXT,
    FIELD5    TEXT,
    FIELD6    TEXT,
    FIELD7    TEXT,
    FIELD8    TEXT,
    FIELD9    TEXT,
    PRIMARY KEY (YCSB_KEY)
);
