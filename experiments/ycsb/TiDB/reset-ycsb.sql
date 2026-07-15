-- Benchmark-Experiment-Host-Manager | experiments/ycsb/TiDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for YCSB on TiDB. The TiKV/RocksDB storage
--          layer has no user-invokable checkpoint. ANALYZE TABLE forces
--          fresh histograms on usertable before each round, rather than
--          relying on TiDB's async auto-analyze job timing.

ANALYZE TABLE usertable;
