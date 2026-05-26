-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create the named schema for benchbase TPC-C on PostgreSQL.
--          The {BEXHOMA_SCHEMA} placeholder is substituted at runtime by
--          the Bexhoma framework.

CREATE SCHEMA {BEXHOMA_SCHEMA};
