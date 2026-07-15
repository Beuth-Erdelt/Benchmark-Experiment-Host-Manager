-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for Benchbase TPC-C on PostgreSQL.
--          Flushes dirty pages to disk and collects fresh statistics so each
--          benchmarking round starts from a consistent, cold state.

CHECKPOINT;
VACUUM ANALYZE;
