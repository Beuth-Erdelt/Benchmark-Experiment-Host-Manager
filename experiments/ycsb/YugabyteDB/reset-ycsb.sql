-- Benchmark-Experiment-Host-Manager | experiments/ycsb/YugabyteDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for YCSB on YugabyteDB. YSQL does not
--          implement CHECKPOINT, so only ANALYZE VERBOSE runs here to
--          refresh planner statistics on usertable before each round.

ANALYZE VERBOSE usertable;
