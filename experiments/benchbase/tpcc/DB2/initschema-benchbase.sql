-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/DB2
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Schema step of Benchbase TPC-C on IBM Db2. Benchbase creates its
--          tables itself (profile db2, ddl-db2.sql of Benchbase) in the default
--          schema DB2INST1 of the user it logs in as; this script only reports
--          the database and schema the tables will be in.
--          No curly braces in this file: bexhoma may fill it with str.format().

VALUES (CURRENT SERVER, CURRENT SCHEMA);
