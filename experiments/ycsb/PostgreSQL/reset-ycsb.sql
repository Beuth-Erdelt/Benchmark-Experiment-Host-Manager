-- Benchmark-Experiment-Host-Manager | experiments/ycsb/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for YCSB on PostgreSQL. Flushes dirty pages
--          to disk and collects fresh statistics on usertable so each
--          benchmarking round starts from a consistent, cold state.

CHECKPOINT;
VACUUM ANALYZE usertable;
