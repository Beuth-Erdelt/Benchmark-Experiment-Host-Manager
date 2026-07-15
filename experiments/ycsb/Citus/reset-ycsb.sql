-- Benchmark-Experiment-Host-Manager | experiments/ycsb/Citus
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for YCSB on Citus. CHECKPOINT only flushes
--          the coordinator node reached by this connection; worker nodes
--          checkpoint on their own schedule. VACUUM and ANALYZE refresh
--          planner statistics on usertable before each round.

CHECKPOINT;
VACUUM usertable;
ANALYZE usertable;
